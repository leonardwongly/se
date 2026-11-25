---
name: se-contest
description: "Run N parallel candidates at the same non-trivial task, on different models where available, then pick the strongest as the base and graft the best parts of the others into it. Use for bake-offs, when asked to compare several implementations, or when one attempt would lock in the wrong shape. For parallel workers splitting different parts of one job use se-swarm; for attacking an existing change use se-challenge."
---

# SE Contest

Open a todolist with one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify) before launching anything.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric, 3-6 concrete gradeable criteria for what success looks like on *this* task. It is the picker's tool in Phase D. Candidates only see the task.
3. Pick the runners from the `arena runners` line in the SE settings file (`~/.claude/rules/se-models.md` in Claude Code, `~/.agents/se-models.md` in other harnesses), by default `claude-fable-5-2-high`, `claude-opus-5-5-high`, and `gemini-4-neon-xhigh`. An `auto` or `inherit-parent` entry is the parent model, so omit `model` and spawn a general-purpose subagent. If your subagent tool rejects a slug, use the nearest valid slug of the same family from its error message or your harness's model list, or drop the seat, keep at least two runners, and say so. Families go by prefix, and the longest match wins: `claude-fable-*`, `claude-*`, and `gemini-*`. Any other slug's family is its text before the first hyphen. Spawn more for multiple design directions, and repeat one model when the work is generation-bound, not judgment-sensitive. Pick each subagent's reasoning level per the Subagents section of the **se-playbook** skill.
4. Give each candidate its own output location (a git worktree where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`), per the **separate-before-serializing-shared-state** principle skill.

## Phase B: Fan out

Spawn all N subagents in one message with `run_in_background: true`, each with the task, the path to the shared grounding, its own output path, and instructions to produce the artifact and a short rationale naming the alternatives it considered and what it rejected.

If a candidate produces no output, proceed with N-1 and note the dropout.

## Phase C: Cross-judge

After all Phase B candidates complete, spawn one readonly judge from the `arena cross-judge pool` line in the SE settings file (`~/.claude/rules/se-models.md` in Claude Code, `~/.agents/se-models.md` in other harnesses), by default `claude-opus-5-5-high`, `gemini-4-neon-xhigh`. The judge is never from the parent's vendor, and Fable counts as Claude for that check, so use the first entry from another vendor. An `auto` or `inherit-parent` entry is the parent model. If you do not know the parent's model, use the first real slug and say that the vendor check did not run. If your subagent tool rejects a slug, use the nearest valid slug of the same family from its error message or your harness's model list, then the next such entry, or skip the judge, and say so. While you read in Phase D, the judge scores each candidate, by path label, on each rubric criterion and recommends a base.

## Phase D: Pick a base

Read every candidate end to end before picking. Score each against the rubric criterion by criterion, not on holistic feel, and compare with the cross-judge when Phase C ran one. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API, per the Laziness Protocol.

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base, usually one or two things per candidate, not most of it. Fold each graft in by hand, per the **redesign-from-first-principles** principle skill, so the result stays coherent under one mental model. Don't paste mechanically.

If the candidates converge on one shape, that is strong agreement. Note it and ship the consensus shape. No graft is needed. If they wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

Verify the synthesized artifact like any other output, per the **prove-it-works** principle skill. If verification finds a problem the arena missed, either Phase A was wrong (re-frame and re-run) or a candidate caught it and you missed the graft (go back to Phase E). Don't paper over it.

## Outputs

One synthesized artifact, with a short synthesis note alongside naming the base and why, the cross-judge's verdict or that Phase C skipped the judge, each graft with its source candidate, what was rejected and why, any convergence or dropouts, and the verification result.


## SE change baseline

Code, configuration, tests, CI, dependencies and behaviour-affecting prompts that this skill creates or changes follow SE's mandatory change baseline. Depth follows risk, and a small diff does not skip it.

- **Ground.** Confirm the actual project, source state, local instructions, maintained contracts and the real test and CI commands before you change anything.
- **Review trust.** Load **se-zero-trust** and review the change with it: untrusted inputs, authoritative identity, the enforcement boundary, and permitted and denied behaviour.
- **Verify.** Load **se-verify** and apply it: run the applicable project checks against the final source state, and keep failures, blockers and limits in the report.
- Checks you run yourself don't replace either skill. Say in your report that both ran.

Install **se-zero-trust** and **se-verify** with this skill.
