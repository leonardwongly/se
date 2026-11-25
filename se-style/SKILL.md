---
name: se-style
description: "Capture the user's working style into a personal skill named <name>-style, drafted or revised from what they say and, optionally, from recent transcripts. Use for 'automate me', 'turn my preferences into a skill', or updating that skill. For making repeated agent mistakes impossible use se-guardrail; for routing a session's learnings into existing skills use se-retro."
---

# SE Style

A guided flow for turning the user's working conventions into a skill agents will follow. The output is one `-style` skill tailored to them (e.g. `jay-style`, `priya-style`).

This skill orchestrates three others: an inline mining pass (see step 1), your harness's skill-authoring skill (authoring), and the **se-prose** skill (prose discipline). It sequences them. It doesn't replace them.

The skill-authoring skill is your harness's skill-authoring skill, such as Anthropic's `skill-creator`. If you have none, follow the Agent Skills format at agentskills.io. "The skill-authoring skill" below means whichever of these you use.

## Flow

### 0. Check for an existing skill

Look recursively for `*-style/SKILL.md` matching the user's handle in your harness's skill folders. In the project: `.claude/skills/` (Claude Code), `.pi/skills/` (Pi), or `.agents/skills/` (Codex, OpenCode, and others). For the user: `~/.claude/skills/`, `~/.pi/agent/skills/`, `~/.codex/skills/`, `~/.config/opencode/skills/`, or `~/.agents/skills/`. Style skills can live in a personal category directory (`<skills>/<handle>/`), not only at the top level. If one exists, confirm intent with your structured-question tool (`AskUserQuestion` in Claude Code, `question` in OpenCode) unless they already said "update my skill" or similar:

- Update the existing skill (default for repeat runs)
- Start fresh (rare, ask why before doing it)

Update mode changes the rest of the flow:
- Step 1 mines only history since the skill was last edited (`git log -1 --format=%cI <path>`).
- Step 2 asks what's changed or missing, not what to capture from zero.
- Step 4 edits the existing file in place. Preserve sections the user hasn't contradicted. Revise ones with new evidence. Add new sections only for genuinely new rules.

### 1. Mine their history

Locate the active workspace's transcripts before fanning out. Use only that workspace's directory. Don't glob across every project's directory. That crosses workspace boundaries and reads private chats from unrelated projects. Where they live depends on your harness:

- **Claude Code:** `~/.claude/projects/<slug>/*.jsonl`, where `<slug>` is the workspace path with every character that isn't a letter or digit turned into "-".
- **Pi:** `~/.pi/agent/sessions/--<slug>--/*.jsonl`, where `<slug>` is the workspace path with the leading slash dropped and each "/" turned into "-".
- **Codex:** `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`. Keep only files whose first line has `payload.cwd` equal to the workspace path.
- **Other harnesses:** the harness's session directory for this workspace.

Survey recent agent conversations within that scope for recurring patterns. Run multiple parallel subagents across slices of history (e.g. last 2-4 weeks, split into 3 slices so each has enough material). Pick each subagent's reasoning level for the job, per the Subagents section of the **se-playbook** skill. Each slice mining subagent reads transcripts from the workspace-scoped path the parent provides, looks for the signals below, and returns a short structured list of patterns it saw with evidence pointers. Default signals worth hunting:

- Response preferences (length, tone, format, "dumb it down" corrections)
- Delegation habits (subagents, models, specialized workflows, parallelism)
- Verification posture (what "done" means, unit tests vs live repro, reviewers)
- Code and prose discipline (style, principles cited, lint/format tools)
- Process conventions (worktrees, commits, PRs, review/merge tooling)
- Meta preferences (fixing skills mid-task, proposing new ones)

Cross-check across slices before elevating a signal. Patterns seen in 2+ slices are high-confidence. Lone signals are weak and usually get dropped.

### 2. Ask the user directly

Mining misses intent that hasn't come up yet. Use your structured-question tool (structured multi-choice: `AskUserQuestion` in Claude Code, `question` in OpenCode) rather than asking the user to type from scratch. If your harness has none, ask in chat with numbered options.

