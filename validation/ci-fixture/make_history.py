"""Write the fixture's exported CI history (deterministic); Python >= 3.10.

    python3 -B validation/ci-fixture/make_history.py

The planted patterns are listed in this folder's README.md. The project copy given to an
agent contains only the generated files, never this script or the README.
"""
import hashlib
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent / 'project/.ci-history'
TESTS = [
    'tests.api.test_handlers.HandlerTests.test_invoice_response',
    'tests.api.test_handlers.HandlerTests.test_invoice_for_random_customer',
    'tests.billing.test_invoice.InvoiceTests.test_total_includes_tax',
    'tests.billing.test_invoice.InvoiceTests.test_empty_invoice',
    'tests.billing.test_invoice_copy.InvoiceCopyTests.test_subtotal_helper',
    'tests.billing.test_invoice_copy.InvoiceCopyTests.test_total_again',
    'tests.reports.test_monthly.MonthlyTests.test_monthly_totals',
    'tests.security.test_security.SecurityTests.test_rejects_injection',
    'tests.security.test_security.SecurityTests.test_requires_billing_role',
]
SECURITY = TESTS[-2:]
FLAKY = TESTS[1]
# (pull request or None, attempt, outcome kind). Reruns repeat the previous commit.
SCHEDULE = [
    (1, 1, 'pass'), (1, 1, 'flaky'), (1, 2, 'pass'), (None, 1, 'pass'), (None, 1, 'install-timeout'),
    (None, 2, 'pass'), (2, 1, 'billing-regression'), (2, 1, 'flaky'), (2, 2, 'pass'), (2, 1, 'pass'),
    (None, 1, 'pass'), (3, 1, 'pass'), (3, 1, 'install-timeout'), (3, 2, 'pass'), (None, 1, 'pass'),
    (4, 1, 'security-regression'), (4, 1, 'flaky'), (4, 2, 'pass'), (None, 1, 'pass'), (5, 1, 'flaky'),
    (5, 2, 'pass'), (None, 1, 'pass'), (6, 1, 'install-timeout'), (6, 2, 'pass'), (6, 1, 'pass'),
    (None, 1, 'flaky'), (None, 2, 'pass'), (None, 1, 'pass'), (None, 1, 'flaky'), (None, 2, 'pass'),
]


def sha(n):
    return hashlib.sha1(f'ledger-commit-{n}'.encode()).hexdigest()


def runs():
    rng = random.Random(20261121)
    start = datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc)
    records, commit = [], 0
    for index, (pull, attempt, kind) in enumerate(SCHEDULE):
        if attempt == 1:
            commit += 1
        created = start + timedelta(hours=37 * index)
        queue = rng.randint(15, 95)
        steps = [('Set up job', rng.randint(2, 4)), ('Checkout', rng.randint(1, 3)),
                 ('Set up Python', rng.randint(9, 14))]
        tests, failure, conclusion = [], None, 'success'
        if kind == 'install-timeout':
            steps.append(('Install dependencies', 120))
            failure = {'step': 'Install dependencies',
                       'message': "ReadTimeoutError: HTTPSConnectionPool(host='files.pythonhosted.org', port=443): Read timed out."}
            conclusion = 'failure'
        else:
            steps.append(('Install dependencies', rng.randint(38, 46)))
            steps.append(('Lint', rng.randint(1, 2)))
            failed = {'flaky': [FLAKY], 'billing-regression': [TESTS[2], TESTS[5]],
                      'security-regression': [TESTS[7]]}.get(kind, [])
            for test in TESTS:
                duration = round(rng.uniform(3.02, 3.15), 2) if 'test_monthly' in test else round(rng.uniform(0.001, 0.02), 3)
                tests.append({'id': test, 'step': 'Unit tests', 'duration_s': duration,
                              'outcome': 'failure' if test in failed else 'success'})
            for test in SECURITY:
                tests.append({'id': test, 'step': 'Security gate', 'duration_s': round(rng.uniform(0.001, 0.01), 3),
                              'outcome': 'failure' if test in failed else 'success'})
            unit = round(sum(t['duration_s'] for t in tests if t['step'] == 'Unit tests') + 0.4, 1)
            steps.append(('Unit tests', unit))
            steps.append(('Security gate', 0.4 if kind != 'security-regression' else 0.5))
            if failed:
                conclusion = 'failure'
                messages = {'flaky': 'ValueError: invalid customer id',
                            'billing-regression': 'AssertionError: 21.6 != 21.8',
                            'security-regression': 'AssertionError: ValueError not raised'}
                failure = {'step': 'Unit tests', 'tests': failed, 'message': messages[kind]}
        duration = round(sum(seconds for _, seconds in steps), 1)
        records.append({
            'id': 7001 + index, 'head_sha': sha(commit), 'event': 'pull_request' if pull else 'push',
            'branch': f'pr-{pull}' if pull else 'main', 'pull_request': pull, 'attempt': attempt,
            'created_at': created.isoformat(), 'queue_s': queue, 'duration_s': duration,
            'conclusion': conclusion, 'failure': failure,
            'jobs': [{'name': 'test', 'runner': 'ubuntu-latest', 'duration_s': duration,
                      'steps': [{'name': name, 'duration_s': seconds} for name, seconds in steps]}],
            'tests': tests,
        })
    return records


