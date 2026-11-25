# Prompts worth copying

Swap in the real paths, skills, and done checks. Informal wording works.

## Understand

- `/se-playbook read <thread>. restate the underlying issue in your own words, in plain english.`
- `/se-restate <long or messy ask>`
- `/se-deepen <the prompt you're about to send>`
- `/se-playbook investigate why <symptom>. give me what we know, what data you used, and your best hypotheses. don't change any code yet.`
- `use /se-how to understand <subsystem>. then use /se-why to find out why it broke recently.`
- `/se-context my work on <topic> from last week, then read <issue>.`
- `/se-explain me why you implemented it this way and not <other way>. what did you trade off?`
- `/se-playbook take over this branch. read the decision log, find what's done, and continue. don't redo finished work.`

## Build

- Bug: `/se-playbook <symptom>. repro first, then fix and verify.`
- Bug in an app: `/se-playbook repro this with /<app>-harness. if it repros on main, fix it and show me a video as proof.`
- Bug with a cheap test: `/se-playbook repro <bug> first. if there's a cheap test path, /se-test-first it. then fix and rerun.`
- Feature: `/se-playbook add <behavior>. <current output> stays byte-identical. verify both.`
- Refactor: `/se-playbook move <code> into one module, zero behavior change. record the current output first and prove it's unchanged after.`
- Perf: `/se-playbook <operation> takes <time> on <fixture>. trace it, fix the measured cause, show me before and after.`

## Design and plan

- `/se-playbook prototype a few options for <feature>. take screenshots or videos for me to compare.`
- `/se-playbook we need <feature>. /se-design it first, and answer open questions with prototypes. let me review before proceeding.`
- `/se-playbook write a tutorial for how i would use <new package> first. then /se-explain me why it beats the current one.`
- `ask /se-contest for a second opinion on this thread and our approach.`
- `/se-playbook turn this design into a plan. small verifiable PRs, each with its own verification steps.`
- `/se-playbook plan the migration of <library> to <target>. small verifiable PRs. the result must match the original exactly, bugs included.`

## Review and ship

- `/se-challenge the whole branch, but skeptically. don't change anything yet. no nitpicks unless it's a real bug or regression.` Read the Dropped list too.
- `/se-formal prove <property> holds in <module>, even when <steps> interleave or retry.` After merges or refactors in that code: `/se-formal-sync`.
- `/se-swarm check every package under <dir> against its check script. one worker per package. one report.`
- `/se-playbook open the pr. small ordered commits, evidence in the description.`
- `/se-playbook babysit this pr. get it green.` For status only: `/se-playbook check on pr <number>. anything outstanding?`
- `/se-playbook land the stack.`

## Away and back

- `/se-playbook im going to bed. <goal> in a fresh worktree off <base>. done means <checks>. keep a decision log. don't ask me before committing. /loop until done. if you're truly stuck after a few hours, stop and write up why.`
- `/se-decision-log catch me up on what you did last night.` Read its Attention section first.
- `/se-recap` catches you up on this chat since your last message and lists every call that waits on you.
- `/se-playbook full autopilot on this queue. each item is independent.`
- `/se-playbook autopilot these changes, but don't merge. i'll land them.`
- `/se-retro capture what we learned so the next run doesn't repeat it.` Approve only edits that change a future decision.
- `/se-plain` restates the last reply in plain words.
