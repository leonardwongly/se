# Validation — mandatory project-grounded baseline

## Automatic-selection evaluation — 5 November 2026

Two fresh CLI agents selected and read relevant installed skills without skill names in their task prompts. Both scoped trials passed. The code trial also fixed missing HTML-reference validation; nine focused regressions and 21 independent acceptance checks passed. See [results, evidence, reproduction and limitations](validation/AUTOMATIC-SELECTION.md). These results are separate from the historical fixture exercises below.

## Available-tools and skills update

All twelve standalone entrypoints now include relevant capability discovery, current tool/skill contract inspection, evidence-based selection, execution and output assessment, plus role-specific use guidance. The update preserves scope, authority, independent usability, verification gates and bounded completion. Textual consistency review and the package checks cover this instruction update; earlier observed agent trials are historical, not reruns of the revised instructions. That earlier review did not include a live routing trial. The later [automatic-selection evaluation](validation/AUTOMATIC-SELECTION.md) records two fresh CLI tasks using the installed skills and global routing instructions; it does not establish general provider adherence or connector reliability.

Current package: twelve skills. See the [expansion review and execution evidence](validation/EXPANSION-REVIEW.md) for proof, visualise, swarm, specialist selection and the updated guides. The nine-skill results below describe the original baseline and remain historical evidence.

Date: 31 October 2026, Asia/Singapore. Scope: nine uninstalled skills, textual review, real execution in two isolated synthetic Python projects, and an interactive-map preview. No production-project or provider enforcement claim is made.

## What ran

| Validation | Actual result | Evidence |
|---|---|---|
| All-nine consistency review | Two identified baseline/grounding gaps corrected and rechecked; no remaining material finding in that scope | [Review and closure](validation/code-baseline/GROUNDING-REVIEW.md) |
| New code: account export | Fixture `make check`: 10 tests passed; tenant enforcement negative control detected four intended failures | [New-code report](validation/code-baseline/NEW-CODE-REPORT.md) |
| Updated code: account archive | Fixture `make check`: 8 tests passed, including 75 actor/account/hint combinations; tests detected the original defects before repair | [Updated-code report](validation/code-baseline/UPDATED-CODE-REPORT.md) |
| Independent new-code checks | 7 tests passed, including cross-tenant denial, allowlisted output, malformed IDs, and unchanged state | [Log](validation/code-baseline/new-independent.log) |
| Independent updated-code checks | 8 tests passed, including forged tenant hints, permitted operations, malformed IDs, and denial without mutation/events | [Log](validation/code-baseline/update-independent.log) |
| Same independent grader on original update | Failed as expected: cross-tenant bypass assertion failed; malformed-ID and hint behavior also violated the contract | [Original log](validation/code-baseline/original-update-independent.log) |
| Interactive map | Current project-grounding paths, required code-change baseline, optional concurrency, and narrow/light/dark layout checks passed in the sandbox preview | [Check record](validation/code-baseline/VISUAL-CHECKS.md) |
| Package structure | Nine entrypoints, names, metadata, default discovery policy, and local links checked with bundled validator plus package checks | [Structural output](validation/STRUCTURAL-RESULTS.txt) |

The independent grader was authored outside the fixture projects; implementing agents were instructed not to read it. Its 15 final tests used project contracts as oracles. This is two observed local coding-agent runs, not a statistically measured agent success rate. The known-defect assertion failure demonstrates sensitivity to the actual tenant bypass; setup/environment failure is not used as evidence of detection.

## Project grounding observed

Both agents used each fixture's local instructions and maintained security contract, traced its active transport/service path, discovered `make check` from the project Makefile, retained source digests/diffs, and distinguished local service authorization from authentication-provider or deployment proof. They did not substitute the archived design for the maintained contract or rely on the original green test suite as adequate evidence.

The export returns only public fields and checks stored identity/tenant/ownership. The archive fix preserves its signature while removing caller-supplied tenant hints from authority. Denied operations leave protected account and event state unchanged, as required by these fixture contracts. Trusted store shape, sequential in-memory state, and pre-authenticated transport identity remain explicit fixture assumptions.

## Reproduce the independent checks

From this repository root:

```sh
python3 validation/code-baseline/grade_fixture.py new validation/code-baseline/new
python3 validation/code-baseline/grade_fixture.py update validation/code-baseline/update
python3 validation/code-baseline/grade_fixture.py update validation/code-baseline/original-update
```

The first two commands should pass; the last is an intentional known-defect run and should fail. To run an implementation's own project checks, change into its `new` or `update` fixture folder and run `make check`. All fixture data and credentials are synthetic. Source, tests, retained failures, final diffs, and source-identity evidence are packaged alongside each fixture.

Historical authoring structural validation used `python3 work/validate_se_bundle.py` in the authoring task, calling the bundled skill-creator `quick_validate.py` for each skill. On another host, run `python3 /path/to/skill-creator/scripts/quick_validate.py /path/to/se-skills/se-verify` for each skill folder. ZIP contents are byte-compared to packaged source and checked for integrity; `MANIFEST.sha256` records package-file digests.

## Limits and history

- Not installed; actual fresh-host skill discovery, automatic routing, and production Codex inline rendering have not been tested.
- The project exercises validate local fixture behavior, not an actual user repository, hosted database, authentication provider, CI runner, concurrent production mutation, or deployment.
- Markdown instructions do not themselves enforce authority or gate decisions. Host/runtime controls must implement those boundaries.
- The all-nine reviewer also supplied five clearly labeled synthetic response examples for low-risk edits, unavailable integration infrastructure, ambiguous targets, stale policy, and general concepts; these are illustrations, not additional executed code tests.
- Earlier [R1–R16 decision responses](validation/FORWARD-RESULTS-2026-10-31.md) and [17-case historical record](validation/history-2026-10-29/VALIDATION.md) are retained as earlier evidence, not counted as fresh trials of the current revision.
- During the original validation, no installation, external publication, production probe, payment, source-control commit, push, merge, or deployment was performed. Subsequent repository publication is separate from that validation scope.

## Publication validation

The portable check is `python3 scripts/validate.py`; see [publication notes](PUBLICATION.md). Current custom UI and README media checks are in [CUSTOM-GUIDE.md](validation/CUSTOM-GUIDE.md). Earlier animation runtime evidence in [ANIMATION-CHECKS.md](validation/ANIMATION-CHECKS.md) is historical. Historical authoring paths were normalized for publication; retained source hashes and observed test outcomes were preserved.
