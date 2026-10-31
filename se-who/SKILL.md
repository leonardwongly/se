---
name: se-who
description: Identify the people, teams, reviewers, decision authorities, and operational owners responsible for an AI or software change. Use for accountability and approval ownership, rather than locating the code that owns a behavior.
---

# SE Who

Identify who performs, reviews, approves, and operates a software change, while keeping
ownership evidence separate from permission to act.

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

## Define the responsibility being resolved

Start from the specific component, change, release, incident, or pending decision.
Distinguish these roles when they affect the task:

- Implementation owner: carries the scoped work through integration.
- Reviewer: checks the relevant technical or domain concerns.
- Decision authority: can accept the product, architecture, or risk decision at issue.
- Operational owner: handles rollout, monitoring, rollback, and follow-up where relevant.

One person may hold several roles. Do not invent a formal committee or approval chain
for a small change when established project practice already answers the question.

## Establish ownership from evidence

1. Prefer explicit current task assignments and maintained ownership records.
2. Inspect relevant service documentation, team records, runbooks, or CODEOWNERS when
   needed. Include the repository, branch, scope, and freshness of the evidence.
3. Use contribution history as a lead for expertise, not proof of current ownership.
4. Report contradictions, stale assignments, and unowned integration boundaries.
5. Label proposed assignments and unresolved owners clearly; never invent identities.

For GitHub review routing, consult CODEOWNERS on the PR's base branch and apply its
matching rules. Check the effective repository review requirements when a claim about
required approval matters. A CODEOWNERS entry alone does not establish those rules.
It also does not grant the agent permission to modify code, merge, deploy, or message
the listed people. A review approval does not imply approval for unrelated actions.

## Make handoffs actionable

- Assign each deliverable a clear integration owner, not just a list of contributors.
- Describe the receiving owner, artifact or interface, completion evidence, and any
  dependency needed before the handoff is usable.
- When authorized concurrent work is involved, give contributors non-overlapping file
  or module ownership where practical, and identify shared interfaces before editing.
- Ensure an integration owner reconciles interfaces and validates the combined result.
  Contributor completion alone does not demonstrate integrated behavior.
- For every code change, assign responsibility for the zero-trust baseline and verification
  evidence, including worker/generated changes. One owner may cover both; do not invent
  a mandatory separate security team where project rules and risk do not require one.
- Preserve other contributors' changes and surface overlapping work before resolving it.

For AI features, identify who defines evaluation acceptance, authorizes tool actions,
handles escalations, and can stop or roll back the feature when those roles are needed.
The model or agent producing a recommendation is not automatically its approver.

## Output contract

For a simple question, name the evidenced role and link its source. For several roles,
use a compact map:

| Surface or decision | Role | Owner or proposed owner | Evidence | Gap or next step |
|---|---|---|---|---|

Include only roles that matter to the requested work. State whether assignments are
confirmed, inferred candidates, or unresolved, and what is needed to resolve a gap.
Provide a handoff draft when useful; sending it requires existing user authorization.

## Boundaries

Do not contact people, assign external tickets, change repository permissions, or edit
ownership records merely because the mapping identifies a suitable owner.
Continue authorized independent work while an ownership question remains unresolved;
pause only the action whose correctness or authorization depends on the answer.
Use the smallest appropriate review scope. Specialist review is justified by the
change's actual complexity or risk, not by a blanket requirement for every task.

## Sources and interpretation

These sources inform responsibility mapping; actual authority comes from task context
and the applicable project's rules.

- [GitHub CODEOWNERS documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners): file ownership and review-routing semantics.
- [Google code review guidance](https://google.github.io/eng-practices/review/reviewer/looking-for.html): match reviewer expertise to the relevant scope.
- [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final): integrate secure development practices into organizational workflows.
