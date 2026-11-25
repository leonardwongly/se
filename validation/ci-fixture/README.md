# CI fixture for se-ci

A small invoicing project with known CI problems, used to evaluate the `se-ci` skill against
[spec 002](../../specs/002-ci-optimization/spec.md). An agent under evaluation gets a copy of
`project/` only, never this README, the grader or the reference answer.

## Layout

| Path | Purpose |
|---|---|
| `project/` | The project handed to the agent, with its CI history exported under `.ci-history/` |
| `make_history.py` | Regenerates `project/.ci-history/` deterministically |
| `grade_ci.py` | Grades a run against the spec's acceptance criteria; `self-test` proves the grader |
| `reference/` | A hand-written passing answer: the grader's positive control |
| `run_eval.py` | Runs the three evaluation runs on Claude Code or Codex and grades them |
| `results/` | Grader output and summaries from recorded evaluations |

## Planted problems (answer key)

| Bucket | Planted problem | Evidence the agent can find |
|---|---|---|
| Required gates | `tests/security` must run on every pull request (policy SEC-7) | workflow comment, issue #14, run 7016 caught an injection regression |
| Flaky | `test_invoice_for_random_customer` draws customer ids that sometimes contain `_`, which the validator rejects | 6 of 30 runs failed and passed on rerun, issue #11, PR comments |
| Slow | `test_monthly_totals` sleeps 3 s for a cache that PR #3 removed | per-test durations in `runs.json`, PR #3 |
| Low value | `tests/billing/test_invoice_copy.py`: `test_subtotal_helper` tests a private helper and never failed; `test_total_again` duplicates `test_total_includes_tax` and failed only with it | runs 7007, the test code |
| Low value | security tests run twice per run (discover and the gate step) | the workflow |
| Coverage gaps | `export_csv` has no test and drops the last row | issue #13, PR #6, the code |
| Recurring failure causes | install timeouts against PyPI; the flaky test | runs 7005, 7013, 7023; issue #11 |
| Infrastructure | no dependency cache: install is about 40 s of a 64 s median run; `requirements.txt` lists packages the code never imports | step durations, PR #5, issue #12 |

Flows: invoice (`handle_invoice` → `app.api` → `app.billing`, with `app.security`) and monthly
report (`python -m app.cli` → `app.reports`). `app/config.py`, `requirements.txt`, the workflow
and `tests/__init__.py` are shared foundations.

Expected selection: a change under `app/billing/` runs the billing and api tests plus the security
gate, not the reports tests. A change to `app/config.py` runs everything.

## Running the evaluation

```sh
python3 -B validation/ci-fixture/grade_ci.py self-test
python3 -B validation/ci-fixture/run_eval.py --agent claude --out /tmp/se-ci-eval
python3 -B validation/ci-fixture/run_eval.py --agent codex --out /tmp/se-ci-eval
```

`run_eval.py` copies `project/` into the output directory, adds the SE skills where each host
looks for project skills (git-excluded, so they are not surveyed as project code), commits it, and
runs three prompts:

1. First run: optimise the CI.
2. After a commit that changes `app/billing/`: update the record and say which tests to run.
3. After a commit that changes `app/config.py`: say which tests to run.

Each reply ends with a `TESTS:` line that the grader reads. One fixture on two hosts is a smoke
evaluation, not a success rate.
