# Question boundaries review

Read-only review of README and all nine current `SKILL.md` entrypoints. Scope: the six question workflows and their interactions with verification, zero trust, and concurrency. Historical validation names were deliberately excluded from findings. No skill files were edited.

## Actionable findings

### QB-1 — P2: readiness handoff can discard an accepted exception or gate precedence

- **Locations:** `outputs/se-skills/se-when/SKILL.md:45-50`, `:75-80`; compare `outputs/se-skills/se-verify/SKILL.md:82-98`.
- **Issue:** `se-when` defines a second readiness vocabulary and asks for a ready/not-ready conclusion, but gives no rule for carrying forward the detailed gate decision or accepted exceptions already produced by `se-verify`. In particular, an exception-covered check remains raw `FAIL` in verification while its gate can be `CONDITIONAL`; the timing workflow only describes that same condition as Failed. It also omits the verification precedence for simultaneous failures, blockers, and missing evidence.
- **Example failure:** verification reports one valid human-excepted failure and overall CONDITIONAL. A subsequent “when can we roll this out?” independently turns that raw failure into an unconditional not-ready answer, or treats an accepted exception as sufficient while a separate required blocker remains. Both lose the earlier decision's conditions.
- **Smallest fix:** add a compact interoperability rule in `se-when`: preserve any existing scoped verification gate, raw check results, accepted exceptions, and prerequisites; readiness language must not weaken or silently replace them. If assessing evidence itself, use the same fail/blocker/missing-evidence/exception precedence, stated inline so the skill stays standalone. Distinguish a conditional rollout sequence from an evidence gate of CONDITIONAL.

### QB-2 — P2: explanation-only zero-trust requests prohibit the inspection needed to answer system-specific questions

- **Locations:** `outputs/se-skills/se-zero-trust/SKILL.md:11`; compare its own `:15-19`, and `outputs/se-skills/se-how/SKILL.md:25-30`, `outputs/se-skills/se-where/SKILL.md:53-55`.
- **Issue:** “without inspecting or changing live systems” conflates read-only inspection with mutation. The skill also promises to explain authorization boundaries and distinguish observed controls from assumptions. A user can explicitly ask for an explanation of their currently deployed authorization boundary, which requires authorized non-mutating inspection to answer accurately.
- **Example failure:** “Explain how our live agent gateway restricts tenant access; inspect its current policy read-only.” `se-how` supports grounding the explanation in current evidence, while selecting `se-zero-trust` forbids the expressly requested inspection and forces a generic answer or an avoidable blocker.
- **Smallest fix:** replace line 11 with an explanation-scope rule permitting relevant authorized read-only inspection while prohibiting mutations or active security probes merely to explain the mechanism. Keep generic explanations free of unnecessary live access.

### QB-3 — P2: material target ambiguity is resolved only before a mutation, although navigation normally never mutates

- **Locations:** `outputs/se-skills/se-where/SKILL.md:20-23`, `:67-75`, `:79`.
- **Issue:** when multiple plausible scopes materially change the answer, the workflow requires identifying ambiguity only “before making changes.” A read-only location answer can therefore proceed to the mandated best-supported-location conclusion without resolving or surfacing which repository/environment the user means.
- **Example failure:** two service checkouts both contain `authorizeRequest`, and the conversation has not established which deployment is being discussed. The agent picks the current checkout, returns a confident file/line location, and never reaches a change step at which its ambiguity instruction applies. The answer directs later work to the wrong system.
- **Smallest fix:** require resolving material target ambiguity before presenting a definitive location. Allow bounded discovery and clearly labeled candidate locations while clarification is pending; do not require clarification when context already identifies the target.

## Boundaries that already hold

- `se-what` distinguishes requirements from assumptions and proposed thresholds, preserves bug-fix intent over existing implementation, and does not itself authorize implementation.
- `se-why` explicitly distinguishes historical evidence from present-day explanation and inferred rationale; its output and scope rules do not justify an additional history-related finding.
- `se-who` separates review ownership from actual authority, uses current assignments before contribution history, and makes external assignment/contact separately authorized.
- `se-how` clearly separates explanation, planning, and already-authorized implementation. Its light acceptance checks overlap usefully with `se-verify`; a mandatory full verification process for every explanation would be counterproductive.
- `se-who` and `se-concurrent` both require an integration owner and combined validation; the latter owns the execution mechanics. This duplication supports standalone use and is not a defect.
- The README already says the nine skills are optional routing aids, not a mandatory pipeline. No sibling dependency or naming defect was established by this review.

## Validation scope

This is a static instruction and handoff review. Example failures are reasoned counterexamples, not executed host-selection or live-repository tests. No claims are made about actual automatic selection quality or production behavior.

## Recheck after parent changes

Directly reread current `se-when`, `se-zero-trust`, `se-where`, `se-concurrent`, and `se-verify` entrypoints; did not rely on the change notification.

- **QB-1 resolved:** `se-when:45-62` now preserves existing gates and exceptions and states the same standalone precedence. `:87-89` distinguishes conditional plans from CONDITIONAL verification gates.
- **QB-2 resolved:** `se-zero-trust:11-13` now allows relevant authorized read-only inspection for actual-system explanations and separately excludes mutations and active probes.
- **QB-3 resolved:** `se-where:20-25` now resolves or surfaces ambiguity before a definitive location and permits clearly labeled candidates during bounded discovery.
- `se-concurrent:32-33`, `:68-73`, and `:80-82` now address termination confirmation, residual writers, and a stable combined validation state. No additional question-workflow conflict identified there.

### Recheck consistency issue — gate precedence wording

`se-verify:27-28` now unconditionally says unresolved scope, criteria, or applicability makes the gate NOT_READY, while `:91-97` declares exact precedence in which FAIL and BLOCKED outrank missing evidence. A known required failure plus a different check with unresolved applicability could consequently be reported NOT_READY under the earlier instruction. `se-when:51-54` correctly places unresolved applicability at the missing-evidence tier.

Smallest fix: make the earlier `se-verify` sentence classify unresolved scope/criteria/applicability as missing required evidence **under the gate precedence below**, rather than assigning an unconditional overall gate. Retain its explicit protection against passing an empty or skipped suite. This is a static ambiguity finding; no runtime misclassification has been observed.