Shape: one or two questions with 4-6 options each, multi-select for category questions. Start broad ("Which areas matter most?"), then follow up on selected areas with specific options. After the structured rounds, one free-form chat question catches anything the options missed.

Don't dump 20 questions.

### 3. Cluster findings

Group the combined signals into sections. Common ones (use only what applies):

- **Response style**: length, tone, format.
- **Autonomy**: how much to do without asking, MCP tool use.
- **Understand first**: which skills to reach for when scoping or investigating a change.
- **Subagents**: default, parallelism, model-to-task, specialized workflows.
- **Prose / code discipline**: principles, lint tools, style guides.
- **Review and verify**: repro posture, verification skills, live-testing tools.
- **Process**: git worktrees, commits, PRs, review/merge tooling.
- **Skills**: skill-authoring habits, fix-the-skill-first, proposing new skills.

The **se-playbook** skill shows the shape. Read it for granularity. Don't copy its content. The user's rules are not the same as se-playbook's.

### 4. Draft the skill

Use the skill-authoring skill to author the skill. Placement:

- Path: preserve an existing style skill's category. For a new style skill, use `<skills>/<handle>/<handle>-style/SKILL.md` when the repo has an established personal category for that handle. Otherwise default to `<skills>/<handle>-style/SKILL.md` in the project, or the user-level skill folder if the user prefers a personal skill. `<skills>` is your harness's skill folder from step 0.
- Handle: the user's first name or chosen identifier.
- Frontmatter `description`: trigger on their name + `/<handle>-style` + "work in their style", not on generic keywords like "write code" or "review PR".
- Frontmatter formatting: follow the skill-authoring skill's YAML rules. Keep `description` as one YAML scalar. Quote it or use `description: >-` with indented continuation lines when punctuation or wrapping requires it.
- Frontmatter `disable-model-invocation: true` by default. Opt out only if the user explicitly wants their style skill to apply on every turn.

### 5. Iterate on prose

Apply the **se-prose** skill and the skill-authoring skill's writing guidelines to every line.

Show the draft to the user and take feedback. Expect multiple iterations. Cut ruthlessly. A style skill is not a manual.

### 6. Land it

Work in a worktree off main. Commit and open a PR. Don't push to main directly.

## Guardrails

- **Don't overfit to one conversation.** A preference stated once and contradicted another time is noise. Require multiple instances before codifying it.
- **Don't be clever.** Restating other skills' contents, inventing metaphors, or writing "poetic" prose for an agent reader is cost without benefit. Keep it operational.
- **Reference, don't inline.** Other skills the user relies on should appear as path references, not pasted excerpts. Same for any principle docs they maintain elsewhere.
- **Keep sections minimal.** Only add a section if the user has a specific, non-default rule there. "Communicate clearly" is not a section. "Short paragraphs. Tables when comparing options. Bullets only when items are genuinely parallel." is.
- **Name conventions generic.** Use "the user" or "the human" in imperatives, not the author's first name.
- **Don't force symmetry.** If a user has no process rules worth writing down, skip the Process section entirely.

## Evaluation

A `-style` skill is subjective output. A test-and-iterate benchmark loop from the skill-authoring skill isn't useful here. Vibe-check with the user: does it read like them? Did it miss anything? Then ship.

Run a description-optimization loop only if the skill's trigger accuracy turns out to be a problem in practice.

## When not to use

- User wants a task-specific skill (not working conventions): the skill-authoring skill alone, no mining required.
- User wants to capture one narrow workflow (e.g. "how I write commit messages"). That's a regular skill, not a style skill.


## SE change baseline

Code, configuration, tests, CI, dependencies and behaviour-affecting prompts that this skill creates or changes follow SE's mandatory change baseline. Depth follows risk, and a small diff does not skip it.

- **Ground.** Confirm the actual project, source state, local instructions, maintained contracts and the real test and CI commands before you change anything.
- **Review trust.** Load **se-zero-trust** and review the change with it: untrusted inputs, authoritative identity, the enforcement boundary, and permitted and denied behaviour.
- **Verify.** Load **se-verify** and apply it: run the applicable project checks against the final source state, and keep failures, blockers and limits in the report.
- Checks you run yourself don't replace either skill. Say in your report that both ran.

Install **se-zero-trust** and **se-verify** with this skill.
