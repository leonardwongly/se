---
name: se-help
description: "Answer questions about the SE skill family: which skill, playbook or principle fits a task, which skills must be installed together, how to set up model roles, and how to word a prompt. Returns the answer, one prompt to send and the file the answer came from, and does not start the work. Use when someone asks which SE skill to use, how SE works, or why an SE run went wrong. To do the work itself, use the skill it recommends, usually se-playbook."
---

# SE Help

Answer the user's question about SE, hand them a prompt they can send, and link the file the answer came from. For a help question, don't start the work. The user asked how, and an SE run spends real tokens, so let them send the prompt.

A message that asks for work, such as "use SE to fix this bug", is not a help question. Read [`se-playbook`](../se-playbook/SKILL.md) and do the work under it.

This file maps questions to the skills that hold the answers. Those files own the details. Read the file you route to before you quote it, and trust it when it disagrees with this map. The links here point into the installed skills, which the user may not be able to open, so give the user the file's public copy: `https://github.com/leonardwongly/se/blob/main/` followed by its path.

## Find out what they need

Infer the need from the message and the conversation. A named situation, such as "which skill reviews a PR?", goes straight to its section. If the need is still unclear, ask one multiple-choice question with these options, then answer only the section they pick:

- Get set up
- Start a task with `/se-playbook`
- Pick a skill for a situation
- Fix a run that went wrong
- Make SE my own

Check the state that changes the answer, and mention it only when it does:

- No SE settings file (`~/.claude/rules/se-models.md` in Claude Code, `~/.agents/se-models.md` in other harnesses) means `/se-setup` hasn't run for this user, so every role uses its default model.
- No `*-harness` skill or other app harness in the project means agents have no scripted way to drive the app. Mention `/se-harness` when the question is about proving a change works.
- No formal verification skill in the project means no property is checked past what tests reach. Mention `/se-formal` when the question is about a race, an invariant, or another case tests rarely hit. When one exists and the code it covers changed after the commit it records as last in sync, mention `/se-formal-sync` if the question touches that code.
- No `CI.md` in the project means `/se-ci` hasn't surveyed its CI yet. Mention it when the question is about slow or flaky CI.

When the settings file is missing and it matters, ask whether the user wants to pick a model for each role and a reasoning budget now. It matters when the user is new, the question is about setup or cost, or the answer depends on which models run. Ask at most once per chat. If the need is also unclear, ask both questions together. Offer two choices:

- Now: give them `/se-setup` to type, and answer their question too.
- Later: answer their question, and add one line saying every role keeps its default model until they run `/se-setup`.

## Get set up

1. Install with `npx skills add leonardwongly/se` and pick the skills and the agent host. Install the groups under **Install together** whole, because those skills call each other.
2. Run [`/se-setup`](../se-setup/SKILL.md). It asks for a reasoning budget, maps a model to each role, and writes the settings file. The file applies to new sessions. Then it offers once each to generate a verification skill and a formal verification skill for the project, unless the project already has one.
3. Start a real task with `/se-playbook`, a goal, and a check that can pass or fail.

Every SE skill can load on its own when a request matches its description, and every one can be typed by name. Offer to word their first prompt with them, per [`references/prompting.md`](references/prompting.md).

If cost is the worry, say where the tokens go and how to spend fewer. SE spends extra tokens on subagents and review panels. Rerun `/se-setup` and pick a smaller budget or cheaper models. A role set to `auto` or `inherit-parent` runs on the chat's model, which saves tokens when the chat runs on a cheaper model. A shorter panel list runs fewer subagents, one for each entry. Fast-mode model slugs cost more, so SE uses them only when the user asks. Save `/se-playbook` for work that needs rigor.

SE skills work in any harness that loads Agent Skills: Claude Code, Codex, Pi, OpenCode, and others. The Harness section of [`se-playbook`](../se-playbook/SKILL.md) maps subagents, questions, transcripts, and settings paths to each harness's own.

## Install together

These skills call other SE skills, so install each with the skills it needs:

