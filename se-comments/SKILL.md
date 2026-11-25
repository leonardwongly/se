---
name: se-comments
description: "Review the comments in a change: a separate reviewer flags comments that restate code, narrate history or have gone stale, you fix the accepted findings, and claimed constraints are offered as checks instead of prose. Comments about an outside rule it cannot check are kept and marked for review. Use before review or commit, or when asked to clean up comments. For prose outside code use se-prose."
---

# SE Comments

Spawn Comment Sicko. Act on accepted findings.

Defer to Comment Sicko's fresh perspective.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch, default `main`, including the working tree.

## Steps

1. Spawn a subagent with `subagent_type: "comment-sicko"`. Pass the scope. Pick each subagent's reasoning level for the job, per the Subagents section of the **se-playbook** skill. Do not restate its rules. If your harness doesn't have comment-sicko registered as a subagent, spawn a general subagent instead: `Agent` in Claude Code (`subagent_type: general-purpose`), `task` in OpenCode (`subagent_type: general`), `spawn_agent` in Codex. Its prompt is [`references/comment-sicko.md`](references/comment-sicko.md) verbatim, then the scope. If your harness has no subagent tool, as in Pi without an extension, run that prompt yourself in a fresh pass over the scope.
2. Inspect its report and diff. Reject application-code edits, scope escapes, exception-protected deletions, misstated `MUST KILL` reasons, and flags that treat kept intentional code as guilty. Reshape flags on our-code surprises stay actionable. Do not restore those comments. A keep survives only with proof it is about something we cannot change. Audit missed scoped lint and TypeScript suppressions. Correctness or safety suppressions stay actionable `MUST KILL`s. Restore deletions only with exact exceptions and scoped proof. Before accepting thin `IMPORTANT` or `do not remove` kills or keeps, trace their symbol or run `/se-why` on it. If a kill is ambiguous, do not restore. If a keep is refuted or still ambiguous, delete it, except a `REVIEW` keep about an outside rule, which stays until someone checks that rule. Report it open. Revert and rerun one rejected report with the failure named. If you reject the rerun too, revert only its rejected findings, report them open, and go on with the accepted ones.
3. Fix trivial accepted flags directly by deleting a dead path, dropping a parameter, or using the real API. If any fix needs a shape, run `/se-design` once for the accepted set and surrounding code. Stop at the sketch. Architect shapes. Step 4 implements.
4. Implement the smallest root-cause fix in scope. Remove every named workaround. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. The [**Fix Root Causes**](../se-principles/references/fix-root-causes.md) and [**Redesign From First Principles**](../se-principles/references/redesign-from-first-principles.md) principles guide intent only. Neither authorizes widening the fence nor fixing instances outside it. Never bolt on symptom guards.
5. Constraint comments say `do not remove`, `do not change wording`, or `talk to X before changing`. Leave keeps about things we cannot change. Offer the cheapest in-scope type, runtime, test, or CI lint. Wait for interactive approval. Unattended and eval require caller pre-approval. If approved, encode then delete. Otherwise delete, report the constraint open, and sketch out-of-scope work.
6. Report the deletion count, restored comments, `REVIEW` keeps, reruns, architect sketch, fixes, encoding offers, encodings, unenforced constraints, and other open work.


## SE change baseline

Code, configuration, tests, CI, dependencies and behaviour-affecting prompts that this skill creates or changes follow SE's mandatory change baseline. Depth follows risk, and a small diff does not skip it.

- **Ground.** Confirm the actual project, source state, local instructions, maintained contracts and the real test and CI commands before you change anything.
- **Review trust.** Load **se-zero-trust** and review the change with it: untrusted inputs, authoritative identity, the enforcement boundary, and permitted and denied behaviour.
- **Verify.** Load **se-verify** and apply it: run the applicable project checks against the final source state, and keep failures, blockers and limits in the report.
- Checks you run yourself don't replace either skill. Say in your report that both ran.

Install **se-zero-trust** and **se-verify** with this skill.
