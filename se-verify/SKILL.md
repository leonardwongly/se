---
name: se-verify
description: Apply mandatory, risk-scaled verification and zero-trust review to every new or modified code change, or assess completion and release claims using revision-bound evidence. Use for behavioral correctness, test quality, and supported acceptance decisions; prerequisite scheduling is separate.
---

# SE Verify

Demonstrate behavior on the relevant revision/environment; separate check outcomes from acceptance or release.
Grounded claim support and causal understanding are the proof responsibility; verification
adds executed checks and acceptance decisions. Apply both directly when companion skills
are unavailable. A citation, explanation, visualization or worker consensus cannot replace a required check.

## Mandatory baseline for code changes

Every new or modified code change requires verification and a zero-trust review before completion, including tests,
generated code, runtime configuration, dependencies, migrations, CI, and behavioral prompts or tools. Scale depth to risk, not a full audit each time.
Apply it directly when companion skills are unavailable; no sibling skill is an installation dependency.

Inventory changed surfaces and affected callers, data, and trust boundaries. Review untrusted inputs,
identity and resource/tenant authorization, validation at enforcement points, least privilege, secret
handling, and failure behavior wherever affected. Distinguish the application's authority over data
and actions from the coding agent's permission to edit or run commands; neither establishes the other.
Record acceptance and zero-trust findings, selected checks, and remaining gaps, including a reason
when a concern does not apply. Existing code or clean lint alone cannot establish absence of security risk.

Ground the assessment in the actual project: verify root, branch/revision and dirty state (or a non-Git
snapshot/digest), applicable local instructions and contracts, and active changed paths/callers and integration boundaries.
Discover actual commands from manifests, CI workflows, and configuration; do not substitute guessed generic commands.
Cite current code locations for findings. Reuse prior evidence only while its scope, source state, and environment remain applicable.

## Map the claims

1. Extract acceptance criteria and material risks from the task and applicable project rules.
2. Name the observable behavior, expected result, and environment required for each claim.
3. Map existing tests or direct observations to each criterion; identify uncovered behavior.
4. Select applicable behavioral, build, type, lint, and integration checks by risk and project requirements.
5. Identify authorization, infrastructure, data, and device prerequisites before execution.

Use a compact matrix when several criteria exist:

| Criterion | Behavior / oracle | Required environment | Check | Result | Evidence |
|---|---|---|---|---|---|

Do not invent acceptance criteria merely to fill a template. Do not remove a required check
because it is inconvenient or unavailable. Explain any justified applicability decision.
Execute the selected checks; listing tools or planned commands is not verification. Do not run every
tool indiscriminately. For low-risk text-only code edits, direct inspection plus an appropriate render
or static check may suffice; record the rationale and avoid weak test additions for ceremony.
If required scope, criteria, or check applicability cannot be established, treat that as
missing required evidence under the gate precedence below; do not override a known
non-excepted failure or blocker. An empty or all-skipped suite cannot establish a behavioral claim.

## Check behavior and test quality

- Prefer externally observable behavior over assertions that repeat implementation details.
- Include relevant failure, boundary, recovery, and permission cases based on actual risk.
- For security-impacting code, execute positive, denial, and boundary regression checks against the
  affected enforcement path; assert denied operations cause no unauthorized resource mutations
  or downstream actions. Expected redacted security logging is allowed when the project contract
  permits it. Inspect actual state and effects, not just the returned status.
- For a user journey, perform the action and inspect visible state and persisted effects.
- Confirm the test reaches the changed path and uses an oracle independent of that path.
- Distinguish a real dependency from a stub; state what a simulated response cannot prove.
- Inspect skipped tests, empty selections, swallowed failures, and missing assertions.
- Treat coverage as a gap-finding signal with an explicit denominator, never proof of correctness.
- Worker-reported success or a self-generated all-green suite alone does not evidence security;
  inspect enforcement and independently assess test oracles, reachability, and observed effects.

For consequential fixes or new harnesses, proportionately test the tests: show failure on the known
defect or a controlled isolated mutation, then success with the fix; a manual negative control may suffice.
Check that failure comes from the intended assertion, not setup, compilation, or connectivity.
Restore any temporary mutation and verify the final source state before reporting success.
Do not mutate production, broaden permissions, or add weak tests solely to increase counts.
If this check is unsafe or unjustified for the task, record its limitation instead of faking proof.

