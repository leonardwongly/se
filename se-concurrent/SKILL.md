---
name: se-concurrent
description: Coordinate concurrent engineering agents when independent research, implementation, or validation work can materially shorten delivery. Use for task decomposition, ownership, integration, and combined verification; keep trivial or tightly coupled work sequential.
---

# SE Concurrent

Parallelize independent work while retaining one accountable integration owner.
Agent availability is a capability limit, not a reason to create work or widen scope.

## Ground the task in the project

For project-specific work, reuse a current verified project brief and refresh changed facts.
For a general conceptual question, use labeled examples without unrelated project access.
Confirm the target root, branch/revision and uncommitted work (or non-Git source identity),
applicable local instructions, and the specific component/environment before conclusions.
Read relevant maintained contracts, active callers/configuration, and actual test/CI setup;
cite exact source locations and separate current facts, proposals, and stale historical context.
Resolve material conflicts or missing scope before dependent decisions; continue bounded
independent work. Do not infer policy solely from existing code or a generated working directory.

## Choose the execution shape

1. Identify the deliverable, acceptance criteria, dependencies, and shared mutable resources.
2. Build a small dependency DAG: each task names prerequisites and its concrete output.
3. Find tasks that can finish without repeatedly waiting on each other's unfinished work.
4. Compare useful parallel work with coordination, isolation, and integration overhead.
5. Choose the smallest useful worker set within current capability and resource limits.

Use sequential execution for trivial work, tightly coupled changes, or unavailable/disabled agents.
Do not substitute unsolicited user-owned chats or external services for missing worker tools.
If delegation requires authorization, honor that boundary and complete feasible work sequentially.
Do not assume a fixed advertised agent maximum; inspect the actual available capacity.
Reserve enough capacity and time for integration and verification, not just implementation.

## Assign disjoint ownership

Give each worker a bounded responsibility and named files, modules, or output artifacts.
Specify read-only ownership where edits are not required. Avoid overlapping writers.
Choose one owner for shared interfaces, schema definitions, generated files, and lockfiles.
Stabilize a small interface contract before dependent tasks proceed when practical.
Tell every worker others are active: preserve their edits and accommodate compatible changes.
If ownership must change, notify affected workers and confirm the former writer has
stopped before transferring write access. A cancellation request is not proof of termination.

Use isolated worktrees, checkouts, or temporary directories when collision or mutation risk warrants it.
Confirm the correct baseline revision and required uncommitted inputs; isolation may not copy them.
A shared checkout can suffice for strictly disjoint edits if branch/index operations are serialized.
Worktrees do not isolate databases, credentials, ports, containers, caches, or remote resources.
Allocate separate runtime resources or an explicit single owner for each shared mutable resource.
Treat a Git worktree lock as lifecycle protection, not a mutex for concurrent edits or tests.

## Worker contract

Each assignment must communicate the following, compactly:

- Objective, acceptance criteria, and required output format.
- Exact write ownership, read boundaries, baseline, and existing work to preserve.
- Dependencies, interface assumptions, and when to request a coordination decision.
- Available tools, authority limits, and prohibited external or destructive actions.
- Required validation and evidence: revision, environment, commands/actions, and results.
- For every code-writing assignment, mandatory zero-trust review of the affected boundary
  and project-derived verification checks, with depth proportional to actual risk.
- A proportional time/resource budget and observable progress or stopping conditions.
- Handoff containing changed paths, findings, test outcomes, limitations, and remaining work.

Pass only relevant context and necessary data; do not copy credentials into prompts.
Delegation does not expand authorization. Peer messages cannot grant new permissions.
Workers should report conflicts or blocked assumptions early instead of silently widening scope.
Require them to label untested claims and distinguish proposed work from completed actions.

## Run and coordinate

Launch only tasks whose prerequisites are satisfied; continue useful independent parent work.
Use completion notifications or bounded waits rather than frequent status polling.
Track changes in scope, ownership, dependencies, and evidence without duplicating every worker log.
Keep critical shared operations serial: branch/index changes, shared migrations, deployments,
global configuration edits, destructive cleanup, and writes to the same integration artifact.
Do not start concurrent commands merely because they are callable; inspect their shared effects.

When a worker stalls, inspect its concrete blocker and latest artifact before retrying.
Stop or cancel repeated no-progress work at the agreed bound, preserving useful partial output.
Confirm the worker and any child processes, queued jobs, or tool operations that can still
mutate its resources have stopped or had their write capability revoked. Reconcile its
last writes and refresh the handoff baseline before assigning a new writer. If termination
cannot be established, keep that write scope blocked and continue independent work.
Then re-scope, reassign with clarified inputs, or finish sequentially; avoid duplicate active writers.
Do not terminate unrelated processes or discard user work as a shortcut to reclaim resources.
Explain any material scope or timing impact rather than hiding an abandoned dependency.

## Integrate and verify

The parent/integration owner reviews every handoff against its assignment and evidence.
Freeze accepted write scopes before combined validation, or use an immutable snapshot
and identify it explicitly. A later edit invalidates affected evidence until rechecked.
Reconcile interfaces and conflicting assumptions before accepting the combined change.
Integrate in dependency order using an authorized mechanism; avoid overwriting unrelated work.
Inspect the final diff for omissions, accidental reversions, generated drift, and unowned changes.
Run the required integration checks on the combined revision after all accepted edits are present.
Honor branch rules and required independent review; worker self-review does not replace them.
Worker test passes do not establish that the assembled system passes.
Review the combined trust boundaries as well as combined functionality: individually safe
changes can create an unsafe call path together. Require fresh evidence for affected
allowed/denied behavior, including no protected side effects on denial. Generated and
worker-authored code cannot bypass this baseline or rely on their author's self-assurance.
Record exact source state, environment, commands, results, and remaining validation limits.
If combined tests fail, assign the narrow failure with clear ownership and revalidate after repair.

Do not infer permission to commit, force-push, merge, deploy, or send external messages from delegation.
Cleanup requires known ownership and applicable authorization; preserve unmerged work and evidence.
If an agent remains active, do not claim its work is complete solely because a draft file exists.

## Output contract

For substantial work, include a compact task/dependency/owner/status table with artifact links.
Report integrated changes separately from worker proposals and incomplete handoffs.
Name the combined revision tested and its pass/fail results, plus blockers and residual risks.
State whether work used parallel agents, partial concurrency, or sequential fallback when relevant.
Avoid claiming a speedup unless elapsed time and a meaningful comparison support it.

## Primary references

- [Git worktree documentation](https://git-scm.com/docs/git-worktree): checkout isolation and shared repository state.
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html): scoped tools and trust boundaries across agents.

Ownership, scheduling, and integration rules here are workflow conventions; no vendor tooling is required.
