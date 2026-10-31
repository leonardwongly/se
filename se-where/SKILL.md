---
name: se-where
description: Locate the implementation, architectural layer, runtime environment, or verification evidence responsible for a specific software or AI behavior. Use for engineering navigation and placement decisions grounded in the current scope, not general file search or geography.
---

# SE Where

Find the location that answers the engineering question and explain why it is the
right location. Distinguish existing responsibility from recommended placement.

## Ground the task in the project

For project-specific work, reuse a current verified project brief and refresh changed facts.
For a general conceptual question, use labeled examples without unrelated project access.
Confirm the target root, branch/revision and uncommitted work (or non-Git source identity),
applicable local instructions, and the specific component/environment before conclusions.
Read relevant maintained contracts, active callers/configuration, and actual test/CI setup;
cite exact source locations and separate current facts, proposals, and stale historical context.
Resolve material conflicts or missing scope before dependent decisions; continue bounded
independent work. Do not infer policy solely from existing code or a generated working directory.
If the authorized task includes code/configuration changes, also complete the mandatory
zero-trust review and project-derived verification for the final changed state. Scale depth
to risk and report missing evidence; a rationale, location, or ownership map alone is not completion.

## Resolve the target

Determine whether the user needs:

- **Implementation:** the entry point, definition, caller, state owner, or test.
- **Architecture:** the layer or service that should own a responsibility.
- **Runtime:** the process, environment, region, deployment, or storage boundary.
- **Evidence:** the artifact, log, run, or observable state that supports a claim.

Use the repository, branch, service, and environment established in the conversation.
If multiple plausible scopes would materially change the answer, resolve or explicitly
surface that ambiguity before presenting a definitive location. Bounded discovery and
clearly labeled candidate locations can proceed while clarification is pending.
A generated working directory is not evidence
that it contains the user's target project.

## Search proportionately

1. Start with the strongest anchor available: a symbol, error, route, configuration
   key, behavior, or known artifact. Choose exact lookup for exact anchors and
   semantic discovery when the location or wording is unknown.
2. Search the relevant current scope using available tools and applicable workspace
   instructions. Do not require a particular search product or build a persistent
   index merely to answer the question.
3. Read enough surrounding evidence to establish responsibility. Follow a caller,
   dependency, registration, or configuration reference when a matching definition
   alone does not establish that the code is active.
4. Stop when evidence answers the question. If no relevant match exists, state the
   searched scope and limits; absence from an index is not proof of nonexistence.

Do not search unrelated private sources or external systems just because they are
available. Use authoritative documentation when the question concerns an external
platform rather than the current workspace.

## Establish ownership and boundaries

For implementation, distinguish the public entry point, underlying implementation,
and relevant tests. Separate generated files from their maintained source. Explain
which location should be changed only if placement or implementation was requested.
For a new/modified-code task, map the affected trust boundary and the project's actual
verification entrypoints alongside the code location. Follow runtime wiring and callers
before treating a similarly named file, archived document, or unused test as active evidence.

For architectural placement, use existing dependency direction, data ownership,
trust boundaries, and lifecycle. Name a concrete proposed module or interface and
why it fits. Avoid inventing a new layer where an existing one owns the behavior.

For runtime location, distinguish configured destination from observed execution.
A manifest does not prove a deployment is active; a local process does not prove
hosted behavior. State the observation time when freshness affects the answer.

For evidence location, connect the artifact to the claim, revision, environment,
and relevant run when available. Distinguish missing, inaccessible, stale, and
contradictory evidence instead of treating them as equivalent.

For AI systems, trace responsibility across prompt construction, retrieval,
inference, tool execution, persistence, and evaluation only as far as the question
requires. The prompt file may not be the component that enforces a safety boundary.

## Output contract

Lead with the best-supported location, then give a short explanation of its role.
For multiple locations, use a compact table of location, responsibility, and
evidence. Provide concrete file and line references or accessible artifact links.
When source locations are unavailable, state that limit and use a clearly proposed
logical interface if useful; never invent a path or line number to fill the format.

Label proposed placements as proposals. Include confidence or an evidence limit
when the answer depends on inferred wiring, incomplete access, or stale artifacts.
If blocked, name the exact missing scope or access needed for the next lookup.

## Boundaries

- Navigation is read-only unless the user also authorizes a change.
- Finding a likely location does not prove a defect, fix, deployment, or release.
- Do not turn a location question into an unsolicited repository-wide audit.
- Do not expose credentials or sensitive log contents to demonstrate a location.

## Reference anchors

- [Google engineering review: navigate a change](https://google.github.io/eng-practices/review/reviewer/navigate.html): understand scope and context before examining details.
- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final): ownership and protection considerations for security-relevant software artifacts.
