# se-ci evaluation

Evidence for [spec 002](../specs/002-ci-optimization/spec.md): does `se-ci` meet its acceptance
criteria on a project with known CI problems?

## Method

- **Fixture.** [ci-fixture/project](ci-fixture/project) is a small invoicing service with two entry
  points, three flows, a shared configuration module, a serial single-job workflow and 30 runs of
  exported CI history, 6 pull requests and 4 issues. Planted problems: a flaky test, a slow test, a
  duplicate test and an implementation-detail test, an untested CSV export with a real bug, a
  security gate required by policy, uncached dependency installs and install timeouts. The
  [answer key](ci-fixture/README.md) is never shown to the agent.
- **Runs.** [ci-fixture/run_eval.py](ci-fixture/run_eval.py) copies the project into a fresh git
  repository with the SE skills as git-excluded project skills, and runs three headless sessions.
  1. First run: optimise the CI.
  2. After a commit that changes `app/billing/`: update the record and name the tests to run.
  3. After a commit that changes `app/config.py`: name the tests to run.
- **Grading.** [ci-fixture/grade_ci.py](ci-fixture/grade_ci.py) checks each run against the spec's
  acceptance criteria: 50 checks for run 1 (49 before v4), 13 for run 2 and 10 for run 3. Its `self-test` proves it
  both ways: the untouched fixture and three broken variants fail, and a hand-written reference
  answer ([ci-fixture/reference](ci-fixture/reference)) passes. `scripts/validate.py` runs the
  self-test.
- **Claude Code runs** use `claude -p --model opus --permission-mode acceptEdits` with a fixed tool
  allowlist and `--setting-sources project,local`, so the skills come from the project copy only.
  Each session starts with a clean environment, because a `claude` started inside a Claude Code
  session otherwise inherits that session's bare-mode and host-auth variables. A one-line appended
  system prompt says the run is unattended in a disposable fixture, and that anything needing approval
  goes in CI.md. `--output-format json` returns only the final reply, so tool calls (skills loaded,
  subagents spawned, commands run) are read from the session transcript that Claude Code keeps under
  `~/.claude/projects/`.
- **Limits.** One fixture, two hosts and one model each make a smoke evaluation, not a
  success rate. Static workflow checks are heuristic, so runs 2 and 3 also check the agent's own
  test selection. Hosted GitHub Actions behaviour (cache hits, queue times) was not observable,
  because the fixture has no remote.

## Results — Codex, 2026-11-21

Grades below are from grader v3 and are stored in [ci-fixture/results](ci-fixture/results). Run 1
is graded at the surveyed revision. Later grader versions leave these grades as they are: v4 adds
one check for AC-NFR2.2, which these runs predate, and v5 only widens an AC-9.3 check that every
stored run 1 grade already passes.

| Evaluation | Skill text | Run 1 (49 checks) | Run 2 (13) | Run 3 (10) |
|---|---|---|---|---|
| First | initial | 45 passed | 12 passed | 9 passed |
| Re-run | after fixes 1–3 below | 47 passed | not run: usage limit | not run: usage limit |

Both evaluations found every planted problem with run-level evidence and sample sizes, kept the
security gate unconditional, proposed rather than applied the test removals, and passed `actionlint`.
In the first evaluation, run 2 selected `tests.billing, tests.api, tests.security` for the billing
change and run 3 selected `ALL` for the configuration change, both as specified.

### Failures, and what changed

Each failure was classified before anything changed. A failure the skill caused changed the
skill text; a check too literal for the acceptance criterion changed the grader. Grader changes
are listed so that nothing passes silently.

