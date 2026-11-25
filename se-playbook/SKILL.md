---
name: se-playbook
description: "Run substantial engineering work through a matched playbook: bug fix, feature, refactoring, perf issue, hillclimb, investigation, runtime or trace forensics, prototype, visual parity, authoring a skill, eval, opening a PR, babysitting or shipping a PR stack, autonomous and autopilot runs, session pickup, pausing safely, multi-phase plans and worktree cleanup. Copies the playbook's steps into the task list, applies se-principles, and calls other SE skills as each step needs them. Use when a task needs rigour from start to verified finish and no single narrower skill covers it, or when asked to work in the SE playbook style. For one explanation use se-how or se-why; when no playbook fits, use se-blueprint."
---

# SE Playbook

Bundled skills live at `../<name>/SKILL.md` from this file, so put this file's absolute path in every `playbook-worker` prompt.

## Non-negotiables

The Principles section below grounds every trigger. In your reply, name each principle that shaped a decision and the specific choice it changed. Cite only principles whose reference file in **se-principles** you read this session.

The remaining triggers live only here:

- First message → restate the user's goal and the smallest change that meets it, then proceed. Open each subagent brief, PR `## Why`, and final report with the goal.
- Starting any agent, whether a subagent or a project worker → the first line of its kickoff is `Read <path>/worker.md before anything else.`, with `<path>` the absolute path of this skill's folder. The operator's rules live in skills that only load from a slash command, so they reach another agent no other way. Keep the rest of the kickoff to the goal and the task, plus this file's absolute path for a `playbook-worker`.
- A fork you could settle by running something → prototype it per `playbooks/prototype.md` instead of asking.
- Code → name the data shape first. Across a function boundary → **se-design**. Fan-out → **se-swarm**. Bakeoff → **se-contest**. Contested design → **se-challenge**.
- Code, configuration, tests, CI, dependencies or behaviour-affecting prompts changed → the SE change baseline below: **se-zero-trust** review and **se-verify** verification before you call it done.
- Prose, your reply included → **se-prose**. Docs, PR descriptions, commit messages → **se-writing**.
- Before commit → reread the diff and cut what the change doesn't need: dead code, debug output, speculative layers, AI slop. Before review → **se-comments**.
- Shipping UI / IDE / CLI → drive it on the real surface with the project's `<app>-harness` skill from **se-harness**, or a named driver. See **Harness**.
- A number you measured → **se-benchmark**. CI speed, flaky tests or test selection → **se-ci**.
- PR status → the **Babysit** playbook. Landing a green stack → the **Shipping** playbook.
- Bot review comments → judge each on its merits, using [review triage](references/review-triage.md).
- Long or unattended work → **se-decision-log**.

## Principles

Read the [**se-principles**](../se-principles/SKILL.md) index at the start of multi-step work, then read the full reference for any principle you apply. Each entry below names when it applies.

**Core**

- [**Laziness Protocol**](../se-principles/references/laziness-protocol.md). Refactoring, sizing a diff, or tempted to add abstractions, layers, or signal threading. Bias to deletion and the smallest change that solves the problem.
- [**Foundational Thinking**](../se-principles/references/foundational-thinking.md). Before writing logic: core types and data structures, scaffold-vs-feature sequencing, what concurrent actors share.
- [**Redesign from First Principles**](../se-principles/references/redesign-from-first-principles.md). Integrating a new requirement into an existing design. Redesign as if it had been foundational from day one.
- [**Attack the Premise**](../se-principles/references/attack-the-premise.md). Two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly before you write another fix that assumes it.
- [**Subtract Before You Add**](../se-principles/references/subtract-before-you-add.md). Sequencing an addition, refactor, or rewrite. Remove dead weight first, then build on the simpler base.
- [**Minimize Reader Load**](../se-principles/references/minimize-reader-load.md). Reviewing or shaping code that's hard to trace. Count layers and hidden state, collapse one-caller wrappers, shrink mutable scope.
- [**Outcome-Oriented Execution**](../se-principles/references/outcome-oriented-execution.md). Planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture, don't preserve throwaway compatibility states.
- [**Experience First**](../se-principles/references/experience-first.md). Product, UX, or feature-scope tradeoffs. Choose user delight over implementation convenience.
- [**Exhaust the Design Space**](../se-principles/references/exhaust-the-design-space.md). A novel interaction or architectural decision with no precedent. Build 2-3 competing prototypes and compare before committing.
- [**Build the Lever**](../se-principles/references/build-the-lever.md). Any non-trivial work. Build the tool that does or proves it (codemod, script, generator), not by hand. The tool is the artifact a reviewer reruns.