| Skill | Also install |
|---|---|
| `se-playbook` | `se-principles`, `se-zero-trust`, `se-verify`, and the skills its playbooks route to: install the whole family |
| `se-explain` | `se-how`, `se-why` |
| `se-writing` | `se-prose` |
| `se-design` | `se-contest` |
| `se-challenge` | `se-contest` |
| `se-impact` | `se-contest`, `se-how`, `se-why`, `se-prose` |
| `se-harness` | `se-harness-sync` |
| `se-formal` | `se-formal-sync`, `se-states` |
| `se-recap` | `se-plain` |
| `se-recap-video` | `se-recap`, `se-plain` |
| `se-ci` | `se-swarm`, `se-visualise`, `se-impact`, `se-benchmark`, `se-decision-log`, `se-principles`, `se-zero-trust`, `se-verify` |
| `se-help` | the skills you want help with |

Skills that change code or configuration also need `se-zero-trust` and `se-verify`, which carry SE's change baseline. The twelve original SE skills (`se-what`, `se-why`, `se-who`, `se-where`, `se-how`, `se-when`, `se-zero-trust`, `se-verify`, `se-concurrent`, `se-proof`, `se-visualise`, `se-swarm`) work on their own. When you recommend a skill, name what it needs installed with it.

## Start a task with `/se-playbook`

`/se-playbook` matches the task to a playbook, copies the playbook's steps into the todo list, and runs the other skills as the steps need them. A good prompt states the goal and how to tell it's done. It doesn't list skills, because a hand-written sequence tends to drop or reorder steps the playbook would keep. Read [`references/prompting.md`](references/prompting.md) before you help word one. It has examples.

`/se-playbook` attaches to the message that starts it, and it fades as the chat moves on. To keep it on for a long chat, use your host's way of keeping a skill active if it has one. Otherwise start each new task with `/se-playbook`. Mid-chat, "new task" makes it match a fresh playbook. `/se-playbook` already uses `playbook-worker` for the subagents its playbook steps spawn. To get the same style from a subagent of your own, spawn it with `subagent_type: "playbook-worker"`.

## Pick a skill

