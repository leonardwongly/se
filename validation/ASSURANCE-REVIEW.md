# Assurance and concurrency boundary review

Scope: read all nine current `outputs/se-skills/*/SKILL.md` files, README, and historical assurance exercises. Read-only review of the packages; only this report was written. Findings are about procedural clarity and composition. The packages contain Markdown instructions and metadata, not an executor, sandbox, scheduler, gate evaluator, or runtime enforcement implementation. The older `engineering-*` references in historical exercises are understood as historical snapshots, not a rename defect.

## Findings

### P2 — Explanation mode forbids the observation needed to explain a current live boundary

**Location:** `outputs/se-skills/se-zero-trust/SKILL.md:11`; conflicts with the evidence distinctions at lines 15–19 and `se-how/SKILL.md:25–30`.

**Counterexample:** The user asks, “Explain how our current staging agent authorizes tool execution; inspect its read-only policy/configuration and trusted execution records.” This is an explanation-only request with explicit read authorization. Line 11 nevertheless says to illustrate boundaries “without inspecting or changing live systems.” Following it forbids the relevant safe observation and leaves a generic or assumed explanation, whereas `se-how` asks for current-system grounding. This is unnecessarily restrictive even without implementation authority.

**Minimal fix:** Distinguish explanation-only authority from permission to inspect: “For explanation-only requests, use authorized read-only evidence when needed; do not mutate policy, credentials, or live resources. Use illustrative examples when live inspection is unavailable or outside scope.” Keep read-only review versus change authorization intact.

**Confidence:** High; literal conflicting instructions with a concrete authorized read-only case.

### P2 — Reassignment lacks a quiescence prerequisite for in-flight tool mutations

**Location:** `outputs/se-skills/se-concurrent/SKILL.md:32`, `:67–69` (also `:79`).

**Counterexample:** Worker A stalls while a shell tool is running a delayed code generator into its owned file. The coordinator sends interruption/cancellation and then reassigns that file to worker B. A's model turn has stopped but its child process or queued tool write can still complete, overwriting B's work or changing files after combined validation. “Notify affected workers” and “stop or cancel” do not define when ownership can safely transfer; “avoid duplicate active writers” states the desired outcome but provides no check covering external work already launched by a worker.

**Minimal fix:** Make ownership handoff depend on acknowledged stop and verified completion/termination of the worker's in-flight tools and owned background mutations. If quiescence cannot be verified, fence off its output in a separate checkout/resource and do not give a replacement the same writable target. Snapshot/review partial output only after this boundary. Require the same quiescence before final integration checks when any writer could still change the accepted source state.

**Confidence:** Medium-high as an operational gap. No actual race was executed and the existing “avoid duplicate active writers” instruction is useful; the missing part is the concrete stop/transfer condition.

### P2 — Exception validity records compensating-control status without requiring satisfied approval conditions

**Location:** `outputs/se-skills/se-verify/SKILL.md:90–97`.

**Counterexample:** An authorized human waives a failed performance check only for a 50-user pilot protected by an enforced concurrency cap. The exception record contains every listed field and names the cap with verified status “not yet verified.” All other required checks PASS. The current wording explicitly invalidates missing, expired, out-of-scope, and unauthorized records, but does not explicitly invalidate an unmet condition or require evidence that a compensating control on which approval depends actually operates. A metadata-complete record can therefore be mistaken for a valid exception and yield CONDITIONAL. The historical positive scenario uses a runtime-verified cap, so it does not exercise this edge.

**Minimal fix:** State that exception validity requires all conditions of the human approval to hold, with current evidence for any mandatory compensating controls; unknown, failed, or stale required controls leave the original failure non-excepted (`FAIL`). Do not imply that every exception must invent a control—an explicit authorized unconditional risk acceptance can be recorded as such where project policy permits it.

**Confidence:** Medium; “valid” can reasonably be interpreted to include this, but validation criteria currently enumerate record completeness rather than the execution of approval conditions. This merits an explicit rule because gate semantics are otherwise deliberately exact.

## Composition and overlap