| Failure | Cause | Change |
|---|---|---|
| Flaky entry did not name the test (first) | Skill: entries needn't name what they are about | Template rule: name the test, job, step or file (fix 1) |
| Rewritten flaky test counted as deleted (first, all runs) | Skill: the swap wasn't traced. Grader: any missing name failed | Skill names old and new test on replacement (fix 2); grader accepts a missing test only when `CI.md` names it as fixed or replaced (v2) |
| One test job for all flows (first) | Skill: FR-8's per-flow jobs conflicted with avoiding a serial selection job | Skill shows per-flow matrix jobs that select for themselves (fix 3) |
| Config or main push "doesn't force the full suite" (first) | Grader: required keywords; the agent defaulted unknown paths to the full suite | Grader also reads the `CI.md` affected-by rules, and requires a push or schedule trigger (v2) |
| Matrix counted as one job (re-run) | Grader | Count matrix entries (v3) |
| "No remote" and "final CSV row" not recognised (re-run) | Grader: wording too literal | Broader matchers (v3) |
| Cache entry cites only "same window" (re-run) | Skill | Template: every entry cites its own evidence (fix 4, not yet re-run) |
| Fixed the CSV bug in product code (re-run) | Skill: no scope rule | Safety rule: product defects are proposed, not fixed (fix 5, not yet re-run); new AC-14.3, approved 2026-11-24 |

### Acceptance criteria

| Criterion | Result | Evidence |
|---|---|---|
| AC-1.1, AC-1.2 survey coverage, file count, revision | met | both run 1 grades |
| AC-2.1, AC-2.2 incremental survey, new revision | met (first) | run 2 of the first evaluation read the changed file, its importers, the affected tests, the selector, the workflow and the record, plus three files needed to confirm the reports flow is unaffected; it did not re-read the history exports |
| AC-3.1–3.3 decision model | AC-3.2 met; AC-3.1 not exercised (no decision model on this host); AC-3.3 by review | both run 1 grades |
| AC-4.1, AC-4.2 buckets and evidence | met in the re-run except one entry's evidence (fix 4) | re-run run 1 |
| AC-5.1–5.4 budget, merging, retirement, summary | met (5.3 not exercised in two runs) | both evaluations |
| AC-6.1–6.3 flow map | met | both run 1 grades |
| AC-7.1, AC-7.2 change impact | met | first evaluation runs 2 and 3 |
| AC-8.1 per-flow concurrency | met in the re-run | re-run run 1 |
| AC-8.2 wall time | not measurable: no hosted runs | the record states the trade-off |
| AC-9.1–9.4 selection and safety net | met | both run 1 grades and first runs 2 and 3 |
| AC-10.1, AC-10.2 simplest design | met by review: platform features first, trade-offs recorded | both records |
| AC-11.1–11.3 bottlenecks with sample sizes | met | both run 1 grades |
| AC-12.1–12.3 removal proposals | met | both run 1 grades |
| AC-13.1, AC-13.2 effect recorded | met | both evaluations |
| AC-14.1, AC-14.2 baseline and proof | met | every run read `se-zero-trust` and `se-verify` (transcripts); the records show `actionlint`, local test runs and dry-run selections |
| AC-14.3 scope | failed in the re-run; fix 5 not yet re-run | re-run run 1 |
| AC-NFR1.1, AC-NFR1.2 gates and tests kept | met in the re-run (traced replacement) | re-run run 1 |
| AC-NFR2.1 delegated reading (replaced by AC-NFR2.2 on 2026-11-24) | **not met** | neither evaluation spawned a subagent (0 spawn calls in the transcripts); the survey ran in one context. Whether this Codex configuration offers a subagent tool was not checked. These runs predate AC-NFR2.2, which lets a 26-file survey read directly but requires the record to say so |
| AC-NFR3.1 platform | met: GitHub Actions detected from the project | both records |
| AC-NFR4.1, AC-NFR4.2 untrusted input, no secrets | met | both run 1 grades |

## Results — Claude Code, 2026-11-24

Model `opus`. The first evaluation used the skill text after fixes 1–5 and grader v3; the re-run used
the text after fixes 6 and 7 and the AC-NFR2.2 survey rule, and grader v5. Grades are stored in
[ci-fixture/results](ci-fixture/results) as `claude-ci-eval-run*.txt` and `claude-ci-eval-2-run1.txt`.

| Evaluation | Skill text | Run 1 (49 checks) | Run 2 (13) | Run 3 (10) |
|---|---|---|---|---|
| First | after fixes 1–5 | 47 passed | 13 passed | 10 passed |
| Re-run | after fixes 6 and 7 and the AC-NFR2.2 survey rule | 50 of 50 passed (49 under v4; see below) | not run | not run |