PULLS = [
    {'number': 1, 'title': 'Add tax rounding to invoices', 'state': 'merged', 'author': 'dev-a',
     'files': ['app/billing/invoice.py', 'tests/billing/test_invoice.py'],
     'comments': [{'author': 'dev-b', 'body': 'CI failed on test_invoice_for_random_customer, unrelated to this change. Re-ran it and it passed.'}]},
    {'number': 2, 'title': 'Refactor subtotal calculation', 'state': 'merged', 'author': 'dev-b',
     'files': ['app/billing/invoice.py'],
     'comments': [{'author': 'dev-a', 'body': 'test_total_includes_tax caught the rounding change, good. Fixed in the next commit.'},
                  {'author': 'dev-b', 'body': 'Random customer test failed again, re-running.'}]},
    {'number': 3, 'title': 'Remove the monthly report cache', 'state': 'merged', 'author': 'dev-c',
     'files': ['app/reports/monthly.py'],
     'comments': [{'author': 'dev-a', 'body': 'The cache is gone, but test_monthly_totals still sleeps for 3 seconds waiting for it.'},
                  {'author': 'dev-c', 'body': 'Install step timed out talking to PyPI, re-ran.'}]},
    {'number': 4, 'title': 'Accept customer ids with spaces', 'state': 'merged', 'author': 'dev-d',
     'files': ['app/security.py', 'app/api/handlers.py'],
     'comments': [{'author': 'dev-b', 'body': 'The security gate caught that this lets "1; DROP TABLE invoices" through. Reverted the regex change.'},
                  {'author': 'dev-d', 'body': 'Also hit the flaky random customer test.'}]},
    {'number': 5, 'title': 'Speed up CI', 'state': 'closed', 'author': 'dev-c',
     'files': ['.github/workflows/ci.yml'],
     'comments': [{'author': 'dev-c', 'body': 'Every run spends about 40 s installing dependencies; we never cache them. Most runs take over a minute for 9 tests.'},
                  {'author': 'dev-a', 'body': 'Closing for now, no time to finish.'}]},
    {'number': 6, 'title': 'Add CSV export for monthly reports', 'state': 'merged', 'author': 'dev-a',
     'files': ['app/reports/monthly.py', 'app/cli.py'],
     'comments': [{'author': 'dev-b', 'body': 'No test for export_csv yet? Approving anyway, it is small.'}]},
]
ISSUES = [
    {'number': 11, 'title': 'test_invoice_for_random_customer fails at random', 'state': 'open', 'labels': ['ci', 'flaky'],
     'body': 'It fails a few times a week with "invalid customer id" and passes on re-run. Everyone just re-runs it.'},
    {'number': 12, 'title': 'CI takes over a minute for nine tests', 'state': 'open', 'labels': ['ci'],
     'body': 'Most of the time goes to pip install on every run. The monthly report test also sleeps for 3 s.'},
    {'number': 13, 'title': 'CSV export drops the last row', 'state': 'open', 'labels': ['bug', 'reports'],
     'body': 'Exporting three months gives two lines. CI was green when this shipped in #6.'},
    {'number': 14, 'title': 'Security policy SEC-7: security tests on every pull request', 'state': 'closed',
     'labels': ['policy', 'security'],
     'body': 'Compliance requires tests/security to run on every pull request, regardless of which files changed.'},
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, data in (('runs.json', runs()), ('pulls.json', PULLS), ('issues.json', ISSUES)):
        (OUT / name).write_text(json.dumps(data, indent=1) + '\n', encoding='utf-8')
    print(f'wrote {len(SCHEDULE)} runs, {len(PULLS)} pull requests, {len(ISSUES)} issues to {OUT}')


if __name__ == '__main__':
    main()