The default answer for work is `/se-playbook`, which runs most of the others when its steps need them. Name a skill directly when the user wants more or less of something than the playbook gives, or a single answer rather than a run. Read the skill before you recommend it, and give one example prompt.

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`/se-playbook`](../se-playbook/SKILL.md) |
| Pin down scope, requirements and acceptance criteria | [`/se-what`](../se-what/SKILL.md) |
| Check that the agent understood their goal and the problem before it starts | [`/se-restate`](../se-restate/SKILL.md) |
| Get a prompt rewritten deeper, not bigger, before sending it: what a top professional would add, their raw material and methods, and an outside check. It returns the prompt and doesn't do the task | [`/se-deepen`](../se-deepen/SKILL.md) |
| Know how code works now, or where new code should live | [`/se-how`](../se-how/SKILL.md) |
| Find where existing behaviour, a layer or evidence lives | [`/se-where`](../se-where/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`/se-why`](../se-why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`/se-explain`](../se-explain/SKILL.md) |
| Know who should explain, build or review something | [`/se-who`](../se-who/SKILL.md) |
| Know what must happen first, and when to roll out | [`/se-when`](../se-when/SKILL.md) |
| Catch up on their own recent work on a topic | [`/se-context`](../se-context/SKILL.md) |
| Catch up on what changed in this chat since their last message, in plain words and small visuals, with every item waiting on them listed and decidable from the reply alone | [`/se-recap`](../se-recap/SKILL.md) |
| Catch up like `/se-recap`, in a short subtitled video of slides, with the waiting calls as text under it | [`/se-recap-video`](../se-recap-video/SKILL.md) |
| Know what a small diff could break outside itself | [`/se-impact`](../se-impact/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`/se-design`](../se-design/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`/se-contest`](../se-contest/SKILL.md) |
| Run parallel checks over slices, race workers, or run a coordinated team to completion | [`/se-swarm`](../se-swarm/SKILL.md) |
| Split independent work across agents with clear ownership and one integration check | [`/se-concurrent`](../se-concurrent/SKILL.md) |
| Have different models review a diff and try to break it | [`/se-challenge`](../se-challenge/SKILL.md) |
| Review a change's trust boundaries, inputs and permissions | [`/se-zero-trust`](../se-zero-trust/SKILL.md) |
| Verify a change, or decide whether a claim of done is supported | [`/se-verify`](../se-verify/SKILL.md) |
| Back a claim or recommendation with evidence and stated limits | [`/se-proof`](../se-proof/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`/se-test-first`](../se-test-first/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`/se-typescript`](../se-typescript/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`/se-comments`](../se-comments/SKILL.md) |
| Clean AI tells out of prose | [`/se-prose`](../se-prose/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`/se-writing`](../se-writing/SKILL.md) |
| Hear the last reply again in plain words | [`/se-plain`](../se-plain/SKILL.md) |
| Explain something with a diagram, chart or animation | [`/se-visualise`](../se-visualise/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`/se-harness`](../se-harness/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`/se-harness-sync`](../se-harness-sync/SKILL.md) |
| Formally verify a race, invariant, or other property that tests rarely reach | [`/se-formal`](../se-formal/SKILL.md) |
| Bring a formal verification back in line after the code it covers changed, and learn whether a failure is drift or a bug | [`/se-formal-sync`](../se-formal-sync/SKILL.md) |
| Show a PM or designer what the user sees as a chart checked by a TLA+ model, with the shortest path to each state that breaks a rule | [`/se-states`](../se-states/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`/se-benchmark`](../se-benchmark/SKILL.md) |
| Make CI faster and more useful: affected-only tests, parallel jobs, flaky and useless tests found with evidence | [`/se-ci`](../se-ci/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`/se-blueprint`](../se-blueprint/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`/se-decision-log`](../se-decision-log/SKILL.md) |
| Apply or look up an engineering principle by name | [`/se-principles`](../se-principles/SKILL.md) |
| Pick a model for each role and a reasoning budget | [`/se-setup`](../se-setup/SKILL.md) |
| Turn their own working habits into a personal style skill | [`/se-style`](../se-style/SKILL.md) |
| Turn what a finished task taught into skill edits | [`/se-retro`](../se-retro/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`/se-guardrail`](../se-guardrail/SKILL.md) |
| Find their way around SE | `/se-help` |

If a skill directory next to this one is missing from the table, read its frontmatter and route by its description.

Close calls:

- `/se-how` explains what the code does. `/se-why` explains the reasons. `/se-explain` runs one or both and explains the result plainly. `/se-where` locates existing behaviour; `/se-how` answers where new code should live.
- `/se-contest` gives every worker the same brief and merges the best parts. `/se-swarm` splits work into slices or a race and returns one report, or runs a coordinated team to completion. `/se-concurrent` plans ownership for independent work.
- `/se-challenge` attacks the diff. `/se-impact` looks for breakage outside the diff and proves the one fact that makes the change safe. `/se-zero-trust` and `/se-verify` are the mandatory review and verification for every change.
- `/se-context` rebuilds context across recent chats. `/se-recap` covers only this chat since the user's last message. Resuming one specific chat or branch is the Session pickup playbook.
- `/se-blueprint` designs one rigorous run. The Autonomous run playbook drives one task to a finish condition. `/se-when` orders prerequisites and rollout.

Not in SE:

- Skill authoring uses your host's skill-authoring skill, such as Anthropic's `skill-creator`.
- `/loop` is built into Claude Code, not an SE skill.
- SE has no `/orchestrate` skill. If the slash menu shows `/orchestrate`, another plugin provides it.

## Playbooks and principles

Playbooks are step lists inside `/se-playbook`, not skills, so they have no slash command. Inside `/se-playbook`, describing the task picks one, and these phrases name one directly:

- "babysit this pr" or "check on pr 123" runs [Babysit](../se-playbook/playbooks/babysit.md). It drives the PR to merge-ready and stops there. It doesn't merge unless the user asks to merge, land, or ship.
- "land the stack" runs [Shipping](../se-playbook/playbooks/shipping.md).
- "take over this branch" runs [Session pickup](../se-playbook/playbooks/session-pickup.md).
- "pause safely" runs [Pause safely](../se-playbook/playbooks/pause-safely.md).
- "full autopilot on this queue" runs [Autopilot-full](../se-playbook/playbooks/autopilot-full.md). "autopilot, don't merge" runs [Autopilot-stack](../se-playbook/playbooks/autopilot-stack.md).
- "run the eval playbook" runs [Eval](../se-playbook/playbooks/eval.md).

Without `/se-playbook`, a phrase such as "babysit this pr" can start another installed skill for the same job instead. The Playbooks section of [`se-playbook`](../se-playbook/SKILL.md) lists every playbook. [Opening a PR](../se-playbook/playbooks/opening-a-pr.md), [Babysit](../se-playbook/playbooks/babysit.md) and [Shipping](../se-playbook/playbooks/shipping.md) cover a PR from open to landed.

For scope and acceptance criteria, use `/se-what`. For order and readiness, use `/se-when`. Your host's plan mode works alongside both. For work that spans phases or stacked PRs, asking `/se-playbook` for a plan runs the [Multi-phase plan playbook](../se-playbook/playbooks/multi-phase-plan.md), which writes the plan and doesn't implement it. For a design question, the Prototype playbook or `/se-design` settles it in code first.

Principles live in [`se-principles`](../se-principles/SKILL.md), which `/se-playbook` reads and cites in its replies. The user rarely opens one. They steer with the names instead, as in "apply prove it works. show me the real output." Typing `/se-principles` opens the index of all 24.

## Fix a run that went wrong

| Symptom | Fix |
|---|---|
| The playbook stopped applying after a few turns | It was attached to one message. Start each task with `/se-playbook`, or keep it active with your host's mechanism. |
| A question got treated as the next step of the last task | Say "new task", or say the turn doesn't need the playbook. |
| A new model choice had no effect | The settings file from `/se-setup` applies to new sessions. Start one. |
| Runs cost more than expected | See the cost paragraph under Get set up. |
| A skill didn't load on its own | SE skills load automatically only when the request matches their description. Name the outcome more concretely, or type the skill's name. |
| A skill reports a missing sibling skill | Install its group from **Install together**. |
| Parallel agents overwrote each other | Give each agent its own worktree, or run them as cloud agents, which each get their own machine. |
| An overnight run moved but finished nothing | `/loop` needs a check that can pass or fail, not a duration. See the [Autonomous run playbook](../se-playbook/playbooks/autonomous-run.md). |
| The reply claims success from a green build | Ask for the real command, flow, stored value, or profile. That's the [prove it works](../se-principles/references/prove-it-works.md) principle. |

For a run that drifts, [`references/prompting.md`](references/prompting.md) has one-line steers, and [`references/recipes.md`](references/recipes.md) has recipes worth copying and pitfalls to skip.

## Make SE my own

- [`/se-style`](../se-style/SKILL.md) drafts a personal style skill from the user's own history, to use alongside `/se-playbook`.
- [`/se-retro`](../se-retro/SKILL.md) after a session turns its lessons into skill edits the user approves.
- [`/se-guardrail`](../se-guardrail/SKILL.md) turns a mistake agents keep repeating into a check that fails.
- `/se-playbook write a skill for <workflow>` runs the [authoring playbook](../se-playbook/playbooks/authoring-a-skill.md). The [eval playbook](../se-playbook/playbooks/eval.md) tests a skill change blind.
- Fix a misbehaving skill in its own PR, not inside the feature work where it went wrong.

## Reply

Lead with the answer. Give at most one example prompt in a code block, adapted from [`references/recipes.md`](references/recipes.md) when one fits, then the link to that file. Keep it short unless the user asked for the whole map.