For model-dependent behavior, evaluate model, prompts, retrieval, tools, and harness together on
representative success, refusal, and recovery cases; record versions and repeat trials where variation matters, within the authorized cost budget.
Grade actual outcomes, calibrate model-based graders against human judgments, and report sample size,
failures, and limits; one successful run does not establish reliability or general model quality.

## Execute and preserve provenance

Record revision/dirty state, environment, versions/configuration, timestamp with timezone, exact command
or manual action, expected/actual outcome, exit status, and evidence location; use a patch/digest where useful.
Keep secrets out of commands and logs; sanitized parameters must remain reproducible in context.
Evidence must identify the source state actually tested, not simply the current branch name.

Run focused checks first, then the required combined checks after integration.
Preserve branch protections, required CI checks, and independent review requirements.
Do not weaken assertions, bypass gates, or disable checks merely to obtain a green result.
Repeat only when changes, failures, stale evidence, or unresolved risk justify it.
Review the final diff and preserve a stable source/configuration snapshot matching the evidence.
If later edits affect a checked surface, invalidate that evidence and rerun the affected checks.
Do not erase a failure with a passing retry; retain the failed run and explain the cause.
If a flaky check passes later, report the instability until a bounded resolution is evidenced.

Separate local/unit, integration, simulator/emulator, physical device, hosted CI, and deployed proof.
A build does not prove a user journey; a local mock does not prove provider integration.
A deployed check applies to its observed deployment identity and configuration.
Do not deploy, purchase infrastructure, or modify production solely to obtain evidence without authorization.

## Individual check states

| State | Meaning |
|---|---|
| `PASS` | Valid evidence demonstrates the expected outcome for the stated scope |
| `FAIL` | Executed check demonstrates a violated expectation |
| `BLOCKED` | A required check cannot complete because of a concrete external prerequisite |
| `NOT_RUN` | Applicable check has no completed execution |
| `NOT_APPLICABLE` | The check does not apply, with a task-specific rationale |

Unavailable infrastructure is `BLOCKED`, never `NOT_APPLICABLE`.
Missing or stale evidence does not turn an earlier recorded `FAIL` into a pass.
Retain raw check results even when an authorized human accepts an exception.

## Gate decision

Evaluate required checks for the declared scope in this exact precedence order:

1. Any unresolved, non-excepted `FAIL` yields gate `FAIL`.
2. Otherwise, any required `BLOCKED` check yields gate `BLOCKED`.
3. Otherwise, missing, invalid, stale, or `NOT_RUN` required evidence yields gate `NOT_READY`.
4. Otherwise, a valid scoped human-accepted exception yields gate `CONDITIONAL`.
5. Otherwise, all required criteria are evidenced and the gate is `PASS`.

An exception records the authorized human, affected check/criterion, reason, residual risk,
scope, expiry or review condition, compensating controls and their verified status, and
remediation owner. Never grant yourself an exception. Validate this record before treating
a failure as excepted, including current evidence that mandatory compensating controls
and other acceptance conditions hold. A documented but unverified or unmet condition
does not activate the exception. An incomplete, expired, out-of-scope, or unauthorized exception leaves
the failure non-excepted, so the first precedence rule yields `FAIL`. A proposed waiver
cannot move a known failure to `NOT_READY` while its approval or required metadata is pending.
Exception-covered failures remain check `FAIL`; the exception affects only the gate decision.
Record no compensating control only when the authorized human explicitly accepted that
arrangement and project policy permits it; do not invent a control or silently drop a mandatory one.
An exception cannot override a separate blocker or missing required evidence under this precedence.
Gate `PASS` is bounded to the declared scope, not blanket production readiness or release permission.

## Output contract

Report gate/scope, changed surfaces, acceptance and zero-trust findings, and check results with evidence and final diff/snapshot references.
Identify the tested revision, environment, limitations, accepted exceptions, and remaining blockers.
For each blocker give the concrete missing prerequisite and next action or responsible owner.
State only completion, deployment, performance, or security claims supported by the recorded evidence.
Do not call code complete with missing baseline evidence; report partial work and the gate. Baseline `PASS` does not certify a full audit or authorize release.

## Primary references

- [Google Testing Blog: Test Behavior, Not Implementation](https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html): behavior-oriented test design.
- [SLSA provenance](https://slsa.dev/spec/v1.2/provenance): tracing artifacts to where, when, and how they were produced.
- [Anthropic: agent evaluations](https://www.anthropic.com/research/demystifying-evals-for-ai-agents): outcomes, repeated trials, and grader calibration.

The check vocabulary and gate precedence are this workflow's conventions, not SLSA requirements.