**Architecture**

- [**Model the Domain**](../se-principles/references/model-the-domain.md). Writing stateful logic, or code that branches a lot or repeats a shape assumption across files. Encode the domain in a structure (state machine, typed model, table or registry, reducer, boundary, the right collection) instead of scattered conditionals.
- [**Boundary Discipline**](../se-principles/references/boundary-discipline.md). Wiring validation, error handling, or framework adapters. Guards at system boundaries, trust internal types, keep business logic pure.
- [**Type System Discipline**](../se-principles/references/type-system-discipline.md). Designing types or a signature in any typed language. Make illegal states unrepresentable, brand primitives, parse external data at boundaries.
- [**Make Operations Idempotent**](../se-principles/references/make-operations-idempotent.md). Designing commands, lifecycle steps, or loops that run amid crashes and retries. Converge to the same end state.
- [**Migrate Callers Then Delete Legacy APIs**](../se-principles/references/migrate-callers-then-delete-legacy-apis.md). Introducing a new internal API while old callers exist. Migrate and delete in one wave.
- [**Separate Before Serializing Shared State**](../se-principles/references/separate-before-serializing-shared-state.md). Concurrent actors might write the same file, branch, key, or object. Eliminate the sharing first.

**Verification**

- [**Prove It Works**](../se-principles/references/prove-it-works.md). After a task, before declaring done. Verify against the real artifact, not a proxy or "it compiles".
- [**Fix Root Causes**](../se-principles/references/fix-root-causes.md). Debugging. Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is legitimate.
- [**Sequence Work into Verifiable Units**](../se-principles/references/sequence-verifiable-units.md). Multi-step work (sweeps, migrations, runs of similar edits) and how you stack commits and PRs. Break work into small units that each end in a check, verify each before the next, and order delivery so the sequence proves itself.
- [**Test Behavior, Not Implementation**](../se-principles/references/test-behavior-not-implementation.md). Writing, changing, or keeping a test. Assert what the code's users can observe, so the test fails when that behavior breaks and keeps passing when only the internals change.
- [**Explain the Number**](../se-principles/references/explain-the-number.md). Apply before you measure, and before you trust, report, or act on a number you measured (a speedup, a regression, a throughput, a latency, or an eval result). Find what limits it, and rule out that it measured something other than the work you think.

**Delegation**

- [**Guard the Context Window**](../se-principles/references/guard-the-context-window.md). Context fills up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents, keep summaries in the main thread.
- [**Never Block on the Human**](../se-principles/references/never-block-on-the-human.md). Tempted to ask "should I do X?" on reversible work. Proceed, present the result, let the human course-correct.

**Meta**

- [**Encode Lessons in Structure**](../se-principles/references/encode-lessons-in-structure.md). You catch yourself writing the same instruction a second time. Encode it as a lint, metadata flag, runtime check, or script instead of more text.

## Autonomy

**Just do it, within the authority you have.** Use the tools the host makes available. Reversible work proceeds without asking. External actions (team chat, ticket updates, kicking off evals) proceed only where the user or the host already allows them; otherwise prepare them and ask. A skill grants no authority: host rules, permission prompts and required approvals still apply.

