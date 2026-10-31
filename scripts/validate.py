"""Portable package integrity and synthetic behavior checks; Python >= 3.10."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {f'se-{name}' for name in (
    'what', 'why', 'who', 'where', 'how', 'when', 'zero-trust', 'verify', 'concurrent',
    'proof', 'visualise', 'swarm'
)}


def require(condition, message):
    if not condition:
        raise SystemExit(f'FAIL: {message}')


def package_files():
    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT)
        if any(part in {'.git', '__pycache__', '.venv'} for part in relative.parts):
            continue
        if path.name == '.DS_Store' or path.suffix in {'.pyc', '.pyo'}:
            continue
        require(not path.is_symlink(), f'symlink outside package contract: {relative}')
        if path.is_file() and relative.as_posix() != 'MANIFEST.sha256':
            yield relative.as_posix(), path


def run(args, cwd=ROOT):
    result = subprocess.run([sys.executable, '-B', *args], cwd=cwd,
                            capture_output=True, text=True, timeout=60,
                            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    return result, result.stdout + result.stderr


def require_tests(result, output, count, label):
    ran = re.search(r'^Ran (\d+) tests? in ', output, re.M)
    require(result.returncode == 0 and ran is not None and
            int(ran.group(1)) == count and re.search(r'^OK$', output, re.M),
            f'{label}: expected {count} passing tests without skips\n{output}')


def main():
    actual = {path.parent.name for path in ROOT.glob('*/SKILL.md')}
    require(actual == EXPECTED, f'expected {len(EXPECTED)} skills, found {sorted(actual)}')
    for name in sorted(EXPECTED):
        text = (ROOT / name / 'SKILL.md').read_text()
        frontmatter = text.split('---', 2)
        require(text.startswith('---\n') and len(frontmatter) == 3, f'{name}: frontmatter')
        require(re.search(rf'^name: {re.escape(name)}$', frontmatter[1], re.M), f'{name}: name')
        require(re.search(r'^description: \S.+$', frontmatter[1], re.M), f'{name}: description')
        require((ROOT / name / 'agents/openai.yaml').is_file(), f'{name}: UI metadata')

    files = dict(package_files())
    manifest = {}
    for line in (ROOT / 'MANIFEST.sha256').read_text().splitlines():
        digest, name = line.split('  ', 1)
        require(name not in manifest and re.fullmatch(r'[0-9a-f]{64}', digest), 'invalid manifest entry')
        manifest[name] = digest
    require(files.keys() == manifest.keys(), 'manifest file inventory differs from package')
    for name, path in files.items():
        require(hashlib.sha256(path.read_bytes()).hexdigest() == manifest[name], f'digest mismatch: {name}')
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                resolved = (path.parent / target.split('#')[0]).resolve()
                require(resolved.is_relative_to(ROOT) and resolved.exists(), f'{name}: invalid link {target}')
    print(f'PASS: {len(EXPECTED)} skill packages, required fields, local links, complete hash manifest')

    fixture = ROOT / 'validation/code-baseline'
    for name, project_count, independent_count in (('new', 10, 7), ('update', 8, 8)):
        result, output = run(['-m', 'unittest', 'discover', '-s', 'tests', '-v'], fixture / name)
        require_tests(result, output, project_count, f'{name} project checks')
        print(f'PASS: {name} project checks')
        result, output = run([str(fixture / 'grade_fixture.py'), name, str(fixture / name)])
        require_tests(result, output, independent_count, f'{name} independent checks')
        print(f'PASS: {name} independent checks')
    result, output = run([str(fixture / 'grade_fixture.py'), 'update', str(fixture / 'original-update')])
    require(result.returncode == 1 and
            'FAIL: test_spoofed_tenant_hint_denied' in output and
            'AssertionError: PermissionError not raised' in output,
            f'negative control did not detect tenant bypass\n{output}')
    print('PASS: original defective implementation rejected for tenant bypass')

    expansion = ROOT / 'validation/expansion'
    result, output = run([str(expansion / 'proof/check_archive.py')])
    require(result.returncode == 1, f'proof exercise must retain observed defects\n{output}')
    observations = json.loads(output)
    bypass = next(case for case in observations['cases']
                  if case['case'] == 'admin cross tenant with target hint')
    require(observations['passed'] == 6 and observations['total'] == 10 and
            not bypass['contract_pass'] and bypass['changed_accounts'] == ['E'] and
            bypass['events_changed'], 'proof exercise did not reproduce unauthorized effects')
    print('PASS: proof exercise reproduces tenant bypass despite original green suite')

    result, output = run(['-m', 'unittest', 'discover', '-s', 'tests', '-v'], expansion / 'swarm/project')
    require_tests(result, output, 10, 'swarm integrated project checks')
    result, output = run([str(fixture / 'grade_fixture.py'), 'update', str(expansion / 'swarm/project')])
    require_tests(result, output, 8, 'swarm independent checks')
    print('PASS: swarm project and independent checks')


if __name__ == '__main__':
    main()
