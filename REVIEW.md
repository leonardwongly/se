# Review and fixes — mandatory project-grounded baseline

## Latest revision: every code change

User-approved policy: mandatory zero-trust review and verification for every new or modified code change, with depth proportional to risk. This supersedes the earlier optional-control interpretation in the guide and visualization.

- Expanded zero trust from an agent-tool emphasis to application inputs, object/tenant authorization, data/sinks, state transitions, dependencies, CI, migrations, tests, generated code, and behavioral prompts/tools.
- Required both security review and functional verification in standalone execution workflows, including Why/Where/Who when the authorized task also changes code. Skill invocation itself is not evidence.
- Added project grounding throughout all nine skills: correct root/source state, local rules and maintained contracts, actual active callers/configuration, project-defined test/CI commands, fresh references, and unresolved-context handling.
- Preserved proportionate treatment of a literal UI label change. Generic conceptual explanations do not trigger unrelated project discovery.
- Distinguished unauthorized protected effects from expected redacted denial logging allowed by the project contract.
- Updated the map to make zero-trust review and verification required for code changes, concurrency optional, and project evidence the starting point for project-specific routes.

An independent all-nine review found two wording gaps: generic grounding could require unrelated private access, and standalone zero-trust work did not explicitly require ordinary functional verification. Both were corrected and rechecked. The [review record](validation/code-baseline/GROUNDING-REVIEW.md) retains initial findings and closure. The final small routing additions to Why/Where/Who, wording cleanup in How, and guide edits received direct review and structural checks; they were not separate coding-agent trials.

Two fresh agents then performed actual local synthetic code tasks using the skills and each fixture's own instructions, contracts, active caller, and Makefile. Independent checks confirmed both final implementations and detected the known defect in the original update fixture. See [current validation](VALIDATION.md).

## Earlier review retained below

The following findings and scenario IDs describe the preceding review. They remain relevant history, but are not additional fresh executions of this revision.

Scope: all nine skills, selection boundaries, cross-skill handoffs, authorization, evidence gates, concurrency, naming, and packaging. Two independent reviewers read all nine entrypoints; the integration owner assessed findings and made changes. A fresh evaluator then answered concrete fictional requests.

## Resolved issues

| ID | Gap or contradiction | Fix | Exercised by |
|---|---|---|---|
| F1 | Timing could lose verification exceptions or apply a different readiness vocabulary. | `se-when` preserves scoped reports and uses the same raw states and gate precedence as `se-verify`; a conditional plan is distinct from a CONDITIONAL gate. | R1, R2, R6, R15, R16 |
| F2 | Explanation mode forbade explicitly authorized read-only live inspection. | `se-zero-trust` permits relevant read-only evidence for system-specific explanations, while retaining mutation/probe boundaries. | R3 |
| F3 | Location ambiguity only needed resolution before mutation, although navigation is read-only. | `se-where` requires resolving or surfacing ambiguity before a definitive location; bounded candidate discovery may continue. | R4 |
| F4 | Cancellation request could be mistaken for a stopped writer; edits could continue after validation. | `se-concurrent` requires confirmed termination or revoked write capability, reconciliation before reassignment, and frozen scopes or an immutable combined snapshot for validation. | R5, R13 |
| F5 | A complete exception record could be accepted while its mandatory control was inactive. | Both verification and timing require current evidence that acceptance conditions hold; explicit policy-permitted no-control acceptance stays possible. | R6, R15 |
| F6 | Empty/skipped suites or unresolved criteria could support an unsupported completion claim. | Missing criteria/applicability are missing evidence under the existing precedence; zero tests cannot establish behavior. A review caught and corrected an initially overbroad NOT_READY sentence so known FAIL/BLOCKED still take priority. | R7, R16 |
| F7 | Generic testing guidance did not address AI behavior variability. | `se-verify` now covers model/prompt/tool/harness versions, representative cases, repeated trials when relevant, persisted outcomes, grader calibration, budgets, and bounded reliability claims. | R8 |

The two independent reviewers confirmed closure of their original findings. The assurance reviewer also confirmed the final F6 precedence correction. The evaluator reported no material contradiction in the final instruction bodies for the exercised cases. These findings are procedural-text issues, not demonstrated vulnerabilities in a running application.

## Overlap decisions

Overlap needed for standalone use remains deliberate. Small tasks need no nine-skill ceremony.

- `se-what` defines the acceptance contract; `se-how` explains or implements a mechanism.
- `se-why` establishes rationale; `se-how` establishes behavior and approach.
- `se-who` maps human/team accountability; `se-where` locates code and system responsibilities.
- `se-when` orders prerequisites while preserving gates; `se-verify` obtains or evaluates the evidence for those gates.
- `se-who` identifies responsibility; `se-concurrent` coordinates actual worker ownership and integration.
- `se-zero-trust` analyzes authority boundaries; `se-verify` qualifies evidence for the controls. Neither is a runtime enforcement mechanism.

Descriptions for Who, When, and Verify now make these boundaries more explicit. Other question-skill instructions had no additional actionable defect established by this review and were retained apart from naming.

## Naming and migration

All nine current folders and frontmatter names use `se-*`; UI titles use `SE …`. Guide labels use `/se-*`, with explicit Codex invocation shown as `$se-*`. No slash-command alias is registered. Existing installed skills are unchanged.

The old `engineering-*` bundle and baseline were preserved in task working storage. Historical validation is retained under `validation/history-2026-10-29` and is labeled as earlier evidence; it is not presented as a rerun of the new package.

See [validation and limits](VALIDATION.md), [raw question review](validation/QUESTION-REVIEW.md), and [raw assurance review with closure](validation/ASSURANCE-REVIEW.md).
