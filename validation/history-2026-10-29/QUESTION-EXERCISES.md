# Forward skill-use exercise: A–F

These are responses to fictional inputs using the named skills. No repository implementation, external access, or live validation was performed. References below are to the skill files read for this exercise.

## A — engineering-what

**Response:** The outcome is a CSV download containing only accounts the requesting administrator is authorized to administer, with API keys omitted. Scope includes authorization at export time, selection of permitted account fields, CSV generation, and the download/error experience; implementation is outside this request.

Proposed acceptance criteria:
- An authenticated admin exporting an eligible account receives its approved fields in valid CSV; mixed account selections cannot expose accounts outside that admin's scope.
- A non-admin, unauthenticated caller, or admin requesting another administrator's accounts cannot obtain those records, including through direct export requests.
- API keys never appear in CSV headers or values, including nested or derived fields. An allowlist of exported fields is a proposed implementation approach pending the field contract.
- CSV handles delimiters, quotes, and newlines correctly; user-controlled formula-like values cannot execute as spreadsheet formulas when opened in the supported spreadsheet clients. The exact supported clients and safe serialization convention need agreement.
- Once a size limit is agreed, requests at and above its boundary have defined, observable outcomes; a failed export cannot silently masquerade as a complete download.

Proposed evidence: backend integration checks with two admins and disjoint account scopes, inspection of generated CSV using seeded API keys, CSV parsing cases, and a browser download/opening check in the intended supported environment. None has run here.

Unresolved: Which account fields may be exported, and what maximum export size and over-limit behavior should users receive? No numeric limit is assumed. Those decisions are needed before this becomes a fully ready implementation brief; the security requirements can be specified now.

**Operative passages:** `engineering-what/SKILL.md:13–19` separates requirements, assumptions, unknowns and scope; `:27–37` requires observable cases, sourced thresholds, evidence and environments; `:45–48` calls for targeted clarification of material behavior; `:61–64` separates acceptance plans from verified completion and forbids implementation merely because scope was defined.

## B — engineering-why

**Response:** The original rationale for choosing Redis is not established. The configuration confirms Redis is used for caching, and “add caching” establishes the change's stated purpose at a high level; neither explains why Redis was selected over another cache or storage approach.

A supported present-day explanation is that caching improves latency on the supplied load-test workload. That measured benefit supports retaining a caching mechanism under those conditions, but it does not isolate Redis-specific benefits or establish the original author's intent. Test workload, revision, environment and measurement details would be needed to assess how broadly the result applies.

Choosing Redis also introduces a service dependency and cache freshness/invalidation concerns; their actual cost in this system is unknown. To answer the historical question, the next useful evidence is the original design record or author discussion comparing requirements and alternatives. Without that, any Redis-specific rationale remains inference.

**Operative passages:** `engineering-why/SKILL.md:13–18` separates historical intent from current explanation; `:25–34` identifies historical sources, measurement limits, and the required unavailable-history caveat; `:41–47` distinguishes measured effects from assumptions and calls for relevant tradeoffs.

## C — engineering-who

**Response:** @identity-team is the evidenced review-routing candidate for `/auth`; deployment approval authority is unresolved. Confirm that CODEOWNERS entry on the PR's base branch and inspect effective review requirements before claiming their approval is mandatory or sufficient.

The CI service account is an execution identity, not evidence of who may authorize this release. The unknown person's issue comment does not establish that the bot is permitted to deploy.

To resolve this, obtain the maintained release policy or explicit authorization from the accountable release owner, including who approves this auth fix, who triggers deployment, and who owns monitoring and rollback. No individual approver or permitted deployment operator can be named from the supplied evidence alone. This response does not approve or initiate deployment.

**Operative passages:** `engineering-who/SKILL.md:8–9` separates ownership evidence from permission; `:15–18` distinguishes reviewer, decision authority and operational owner; `:26–37` requires supported ownership, current CODEOWNERS/review rules and separate action permission; `:66–71` limits external actions and pauses only dependent work.

## D — engineering-where

**Response:** Proposed placement: enforce tenant authorization at the shared service operations invoked by both API routes and background workers, before tenant data is read or changed. A proposed service-level authorization interface would take the authenticated caller or constrained worker identity, requested action, and target tenant/resource, then deny access unless the policy permits that operation. This is a design proposal, not an observed existing interface or filename.

API entry points should establish a trustworthy caller context; workers need an explicitly scoped identity rather than implicit unrestricted access. Hiding browser buttons is a usability measure and cannot protect direct calls. A stored `tenant_id` provides a scoping attribute, but does not itself enforce access. Database constraints or row-level policies may provide another enforcement layer if supported by the actual access model.