**Always pause** for irreversible writes: force-push to shared branches, deploys, data deletion, customer messages.

**Session overrides:** "Don't stop" / "going to bed" / "run until done" / "be fully autonomous" → keep going on the work already authorised.

**No is an acceptable answer.** Asked whether to do something, invited to add scope, or shown an approach, reply with your real judgment. Decline, push back, or say "this doesn't earn its place" when true. A recommendation is a judgment, not a validation. Agreement is not the default, candor over sycophancy.

## Subagents

**Use `subagent_type: "playbook-worker"` for any subagent you spawn directly inside a playbook step.** The chat that receives `/se-playbook` runs the playbook itself. Routed workflow skills (`se-challenge`, `se-swarm`) set their own `subagent_type`. Respect it.

**Defaults for every subagent call.** Run in the background where the tool allows it, use agent mode (read-only strips MCP), pass file pointers rather than inlined context, and give an explicit model per role, project workers included. `/se-setup` writes the SE settings file (`~/.claude/rules/se-models.md` in Claude Code, `~/.agents/se-models.md` in other harnesses), whose per-role lines override the defaults below and the role models in the routed skills (`se-contest`, `se-swarm`, `se-challenge`). A role with no line keeps its default. A line of `inherit-parent` or `auto` runs the role on the parent model, so omit `model` and spawn a general-purpose subagent, because `playbook-worker` defaults to Opus 5.5. Each code playbook reads its own line (`feature, refactoring`, `bug-fix`, `perf-issue`, or `hillclimb`), prose and judgment read `judgment and prose`, and trivial mechanical edits read `swarm workers`. If the settings file has no `# defaults: 3` line, an older setup wrote it. Keep honoring its lines, and tell the user once per session to rerun `/se-setup`.

- Code, prose, and judgment: `claude-opus-5-5-xhigh`.
- Trivial mechanical edits: `claude-opus-5-5-high`.
- Diverse review and design panels: one runner each on `claude-fable-5-2-high`, `claude-opus-5-5-high`, and `gemini-4-neon-xhigh`.

**Fable 5.2 is an exception.** It runs outside a panel only when the user named it for this task or two Opus 5.5 xhigh runs of the same brief failed its check. Say which. Difficulty alone never qualifies.

**Match the model to the job.** Start from the role's line or default, keep its family, and set the level the job needs. The `/se-setup` budget sets each role's starting level. Panel seats keep their listed level. Raise any other role one step, up to xhigh, for the hardest or subtlest work, lower it one step for judgment, and two or more steps for routine work. No role runs above xhigh. Use a `-fast` slug only when the user asked for fast mode, because it costs more. Verification always runs on the `swarm workers` model, `claude-opus-5-5-high` by default. A Gemini seat runs at `gemini-4-neon-xhigh` unless its line names another level. If your subagent tool rejects a slug, never pass it again. Fall back to the role's line or default, then the calling skill's fallback, then the closest valid slug of the same family, then omit `model`. Say so.

You own every subagent's work. Review the diff and write your own summary. A second opinion is the same prompt on another vendor's model.

**Fresh subagents by default.** Give a fix round, a follow-up, a retry, or the next queue item to a fresh subagent with the original brief, every later directive, and the prior agent's report and branch. Resume an existing subagent only when the work needs state that lives in it and is costly to move: its checkout, its uncommitted changes, or a process it still runs.

## Harness

SE skills run in any harness that loads Agent Skills: Claude Code, Codex, Pi, OpenCode, and others. Read harness-specific instructions in this skill, its playbooks, and the routed skills through these mappings. If you can't tell which harness you are, check which of the paths below exist.

