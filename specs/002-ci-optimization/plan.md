# 002 — Plan

## Shape

`se-ci/` is one skill.

`se-ci/SKILL.md` walks through the run loop:

1. ground
2. survey (first or incremental)
3. classify
4. update the record
5. update the flow map
6. find bottlenecks
7. propose and make CI changes
8. verify
9. record the effect

`se-ci/references/` holds the material each step loads on demand:

| File | Contents |
|---|---|
| `ci-md-template.md` | Record skeleton: summary, survey coverage, the 7 buckets, flow map, changelog, and the entry format from AC-4.1 |
| `decision-model.md` | How to find a decision model, the classification prompt and JSON schema for the fallback, and score recording |
| `flow-map.md` | How to derive flows from entry points, routes, jobs and dependency graphs; the Mermaid conventions; shared-foundation marking |
| `affected-tests.md` | Selection mechanisms per ecosystem, preferring what is already installed. Also the fallback rules from AC-9.2 and AC-9.3 |
| `ci-shape.md` | Concurrency, matrix and sharding, caching, and job graph patterns for GitHub Actions, GitLab CI and generic runners; FR-8 checks |
| `bottlenecks.md` | Metrics and where to read them (`gh run list`, `gh api …/jobs` timing, JUnit reports, test durations); flake detection; value scoring |
| `pruning.md` | Evidence rules for FR-12, never-remove rules, and the separate-change procedure |

The selection mechanisms in `affected-tests.md`:

| Ecosystem | Mechanism |
|---|---|
| Path filters | `paths` / `rules:changes` in the CI platform |
| JavaScript monorepos | `nx affected`, `turbo --filter`, `jest --findRelatedTests` |
| Python | `pytest --testmon`, or an import graph |
| Go | `go list -deps` |
| Bazel | `bazel query rdeps` |

`agents/openai.yaml` matches the other skills.

## Links to other skills (install-together group, as decided for spec 001)

| Step | Skill |
|---|---|
| Parallel first-run survey | `se-swarm` (fan-out) |
| Flow map rendering | `se-visualise` |
| Change impact | `se-impact` |
| Numbers | `se-benchmark` |
| Run log | `se-decision-log` |
| Removal reasoning | `se-principles` › "subtract before you add", "test behavior, not implementation", "explain the number" |
| Baseline | `se-zero-trust`, `se-verify` |

Each link has a one-line fallback for when that skill isn't installed. The README group lists `se-ci` with these skills.

## Key decisions

- **The record lives in one file, `CI.md`, with the flow map inside it.** One place to read, and it keeps the budget honest.
  - Rejected: a separate diagram file, because it drifts from the record.
- **The buckets are fixed.** A decision model needs a predefined option set, and fixed buckets keep runs comparable.
- **Decision model detection order:**
  1. a tool in the host's catalog that does classification;
  2. a model or endpoint the project configures;
  3. otherwise the fallback (AC-3.2), run on a cheap model, which is Haiku per your model guide.

  Paid or off-machine calls need approval (AC-3.3).
- **The safety net comes before any selection.** AC-9.2–9.4 apply before a single test is skipped. Without them, affected-only testing trades speed for silent misses.
- **Removals are proposals.** Removals ship as their own PR with an evidence table, so review cost stays low and the action can be undone.

## Test strategy

The fixture lives in `validation/ci-fixture/`. It's a small Python project with three flows (`api`, `billing`, `reports`) and one shared `config` module. It has a GitHub Actions workflow that runs everything in one serial job.

Planted problems:

| Problem | Planted case |
|---|---|
| Slow | a test that sleeps for 3 seconds |
| Flaky | a test seeded to fail 30% of runs |
| Redundant | a duplicate assertion test |
| Never fails | a test with no failures in the history |
| Required gate | a security check |
| Coverage gap | an untested `reports` export path |

The fixture also includes a recorded history: JSON for 30 CI runs, 6 PRs and 4 issues under `.ci-history/`. (Implementation note: the project README points agents at the exported files, so the planned offline `gh` shim was not needed. The grader also gained a `self-test` mode with a hand-written reference answer as its positive control, and `validate.py` runs it.)

The grader is `validation/ci-fixture/grade_ci.py`. It checks the output of two headless runs (`claude -p`, then `codex exec`) of `se-ci`.

| Run | Criteria | What the grader checks |
|---|---|---|
| Run 1 (first) | AC-1.1–1.2 | `CI.md` exists and states the survey coverage and file count |
| | AC-4.1–4.2, AC-5.1, AC-5.4 | every planted problem sits in the right bucket with evidence, within the budget |
| | AC-6.1–6.3 | the flow map has the 3 flows plus the shared foundation |
| | AC-8.1, AC-9.1–9.4 | the proposed workflow has parallel per-flow jobs, affected selection, a full-suite fallback and a default-branch full run, and keeps the gate |
| | AC-12.1–12.3 | removal is proposed separately, not applied |
| | AC-3.2 | the method used is labelled |
| Run 2, after a scripted `billing` change | AC-2.1–2.2 | incremental update with a new revision marker |
| | AC-5.2 | no duplicate entries |
| | AC-7.1, AC-9.1 | affected flows are `billing` plus its dependents only |
| | AC-13.1 | the before-and-after effect is recorded |
| Run 3, after a `config` change | AC-7.2, AC-9.2 | the full suite is selected |

Run 3 is cheap: it only asks which tests to run.

Structural checks go through the spec 001 validator: inventory, links, references and description length.

AC-NFR1.1–1.2 and AC-NFR4.1–4.2 are checked by the grader. It confirms the gate is still present and no test was skipped or deleted in the changed workflow, and it scans `CI.md` for secret patterns.

Limits: one fixture and two hosts make a smoke evaluation, not a success rate. That gets recorded as such.

## Affected files

- New: `se-ci/` (`SKILL.md`, `agents/openai.yaml`, and 7 references), `validation/ci-fixture/…`, `validation/CI-SKILL.md` (results).
- Changed: `scripts/validate.py` (`EXPECTED` gains `se-ci`; fixture grading added as a dry structural check), `README.md` and `MANIFEST.sha256`.

## Risks

| Risk | Mitigation |
|---|---|
| Affected-only selection misses a break | the AC-9.2–9.4 safety net, and the record logs any break caught by a full run |
| The record bloats over time | the budget, merging and retirement (FR-5), and the grader checks the budget |
| "Read every line" is costly on big repos | delegated readers above the size threshold (AC-NFR2.2; the skill's rule of thumb is about 100 files or 250 KB of text); only the first run does it |
| Classification is wrong | a fixed option set, recorded scores, and a confidence threshold below which an entry is marked "unconfirmed" |

## Order

Implement after spec 001, because `se-ci` links to the ported skills. Use the same branch and PR. The commits are separate.
