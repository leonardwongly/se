"""Independent public-CLI Markdown URL checks; mutate only disposable copies."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

CASES = [
    ('query', 'docs/index.html?cache=1#skills', 0),
    ('encoded', 'docs/%69ndex.html', 0),
    ('missing-query-url', 'docs/absent-oracle.html?redirect=https://example.invalid', 1),
    ('escape-query-url', '../../outside-oracle.css?redirect=https://example.invalid', 1),
]


def inventory(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()
            and not any(x in {'.git', '__pycache__', '.venv'} for x in p.relative_to(root).parts)
            and p.name != '.DS_Store' and p.suffix not in {'.pyc', '.pyo'}}


def main():
    source = Path(sys.argv[1]).resolve(strict=True)
    before = inventory(source)
    results = []
    for name, target, expected in CASES:
        with tempfile.TemporaryDirectory(prefix='markdown-url-oracle-') as directory:
            root = Path(directory) / 'package'
            shutil.copytree(source, root, ignore=shutil.ignore_patterns(
                '.git', '__pycache__', '.venv', '.DS_Store', '*.pyc', '*.pyo'))
            (root / 'README.md').write_text((root / 'README.md').read_text()
                                          + f'\n[Independent oracle]({target})\n')
            hashes = inventory(root)
            (root / 'MANIFEST.sha256').write_text(''.join(
                f'{digest}  {path}\n' for path, digest in sorted(hashes.items())
                if path != 'MANIFEST.sha256'))
            run = subprocess.run([sys.executable, '-B', 'scripts/validate.py'], cwd=root,
                                 capture_output=True, text=True, timeout=60)
            output = run.stdout + run.stderr
            passed = run.returncode == expected
            if expected == 1:
                passed &= 'README.md' in output and target in output and 'FAIL:' in output
            else:
                passed &= 'PASS: swarm project and independent checks' in output
            results.append({'case': name, 'expected_exit': expected, 'actual_exit': run.returncode,
                            'pass': bool(passed), 'output': output.strip()})
    unchanged = inventory(source) == before
    success = unchanged and all(case['pass'] for case in results)
    print(json.dumps({'result': 'PASS' if success else 'FAIL', 'source_unchanged': unchanged,
                      'validator_sha256': before['scripts/validate.py'], 'cases': results}, indent=2))
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
