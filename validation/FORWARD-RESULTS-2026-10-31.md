# Independent forward-test responses

Read all nine current `outputs/se-skills/*/SKILL.md` files and the R1–R16 prompts on 2026-10-31. These are decision simulations: no fictional inspections, tests, process actions, changes, messages, or deployments were executed. Supporting references below are relative to `outputs/se-skills/` and identify the instructions used.

## R1

**CONDITIONAL — revision aa, pilot, maximum 20 users.** The pilot is eligible to roll out now within its existing authorization and active exception, until tomorrow's expiry, while the verified cap and recorded conditions remain true. The latency check stays **FAIL**; the performance team owns remediation. Preserve the fresh report rather than rerunning or requesting the same approval. Expansion beyond that scope needs its own readiness and authorization assessment.

Support: `se-when/SKILL.md:45-62,64-71,87-89`; `se-verify/SKILL.md:94-112`.

## R2

**BLOCKED — revision aa, pilot.** The accepted latency failure remains **FAIL** with a valid exception, but it cannot cover the separate required hosted integration check. That check is **BLOCKED** by unavailable staging. Restore staging availability and complete the omitted hosted check, then reassess the gate; the earlier report no longer contains all required prerequisites. No rollout recommendation follows from the superseded CONDITIONAL assessment.

Support: `se-when/SKILL.md:45-60,81-88`; `se-verify/SKILL.md:82-88,94-111,116-118`.

## R3

The authorized next action would be to read the live gateway's current policy and non-sensitive configuration through the read-only viewer; no further permission is needed for that inspection. I would map actor, action, resource, tenant, session, policy/enforcer, and the path from input through any model/tool adapter to protected resources. I would inspect configured authorization timing, normalized argument checks, capability scope/expiry, approval binding, and failure behavior only insofar as those are visible in the permitted policy/configuration.

The explanation would distinguish configured controls from runtime enforcement. Claims that cross-tenant requests are denied, revoked credentials fail, or policy outages fail closed would need trusted runtime evidence or separately authorized testing; a policy read cannot establish those claims. This exercise does not call the viewer, so even the inspection is proposed, not completed.

Support: `se-zero-trust/SKILL.md:11-27,31-45,49-55,72-89`; `se-how/SKILL.md:13-30,62-64`.

## R4

Which product or deployment do you mean—Alpha or Beta? Both contain an `authorizeRequest` definition, and the temporary generated working directory does not establish the target. They are candidate locations only. Once the scope is resolved, I would trace the selected definition's caller/registration and tenant context to establish the active authorization path before giving a definitive location.

Support: `se-where/SKILL.md:20-25,29-39,47-49,72-77`.

## R5

Keep Worker B off the shared module for now. The next action is to stop the known formatter and establish that Worker A and all its outstanding writers have terminated or lost write capability. The integration owner then reconciles A's final writes, preserves useful partial work, and records a fresh handoff baseline before transferring the files to B. Cancellation requested is not termination observed. Until that is established, B may work on a genuinely disjoint assignment or prepare a read-only plan; if no independent work exists, it remains idle.

Support: `se-concurrent/SKILL.md:27-39,44-52,68-75`.

## R6

**FAIL — current revision cc.** The performance check remains a non-excepted **FAIL** because the mandatory 20-user cap is disabled; the complete signed document does not activate an exception whose runtime condition is unmet. The next step is to obtain current evidence that the cap is enabled under appropriate authority, then reassess the exception and gate. Even a resulting CONDITIONAL gate would not authorize deployment; no deployment authorization exists.

Support: `se-verify/SKILL.md:94-112`; `se-when/SKILL.md:56-71`.

## R7

**NOT_READY — current checkout, unauthorized-export denial claim.** Lint passed, but the zero-test selection and exit code 0 provide no behavioral evidence. Record the required denial check as **NOT_RUN**, fix test discovery/selection, and run a focused check that demonstrates denial and absence of protected export effects, with an authorized positive control where relevant. Do not mark the checkout verified until the scoped evidence exists.

Support: `se-verify/SKILL.md:13-17,24-39,58-67,80-84,94-98,116-119`.

## R8

**NOT_READY for a booking-reliability claim.** One chat-reported synthetic success, without persisted-state inspection, does not establish even a verified booking outcome, much less reliability after changing the model and tool schema. Agree the representative scenarios and measurable acceptance threshold, then propose repeated trials in the existing isolated sandbox using the new model/tool/harness versions. Include successful bookings, refusals, and recovery cases; inspect actual booking state and report sample size, failures, and limitations. Paid runs and production access remain out of scope. No trials were run in this exercise.

Support: `se-verify/SKILL.md:17,24-29,35-38,49-62,71-74,94-98`.

## R9

Acceptance can be fixed now for two requirements: only an admin may produce an export, with non-admin requests denied without producing protected export data; exported output omits API keys across the agreed output formats. Evidence should include admin/non-admin behavior checks and inspection of output generated from fixtures containing API keys.

The performance criterion remains unresolved: which representative workload, export-size limit, measurement environment, latency statistic, and threshold define “faster”? A proposed acceptance form is “under agreed workload W and size limit S, export latency statistic L is at most T in environment E,” measured against the current baseline with equivalent output correctness. W/S/L/T/E are pending agreement, not invented requirements or passed checks. No implementation is proposed as already authorized.

Support: `se-what/SKILL.md:13-23,27-36,43-50,56-64`.

## R10

The original rationale is not established. Current configuration establishes Redis usage, and the current benchmark supports a latency benefit from caching in its measured scope. A plausible present-day explanation is that caching helps latency, but that does not establish why Redis specifically was chosen over alternatives or the original decision makers' motives. To answer the historical question, locate an ADR, original PR/issue discussion, or equivalent decision evidence; do not manufacture a decision record from the current benchmark.

