# 001 — Integrate pstack into SE

**Status:** Approved (2026-11-21)

Implementation is complete. Verification is incomplete; see the verification report linked from REVIEW.md. The amended criteria (AC-10.3, FR-14) and the added AC-12.2 were approved on 2026-11-24.

## Problem and motivation

pstack is an MIT-licensed skill set by Lauren Tan. It has a router with 22 playbooks, 24 engineering principles and 31 single-purpose tools. SE has 12 skills built around grounded evidence, zero-trust review and verification. Today the two sets are installed separately and overlap in three places: how, why and swarm.

The maintainer wants one family under SE's own names. pstack's capabilities should be available inside SE, and every link between skills should keep working after the rename.

Today's pstack copy also has problems of its own that block a clean merge:

- It refers to features only Cursor has: Bugbot, Cursor rule files, Custom Mode, the AskQuestion tool and Cursor team-kit control skills.
- Its help skill links to guide pages that aren't shipped with the skills.
- Its skills run only when typed.
- Its naming (`principle-*`, `poteto-*`, `*-mode`, `create-*-skill`, `maintain-*-skill`) doesn't match SE's.

## User stories

- **US-1:** As an SE user, I want pstack's playbooks, principles and tools as `se-*` skills, so that I install and learn one family.
- **US-2:** As an SE user, I want every skill to be picked automatically when it fits and to be typeable by name, so that I don't need to memorise commands.
- **US-3:** As a maintainer, I want a check that proves every reference between skills resolves, so that a rename can't silently break the links.
- **US-4:** As a maintainer, I want the original author credited and the license honoured, so that the published package stays compliant.
- **US-5:** As an SE user, I want ported skills that change code to follow SE's mandatory change baseline, so that the family has one quality bar.

## Functional requirements

### FR-1 Rename table

Each pstack capability shall be available under the SE name below.

| pstack skill | SE skill |
|---|---|
| `poteto-mode` (router and its 22 playbooks) | `se-playbook` |
| `poteto-help` | `se-help` |
| `setup-pstack` | `se-setup` |
| `how` | merged into `se-how` |
| `why` | merged into `se-why` |
| `swarm` | merged into `se-swarm` |
| 24 `principle-*` skills | `se-principles` |
| `teach` | `se-explain` |
| `recall` | `se-context` |
| `in-your-own-words` | `se-restate` |
| `architect` | `se-design` |
| `arena` | `se-contest` |
| `interrogate` | `se-challenge` |
| `sharpen` | `se-deepen` |
| `figure-it-out` | `se-blueprint` |
| `statechart` | `se-states` |
| `tdd` | `se-test-first` |
| `typescript-best-practices` | `se-typescript` |
| `no-comments` | `se-comments` |
| `unslop` | `se-prose` |
| `technical-writing` | `se-writing` |
| `create-verification-skill` | `se-harness` |
| `maintain-verification-skill` | `se-harness-sync` |
| `create-formal-verification-skill` | `se-formal` |
| `maintain-formal-verification-skill` | `se-formal-sync` |
| `benchmark-checklist` | `se-benchmark` |
| `blast-radius` | `se-impact` |
| `show-me-your-work` | `se-decision-log` |
| `ketchup` | `se-recap` |
| `ketchup-video` | `se-recap-video` |
| `bro` | `se-plain` |
| `automate-me` | `se-style` |
| `correct` | `se-guardrail` |
| `reflect` | `se-retro` |
| ~~`make-bot-ui`~~ | not ported (decided 2026-11-21: it is specific to Grok Bot webhooks and Tailscale, and unrelated to engineering rigour) |

- **AC-1.1:** When the package is listed, the system shall contain exactly the 12 existing skills plus the ported skills in the table and `se-ci` (spec 002), and no other skill.
- **AC-1.2:** For each row, the SE skill shall carry the guidance of the pstack skill it replaces, apart from changes required by FR-4, FR-5, FR-8 and FR-12.

### FR-2 Merge overlapping skills

pstack's `how`, `why` and `swarm` guidance shall be merged into `se-how`, `se-why` and `se-swarm` rather than shipped as separate skills.