Next evidence: trace one API call and one worker call through the service to database access; inspect how caller identity and tenant context are derived, whether every data path passes the proposed boundary, and how queries scope tenant data. Then inspect the actual tenancy policy and test allowed access, cross-tenant denial and missing identity for both callers. Current service-layer enforcement is unverified; no filenames can be established from this scenario.

**Operative passages:** `engineering-where/SKILL.md:8–9` separates existing responsibility from recommendations; `:32–35` requires caller/wiring evidence and acknowledges lookup limits; `:49–51` bases placement on dependency direction, ownership and trust boundaries; `:67–73` calls for concrete references while explicitly labeling proposals and evidence limits.

## E — engineering-how

**Response:** Introduce a durable idempotency record before contacting the payment provider. The acceptance condition is that retries of one logical payment cannot produce multiple charges and receive the same eventual outcome; a reused key with a different payment request is rejected. Provider support is a design dependency: a local database record alone cannot guarantee this across a crash after the provider charges but before the receipt is saved.

Proposed sequence:
1. Define a stable retry key scoped to the authenticated customer and logical payment; fingerprint the normalized payment details. Atomically create a pending record with a unique scoped-key constraint before making the provider call. Concurrent requests either retrieve the stored outcome or receive a defined pending response; they do not independently charge.
2. Confirm provider idempotency semantics, key scope/retention, and reconciliation or lookup support. If supported, use the same provider key for the same payment on every retry. Do not generate a fresh key after a timeout.
3. Store the provider reference, receipt and completed local outcome together transactionally. Replay the completed result on subsequent matching requests, with authorization checked on every request.
4. Treat timeouts and crashes as an unknown outcome until reconciled. A worker that resumes pending work must not blindly charge again. If the provider has neither reliable idempotency nor a safe way to establish the original outcome, hold uncertain payments for reconciliation instead of promising safe automatic retry.
5. Agree retention and retry windows against provider guarantees, and define recovery for abandoned pending requests before enabling retries.

Proposed validation covers simultaneous same-key calls, changed-payload reuse, cross-customer access, timeout after a charge, crash before receipt persistence, and reconciliation after restart. Provider integration evidence is required for the charge guarantee; local mocks cannot establish it. No code was changed and none of these checks ran.

**Operative passages:** `engineering-how/SKILL.md:13–18` keeps explanatory work read-only and preserves scope; `:22–30` requires design-relevant uncertainty and failure tracing; `:43–50` requires acceptance, persistent-state/contracts, tradeoffs and verifiable increments; `:58–64` requires relevant validation and labels advice-only checks as proposed.

## F — engineering-when

**Response:** Not ready to remove the old column in the deployed environment: 20% of instances still read it, and the completed backfill has no validation evidence. Removal should be gated by observed compatibility and data correctness rather than a date.

1. Validate the backfill against the agreed mapping and invariants, including missing, incorrect and concurrently changed records. Current state: **unverified**. A report that the job finished does not satisfy correctness.
2. Complete migration of all dependent readers and writers, including the remaining instances and any workers or scheduled jobs, then verify they no longer depend on the old column. Current state: **failed** for the required absence of old readers. Plan this rollout now; execution needs deployment authorization.
3. Verify the new application and data together in the target environment and establish an observation window using relevant traffic/job cycles. Confirm the supported rollback version also works without the old column, or agree a tested forward-recovery plan. Current state: **unverified**; no arbitrary duration is assumed.
4. Only after those gates pass, obtain explicit authorization for the destructive schema change and schedule it with an operational owner and recovery path. Preserve the column until then. Removing it is the point after which rollback to an old-column-dependent application is unsafe without restoration.

Immediate next work is to specify and obtain backfill validation evidence and inventory remaining consumers. No deployment or data modification is authorized or performed by this plan.

**Operative passages:** `engineering-when/SKILL.md:8–9` makes timing prerequisite-driven; `:23–37` requires dependency completion evidence, integration checks and irreversible-step recovery; `:45–59` defines satisfied/failed/unverified/blocked and separates readiness from action permission; `:69–80` requires the next readiness action and explicit limits instead of an invented date.

## Contradictions and unclear instructions encountered

- No blocking contradictions within the six skills were encountered in these scenarios.
- `engineering-where` asks for a “concrete proposed module or interface” and concrete file/line references. The exercise explicitly forbids inventing filenames and supplies no source files. I satisfied the former with a clearly proposed logical interface and stated the source-location evidence gap. This works, but the skill could explicitly say to omit unavailable file references rather than risk pressuring an agent to invent them.
- `engineering-when` distinguishes failed and unverified gates but does not prescribe a universal aggregate gate status. That was sufficient here: known active consumers justify “not ready,” while backfill correctness remains unverified rather than failed.
