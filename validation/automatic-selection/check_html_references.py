#!/usr/bin/env python3
"""Black-box HTML link acceptance oracle; all fixture mutations stay in temp copies."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

IGNORE = {'.git', '__pycache__', '.venv'}
PAGES = ('docs/index.html', 'docs/skill-map.html')
RETAINED_MARKERS = (
    'PASS: 12 skill packages',
    'PASS: new project checks',
    'PASS: new independent checks',
    'PASS: update project checks',
    'PASS: update independent checks',
    'PASS: original defective implementation rejected for tenant bypass',
    'PASS: proof exercise reproduces tenant bypass despite original green suite',
    'PASS: swarm project and independent checks',
)


def ignored(directory, names):
    return [name for name in names if name in IGNORE or name == '.DS_Store'
            or name.endswith(('.pyc', '.pyo'))]


def inventory(root):
    """Independent inventory: never import or call the validator's helpers."""
    entries = {}
    for directory, directories, filenames in os.walk(root):
        directories[:] = sorted(name for name in directories if name not in IGNORE)
        for name in sorted(filenames):
            path = Path(directory) / name
            relative = path.relative_to(root).as_posix()
            if relative == 'MANIFEST.sha256' or name == '.DS_Store' or name.endswith(('.pyc', '.pyo')):
                continue
            if path.is_symlink():
                raise AssertionError(f'oracle refuses source symlink: {relative}')
            entries[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return entries


def refresh_manifest(root):
    entries = inventory(root)
    (root / 'MANIFEST.sha256').write_text(''.join(
        f'{digest}  {name}\n' for name, digest in sorted(entries.items())), encoding='utf-8')


def append_html(root, page, markup):
    with (root / page).open('a', encoding='utf-8') as handle:
        handle.write('\n' + markup + '\n')


def run_case(source, label, *, page=None, markup=None, expected=0, target=None,
             added=None, refresh=True, corrupt=False, observe=False):
    with tempfile.TemporaryDirectory(prefix='se-html-oracle-') as directory:
        sandbox = Path(directory)
        root = sandbox / 'package'
        shutil.copytree(source, root, ignore=ignored, symlinks=True)
        # This known non-sensitive file proves containment rejection, rather than absence.
        (sandbox / 'oracle-outside.txt').write_text('oracle boundary fixture\n', encoding='utf-8')
        if markup is not None:
            append_html(root, page, markup)
        for relative, contents in (added or {}).items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding='utf-8')
        if refresh:
            refresh_manifest(root)
        if corrupt:
            with (root / 'docs/assets/guide.css').open('a', encoding='utf-8') as handle:
                handle.write('\n/* independent stale digest */\n')
        guard = sandbox / 'network-guard'
        guard.mkdir()
        log = sandbox / 'network-attempts.txt'
        (guard / 'sitecustomize.py').write_text('''import os, sys

def block_network(event, args):
    if event in {"socket.connect", "socket.connect_ex", "socket.getaddrinfo", "socket.gethostbyname", "socket.gethostbyaddr", "socket.sendto"}:
        with open(os.environ["SE_ORACLE_NETWORK_LOG"], "a") as stream:
            stream.write(event + "\\n")
        raise RuntimeError("independent oracle forbids network")
sys.addaudithook(block_network)
''', encoding='utf-8')
        environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1',
                           PYTHONPATH=str(guard), SE_ORACLE_NETWORK_LOG=str(log))
        process = subprocess.run([sys.executable, '-B', 'scripts/validate.py'],
                                 cwd=root, env=environment, text=True, capture_output=True, timeout=90)
        output = process.stdout + process.stderr
        reasons = []
        if log.exists():
            reasons.append('Python network operation attempted: ' + log.read_text().strip())
        if not observe:
            if process.returncode != expected:
                reasons.append(f'expected exit {expected}, got {process.returncode}')
            if expected == 0:
                missing = [marker for marker in RETAINED_MARKERS if marker not in output]
                if missing:
                    reasons.append('missing retained package checks: ' + repr(missing))
            else:
                for token in filter(None, ('FAIL:', page, target)):
                    if token not in output:
                        reasons.append(f'failure did not identify {token!r}')
        return {'case': label, 'status': 'OBSERVATION' if observe and not reasons else ('FAIL' if reasons else 'PASS'),
                'exit': process.returncode, 'reasons': reasons,
                'output': output if reasons or observe else output.strip().splitlines()[-1:]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='read-only repository or final trial package')
    parser.add_argument('--expect-known-gap', action='store_true',
                        help='prove original validator wrongly accepts a missing HTML target')
    options = parser.parse_args()
    source = options.source.resolve(strict=True)
    before = inventory(source)
    before_manifest = (source / 'MANIFEST.sha256').read_bytes()
    results = [run_case(source, 'unmodified-package', refresh=False)]
    if options.expect_known_gap:
        results.append(run_case(source, 'original-known-gap-missing-image', page=PAGES[0],
                                markup='<img src="oracle-missing-image.png">', expected=0))
    else:
        for page in PAGES:
            suffix = Path(page).name
            cases = [
                ('valid-query-fragment', '<script src="assets/guide.js?rev=2#start"></script><a href="index.html?mode=1&amp;rev=2#skills">local</a>', 0, None, {}),
                ('valid-percent-encoded-space', '<img src="images/oracle%20space.svg?rev=2#part">', 0, None,
                 {'docs/images/oracle space.svg': '<svg xmlns="http://www.w3.org/2000/svg"/>'}),
                ('valid-parent-inside-package', '<a href="../README.md#usage">readme</a>', 0, None, {}),
                ('ignored-nonlocal-and-fragment', '<a href="https://oracle.invalid/missing.html">remote</a><script src="//oracle.invalid/script.js"></script><img src="data:image/svg+xml,%3Csvg/%3E"><a href="#missing-anchor">fragment</a>', 0, None, {}),
                ('missing-image', '<img src="oracle-missing-image.png">', 1, 'oracle-missing-image.png', {}),
                ('missing-script', '<script src="oracle-missing-script.js"></script>', 1, 'oracle-missing-script.js', {}),
                ('missing-href', "<link href='oracle-missing-sheet.css?cache=3#theme' rel='stylesheet'>", 1, 'oracle-missing-sheet.css', {}),
                ('outside-existing-target', '<a href="../../oracle-outside.txt">outside</a>', 1, 'oracle-outside.txt', {}),
                ('encoded-outside-existing-target', '<img src="%2e%2e/%2e%2e/oracle-outside.txt">', 1, 'oracle-outside.txt', {}),
            ]
            for name, markup, expected, target, added in cases:
                results.append(run_case(source, f'{suffix}:{name}', page=page, markup=markup,
                                        expected=expected, target=target, added=added))
        results.append(run_case(source, 'retained-hash-mismatch-rejected', corrupt=True,
                                expected=1, target='digest mismatch: docs/assets/guide.css'))
        results.append(run_case(source, 'retained-inventory-mismatch-rejected', refresh=False,
                                added={'oracle-extra.txt': 'extra\n'}, expected=1,
                                target='manifest file inventory differs from package'))
        results.append(run_case(source, 'root-relative-contract-observation', page=PAGES[0],
                                markup='<a href="/docs/assets/guide.css">root relative</a>', observe=True))
    unchanged = before == inventory(source) and before_manifest == (source / 'MANIFEST.sha256').read_bytes()
    failed = any(result['status'] == 'FAIL' for result in results) or not unchanged
    print(json.dumps({'source': str(source), 'validator_sha256': before.get('scripts/validate.py'),
                      'source_unchanged': unchanged, 'known_gap_mode': options.expect_known_gap,
                      'result': 'FAIL' if failed else 'PASS', 'cases': results}, indent=2))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
