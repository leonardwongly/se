"""Grade an se-ci run on the CI fixture against spec 002's acceptance criteria; Python >= 3.10.

    python3 -B grade_ci.py run1 <project> --original <fixture project>
    python3 -B grade_ci.py run2 <project> --original <fixture project> --answer <reply.txt>
    python3 -B grade_ci.py run3 <project> --original <fixture project> --answer <reply.txt>
    python3 -B grade_ci.py negative-control <fixture project>
    python3 -B grade_ci.py self-test

`self-test` proves the grader both ways: the untouched fixture and three broken variants fail,
and the reference answer in reference/ passes runs 1 to 3.

Prints one PASS or FAIL line per check, tagged with its acceptance criterion, then a summary.
Exits 0 only when every check passes. A check that cannot run (for example, no YAML parser)
fails; it never passes silently.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

BUCKETS = {
    'required': r'required gates?',
    'flaky': r'flaky',
    'slow': r'slow',
    'low': r'low[- ]value',
    'gaps': r'coverage gaps?',
    'recurring': r'recurring failure',
    'infra': r'infrastructure',
}
EVIDENCE = re.compile(r'70\d\d|#\d+|[\w./-]+\.(?:py|ya?ml|txt|json)\b|\.github/|\bruns?\s*\d+|\bn\s*=\s*\d+|\d+\s*(?:of|/)\s*\d+|\d+\s+runs?\b', re.I)
SECRETS = re.compile(r'ghp_[A-Za-z0-9]{10}|github_pat_|AKIA[0-9A-Z]{12}|-----BEGIN|password\s*[:=]\s*\S', re.I)
TEST_MODULES = ('tests.api', 'tests.billing', 'tests.reports', 'tests.security')


class Grader:
    def __init__(self, quiet=False):
        self.results = []
        self.failures = []
        self.quiet = quiet

    def check(self, ac, description, passed, detail=''):
        self.results.append(bool(passed))
        line = f'{"PASS" if passed else "FAIL"} {ac}: {description}'
        if not passed:
            self.failures.append(line)
        if not self.quiet:
            print(line + (f' ({detail})' if detail and not passed else ''))

    def finish(self):
        failed = self.results.count(False)
        print(f'Ran {len(self.results)} checks: {len(self.results) - failed} passed, {failed} failed')
        return 0 if failed == 0 and self.results else 1


def sections(text):
    """Map lower-case level-2 headings to their body text."""
    out, current = {}, None
    for line in text.splitlines():
        match = re.match(r'^##\s+(.+?)\s*$', line)
        if match:
            current = match.group(1).lower()
            out[current] = []
        elif current is not None:
            out[current].append(line)
    return {key: '\n'.join(value) for key, value in out.items()}


def bucket(secs, pattern):
    for heading, body in secs.items():
        if re.search(pattern, heading):
            return body
    return None


def head_sha(project):
    result = subprocess.run(['git', '-C', str(project), 'rev-parse', 'HEAD'], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ''


def load_workflows(project):
    try:
        import yaml
    except ImportError:
        yaml = None
    workflows = {}
    for path in sorted((project / '.github/workflows').glob('*.y*ml')):
        text = path.read_text(encoding='utf-8')
        if yaml is not None:
            data = yaml.safe_load(text)
        elif shutil.which('ruby'):
            import json
            out = subprocess.run(['ruby', '-ryaml', '-rjson', '-e', 'puts JSON.dump(YAML.safe_load(File.read(ARGV[0]), aliases: true))', str(path)],
                                 capture_output=True, text=True, check=True).stdout
            data = json.loads(out)
        else:
            return None
        if isinstance(data, dict) and True in data and 'on' not in data:
            data['on'] = data.pop(True)  # YAML 1.1 reads the key `on` as true
        workflows[path.name] = (text, data)
    return workflows


def job_text(job):
    return '\n'.join(str(step.get('run', '')) + ' ' + str(step.get('uses', '')) + ' ' + str(step.get('with', ''))
                     for step in job.get('steps', []) or [])


def test_methods(project):
    names = set()
    for path in (project / 'tests').rglob('test_*.py'):
        names.update(re.findall(r'^\s+def (test_\w+)', path.read_text(encoding='utf-8'), re.M))
    return names


def skip_count(project):
    return sum(len(re.findall(r'unittest\.skip|@skip|skipIf|skipUnless|pytest\.mark\.skip', p.read_text(encoding='utf-8')))
               for p in (project / 'tests').rglob('*.py'))


def tests_line(answer):
    lines = [line for line in answer.splitlines() if line.strip().upper().startswith('TESTS:')]
    if not lines:
        return None
    value = lines[-1].split(':', 1)[1].strip()
    if value.upper().startswith('ALL'):
        return set(TEST_MODULES)
    return {module for module in TEST_MODULES if module in value or module.replace('.', '/') in value}


def common(g, project, original, text):
    lines = text.splitlines()
    g.check('AC-5.1', 'CI.md stays within 250 lines', len(lines) <= 250, f'{len(lines)} lines')
    g.check('AC-NFR4.2', 'CI.md holds no secrets or tokens', not SECRETS.search(text))
    # A test may be renamed or replaced by a fix (for example a flaky test made deterministic)
    # only when the record names it as fixed or replaced; a silent disappearance fails.
    missing = test_methods(original) - test_methods(project)
    untraced = [name for name in sorted(missing)
                if not any(name in line and re.search(r'replac|rewr|renam|fix|deterministic|split', line, re.I)
                           for line in text.splitlines())]
    g.check('AC-NFR1.2', 'no original test was deleted without a traced replacement', not untraced,
            f'untraced {untraced}')
    g.check('AC-NFR1.2', 'no test was newly skipped', skip_count(project) <= skip_count(original))
    g.check('AC-12.3', 'the proposed low-value test is still in place', (project / 'tests/billing/test_invoice_copy.py').is_file())


def grade_run1(g, project, original):
    path = project / 'CI.md'
    g.check('AC-4.1', 'CI.md exists at the project root', path.is_file())
    if not path.is_file():
        return
    text = path.read_text(encoding='utf-8')
    secs = sections(text)
    common(g, project, original, text)
    sha = head_sha(project)
    g.check('AC-1.2', 'CI.md records the surveyed revision', bool(sha) and sha[:7] in text, sha[:7])
    g.check('AC-1.2', 'CI.md records a file count', re.search(r'\b\d+\s+(?:\w+\s+){0,2}files?\b', text, re.I))
    survey = bucket(secs, r'survey') or ''
    g.check('AC-1.1', 'survey coverage names pull requests, issues, CI history and configuration',
            all(re.search(p, survey, re.I) for p in (r'pull requests?|PRs?\b', r'issues?', r'runs?|history', r'workflow|ci config')))
    g.check('AC-1.1', 'survey coverage says what was not accessible',
            re.search(r'not accessible|inaccessible|could not|unavailable|not available|no remote|contains? no|'
                      r'absent|missing|none', survey, re.I))
    g.check('AC-NFR2.2', 'survey coverage says whether reading was delegated or direct',
            re.search(r'delegat|subagent|parallel readers?|read (?:it |them )?directly|reading: direct|'
                      r'one context|single context', survey, re.I))
    g.check('AC-3.2', 'CI.md labels the classification method',
            re.search(r'decision model', text, re.I) and re.search(r'fallback|no decision model|not available|unavailable', text, re.I))
    for key, pattern in BUCKETS.items():
        g.check('AC-4.1', f'bucket heading present: {pattern}', bucket(secs, pattern) is not None)
    planted = [
        ('flaky', r'test_invoice_for_random_customer|random[_ ]customer', 'flaky test found'),
        ('slow', r'test_monthly|sleep', 'slow test found'),
        ('low', r'test_invoice_copy|test_subtotal_helper|test_total_again', 'duplicate and implementation-detail tests found'),
        ('gaps', r'export_csv|csv export|export.*\bcsv\b|\bcsv\b.*(?:export|row)', 'untested CSV export found'),
        ('recurring', r'timeout|timed out|pip|install', 'install timeouts named as a recurring cause'),
        ('infra', r'cach', 'missing dependency cache found'),
        ('required', r'security', 'security gate recorded as required'),
    ]
    for key, pattern, description in planted:
        body = bucket(secs, BUCKETS[key]) or ''
        hit = [line for line in body.splitlines() if re.search(pattern, line, re.I)]
        g.check('AC-4.1', description, bool(hit))
        block = body[body.lower().find(hit[0].lower()):][:600] if hit else ''
        g.check('AC-4.2', f'evidence cited for: {description}', bool(EVIDENCE.search(block)))
    top = '\n'.join(text.splitlines()[:40])
    items = re.findall(r'^\s*(?:\d+\.|[-*])\s+\S', top.split('\n', 1)[-1], re.M)
    g.check('AC-5.4', 'CI.md opens with a top-three summary', re.search(r'matters|summary|top', top, re.I) and len(items) >= 3)
    mermaid = '\n'.join(re.findall(r'```mermaid\n(.*?)```', text, re.S))
    g.check('AC-6.1', 'flow map includes both entry points', re.search(r'handle_invoice|/invoice', mermaid) and re.search(r'cli', mermaid, re.I))
    g.check('AC-6.2', 'flow map attaches tests to billing, reports and api',
            all(re.search(p, mermaid, re.I) for p in (r'tests/billing|test_invoice', r'tests/reports|test_monthly', r'tests/api|test_handlers')))
    g.check('AC-6.3', 'config is marked as a shared foundation',
            any(re.search(r'config', line, re.I) and re.search(r'shared|foundation', line, re.I) for line in text.splitlines()))
    g.check('AC-11.3', 'numbers state their sample size', re.search(r'\b30\b\s*(?:CI\s+)?runs?|n\s*=\s*30|/\s*30\b|of\s+30\b', text, re.I))
    proposals = bucket(secs, r'proposal|approval') or ''
    g.check('AC-12.1', 'removal or merge of the duplicate tests is proposed with evidence',
            re.search(r'test_invoice_copy|test_subtotal_helper|test_total_again', proposals + (bucket(secs, BUCKETS['low']) or ''))
            and re.search(r'remov|delet|merg|drop', proposals + (bucket(secs, BUCKETS['low']) or ''), re.I))
    g.check('AC-12.3', 'the removal waits on approval', re.search(r'test_invoice_copy|test_subtotal_helper|test_total_again', proposals))
    g.check('AC-13.1', 'the changelog records this run', re.search(r'\d{4}-\d{2}-\d{2}', bucket(secs, r'changelog') or ''))
    changed = sorted(str(path.relative_to(project)) for path in (project / 'app').rglob('*.py')
                     if not (original / path.relative_to(project)).is_file()
                     or path.read_bytes() != (original / path.relative_to(project)).read_bytes())
    g.check('AC-14.3', 'product code is unchanged; defects are proposed, not fixed', not changed, ', '.join(changed))
    grade_workflow(g, project)


def grade_workflow(g, project):
    workflows = load_workflows(project)
    g.check('AC-8.1', 'workflows parse as YAML', workflows is not None and len(workflows) > 0)
    if not workflows:
        return
    jobs = {(name, job_id): job for name, (_, data) in workflows.items() for job_id, job in (data.get('jobs') or {}).items()}
    texts = '\n'.join(text for text, _ in workflows.values())
    scripts = '\n'.join(p.read_text(encoding='utf-8', errors='replace') for p in project.rglob('*')
                        if p.is_file() and p.suffix in {'.py', '.sh'} and '.github' not in p.parts and 'tests' not in p.parts
                        and 'app' not in p.parts and '.claude' not in p.parts and '.agents' not in p.parts)
    def instances(job):
        # A matrix job runs one job per entry; count entries in lists or in fromJSON(...) arrays.
        matrix = ((job.get('strategy') or {}).get('matrix')) or {}
        if not isinstance(matrix, dict):
            return 1
        counts = []
        for key, value in matrix.items():
            if key in ('include', 'exclude'):
                continue
            if isinstance(value, list):
                counts.append(len(value))
            elif isinstance(value, str):
                arrays = [len(json.loads(found)) for found in re.findall(r'\[[^\[\]]*\]', value.replace("'", '"'))
                          if found.strip('[] ')]
                counts.append(max(arrays) if arrays else 1)
        return max(counts) if counts else 1

    flow_jobs = [key for key, job in jobs.items()
                 if re.search(r'tests[./](?:billing|reports|api)|discover|matrix\.', job_text(job))
                 and 'security' not in key[1]]
    test_jobs = sum(instances(jobs[key]) for key in flow_jobs)
    g.check('AC-8.1', 'tests run in more than one job, organised by flow or module', test_jobs >= 2, f'{test_jobs} test jobs')
    bad_needs = []
    for (name, job_id), job in jobs.items():
        needs = job.get('needs') or []
        for needed in [needs] if isinstance(needs, str) else needs:
            other = jobs.get((name, needed), {})
            if not other.get('outputs') and 'upload-artifact' not in job_text(other):
                bad_needs.append(f'{job_id}->{needed}')
    g.check('AC-8.1', 'jobs wait only on jobs whose output they use', not bad_needs, ', '.join(bad_needs))
    selection = re.search(r'paths-filter|git diff|changed[-_ ]files|affected|outputs\.|paths:', texts + scripts, re.I)
    g.check('AC-9.1', 'pull requests select tests by affected flow', selection)
    record = (project / 'CI.md').read_text(encoding='utf-8') if (project / 'CI.md').is_file() else ''
    rows = [line for line in record.splitlines() if line.lstrip().startswith(('|', '-', '*'))]
    full = r'\bfull\b|\ball\b|every flow|whole suite'
    stated_shared = (any(re.search(r'config', row) and re.search(full, row, re.I) for row in rows) and
                     any(re.search(r'requirements|manifest|dependenc', row, re.I) and re.search(full, row, re.I) for row in rows))
    g.check('AC-9.2', 'shared foundations (config, dependencies) force the full suite',
            (re.search(r'config', texts + scripts) and re.search(r'requirements', texts + scripts)) or stated_shared)
    triggers = [data.get('on') or {} for _, data in workflows.values()]
    runs_on_main = any('schedule' in on or 'main' in str((on.get('push') or {}).get('branches', '')) for on in triggers
                       if isinstance(on, dict))
    signalled = re.search(r"event_name\s*==\s*'push'|event_name\s*!=\s*'pull_request'|refs/heads/main|"
                          r"github\.ref_name\s*==\s*'main'|schedule", texts + scripts)
    stated_main = any(re.search(r'\bmain\b|default branch|\bpush\b|schedule', row, re.I) and re.search(full, row, re.I)
                      for row in rows)
    # v5: the statement may also be a paragraph line, if it names main pushes or a schedule and every flow.
    stated_main = stated_main or any(
        re.search(r'\bpush(?:es)? to `?main`?|`main`|default branch|\bschedule', line, re.I) and
        re.search(r'every flow|all flows|full suite|whole suite|all tests', line, re.I)
        for line in record.splitlines())
    g.check('AC-9.3', 'the default branch or a schedule runs the full suite', runs_on_main and (signalled or stated_main))
    gate = [key for key, job in jobs.items() if re.search(r'tests[./]security', job_text(job)) and not job.get('if')]
    on_pr = [name for name, (_, data) in workflows.items()
             if 'pull_request' in (data.get('on') or {}) and not ((data.get('on') or {}).get('pull_request') or {}).get('paths')]
    g.check('AC-9.4', 'the security gate runs unconditionally on every pull request',
            any(name in on_pr for name, _ in gate), f'gate jobs {gate}, unfiltered PR workflows {on_pr}')
    if shutil.which('actionlint'):
        result = subprocess.run(['actionlint', *map(str, sorted((project / '.github/workflows').glob('*.y*ml')))],
                                capture_output=True, text=True)
        g.check('AC-14.2', 'actionlint accepts the workflows', result.returncode == 0, result.stdout.strip()[:300])
    else:
        g.check('AC-14.2', 'actionlint accepts the workflows', False, 'actionlint not installed')


def grade_followup(g, project, original, answer, expected, forbidden, run):
    path = project / 'CI.md'
    g.check('AC-2.2', 'CI.md exists after the follow-up run', path.is_file())
    if not path.is_file():
        return
    text = path.read_text(encoding='utf-8')
    secs = sections(text)
    common(g, project, original, text)
    sha = head_sha(project)
    if run == 2:
        g.check('AC-2.2', 'CI.md records the new revision', sha[:7] in text, sha[:7])
        duplicates = []
        for key, pattern in (('flaky', r'random_customer'), ('slow', r'test_monthly'), ('gaps', r'export_csv')):
            body = bucket(secs, BUCKETS[key]) or ''
            entries = [line for line in body.splitlines() if re.match(r'^\s*[-*]\s', line) and re.search(pattern, line)]
            if len(entries) > 1:
                duplicates.append(key)
        g.check('AC-5.2', 'no bucket repeats an entry', not duplicates, ', '.join(duplicates))
        changelog = bucket(secs, r'changelog') or ''
        g.check('AC-13.1', 'the changelog records both runs', len(re.findall(r'\d{4}-\d{2}-\d{2}', changelog)) >= 2 or sha[:7] in changelog)
    selected = tests_line(answer)
    g.check(f'AC-7.{1 if run == 2 else 2}', 'the reply ends with a TESTS line', selected is not None)
    if selected is None:
        return
    g.check(f'AC-7.{1 if run == 2 else 2}', f'selection includes {sorted(expected)}', expected <= selected, sorted(selected))
    g.check(f'AC-9.{1 if run == 2 else 2}', f'selection excludes {sorted(forbidden) or "nothing"}', not (forbidden & selected), sorted(selected))
    g.check('AC-9.4', 'the security gate is selected', 'tests.security' in selected)


def reference_project(workdir):
    """The fixture plus the reference answer, committed, with {{HEAD}} filled in."""
    here = Path(__file__).resolve().parent
    project = workdir / 'project'
    shutil.copytree(here / 'project', project)
    for item in ('CI.md', '.github', 'ci'):
        source = here / 'reference' / item
        if source.is_dir():
            shutil.copytree(source, project / item, dirs_exist_ok=True)
        else:
            shutil.copy2(source, project / item)
    git = ['git', '-C', str(project), '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid']
    subprocess.run(git[:3] + ['init', '-q'], check=True)
    subprocess.run(git + ['add', '-A'], check=True)
    subprocess.run(git + ['commit', '-q', '-m', 'reference'], check=True)
    record = project / 'CI.md'
    record.write_text(record.read_text().replace('{{HEAD}}', head_sha(project)[:7]))
    return project


def self_test():
    import tempfile
    here = Path(__file__).resolve().parent
    g = Grader()
    original = here / 'project'

    def run(mode, project, answer=''):
        inner = Grader(quiet=True)
        if mode == 'run1':
            grade_run1(inner, project, original)
        elif mode == 'run2':
            grade_followup(inner, project, original, answer, {'tests.billing', 'tests.api', 'tests.security'},
                           {'tests.reports'}, 2)
        else:
            grade_followup(inner, project, original, answer, set(TEST_MODULES), set(), 3)
        return inner

    inner = run('run1', original)
    g.check('self-test', 'untouched fixture fails run 1', inner.results and not all(inner.results))
    with tempfile.TemporaryDirectory() as temp:
        project = reference_project(Path(temp))
        for mode, answer in (('run1', ''), ('run2', 'answer-run2.txt'), ('run3', 'answer-run3.txt')):
            text = (here / 'reference' / answer).read_text() if answer else ''
            inner = run(mode, project, text)
            g.check('self-test', f'reference answer passes {mode}', inner.results and all(inner.results), '; '.join(inner.failures))
        inner = run('run2', project, 'TESTS: tests.billing, tests.api, tests.reports, tests.security')
        g.check('self-test', 'over-broad selection fails run 2', not all(inner.results))
        inner = run('run3', project, 'TESTS: tests.billing, tests.security')
        g.check('self-test', 'partial selection fails run 3', not all(inner.results))
        (project / 'tests/billing/test_invoice_copy.py').unlink()
        inner = run('run1', project)
        g.check('self-test', 'deleting a proposed test fails run 1', not all(inner.results))
    return g.finish()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('mode', choices=('run1', 'run2', 'run3', 'negative-control', 'self-test'))
    parser.add_argument('project', type=Path, nargs='?')
    parser.add_argument('--original', type=Path, default=Path(__file__).resolve().parent / 'project')
    parser.add_argument('--answer', type=Path)
    args = parser.parse_args(argv)
    g = Grader()
    if args.mode == 'negative-control':
        # The untouched fixture must fail run 1: no record, no flow map, a serial workflow.
        inner = Grader(quiet=True)
        grade_run1(inner, args.project, args.original)
        g.check('negative-control', 'the untouched fixture fails run 1', inner.results and not all(inner.results))
        return g.finish()
    if args.mode == 'self-test':
        return self_test()
    answer = args.answer.read_text(encoding='utf-8') if args.answer else ''
    if args.mode == 'run1':
        grade_run1(g, args.project, args.original)
    elif args.mode == 'run2':
        grade_followup(g, args.project, args.original, answer,
                       {'tests.billing', 'tests.api', 'tests.security'}, {'tests.reports'}, 2)
    else:
        grade_followup(g, args.project, args.original, answer, set(TEST_MODULES), set(), 3)
    return g.finish()


if __name__ == '__main__':
    sys.exit(main())