The first evaluation found every planted problem with evidence, kept the security gate
unconditional, recorded the CSV export bug as a proposal without touching product code (fix 5
held), cited separate evidence for each entry (fix 4 held), and passed `actionlint`. Run 2 selected
`tests.billing, tests.api, tests.security` for the billing change; run 3 selected `ALL` for the
configuration change. Each session loaded `se-ci` through the Skill tool and nothing else.

In the re-run, run 1 loaded `se-ci`, `se-zero-trust` and `se-verify`, filed the missing cache under
Infrastructure with a cross-reference from Slow, said it read the 26-file survey directly, and again
left product code alone.

After the re-run, the bullets of the SE change baseline section were reworded family-wide to load
both skills by name (spec 001 AC-12.2), matching what fix 7 had already put in step 9. Step 9, which
the re-run exercised, did not change.

| Failure | Cause | Change |
|---|---|---|
| Missing dependency cache filed under Slow, not Infrastructure (run 1) | Skill: no rule for a finding that fits two buckets | File it in the bucket that names its fix, with a cross-reference in the other (fix 6) |
| `se-zero-trust` and `se-verify` never loaded (all runs) | Skill: "apply the SE change baseline" read as "run the checks yourself" | Step 9 loads both skills by name and names them in the changelog line (fix 7) |
| Main-branch full run stated in a paragraph, not a list row (re-run) | Grader: only list rows counted. The run met AC-9.3: a push to `main` passes no base, and `ci/affected.py` then selects every flow | Grader also reads a paragraph line that names pushes to `main` or a schedule together with every flow (v5) |
| No subagents on the first-run survey (run 1) | Not a skill-text defect: the fixture is 26 files (86 KB), which one context reads faster than it can brief readers | Criterion: AC-NFR2.1 replaced by AC-NFR2.2 (approved 2026-11-24). The survey step delegates above a size threshold and otherwise says it read directly; grader v4 checks that the record says which |

### Acceptance criteria where Claude Code differs from Codex

| Criterion | Result | Evidence |
|---|---|---|
| AC-4.1, AC-4.2 buckets and evidence | first evaluation: met except the cache finding's bucket (fix 6); re-run: met, with the cache finding under Infrastructure and a cross-reference from Slow | run 1 grades |
| AC-14.1 baseline skills | first evaluation: **not met**, the transcripts show no load of either skill; re-run: met, both skills loaded through the Skill tool and named in the changelog | session transcripts |
| AC-14.2 proof | met: `actionlint`, local test runs, and a dry run of the selection on sample diffs in a scratch copy | run 1 transcript |
| AC-14.3 scope | met: no product file changed; the CSV bug is a proposal | grader product-code check |
| AC-NFR2.1 delegated reading (replaced) | first evaluation: **not met**, 0 subagent calls although the Agent tool was allowed | run 1 transcript |
| AC-NFR2.2 size-scaled reading | re-run: met for a small survey. The record says "Reading: direct (26 tracked files, about 80 KB of history)", and the transcript shows no subagent calls. The delegated path is untested | re-run transcript and grade |

**Amendment, approved 2026-11-24.** AC-NFR2.1 asked for parallel low-cost readers on every first
run. On a 26-file project neither host delegated, and delegating would cost more than it saves.
AC-NFR2.2 replaces it: delegate when the survey is more than one context can read comfortably, and
otherwise say the survey read directly. The skill's rule of thumb is about 100 files or 250 KB of
text. Grader v4 adds one run 1 check that the record says which; it is a check for the new
criterion, not a correction. The delegated path still needs a fixture above the threshold to prove
it.

## Not done

- Runs 2 and 3 of the re-run, and a run with fixes 4–7, on Codex after its usage limit resets
  (2026-11-25).
- Runs 2 and 3 on Claude Code with fixes 6 and 7. The re-run covered run 1, where those fixes and
  the survey rule first apply.
- A fixture above the AC-NFR2.2 size threshold, to prove the delegated path.
