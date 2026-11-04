"""Installation comparison regressions using only disposable local fixtures."""
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import check_installed


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/check_installed.py'
PACKAGES = ('se-concurrent', 'se-how', 'se-proof', 'se-swarm', 'se-verify',
            'se-visualise', 'se-what', 'se-when', 'se-where', 'se-who',
            'se-why', 'se-zero-trust')
PATHS = sorted(f'{name}/{leaf}' for name in PACKAGES
               for leaf in ('SKILL.md', 'agents/openai.yaml'))


class InstallationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.installed = self.base / 'installed'
        for relative in PATHS:
            destination = self.installed / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)

    def run_cli(self, *arguments):
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), *arguments],
                                cwd=self.base, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.stderr, '')
        return result, json.loads(result.stdout)

    def check(self):
        return self.run_cli('--skills-dir', str(self.installed))

    def statuses(self, report):
        return {item['path']: item['status'] for item in report['files']}

    def test_complete_match_is_deterministic_and_read_only(self):
        before = {path: (self.installed / path).read_bytes() for path in PATHS}
        result, report = self.check()
        repeated, _ = self.check()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report, {'status': 'match', 'errors': [],
                                 'files': [{'path': path, 'status': 'match'} for path in PATHS]})
        self.assertEqual(result.stdout, repeated.stdout)
        self.assertEqual(before, {path: (self.installed / path).read_bytes() for path in PATHS})
        self.assertEqual(sorted(p.relative_to(self.installed).as_posix()
                                for p in self.installed.rglob('*') if p.is_file()), PATHS)

    def test_missing_and_binary_modified_files(self):
        (self.installed / 'se-what/SKILL.md').unlink()
        target = self.installed / 'se-why/agents/openai.yaml'
        original = target.read_bytes()
        target.write_bytes(b'\xff' + original[1:])
        result, report = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report['status'], 'different')
        self.assertEqual(self.statuses(report)['se-what/SKILL.md'], 'missing')
        self.assertEqual(self.statuses(report)['se-why/agents/openai.yaml'], 'modified')
        self.assertEqual(sum(item['status'] == 'match' for item in report['files']), 22)
        self.assertEqual(target.read_bytes(), b'\xff' + original[1:])

    def test_shorter_longer_and_empty_files_are_modified(self):
        target = self.installed / PATHS[0]
        original = target.read_bytes()
        for contents in (b'', original[:-1], original + b'\x00', original * 100):
            with self.subTest(size=len(contents)):
                target.write_bytes(contents)
                result, report = self.check()
                self.assertEqual(result.returncode, 1)
                self.assertEqual(self.statuses(report)[PATHS[0]], 'modified')

    def test_unrelated_skills_and_extra_files_are_ignored(self):
        (self.installed / 'unrelated').symlink_to(self.base / 'absent', target_is_directory=True)
        (self.installed / 'se-what/extra.py').write_text('raise AssertionError("must not run")')
        result, report = self.check()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(report['files']), 24)

    def test_explicit_relative_directory_is_used(self):
        result, report = self.run_cli('--skills-dir', 'installed')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report['status'], 'match')

    def test_argument_errors_are_json_and_nonzero(self):
        for arguments in ((), ('--skills-dir',), ('--unknown', 'x'),
                          ('--skills-dir', str(self.installed), '--extra'),
                          ('--skills-di', str(self.installed))):
            with self.subTest(arguments=arguments):
                result, report = self.run_cli(*arguments)
                repeated, _ = self.run_cli(*arguments)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(report['status'], 'error')
                self.assertEqual(report['errors'][0]['scope'], 'arguments')
                self.assertEqual(result.stdout, repeated.stdout)

    def test_unusable_root_is_json_and_nonzero(self):
        regular = self.base / 'regular'
        regular.write_text('not a directory')
        for path, reason in (('', 'empty_path'), (str(self.base / 'absent'), 'missing'),
                             (str(regular), 'not_directory')):
            with self.subTest(path=path):
                result, report = self.run_cli('--skills-dir', path)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(report['files'], [])
                self.assertEqual(report['errors'], [{'scope': 'installation', 'reason': reason}])

    def test_root_symlink_rejected_including_trailing_slash(self):
        alias = self.base / 'alias'
        alias.symlink_to(self.installed, target_is_directory=True)
        for path in (str(alias), str(alias) + '/', str(alias) + '/.'):
            with self.subTest(path=path):
                result, report = self.run_cli('--skills-dir', path)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(report['errors'], [{'scope': 'installation', 'reason': 'symlink'}])

    def test_selected_directory_ancestor_alias_uses_normal_resolution(self):
        alias = self.base / 'ancestor'
        alias.symlink_to(self.base, target_is_directory=True)
        result, _ = self.run_cli('--skills-dir', str(alias / 'installed'))
        self.assertEqual(result.returncode, 0)

    def test_symlinked_expected_components_rejected_without_reading_targets(self):
        for relative in ('se-what', 'se-what/agents', 'se-what/SKILL.md',
                         'se-what/agents/openai.yaml'):
            with self.subTest(relative=relative):
                target = self.installed / relative
                backup = self.base / 'backup'
                target.rename(backup)
                target.symlink_to(backup, target_is_directory=backup.is_dir())
                try:
                    result, report = self.check()
                    self.assertEqual(result.returncode, 1)
                    affected = [path for path in PATHS if path == relative or path.startswith(relative + '/')]
                    for path in affected:
                        self.assertEqual(self.statuses(report)[path], 'symlink')
                finally:
                    target.unlink()
                    backup.rename(target)
        target = self.installed / 'se-what/SKILL.md'
        target.unlink()
        target.symlink_to(self.base / 'dangling')
        result, report = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.statuses(report)['se-what/SKILL.md'], 'symlink')

    def test_nonregular_paths_rejected_without_fifo_blocking(self):
        target = self.installed / 'se-what/SKILL.md'
        target.unlink()
        os.mkfifo(target)
        result, report = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.statuses(report)['se-what/SKILL.md'], 'not_regular')
        target.unlink()
        target.mkdir()
        result, report = self.check()
        self.assertEqual(self.statuses(report)['se-what/SKILL.md'], 'not_regular')
        shutil.rmtree(self.installed / 'se-why/agents')
        (self.installed / 'se-why/agents').write_bytes(b'not a directory')
        result, report = self.check()
        self.assertEqual(self.statuses(report)['se-why/agents/openai.yaml'], 'not_directory')

    def test_permission_failure_is_reported(self):
        real_open = os.open
        def denied(path, flags, **kwargs):
            if path == Path(self.installed):
                raise PermissionError(13, 'denied')
            return real_open(path, flags, **kwargs)
        with patch.object(check_installed.os, 'open', side_effect=denied), \
                patch.object(check_installed.os, 'supports_dir_fd', {os.stat, denied}):
            # The supported-function set must include the patched callable.
            check_installed.os.supports_dir_fd.add(check_installed.os.open)
            report, code = check_installed.check_installation(str(self.installed))
        self.assertEqual(code, 2)
        self.assertEqual(report['errors'], [{'scope': 'installation', 'reason': 'unreadable'}])

    def test_source_failure_cannot_reduce_inventory_to_a_pass(self):
        empty = self.base / 'empty-source'
        empty.mkdir()
        with patch.object(check_installed, 'ROOT', empty):
            report, code = check_installed.check_installation(str(self.installed))
        self.assertEqual(code, 2)
        self.assertEqual(report['status'], 'error')
        self.assertEqual(len(report['errors']), 24)
        self.assertEqual([item['path'] for item in report['errors']], PATHS)

    def test_no_network_or_content_execution(self):
        with patch.object(socket, 'socket', side_effect=AssertionError('network')), \
                patch.object(subprocess, 'Popen', side_effect=AssertionError('process')):
            report, code = check_installed.check_installation(str(self.installed))
        self.assertEqual(code, 0)
        self.assertEqual(report['status'], 'match')

    def test_leaf_swap_to_symlink_is_denied_at_open(self):
        target = self.installed / 'se-what/SKILL.md'
        outside = self.base / 'outside'
        outside.write_bytes(b'outside sentinel')
        parent = os.open(target.parent, os.O_RDONLY | os.O_DIRECTORY)
        self.addCleanup(os.close, parent)
        real_open = os.open
        def swap(path, flags, **kwargs):
            target.unlink()
            target.symlink_to(outside)
            return real_open(path, flags, **kwargs)
        with patch.object(check_installed.os, 'open', side_effect=swap):
            with self.assertRaises(check_installed.PathError) as caught:
                check_installed.open_path('SKILL.md', directory=False, parent=parent)
        self.assertEqual(caught.exception.reason, 'symlink')
        self.assertEqual(outside.read_bytes(), b'outside sentinel')


if __name__ == '__main__':
    unittest.main()