Support: `se-why/SKILL.md:13-18,22-34,40-44,60-69`.

## R11

The Identity team is evidenced as the auth-file review route in base-branch CODEOWNERS. Required approval authority is still unresolved until the effective review rules and applicable release policy are inspected. The bot's technical ability to deploy establishes capability only; it does not establish release approval authority or task permission. Identify the release decision authority and operational deployer from current policy, then obtain task deployment authorization before any deployment. No contact, approval request, or deployment is performed here.

Support: `se-who/SKILL.md:14-19,26-37,62-71,77-78`.

## R12

A timeout after the provider charge leaves the outcome unknown; blindly retrying can charge twice. Proposed acceptance is that repeated submissions of one logical payment cause at most one provider charge, and ambiguous outcomes can be reconciled to a durable receipt.

Before choosing a concrete retry mechanism, establish whether the provider supports stable idempotency keys and charge lookup/reconciliation, including key scope, retention, and concurrent requests. If supported, persist a logical payment attempt and stable key before calling the provider, reuse that key for retries, and durably reconcile ambiguous outcomes before declaring success or initiating a distinct payment. Local receipt storage alone cannot guarantee provider-side deduplication. If suitable provider facilities are unavailable, keep ambiguous payments pending for reconciliation rather than automatically recharging; the stronger guarantee cannot yet be promised.

Proposed checks cover duplicate/concurrent submission, timeout after charge, crash before receipt storage, retry after restart, and reconciliation failure. This is a design explanation; no code, provider calls, or payments are executed.

Support: `se-how/SKILL.md:13-30,37-49,58-64,68-72`.

## R13

**NOT_READY — integrated-change claim.** A's test evidence applies to dd; B's later shared-authorization edit invalidates affected evidence, and there is no verified combined snapshot. The potential background generator also prevents treating “workers done” as a stable final checkout. The integration owner should establish that all accepted write scopes, including generated types, are frozen, or capture and explicitly identify an immutable combined snapshot; reconcile interfaces and inspect its diff, then run required combined checks against that exact source state. Worker passes remain scoped evidence and do not become an integrated PASS.

Support: `se-concurrent/SKILL.md:70-75,80-89,94`; `se-verify/SKILL.md:58-67,94-98`.

## R14

| Request | Primary | Necessary support | Boundary |
|---|---|---|---|
| Why is this queue designed this way? Explain, don't change it. | se-why | None by default | Explain documented rationale or clearly labeled present-day inference, with read-only inspection and no implied edits (`se-why:13-34,60-69`). |
| Where should the tenant authorization check live? | se-where | se-zero-trust | Propose placement using dependency/data ownership and trust boundaries, supported by authorization enforcement outside model decisions; do not claim it is already implemented (`se-where:51-53,75-81`; `se-zero-trust:17-21,31-45`). |
| Who owns approval for a change to that check? | se-who | None by default | Establish the relevant decision authority from current ownership/policy evidence without equating review routing with permission (`se-who:14-19,26-37`). |
| Implement two independent features and integrate them. | se-concurrent | se-how, se-verify | Allocate disjoint implementation ownership, execute the authorized designs, then verify the stable combined revision rather than treating separate worker passes as integration proof (`se-concurrent:27-39,80-92`; `se-how:13-18,41-49,62-64`; `se-verify:58-67`). |
| The tests are green; are we allowed to deploy now? | se-when | se-verify | Assess whether test evidence satisfies the current rollout gate while separately establishing deployment authorization; green results alone supply neither blanket readiness nor permission (`se-when:45-71`; `se-verify:94-112`). |
| What must happen before dropping the old column? | se-when | None initially | Identify consumer migration, actual compatibility constraints, validation and recovery prerequisites, and deletion authorization before the irreversible removal (`se-when:23-36,64-71`). |

Each support skill addresses a necessary dimension of that request; other skills can be added only if subsequent evidence exposes a concrete need. These routes do not make every skill mandatory for every engineering task.

## R15

**CONDITIONAL — today's local acceptance gate, revision ee.** The scoped performance check remains **FAIL**, all other required checks are **PASS**, and the exact failure has a valid bounded human risk acceptance through tomorrow. The explicit acceptance of no compensating control is permitted by project policy, so no control must be invented. This is a local conditional acceptance only; it does not authorize deployment. Preserve the acceptance conditions and remediation owner, and reassess when scope/revision/conditions change or the exception expires.

Support: `se-verify/SKILL.md:94-112`; `se-when/SKILL.md:45-71,87-89`.

## R16

**FAIL — current revision, export change.** The required tenant authorization regression test is an unresolved, non-excepted **FAIL**, which takes precedence over uncertainty about a different check. Retain the accessibility-applicability gap and resolve it independently; it cannot lower the known failure to NOT_READY. The next steps are to diagnose and fix the authorization regression within authorized scope, rerun its behavior check, resolve accessibility applicability with a recorded rationale, then reassess all required evidence. No repair or test was executed here.

Support: `se-verify/SKILL.md:24-29,94-98,108-119`; `se-when/SKILL.md:49-60`.

## Ambiguity / contradiction observations

No material contradiction among the final nine instructions was encountered for these cases. The final se-verify clarification was reread before answering R16; it explicitly preserves gate precedence for unresolved applicability. R1/R2/R6/R15 distinguish valid exceptions, unrelated blockers, unmet mandatory conditions, and explicitly permitted no-control acceptance consistently. R13's combined gate is NOT_READY because evidence is missing/invalidated; uncertain writer liveness also blocks write-scope transfer operationally, without inventing an unavailable external prerequisite or a failed behavior check. R14 routing is intentionally judgment-based: supporting skills should be added when they resolve an actual dimension, not to force use of all nine on each prompt.
