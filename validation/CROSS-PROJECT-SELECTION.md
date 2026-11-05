# Final-policy evaluation on a second real project

This evaluation uses eight fresh tasks on **ProjectPortfolio**, a Node-based static
website, rather than repeating the maintenance tasks in this skills repository.
All tasks run under the same final routing policy from the earlier evaluation.
The task prompts omit skill names and invocation syntax. Selection, delivered
instructions, task application and project checks are assessed separately.

**All twelve expected skill roles were selected and applied across the eight fresh
tasks under one unchanged final policy. All eight bounded task outcomes passed
independent application review, including three actual task delegates.** A review
pass means the reviewer correctly found and assessed defects; it does not mean
the original project was defect-free. No additional routing-policy repair or
selection-task rerun was needed. Independent grading and subsequent remediation
workers are outside the eight-task/three-delegate cohort.

## Frozen system and task matrix

The public project baseline is
[`4a50ea995c37132bcfee5c64fd908d35ca0cef96`](https://github.com/leonardwongly/ProjectPortfolio/tree/4a50ea995c37132bcfee5c64fd908d35ca0cef96).
The original checkout was clean. Separate local checkouts isolate the read-only,
implementation and visual tasks; the original project is not modified or published
by this evaluation. The resulting maintenance patch is an evaluation artifact,
not a change merged into ProjectPortfolio or deployed to its website.

Before launching any task, the coordinator froze the eight prompts, expected
minimum selections, acceptance criteria, project revision, global instruction
hash and all twelve installed instruction hashes. The final global policy hash is
`5b6d6d2b2250889c07d879035c9fd9c777ec32eea2ed92e768bc455ab998e255`.
The runner checks policy and skill identities before each launch and the policy
again after completion. The [routing section](expanded-selection/routing-policy.md)
is unchanged; unrelated global configuration stays private.

| Fresh task | Expected skills | Required application |
|---|---|---|
| Scope | `se-what`, `se-proof` | Project-grounded brief for machine-readable audit output, compatible human mode and observable acceptance. |
| Rationale | `se-why`, `se-proof` | Explain exclusive staging, revalidation and rename using actual writer, callers, history and counterexamples. |
| Mechanism | `se-where`, `se-how`, `se-proof` | Locate and trace preload, fetch, cached fallback, emergency response and non-navigation behavior. |
| Readiness | `se-when`, `se-verify`, `se-proof` | Sequence a future reading update; execute available checks and distinguish current evidence from future release readiness. |
| Expertise | `se-who`, `se-proof` | Launch one read-only scanner reviewer, then independently assess its findings. |
| Verification | `se-zero-trust`, `se-verify`, `se-proof` | Exercise allowed/denied update messages and show a missing-origin-guard mutation causes the intended assertion failure. |
| Visual | `se-visualise`, `se-proof`, `se-zero-trust`, `se-verify` | Produce a source-grounded animated fallback explanation and test its actual rendered controls. |
| Team | `se-who`, `se-swarm`, `se-concurrent`, `se-proof`, `se-zero-trust`, `se-verify` | Two workers implement disjoint CLI changes; coordinator integrates and verifies stable combined output. |

[Inputs and prompt identities](cross-project/inputs.json),
[acceptance criteria](cross-project/ACCEPTANCE.md),
[actual read observations](cross-project/observations.json), and
[independent application grades](cross-project/application-grades.json) retain the
basis for each outcome. Expected selections are minimum matches, not a prohibition
on other relevant skills. Extra selections are recorded; this is not a false-positive
routing benchmark. The scope and team prompts are independent tasks: an explicitly
labeled proposal in the brief is not required to match the team's separately frozen
implementation contract.

## Actual use and delegation

A skill announcement or successful file access alone is insufficient. Selected
receipts identify the actual installed-file read, instruction delivery, and
corresponding source inspection, checks or artifacts. Application grades assess
whether the task outcome follows from that evidence. They are model-assisted
reviews plus executable checks, not human-calibrated evaluation scores.

Native delegated-agent records are audited by their own turn identifiers, excluding
inherited parent turns. The implementation workers read relevant instructions in
their own contexts. Their initial aggregate outputs were truncated; they recovered
missing sections before edits. The audit checks source segments and their ordering,
not just a parent's claim that instructions were handed off. The specialist's
own-context evidence is recorded separately. Exact private handoff text, session
identifiers and raw transcripts are not published. Only top-level prompts are
asserted to omit skill names; this does not establish name-free handoffs or child
discovery independent of parent guidance.

The team uses exactly two concurrent implementation workers with disjoint script
and test ownership. The parent owns the shared runbook and combined checks. The
specialist task explicitly requests one reviewer. This evaluates skill selection
for requested delegation; it does not establish that agents independently choose
the optimal team size or that concurrency is faster than serial work.

## Real work and behavioral evidence

The team adds `--json` to the existing reading metadata and performance-budget
CLIs. It preserves no-argument human output, existing exports and audit protections.
JSON outcomes distinguish `pass`, `fail` and `error`; argument rejection occurs
before project input access. Tests use actual subprocess entrypoints and temporary
fixtures, including invalid arguments, malformed/missing input and unsafe paths.

The independent checker was designed from the frozen contract before inspecting
worker implementation. Its SHA-256 remains
`43a2870c98858bade479c2bbffc3e831cd8db32d51859bdbb25017892494c1c8`.

| Evidence | Original / initial result | Final scoped result |
|---|---|---|
| Independent CLI checker | 6/38 pass; 32 intended new-contract failures | 38/38 pass |
| Team's combined focused tests | Original new-test controls detect human output/argument-order defects | 41/41 pass |
| Original broader operations suite | 27 pass; one startup failure from missing `yaml` | Preserved as blocked in the trial environment |
| Separate CLI-only integration | Reuses existing lock-matching dependencies; no installation | 350/350 security tests pass; `npm run validate` passes |
| Final integration including scanner repair | Original scanner oracle: 4/14 | 14/14 scanner and 38/38 CLI checks; 357/357 security tests within passing `npm run validate` |
| Service-worker mutation check | Actual source: 6/6 pass | Removing only origin guard: 5/6, intended protected-effect assertion fails |

These are overlapping suites and separate environments, not additive coverage.
The service-worker checks use the actual source in a Node VM with stubbed browser
APIs. They establish the tested guards and effects in that harness, not real
browser activation or production behavior. The mutation is confined to an
in-memory copy; tracked files remain unchanged.

The integration check uses an immutable source copy with existing dependencies
matching the project's lockfile (`yaml` 2.9.1 and Playwright 1.63.0). It does not
retroactively turn the original missing-dependency run into a pass. `npm run validate`
executes the build, generated-file parity, repository hygiene, reading/performance
audits, security tests and configured aggregate coverage thresholds. Subprocess CLI
branches have separate behavioral evidence and are not all represented in the
parent-process coverage report. No repository-wide coverage claim is made.

[Original checker results](cross-project/team-oracle-before.json),
[repaired results](cross-project/team-oracle-after.json),
[checker design and limits](cross-project/team-oracle-notes.md), and
[integration results](cross-project/integration-results.json) preserve these boundaries.

## Visual and preserved repairs

The [animated walkthrough artifact](cross-project/offline-navigation-walkthrough.html)
explains four requested navigation paths plus HTTP-error and non-navigation
boundaries. It is an explanation of the pinned service-worker revision, not a live
service worker or production telemetry. Motion is schematic. It includes finite
playback, manual stepping, pause/reset, keyboard access, static text and reduced
motion. Relative source links target its original project location; the published
copy is retained byte-for-byte, and the reproduction instructions restore that
location. Relative-link navigation was not verified in the blank-page preview.

The visual task retained a failed supplemental harness assertion about asynchronous
call order, corrected it against actual source behavior, and reran it. Browser
`file:` navigation and a local server were blocked. The task used exact HTML in a
blank browser preview instead; this is preview evidence, not a successfully served
or deployed website. A keyboard interaction issue was repaired and affected checks
were repeated. Final-source identity and actual preview claims are evaluated in the
application grade.

Other retained failures include macOS temporary-path aliases initially preventing
new subprocess tests from reaching their entrypoints, and an initial heredoc setup
failure in the mutation check. Corrected controls then reached the intended
behavioral assertions; setup failures are not counted as detector sensitivity.
The final policy's truncated-read recovery was exercised without changing the
policy or suppressing the original truncated output.

## Confirmed project defects and separate remediation

The specialist review correctly identified two defects on the frozen baseline:
malformed attribute tokens emitted diagnostics without consuming the attribute
budget, and some EOF-truncated start tags produced no diagnostic. A 2,051-byte
input generated 1,024 findings totaling 1,082,368 logical characters despite
`maxAttributes: 1`. This measures diagnostic text, not heap allocation or an
observed exhaustion event. Existing tests passed while these cases remained uncovered.

The original review also reported a double-`<` discrepancy as unresolved browser
behavior. A **separate post-trial DOMParser probe** then confirmed that
`<<img src="data:...">` produces an image element and literal `<` text in the
observed browser. The scanner had discarded that attribute. This establishes a
scanner/browser difference, not a remote-resource download or deployed exploit.
[Browser observations](cross-project/scanner-browser.json) retain that distinction.

A separately assigned repair worker changed only the helper and a new regression
file in the integration copy. Malformed tokens now consume the existing budget;
diagnostics use bounded text with source offsets; EOF is checked after the final
token; and an invalid opener no longer swallows a following valid start tag.
A separate reviewer inspected those changes and both callers. The independently
frozen scanner checker moves from **4/14 to 14/14**; its positive controls passed
before repair, and its ten failures reached intended assertions.

The original eight trial records remain unchanged. The final combined patch passes
**357 security tests**, `npm run validate`, the original **38-case CLI checker**, and
the **14-case scanner checker**. Both patches together reproduce all seven final
changed files byte-for-byte. [Final integration results](cross-project/final-integration-results.json),
[original scanner results](cross-project/scanner-oracle-before.json),
[repaired scanner results](cross-project/scanner-oracle-after.json), and
[separate remediation review](cross-project/remediation-review.json) identify the
tested sources and limits. No claim of full HTML-parser equivalence is made.

## Reproduce the deterministic checks

Use a disposable checkout at the pinned ProjectPortfolio revision. The patch is
[maintenance.patch](cross-project/maintenance.patch); it reproduces all five tested
changed files byte-for-byte. Apply the separate
[scanner-hardening.patch](cross-project/scanner-hardening.patch) afterward to reproduce
the final seven-file integration. Neither patch is applied to the original checkout.
The [checker](cross-project/check_team.py) needs Python and Node, with no added
Python packages. Use absolute paths appropriate to your machine:

```sh
git -C "$PROJECT" checkout 4a50ea995c37132bcfee5c64fd908d35ca0cef96
python3 "$EVIDENCE/check_team.py" "$PROJECT" before.json
git -C "$PROJECT" apply "$EVIDENCE/maintenance.patch"
python3 "$EVIDENCE/check_team.py" "$PROJECT" after-cli.json
node "$EVIDENCE/check_scanner.mjs" "$PROJECT" scanner-before.json
git -C "$PROJECT" apply "$EVIDENCE/scanner-hardening.patch"
node "$EVIDENCE/check_scanner.mjs" "$PROJECT" scanner-after.json
python3 "$EVIDENCE/check_team.py" "$PROJECT" final-cli.json
```

The initial CLI and scanner checks intentionally exit 1 on original behavior.
The final checkout passes 38 CLI cases and 14 scanner cases. For full local integration, provision dependencies from
the project's lockfile through your normal authorized process, then run
`node --test tests/security/*.test.mjs` and `npm run validate` in that checkout.
The walkthrough can be copied unchanged to its original
`docs/offline-navigation-walkthrough.html` location for local preview.

These commands rerun deterministic checks, not agent selection. Repeating selection
requires fresh CLI sessions with the saved prompts, installed instructions and
policy, equivalent tools/access, and independent inspection of actual tool outputs
and delegated own-turn evidence. Use `codex exec -C "$PROJECT" -s read-only --json
-o result.txt - < task.txt` for read-only prompts; implementation and visual prompts
use `workspace-write` in separate checkouts. Do not use an ephemeral session if you
need native delegated-agent evidence. Skill names appear in global routing and
catalog descriptions, so this is configured automatic routing, not metadata-only
or instruction-free discovery.

## Limits

- One different public project, one configured macOS host, one run per fresh task;
  no statistical reliability estimate, repeated-sampling study or hidden benchmark.
- Codex CLI 0.166.0 with locally configured `gpt-6-astra`, high reasoning, OpenAI
  provider. Provider model identity is not independently attested. This does not
  validate fresh desktop-native routing or other models/platforms/projects.
- Node 26.13.0 was used; the project CI targets Node 24. Node 24, hosted CI,
  `validate:full`, production services and deployment were not exercised.
- Filesystem guards instrument named APIs and snapshots detect retained mutations;
  they are not an operating-system audit of transient effects or all races.
- Sanitized receipts and raw-log hashes identify retained private evidence; public
  readers can reproduce code checks but cannot independently inspect every omitted
  session event from this repository alone.
- A correct readiness assessment can report `BLOCKED`. Application success does
  not convert a blocked release gate into readiness, authorize deployment, or
  certify security, accessibility or user comprehension.
