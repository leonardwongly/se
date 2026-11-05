#!/usr/bin/env python3
"""Frozen black-box oracle for team.prompt.txt; no dependencies or project edits.
Usage: python3 check_team.py PROJECT_ROOT OUTPUT_JSON
Copies actual scripts into disposable synthetic projects, runs actual Node entrypoints,
and preserves raw outcomes. Does not inspect implementation bodies to choose assertions.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

READING = 'audit-reading-metadata.mjs'
PERFORMANCE = 'check-performance-budget.mjs'
FILES = {
    'index.html': 90*1024, 'work.html': 90*1024,
    'case-study-agentforge.html': 48*1024, 'case-study-agentic.html': 48*1024,
    'case-study-apple-calendar-mcp.html': 48*1024, 'reading.html': 140*1024,
    'offline.html': 20*1024, 'css/custom.css': 50*1024,
    'css/case-study.css': 8*1024, 'js/main.js': 32*1024,
    'js/site.js': 8*1024, 'pwabuilder-sw.js': 8*1024,
}
DIRS = {'book': 80*1024**2, 'fonts': 512*1024, 'images': 8*1024**2, 'js/vendor': 2*1024**2}
EXPORTS = {
    READING: ['ALLOWED_DUPLICATE_COVER_GROUPS', 'MAX_COVER_FILE_BYTES', 'MAX_READING_METADATA_BYTES',
              'auditReadingMetadata', 'readReadingData', 'resolveSafeCoverPath', 'sha256SafeCoverFile'],
    PERFORMANCE: ['MAX_ASSET_INVENTORY_ENTRIES', 'checkPerformanceBudget',
                  'collectRenderedAssetReferences', 'createAssetInventoryReport', 'walkFiles'],
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def snapshot(root):
    result = {}
    for item in sorted(root.rglob('*')):
        info = item.lstat()
        result[str(item.relative_to(root))] = {
            'mode': info.st_mode, 'mtime_ns': info.st_mtime_ns,
            'content': ('symlink:' + os.readlink(item)) if item.is_symlink() else
                       sha(item.read_bytes()) if item.is_file() else 'directory',
        }
    return result

def write(root, name, data):
    target = root / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data if isinstance(data, bytes) else data.encode())

def fixture(root, cli, kind):
    if kind == 'absent':
        return
    if cli == READING:
        entry = {'title': 'Test Book', 'author': 'Test Author', 'isbn': '123', 'year': '2026'}
        if kind == 'finding':
            entry.pop('title')
        elif kind == 'traversal':
            entry['cover'] = '../outside.jpg'
        elif kind == 'valid':
            entry['cover'] = 'book/test.jpg'
            write(root, 'book/test.jpg', b'synthetic cover bytes')
        data = '{' if kind == 'malformed' else json.dumps([entry])
        write(root, 'data/reading.json', data)
        if kind == 'symlink':
            (root / 'data/reading.json').rename(root / 'data/actual.json')
            (root / 'data/reading.json').symlink_to('actual.json')
        if kind == 'wrong-shape':
            write(root, 'data/reading.json', '{}')
    else:
        for name in FILES:
            write(root, name, 'x')
        for name in DIRS:
            (root / name).mkdir(parents=True, exist_ok=True)
        if kind == 'finding':
            write(root, 'work.html', b'x'*(90*1024+1))
        elif kind == 'malformed':
            write(root, 'reading.html', '<img src="../outside.jpg">')
        elif kind == 'symlink':
            (root / 'index.html').unlink()
            (root / 'index.html').symlink_to('work.html')

# Guard only invalid-argument cases. The real entrypoint and modules still execute;
# input access is denied by instrumented core fs operations before any fixture read.
# This establishes ordering for these fs APIs, not OS-level universal read detection.
GUARD = r'''
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { syncBuiltinESMExports } from 'node:module';
const root = process.env.ORACLE_FIXTURE_ROOT;
for (const name of ['readFileSync', 'openSync', 'lstatSync', 'statSync', 'existsSync', 'readdirSync', 'realpathSync', 'accessSync']) {
  const original = fs[name];
  fs[name] = function(value, ...rest) {
    if (typeof value === 'string' || value instanceof URL || Buffer.isBuffer(value)) {
      const target = path.resolve(value instanceof URL ? fileURLToPath(value) : String(value));
      if ((target === root || target.startsWith(root + path.sep)) && !target.startsWith(root + path.sep + 'scripts' + path.sep)) {
        process.stderr.write('ORACLE_INPUT_ACCESS:' + name + ':' + path.relative(root, target) + '\n');
        process.exit(97);
      }
    }
    return original.call(this, value, ...rest);
  };
}
syncBuiltinESMExports();
'''

def fmt(value):
    return f'{value/1024**2:.2f} MiB' if value >= 1024**2 else f'{value/1024:.1f} KiB'

def performance_expected(kind):
    sizes = {name: 1 for name in FILES}
    if kind == 'finding':
        sizes['work.html'] = 90*1024+1
    report = [f'{name}: {fmt(sizes[name])} / {fmt(budget)}' for name, budget in FILES.items()]
    report += [f'{name}/: 0.0 KiB / {fmt(budget)}' for name, budget in DIRS.items()]
    report += ['rendered reading media: 0.0 KiB / 12.00 MiB', 'rendered reading 2x media: 0.0 KiB / 6.00 MiB']
    return {'failures': ['work.html is 90.0 KiB, above 90.0 KiB'] if kind == 'finding' else [],
            'report': report, 'inventory': {'directoryTotals': [{'path': name+'/', 'size': 0} for name in sorted(DIRS)], 'largestFiles': []}}

def expected_human(cli, kind):
    if cli == READING:
        return (0, 'Reading metadata audit OK.\n', '') if kind == 'valid' else (1, '', 'Reading metadata audit failed with 1 finding(s):\n- reading[0]: missing title\n')
    data = performance_expected(kind)
    stdout = 'Performance budget report:\n' + ''.join('- '+s+'\n' for s in data['report']) + 'Largest asset files:\n'
    stderr = '' if kind == 'valid' else 'Performance budget failed with 1 finding(s):\n- work.html is 90.0 KiB, above 90.0 KiB\n'
    return (0 if kind == 'valid' else 1, stdout, stderr)

def main():
    project, output = map(lambda p: Path(p).resolve(), sys.argv[1:])
    results = []
    source_files = sorted((project / 'scripts').rglob('*'))
    source = {str(p.relative_to(project)): sha(p.read_bytes()) for p in source_files if p.is_file()}
    for cli in (READING, PERFORMANCE):
        cases = [(f'json-{kind}', kind, ['--json'], status, 0 if status == 'pass' else 1, False)
                 for kind, status in [('valid', 'pass'), ('finding', 'fail'), ('malformed', 'error' if cli == READING else 'fail'), ('absent', 'error'), ('symlink', 'error')]]
        if cli == READING:
            cases += [('json-traversal', 'traversal', ['--json'], 'fail', 1, False), ('json-wrong-shape', 'wrong-shape', ['--json'], 'error', 1, False)]
        cases += [(f'human-{kind}', kind, [], None, 0 if kind == 'valid' else 1, False) for kind in ('valid', 'finding')]
        args_cases = [['--unknown'], ['position'], ['--'], ['--json', '--json'],
                      ['--unknown', '--json'], ['--json', '--unknown'],
                      ['position', '--json'], ['--json', 'position'],
                      ['--json=1'], ['--json', '--json', '--unknown']]
        cases += [(f'invalid-{i}', 'absent', args, 'error' if '--json' in args else None, 2, True) for i, args in enumerate(args_cases)]
        cases += [('import-no-running', 'absent', [], None, 0, True)]
        for name, kind, args, status, code, guard in cases:
            with tempfile.TemporaryDirectory(prefix='team-oracle-') as scratch:
                root = Path(scratch).resolve()
                shutil.copytree(project / 'scripts', root / 'scripts', symlinks=True)
                fixture(root, cli, kind)
                write(root, 'oracle-guard.mjs', GUARD)
                before = snapshot(root)
                env = dict(os.environ, ORACLE_FIXTURE_ROOT=str(root))
                env.pop('NODE_OPTIONS', None)
                command = ['node'] + (['--import', str(root / 'oracle-guard.mjs')] if guard else [])
                if name == 'import-no-running':
                    js = 'const m = await import(' + json.dumps((root / 'scripts' / cli).as_uri()) + '); process.stdout.write(JSON.stringify(Object.keys(m).sort())+"\\n");'
                    command += ['--input-type=module', '-e', js]
                else:
                    command += [str(root / 'scripts' / cli), *args]
                actual = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, timeout=10)
                failures = []
                if actual.returncode != code:
                    failures.append(f'exit expected {code}, got {actual.returncode}')
                if before != snapshot(root):
                    failures.append('fixture mutation detected')
                if name == 'import-no-running':
                    try:
                        keys = json.loads(actual.stdout)
                        if not set(EXPORTS[cli]) <= set(keys):
                            failures.append('existing exports missing')
                    except Exception:
                        failures.append('import did not produce export names alone')
                    if actual.stderr:
                        failures.append('import wrote stderr')
                elif status is not None:
                    if actual.stderr:
                        failures.append('JSON stderr is not empty')
                    obj = None
                    try:
                        obj = json.loads(actual.stdout)
                        if not isinstance(obj, dict):
                            raise ValueError('not object')
                        if not actual.stdout.endswith('\n') or actual.stdout.endswith('\n\n'):
                            failures.append('JSON must end with one newline')
                    except Exception:
                        failures.append('stdout is not one JSON object followed by newline')
                    if obj is not None:
                        if obj.get('status') != status:
                            failures.append(f'status expected {status}, got {obj.get("status")}')
                        array_keys = ['findings'] if cli == READING else ['failures', 'report']
                        for key in array_keys:
                            if not isinstance(obj.get(key), list) or any(not isinstance(s, str) for s in obj.get(key, [])):
                                failures.append(f'{key} must be string array')
                        if status == 'error':
                            if not isinstance(obj.get('error'), str) or not obj['error']:
                                failures.append('error string missing')
                            if any(obj.get(key) != [] for key in array_keys):
                                failures.append('execution/argument error arrays must be empty')
                            if cli == PERFORMANCE and obj.get('inventory', 'MISSING') is not None:
                                failures.append('error inventory must be null')
                        elif cli == READING:
                            findings = obj.get('findings')
                            if kind == 'valid' and findings != []:
                                failures.append('valid reading should have no findings')
                            if kind == 'finding' and findings != ['reading[0]: missing title']:
                                failures.append('reading finding content changed')
                            if kind == 'traversal' and (not findings or not any('cover' in s for s in findings)):
                                failures.append('unsafe cover path not rejected')
                        elif kind in ('valid', 'finding'):
                            for key, expected in performance_expected(kind).items():
                                if obj.get(key) != expected:
                                    failures.append(f'performance {key} does not match frozen expected result')
                        elif not obj.get('failures') or not isinstance(obj.get('inventory'), dict):
                            failures.append('malformed asset reference findings/inventory absent')
                elif name.startswith('human-'):
                    if (actual.returncode, actual.stdout, actual.stderr) != expected_human(cli, kind):
                        failures.append('legacy human output changed')
                elif actual.stdout or not actual.stderr:
                    failures.append('human argument error must use stderr only')
                results.append({'cli': cli, 'case': name, 'args': args, 'fixture': kind,
                                'expected_exit': code, 'expected_status': status, 'exit': actual.returncode,
                                'stdout': actual.stdout.replace(str(root), '<fixture>'),
                                'stderr': actual.stderr.replace(str(root), '<fixture>'),
                                'failures': failures, 'passed': not failures})
    source_after = {str(p.relative_to(project)): sha(p.read_bytes()) for p in sorted((project / 'scripts').rglob('*')) if p.is_file()}
    if source != source_after:
        raise RuntimeError('Source scripts changed during oracle execution; results are stale')
    record = {'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'project': str(project), 'checker_sha256': sha(Path(__file__).read_bytes()),
              'node': subprocess.check_output(['node', '--version'], text=True).strip(),
              'python': sys.version.split()[0], 'source_sha256': source,
              'passed': sum(r['passed'] for r in results), 'total': len(results), 'results': results}
    output.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps({'passed': record['passed'], 'total': record['total'], 'output': str(output), 'checker_sha256': record['checker_sha256']}))
    return 0 if record['passed'] == record['total'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