- **Subagents.** "Subagent" means your subagent tool: `Agent` in Claude Code (`subagent_type: general-purpose`), `task` in OpenCode (`subagent_type: general`), `spawn_agent` in Codex. Drop parameters your tool doesn't have. A cloud agent means one where your harness offers it. Otherwise, run that agent locally in its own worktree. If your harness has no subagent tool, as in Pi without an extension, do each delegated step yourself, one after another.
- **`playbook-worker`.** Where it isn't registered as a subagent, spawn a general subagent whose prompt starts with: "Read <this file's absolute path> in full, including its Principles section, before any work." Then give the task.
- **Model settings.** Claude Code loads `~/.claude/rules/se-models.md` automatically. Elsewhere, `/se-setup` writes `~/.agents/se-models.md`. Read it at task start if it exists. If a model name doesn't resolve in your harness, use its closest equivalent. Model names carry the reasoning level (`-xhigh`, `-high`) and, when the user asked for it, fast mode (`-fast`). Where your subagent tool sets these separately, pass the level with its effort option (`effort` on Claude Code's `Agent`), and skip what your tool can't set.
- **Transcripts.** Read only the active workspace's sessions, never other projects'. Claude Code: `~/.claude/projects/<slug>/*.jsonl`, where `<slug>` is the workspace path with every character that isn't a letter or digit turned into "-". Pi: `~/.pi/agent/sessions/--<slug>--/*.jsonl`, where `<slug>` is the workspace path with the leading slash dropped and each "/" turned into "-". Codex: `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`, keeping files whose first line has `payload.cwd` equal to the workspace path. OpenCode: `~/.local/share/opencode/storage/`.
- **Skill folders.** Project: `.claude/skills/` (Claude Code), `.pi/skills/` (Pi), `.agents/skills/` (Codex, OpenCode, and others). User: `~/.claude/skills/`, `~/.pi/agent/skills/`, `~/.codex/skills/`, `~/.agents/skills/`.
- **Questions.** Use your structured-question tool: `AskUserQuestion` in Claude Code, `question` in OpenCode. Without one, ask in chat with numbered options.
- **Tools SE doesn't ship.** For skill authoring, use your harness's skill-authoring skill, such as Anthropic's `skill-creator`, or follow the Agent Skills format at agentskills.io. To drive the app, use the project's `<app>-harness` skill from **se-harness**. Without one, use the automation you have: Playwright or a CDP browser for web and Electron, tmux or a PTY for CLIs and TUIs. `/loop` is built into Claude Code. Without it, wait between checks with a timed shell command.

## Writing the reply

Write short declarative sentences with no long dash and no colon as a connector. Lead with what changes for the user. Give each claim its evidence or a label (measured, inferred, or guess). Never hand the human a check you could run.

## Playbooks

Match the task to a playbook and open its steps at `playbooks/<title>.md`, with the title in kebab case. Copy its steps into the todolist tool first. Large, cross-cutting, or unattended work, or a task no playbook fits, routes to the **se-blueprint** skill.

Investigation, Bug fix, Perf issue, Hillclimb, Runtime forensics, Trace forensics, Feature, Refactoring, Prototype, Visual parity, Authoring a skill, Eval, Babysit, Shipping, Autonomous run, Autopilot-full, Autopilot-stack, Session pickup, Pause safely, Multi-phase plan, Worktree cleanup, Opening a PR.

## SE change baseline

Code, configuration, tests, CI, dependencies and behaviour-affecting prompts that a playbook creates or changes follow SE's mandatory change baseline. Depth follows risk, and a small diff does not skip it.

- **Ground.** Confirm the actual project, source state, local instructions, maintained contracts and the real test and CI commands before you change anything.
- **Review trust.** Load **se-zero-trust** and review the change with it: untrusted inputs, authoritative identity, the enforcement boundary, and permitted and denied behaviour.
- **Verify.** Load **se-verify** and apply it: run the applicable project checks against the final source state, and keep failures, blockers and limits in the report.
- Checks you run yourself don't replace either skill. Say in your report that both ran.

Install **se-zero-trust** and **se-verify** with this skill.
