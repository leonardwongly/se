"""Read-only comparison of an explicit skill installation; Python >= 3.10.

Requires descriptor-relative no-follow opens (supported on macOS and Linux).
The selected directory itself and all expected descendants must not be symlinks.
Ancestors of the selected directory retain normal operating-system resolution.
"""
import argparse
import errno
import json
import os
from pathlib import Path
import stat
import sys

# Importing the repository inventory must not create cache files in an installation.
sys.dont_write_bytecode = True
from validate import EXPECTED, ROOT


class InputError(Exception):
    pass


class PathError(Exception):
    def __init__(self, reason):
        self.reason = reason


class JSONArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise InputError(message)


def error_reason(error):
    return {
        errno.ENOENT: 'missing',
        errno.ELOOP: 'symlink',
        errno.ENOTDIR: 'not_directory',
        errno.EACCES: 'unreadable',
        errno.EPERM: 'unreadable',
    }.get(error.errno, 'io_error')


def open_path(path, *, directory, parent=None):
    """Classify without following links; enforce that policy again at open time."""
    try:
        before = os.stat(path, dir_fd=parent, follow_symlinks=False)
        if stat.S_ISLNK(before.st_mode):
            raise PathError('symlink')
        valid_type = stat.S_ISDIR if directory else stat.S_ISREG
        if not valid_type(before.st_mode):
            raise PathError('not_directory' if directory else 'not_regular')
        flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
        if directory:
            flags |= os.O_DIRECTORY
        descriptor = os.open(path, flags, dir_fd=parent)
        try:
            if not valid_type(os.fstat(descriptor).st_mode):
                raise PathError('not_directory' if directory else 'not_regular')
        except BaseException:
            os.close(descriptor)
            raise
        return descriptor
    except OSError as error:
        raise PathError(error_reason(error)) from error


def read_expected_path(root_descriptor, relative, limit=None):
    """Never resolve an expected path via a symlink; bound installed-file reads."""
    descriptors = []
    parent = root_descriptor
    try:
        parts = relative.split('/')
        for part in parts[:-1]:
            parent = open_path(part, directory=True, parent=parent)
            descriptors.append(parent)
        descriptor = open_path(parts[-1], directory=False, parent=parent)
        with os.fdopen(descriptor, 'rb') as source:
            return source.read() if limit is None else source.read(limit)
    except OSError as error:
        raise PathError(error_reason(error)) from error
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def check_installation(skills_dir):
    report = {'status': 'error', 'files': [], 'errors': []}
    supported = (all(hasattr(os, name) for name in
                     ('O_NOFOLLOW', 'O_DIRECTORY', 'O_NONBLOCK'))
                 and os.open in os.supports_dir_fd
                 and os.stat in os.supports_dir_fd
                 and os.stat in os.supports_follow_symlinks)
    if not supported:
        report['errors'].append({'scope': 'platform', 'reason': 'no_safe_path_access'})
        return report, 2
    descriptors = []
    scope = 'installation'
    try:
        if not skills_dir:
            raise PathError('empty_path')
        installed = open_path(Path(skills_dir), directory=True)
        descriptors.append(installed)
        scope = 'repository'
        repository = open_path(ROOT, directory=True)
        descriptors.append(repository)
        paths = sorted(f'{name}/{filename}' for name in EXPECTED
                       for filename in ('SKILL.md', 'agents/openai.yaml'))
        for relative in paths:
            try:
                expected = read_expected_path(repository, relative)
            except PathError as error:
                report['errors'].append({'scope': 'repository', 'path': relative,
                                         'reason': error.reason})
                continue
            try:
                actual = read_expected_path(installed, relative, len(expected) + 1)
                status = 'match' if actual == expected else 'modified'
            except PathError as error:
                status = error.reason
            report['files'].append({'path': relative, 'status': status})
    except (PathError, ValueError) as error:
        reason = error.reason if isinstance(error, PathError) else 'invalid_path'
        report['errors'].append({'scope': scope, 'reason': reason})
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)
    if report['errors']:
        return report, 2
    matched = all(item['status'] == 'match' for item in report['files'])
    report['status'] = 'match' if matched else 'different'
    return report, 0 if matched else 1


def main(argv=None):
    parser = JSONArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--skills-dir', required=True, metavar='PATH',
                        help='explicit installation directory to compare, without modification')
    try:
        args = parser.parse_args(argv)
        report, code = check_installation(args.skills_dir)
    except InputError as error:
        report = {'status': 'error', 'files': [],
                  'errors': [{'scope': 'arguments', 'reason': str(error)}]}
        code = 2
    print(json.dumps(report, sort_keys=True, separators=(',', ':')))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
