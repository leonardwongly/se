---
name: se-when
description: Plan prerequisites, execution order, migration sequencing, and rollout timing using current engineering readiness evidence. Use for when to proceed or what must happen first; preserve verification gates rather than replacing them with a schedule. Does not create automations or grant deployment permission.
---

# SE When

Translate an engineering timing question into observable prerequisites and a safe
execution sequence. Use calendar dates only when grounded in actual constraints.

## Ground the task in the project

For project-specific work, reuse a current verified project brief and refresh changed facts.
For a general conceptual question, use labeled examples without unrelated project access.
Confirm the target root, branch/revision and uncommitted work (or non-Git source identity),
applicable local instructions, and the specific component/environment before conclusions.
Read relevant maintained contracts, active callers/configuration, and actual test/CI setup;
cite exact source locations and separate current facts, proposals, and stale historical context.
Resolve material conflicts or missing scope before dependent decisions; continue bounded
independent work. Do not infer policy solely from existing code or a generated working directory.

## Frame the decision

Identify the action whose timing matters, its target environment, the desired
outcome, and any fixed deadline or dependency. Distinguish “what must happen first?”,
“are we ready now?”, and “what is the realistic schedule?”.

Use existing context before asking for missing information. Ask when uncertainty
changes the migration order, compatibility window, authorization, or release impact.
For estimates, state assumptions and uncertainty instead of inventing precision.

## Build the dependency sequence

1. Identify prerequisites that directly enable the requested action. Include
   contracts, data preparation, required access, and dependent releases as relevant.
2. Separate hard dependencies from work that can proceed independently. Name an
   owner when known; otherwise identify the responsible role without inventing one.
3. Define a completion condition for each consequential step. Prefer an observable
   result to labels such as “testing complete” or “production ready”.
4. Put integration checks at the point where dependencies meet. Avoid postponing
   discovery of incompatible assumptions until the final rollout.
5. Identify irreversible steps and the latest point at which a safe pause, rollback,
   or forward recovery remains available. Match detail to the actual risk.

For compatible schema or API changes, consider whether consumers can migrate
gradually before old behavior is removed. Verify the system's actual compatibility
constraints rather than applying a migration pattern mechanically.

For AI changes, place evaluation before decisions that depend on model quality.
Use representative cases and agreed acceptance criteria when quality is uncertain.
Identify when human review is needed and how changed prompts, models, retrieval,
or tool permissions affect the relevance of earlier evaluation results.

## Assess readiness using evidence

Every new/modified-code task must supply a project-grounded zero-trust review and
verification evidence before unconditional completion. A small change may justify
lightweight checks; it does not waive either responsibility. A missing required baseline
record is missing evidence under the gate precedence below, not assumed acceptance.

Consume an existing verification report only when its scope, revision, environment,
and conditions still apply. Preserve its raw check results, gate, accepted exceptions,
and blockers; a timing recommendation must not silently strengthen or weaken that decision.

When assessing readiness directly, record checks as `PASS`, `FAIL`, `BLOCKED`,
`NOT_RUN`, or justified `NOT_APPLICABLE`. Missing infrastructure is `BLOCKED`.
Use this same gate precedence: unresolved non-excepted failure → `FAIL`; otherwise
required external blocker → `BLOCKED`; otherwise missing, stale, invalid, not-run,
or unresolved-applicability evidence → `NOT_READY`; otherwise an active valid exception
→ `CONDITIONAL`; otherwise all required criteria evidenced → `PASS`.

A valid exception needs the authorized human, affected criterion, reason, residual risk,
scope, expiry/review condition, remediation owner, and currently verified compensating
controls and acceptance conditions. Missing or invalid exception evidence leaves the
failure non-excepted. Keep its raw `FAIL`; an exception cannot cover a separate blocker
or missing required evidence. An unknown scope or empty suite cannot establish `PASS`.
An explicit human acceptance of no compensating control is valid only where project
policy permits it; it cannot substitute for an unmet mandatory condition.

Do not treat a skipped check, missing environment, or proposed test as satisfied.
Keep local, integration, hosted, and production evidence distinct. Reuse valid
evidence unless a changed assumption, revision, or environment invalidates it.

Readiness and permission are separate: passing gates does not authorize deployment,
data deletion, external messages, or other actions outside the user's scope.
Existing user authorization remains valid within its stated scope; do not ask again
merely because the plan reaches an already-authorized step.

## Choose rollout timing when applicable

Consider operational support, dependency availability, traffic characteristics,
observation windows, and a tested recovery path where they affect this rollout.
For staged delivery, define the first cohort, expansion condition, observation
signal, and stop condition. Do not recommend a canary without a useful comparison
or reliable signals that can reveal the relevant failure.

If evidence is incomplete, state the next action that would resolve readiness and
what work can proceed meanwhile. Do not substitute a confident date for a missing
dependency, and do not create reminders, monitors, or automations unless requested.

## Output contract

Lead with the next eligible action or remaining prerequisite, qualified by environment
and evidence. When reporting a verification gate, retain its exact status and conditions.
A sequence described as “if X, then Y” is a plan, not a `CONDITIONAL` verification gate.
For a simple question, a short ordered list is enough.

For a larger decision, show step, prerequisite, completion evidence, current state,
and owner if known. Include material schedule assumptions, deployment authorization
status when relevant, and the exact next step. Label estimates and proposed checks.

Avoid imposing release gates on a small local edit that has no release decision.

## Reference anchors

- [DORA: continuous integration](https://dora.dev/capabilities/continuous-integration/): frequent integration and timely feedback.
- [Google SRE Workbook: canarying releases](https://sre.google/workbook/canarying-releases/): staged rollout evaluation and actionable signals.