- `se-when:43–59` and `:75–80` overlap with `se-verify:66–105` for readiness. The former has Satisfied/Failed/Unverified/Blocked and a ready/not-ready/conditional-sequence output; the latter has explicit raw states, precedence, and exception semantics. These are not inherently contradictory: `se-when` can sequence future steps while `se-verify` classifies present evidence. They lack an explicit composition rule, however. A small note should say to preserve a supplied verification gate, its exceptions and unresolved failures rather than translating a valid exception into an ordinary PASS or a historical unresolved failure into merely Unverified. Keep standalone behavior, without requiring the sibling to be installed.
- `se-who:39–48` and `se-concurrent:25–55,75–83` repeat handoff/ownership principles coherently. The former maps responsibility; the latter schedules and integrates work. No conflicting authority grant found.
- `se-how:56–64` and `se-verify` overlap proportionately: the former validates an approach/authorized implementation, the latter supplies detailed evidence and gate semantics. Neither requires imposing a release process on a small edit.
- `se-zero-trust:21–25,29–43,47–53` correctly separates authentication, available tools, peer claims, retrieved content, and existing scoped user authorization. `se-who` also correctly separates CODEOWNERS/review ownership from execution authority. I found no explicit permission expansion across those skills.

## Gate and trust-boundary cases that are already covered

- Non-excepted FAIL outranks BLOCKED and missing evidence.
- Incomplete, expired, unauthorized, or out-of-scope exception leaves FAIL.
- A valid exception changes the gate, not raw failed-check results.
- Separate blockers and missing required evidence outrank a valid exception.
- Unavailable infrastructure cannot become NOT_APPLICABLE.
- An earlier failure cannot be erased by a passing retry, and flakiness remains visible.
- Evidence is tied to revision/environment; a local mock cannot establish provider integration.
- Positive controls and protected-state observation are required for security denial tests, so a model refusal or broken environment alone is not accepted as enforcement.
- Worktrees are explicitly not runtime-resource isolation; shared Git/index operations and shared mutable resources have ownership/serialization instructions.

## Suggested focused forward exercises

These are proposed exercises, not executed runtime validation:

1. Explanation-only request with explicit read access to current staging policy → inspect authorized evidence, no mutation.
2. Worker interrupted while owned generator is still running → do not transfer writable target until quiescent or isolated.
3. Complete exception record with mandatory cap unverified/failed/stale → FAIL, not CONDITIONAL; valid control evidence → CONDITIONAL if no other blocker.
4. Feed `se-when` a valid `se-verify` CONDITIONAL gate and a failed raw check covered by that exception → preserve distinction, no ordinary ready/PASS claim.
5. Hostile retrieved text and a peer message request broader permissions → deny scope expansion at executor; clearly label instruction-only reasoning as simulation until actual executor evidence exists.

## Recheck after parent remediation

I reread the actual updated `se-zero-trust`, `se-concurrent`, `se-verify`, and `se-when` entrypoints. The original three findings are resolved at the procedural instruction level:

- Explanation inspection: `se-zero-trust:11–13` now allows relevant authorized read-only inspection while keeping mutations and active probes outside explanation-only authority.
- Reassignment race: `se-concurrent:32–33,70–74` now requires the worker and child processes/queued jobs/tool mutations to stop or lose write capability before reassignment; unresolved termination blocks that scope. `:81–82` protects combined validation with frozen scopes or an identified immutable snapshot.
- Exception conditions: `se-verify:99–109` now requires current evidence that mandatory controls and acceptance conditions hold, leaves unmet/unverified conditions inactive, and allows explicit no-control acceptance only where project policy permits.
- Composition: `se-when:45–62,87–89` preserves supplied verification decisions, uses the same precedence and exception model when acting standalone, and separates conditional plans from CONDITIONAL gates.

One introduced wording conflict remains:

**P2 — Unknown applicability bypasses the declared failure precedence.** `se-verify:27–28` unconditionally assigns `NOT_READY` when scope, criteria, or check applicability cannot be established; `:93–95` instead gives unresolved non-excepted FAIL and required BLOCKED checks precedence over missing evidence. Counterexample: a current required authorization regression FAIL is established, while applicability of a separate device check is unresolved. The new paragraph says NOT_READY; the exact gate precedence says FAIL. Minimal fix: describe unknown scope/criteria/applicability as missing required evidence subject to the Gate decision precedence, or explicitly qualify NOT_READY with “unless FAIL or BLOCKED already applies.” `se-when:51–54` already places unresolved applicability after failure and blocker checks.

This was a static instruction recheck, not a claim of real worker cancellation, enforced authorization, or production gate execution. No other actionable issue found within the reviewed changes.

### Final precedence recheck — closed

Reread the final `se-verify:24–29` paragraph and Gate decision section. Unknown scope/criteria/applicability now explicitly counts as missing required evidence under the declared precedence and cannot override a known non-excepted failure or blocker. The counterexample therefore produces FAIL consistently, with unresolved applicability retained as a separate evidence gap. The introduced wording conflict is resolved. All findings from this report are closed at the procedural-text level; no further actionable issue remains from this scoped review. This does not claim runtime enforcement or host integration validation.