- **AC-2.1:** Given a "where should this live" or "which layer owns this" question, `se-how` shall cover placement and ownership as well as mechanisms.
- **AC-2.2:** Given a postmortem, regression or "why did we pick this threshold" question, `se-why` shall cover it with a cited answer.
- **AC-2.3:** Given a request to race, gauntlet or fan out N workers into one report, `se-swarm` shall cover that pattern alongside its existing team-execution guidance.
- **AC-2.4:** The merged skills shall keep every existing SE section and baseline statement.

### FR-3 One principles skill

The 24 principles shall live in one skill, `se-principles`. Each principle shall remain individually addressable by its title, such as "prove it works".

- **AC-3.1:** `se-principles` shall have an index listing all 24 principles, each with a one-line rule and the situations that trigger it.
- **AC-3.2:** When a skill refers to a principle, the reference shall resolve to that principle's full text.
- **AC-3.3:** When the router starts a multi-step task, it shall read the principles index, as pstack's router does today.

### FR-4 No pstack naming conventions

Skill names, generated-skill names, commands, descriptions and skill bodies shall not use pstack's naming. That means:

- no "pstack" or "poteto";
- no `principle-` prefix;
- no `-mode` skill naming;
- no `create-…-skill` or `maintain-…-skill` naming;
- no old pstack skill names used as references.

The attribution notice (FR-9) is the only exception.

- **AC-4.1:** When the residue check runs over the skill packages, it shall find none of the terms above outside the attribution notice.
- **AC-4.2:** When `se-harness`, `se-formal` or `se-style` generate a project-local skill, the generated name shall follow SE's naming, not pstack's (`verify-*`, `*-mode`).
- **AC-4.3:** Ordinary English words that are also old skill names (how, why, correct, teach, reflect, recall, sharpen, arena) shall remain unchanged in prose.

### FR-5 Linkage

Every reference from one skill to another shall name an existing SE skill, or a file that exists in the package. This covers typed commands, named skills, bold skill names and relative paths. References to material outside the package shall be replaced with in-package equivalents or removed. That outside material is pstack's guide pages, its README, its Claude Code adapter page and Cursor team-kit skills.

- **AC-5.1:** When the linkage check runs, every relative link in every skill file shall resolve inside the package.
- **AC-5.2:** When the linkage check runs, every skill-shaped reference (`/se-x`, `` `se-x` ``, `**se-x**`) shall name a skill in the package.
- **AC-5.3:** Given a reference that doesn't resolve, the linkage check shall fail and name the file, line and reference.
- **AC-5.4:** Every link between skills that exists in pstack shall exist between the corresponding SE skills, unless removed under FR-8 with the reason recorded.

### FR-6 Install together

Skills that call each other shall be documented as groups to install together. SE's "works without sibling skills" promise shall be limited to the skills that stay standalone.

- **AC-6.1:** The README shall list each skill that depends on others, and the skills it needs.
- **AC-6.2:** The 12 original SE skills shall stay usable on their own. Merged content shall add no mandatory dependency to them.
- **AC-6.3:** `se-help` shall say which group a skill belongs to when it recommends that skill.

### FR-7 Automatic and typed invocation

Every skill shall be selectable automatically when a task fits, and also invocable by typing its name.

- **AC-7.1:** No skill shall be marked typed-only.
- **AC-7.2:** Each description shall say what the skill does, when to use it, and, where a neighbouring skill is close, when to use the neighbour instead.

### FR-8 Host neutrality

Cursor-only features shall be replaced with host-neutral wording, or with Claude Code and Codex equivalents where a host path is needed. This covers Bugbot, Cursor rule files, Custom Mode, the AskQuestion tool and team-kit control skills.

- **AC-8.1:** The residue check shall find no Cursor-only feature named as a requirement.
- **AC-8.2:** Where pstack required a team-kit control skill to prove behaviour on a live app, the SE skill shall use the project's generated harness skill (FR-1, `se-harness`) or a named driver instead.
- **AC-8.3:** `se-setup` shall write its model choices to a location the current host reads, and say where.

### FR-9 Attribution and license

The MIT license text and copyright notice for the ported material shall ship with the package. The notice shall name the source repository and the pinned commit.

- **AC-9.1:** The package shall contain the full MIT license text with "Copyright (c) 2026 Lauren Tan".
- **AC-9.2:** The README shall credit the source and point to the notice.

