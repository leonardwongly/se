---
name: se-what
description: Define scope, requirements, and observable acceptance criteria for AI or software engineering changes, especially ambiguous feature requests, bug fixes, and implementation briefs.
---

# SE What

Turn a software change request into a bounded, testable agreement about the outcome.
Use this for engineering scope and acceptance, not unrelated questions containing “what.”

## Ground the task in the project

For project-specific work, reuse a current verified project brief and refresh changed facts.
For a general conceptual question, use labeled examples without unrelated project access.
Confirm the target root, branch/revision and uncommitted work (or non-Git source identity),
applicable local instructions, and the specific component/environment before conclusions.
Read relevant maintained contracts, active callers/configuration, and actual test/CI setup;
cite exact source locations and separate current facts, proposals, and stale historical context.
Resolve material conflicts or missing scope before dependent decisions; continue bounded
independent work. Do not infer policy solely from existing code or a generated working directory.

## Establish the requested outcome

1. Extract the affected user, triggering action, current behavior, and desired result.
2. Separate explicit requirements from assumptions, suggestions, and unknowns.
3. Inspect only the product documentation, implementation, or issue evidence needed
   to establish the current contract. Record conflicts instead of silently choosing.
4. Identify the smallest complete change that delivers the outcome, including any
   necessary callers, data handling, documentation, and operational integration.
5. State meaningful non-goals to prevent accidental expansion; avoid a catalog of
   irrelevant exclusions.

Do not equate existing implementation with intended behavior when the task is a bug fix.
Do not convert a proposed solution into a mandatory implementation without evidence.

## Write acceptance criteria

- Express criteria as observable behavior under a concrete condition.
- Include successful operation and the failure or boundary cases that could invalidate
  this change: for example denied access, malformed input, or interrupted persistence.
- Include compatibility, performance, accessibility, or security constraints when
  required by the request, existing contract, or the changed behavior's actual risk.
- Give thresholds a source. Mark unagreed values as proposed rather than inventing a
  service level, latency budget, or reliability promise.
- Identify what evidence would demonstrate each criterion and in which environment.
  A build result cannot substitute for a requested browser or device interaction.
- Keep implementation preferences separate from externally observable requirements.

For every proposed new/modified code change, include zero-trust review and verification
in the completion contract. Capture the actual project's trust boundaries and security
requirements; no-boundary-change is a conclusion to support, not an automatic exemption.
Specify evidence for changed behavior and affected allowed/denied operations. Scale depth
to risk; avoid inventing new policies, arbitrary thresholds, or a full audit for a trivial edit.

For AI features, identify model inputs and outputs, allowed actions, human decision
points, and the consequences of wrong or absent answers. When evaluation is needed,
specify representative cases and a measurable acceptance rule; label a proposed rule.
Do not treat a polished example or model self-assessment as evidence of general quality.

## Resolve uncertainty proportionately

Proceed with a stated, reversible assumption when it preserves the requested outcome.
Ask a targeted question when alternatives materially change behavior, authorization,
data contracts, architecture, or the meaning of success. Continue independent discovery.
Do not ask the user to restate information already available from authoritative context.
If the scope expands during implementation, expose the changed requirement and its
consequence before treating the expanded work as accepted.

## Output contract

Use a paragraph for a small change, or this compact structure for a larger brief:

- **Outcome:** actor, trigger, and intended result.
- **Scope:** affected surfaces and necessary integration; meaningful non-goals.
- **Acceptance:** criterion, required evidence, environment, and any proposed threshold.
- **Uncertainty:** assumptions and unresolved decisions with their practical impact.

Separate a ready implementation brief from verified completion. Acceptance criteria
are a plan for evidence; report them as passed only after observing that evidence.
Do not modify code, publish, or contact stakeholders merely because scope was defined.
Continue implementation when it is already part of the user's authorized task.

## Sources and interpretation

These sources inform the workflow; they do not impose every listed practice on every task.

- [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final): security practices can be integrated into an existing development lifecycle.
- [Google code review guidance](https://google.github.io/eng-practices/review/reviewer/looking-for.html): assess user-facing functionality, complexity, and meaningful tests.
