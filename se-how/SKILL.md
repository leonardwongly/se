---
name: se-how
description: Explain how a software or AI system works, or develop an evidence-backed implementation approach for a specific engineering change. Use for mechanism tracing and implementation planning; a how-to question alone does not authorize code changes.
---

# SE How

Turn a concrete engineering question into a traceable explanation or an executable
implementation approach. Match the depth to the decision the user needs to make.

## Ground the task in the project

For project-specific work, reuse a current verified project brief and refresh changed facts.
For a general conceptual question, use labeled examples without unrelated project access.
Confirm the target root, branch/revision and uncommitted work (or non-Git source identity),
applicable local instructions, and the specific component/environment before conclusions.
Read relevant maintained contracts, active callers/configuration, and actual test/CI setup;
cite exact source locations and separate current facts, proposals, and stale historical context.
Resolve material conflicts or missing scope before dependent decisions; continue bounded
independent work. Do not infer policy solely from existing code or a generated working directory.

## Choose the mode

- For “how does this work?”, explain the observed mechanism and its boundaries.
- For “how should we implement this?”, propose a concrete approach and validation.
- For “implement this” or equivalent authorized work, use the approach to execute
  the requested change; an explanation request by itself remains read-only.
- Preserve any existing authorization in the conversation. Do not ask again for
  permission already granted or expand it to deployment or external messages.

## Trace the relevant behavior

1. Identify the intended result, entry point, and important constraints in the grounded
   project scope. Ask only about uncertainty that changes the design,
   contract, data handling, authorization, or externally visible behavior.
2. Inspect the smallest useful set of implementation, configuration, callers,
   tests, or operational evidence. Prefer the current system over a generic pattern.
3. Trace inputs through transformations, state changes, dependencies, and outputs.
   Identify where failures are surfaced, retried, or suppressed when relevant.
4. Separate directly observed behavior from inferred intent and proposed changes.
   A test proves only the behavior and environment it actually exercises.

For a greenfield request, state the assumptions that substitute for missing
implementation evidence. Do not invent repository symbols or observed behavior.

## Explain or design the mechanism

For an existing system, give the shortest causal chain that answers the question.
Use a concrete input and output or a small diagram when it reduces ambiguity.
Include an important failure path if omitting it would misrepresent the mechanism.

For a proposed change:

- Define the observable acceptance condition before choosing implementation steps.
- Reuse established interfaces and repository patterns where they fit the need.
- Identify affected contracts, persistent state, and compatibility implications.
- Compare alternatives only when their tradeoffs materially affect the choice.
- Recommend the simplest approach that satisfies the constraints; name the cost
  or limitation of the chosen approach and a mitigation when needed.
- Order the work into verifiable increments, with integration and cleanup included.

For AI features, distinguish deterministic orchestration from model decisions.
Where relevant, specify context sources, tool authority, output validation,
evaluation examples, and what happens when the model is wrong or unavailable.
Do not treat prompt wording or a single successful response as a correctness proof.

## Validate the approach

Map the acceptance condition to a relevant check: a traced example, behavioral
test, integration run, evaluation set, or observable user journey. State what
would falsify the explanation or demonstrate that the implementation is incomplete.

Every new or modified code change requires a zero-trust review and verification,
including generated code, tests, dependencies, migrations, CI/runtime configuration,
and behavior-affecting prompts or tool schemas. These responsibilities apply whether
or not companion skills are installed; perform the baseline directly when needed.

1. Inspect the actual changed surfaces and relevant callers. Identify untrusted inputs,
   authoritative identity, resources/actions, enforcement points, sensitive data and effects.
   If no trust boundary changes, support that conclusion from the diff and call path.
2. Apply the project's contracts and controls at the actual enforcement boundary.
   New, existing, copied, or agent-generated code receives the same scrutiny.
3. Execute applicable checks discovered from this project's manifests, tests and CI.
   Cover changed behavior and, for affected boundaries, authorized and denied cases with
   no protected side effects on denial. Do not substitute lint or a worker's claim for behavior.
4. Inspect the final diff and stable source state, retain commands/results and limitations,
   and state whether security and functional acceptance are evidenced. Missing required
   checks prevent an unconditional completion claim; use the project/verification gate.

Scale depth to risk: a literal UI-text edit may need a grounded boundary review and
render/static check; changed authorization needs behavior-level regression evidence.
Do not add meaningless tests for ceremony or exempt the baseline because the diff is small.
When only advice was requested, label checks as proposed rather than executed.

## Output contract

Lead with the mechanism or recommended approach. Then provide, as needed:

- A short flow or ordered implementation steps with concrete affected locations.
- Evidence links or file references, and explicit assumptions where evidence ends.
- Acceptance checks, their executed or proposed status, and material limitations.

Use a brief answer for a narrow question. The mandatory change baseline does not
require a full architecture audit, benchmark suite, or release process for every edit.

## Reference anchors

Consult these when the corresponding decision needs deeper support; they are not
additional mandatory gates or evidence that a particular implementation is correct.

- [Google engineering review: what to look for](https://google.github.io/eng-practices/review/reviewer/looking-for.html): design, functionality, complexity, and tests.
- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final): secure development practices when the change affects security controls.