### FR-10 Bundled scripts keep working

The PR watcher, the worktree audit, the decision-log helper and the statechart pipeline shall work after the rename.

- ~~**AC-10.1:** When each script's own test suite runs, all tests shall pass with the same counts as on the pinned source.~~ Replaced by AC-10.3: the pinned source itself does not pass every statechart test on this machine.
- **AC-10.3:** When each script's own test suite runs, it shall produce the same pass, fail and skip counts, with the same failing tests, as the pinned source on the same machine. (Amended 2026-11-21, approved 2026-11-24. Baseline: PR watcher 56 pass and 0 fail; statechart 228 pass, 2 fail and 70 skipped. The 70 skipped need `tla2tools.jar`.)
- **AC-10.2:** The PR watcher shall keep the mirror's two safety fixes: it ignores fork PRs, and it strips control characters from review text.

### FR-11 Validation covers the new family

The package validator shall check the new skill inventory, linkage (FR-5) and residue (FR-4, FR-8). The installed-file checker shall compare every file of every skill package, not only the entry file and UI metadata.

- **AC-11.1:** When the validator runs on the finished package, it shall pass.
- **AC-11.2:** Given a broken link, a reference to a missing skill, or a residual pstack term, the validator shall fail with a message naming it, and a regression test shall prove each case.
- **AC-11.3:** Given an installation missing a playbook or reference file, the installed-file checker shall report that file as missing.

### FR-12 SE change baseline in ported skills

Ported skills that create or change code shall state that SE's mandatory change baseline applies: grounding, zero-trust review and verification.

- **AC-12.1:** Each ported skill that edits code or configuration shall reference `se-zero-trust` and `se-verify` for its review and verification steps.
- **AC-12.2:** Each such skill shall tell the agent to load `se-zero-trust` and `se-verify` for those steps, so that checks the agent runs itself do not stand in for them. (Added 2026-11-24, after a playbook-driven bug fix changed product code without loading either skill; approved 2026-11-24.)

### FR-13 Selection still routes correctly

With every skill now automatic, routing shall be evaluated.

- **AC-13.1:** When a set of task prompts without skill names runs in fresh agent sessions with the full package installed, each prompt's expected skill shall be read. The set shall cover the overlap areas: how/explain, why, swarm/contest, verify/harness/benchmark, writing/prose/plain, and design/blueprint/playbook.
- **AC-13.2:** Misroutes shall be recorded. Description fixes shall be re-run until the evaluation passes, or the remaining gap shall be reported.

### FR-14 SE authority and cost rules in ported guidance

Added 2026-11-21 during implementation, approved 2026-11-24. Two pieces of pstack guidance went against rules SE and the maintainer already hold. pstack's router let external actions "proceed without asking", and it ran Opus 5.5 in fast mode by default.

- **AC-14.1:** The router's autonomy guidance shall say that external actions proceed only where the user or the host already allows them, and that host rules, permission prompts and required approvals still apply.
- **AC-14.2:** No default model name in a ported skill shall select fast mode. Fast mode shall be used only when the user asks for it.

## Non-functional requirements

### NFR-1 Compatibility

- **AC-NFR1.1:** The existing validator checks shall still pass: both fixture suites, the independent graders, the negative control and the proof and swarm exercises.
- **AC-NFR1.2:** The 12 existing skill names shall not change.

### NFR-2 Licensing

- **AC-NFR2.1:** No ported file shall be published without the attribution required by FR-9.

### NFR-3 Selection cost

- **AC-NFR3.1:** Every description shall be 1,024 characters or fewer.

### NFR-4 Script safety

- **AC-NFR4.1:** Ported scripts shall gain no new network access, credential handling or write targets beyond the pinned source.

## Out of scope

- Redesigning the animated guide and skill explorer in `docs/` beyond keeping their links valid. This is a separate follow-up.
- Porting pstack's long-form guide pages. `se-help` covers what it needs.
- Automatically syncing future upstream pstack changes.
- Removing the globally installed pstack copy from this machine. That is offered separately.

## Open questions

None. `make-bot-ui` is not ported (decided at approval, 2026-11-21).
