# Automatic selection across the 44-skill family

Evidence for [spec 001](../specs/001-pstack-integration/spec.md) FR-13: with every skill selectable
automatically, do task prompts that name no skill still reach the right one?

## Method

- **Prompts.** 19 prompts in [pstack-selection/prompts.json](pstack-selection/prompts.json): three for
  each overlap area named in AC-13.1 (how/explain, why, swarm/contest, verify/harness/benchmark,
  writing/prose/plain, design/blueprint/playbook) and one for `se-ci`. None names a skill. Each lists
  the skills that count as a correct route.
- **Sessions.** One fresh headless session per prompt, in its own copy of the CI fixture project
  ([ci-fixture/project](ci-fixture/project)): `codex exec --ephemeral --json`, read-only unless the
  prompt asks for a change. Runner: [pstack-selection/run_selection.py](pstack-selection/run_selection.py).
- **Installation.** The 44 skills at the evaluated revision, installed globally with
  `npx skills add <checkout> -g -a claude-code -a codex -a qoder -s '*' -y --copy` and verified with
  `scripts/check_installed.py` (577 of 577 files match in `~/.agents/skills`, which Codex reads, and
  in `~/.claude/skills`, which Claude Code reads). The family was reinstalled and checked again after
  every description change.
  Before the run, the original pstack skills and the older 12-skill SE copies were removed from
  every global skill folder, with the maintainer's approval, so no older copy could answer.
- **Pass rule.** A prompt passes when the transcript shows the session reading the `SKILL.md` of an
  expected skill. Reading a skill is a routing signal, not proof that it was applied well.
- **Conditions.** The maintainer's global `~/.codex/AGENTS.md`, which routes engineering tasks to the
  twelve original SE skills, stayed in place. This therefore tests global routing instructions plus
  installed-skill selection, as the earlier evaluations did.
- **Claude Code runs** use `claude -p --output-format stream-json --model opus` with
  `--setting-sources user,project,local`, because user-level skills in `~/.claude/skills` are not
  loaded without the `user` source. That source also brings the maintainer's user settings, hooks and
  global CLAUDE.md, as in normal use. Each session starts with a clean environment: a `claude` started
  from inside a Claude Code session otherwise inherits that session's variables, including the one
  that switches on bare mode, which skips skill discovery. A one-line appended system prompt says the run
  is unattended in a disposable fixture. The pass rule counts a `Skill` tool call or a `SKILL.md` read.
- **Rounds (Claude Code).** A round runs each chosen prompt once. After a round, each miss was
  read from its transcript; where the description was the likely cause it was changed, the family was
  reinstalled and checked, and only the affected prompts ran again. A change that fixed nothing was
  reverted.
- **Project instruction (Claude Code, round 5).** `run_selection.py --instructions <file>` writes a
  file into each fixture copy as its `CLAUDE.md` (or `AGENTS.md` for Codex) and commits it, as a
  project would. Rounds 5 to 8 used [pstack-selection/load-skill-instruction.md](pstack-selection/load-skill-instruction.md),
  two generic sentences that name no prompt or task type.
- **Conditional skill.** `se-typescript` declares `paths: ["**/*.ts", "**/*.tsx"]`, so Claude Code
  lists it only in projects with TypeScript files. In a probe outside such a project, a headless
  session listed the other 43 skills and not this one.

## Results — Codex, 2026-11-21

**Incomplete: 8 of 19 prompts ran; 7 of those 8 routed as expected.** The other 11 sessions were
stopped by the Codex account's usage limit (resets 2026-11-25). Raw results:
[results-codex-2026-11-21.json](pstack-selection/results-codex-2026-11-21.json).

| Prompt | Expected | Read first (in order) | Result |
|---|---|---|---|
| how-1 invoice walkthrough | se-how or se-explain | se-how, se-proof, se-where | pass |
| how-2 where a refund feature should live | se-how | se-where, se-proof | **misroute** |
| how-3 teach me this codebase | se-explain | se-explain, se-proof, se-how, … | pass |
| why-1 why the 3 s sleep | se-why | se-proof, se-why | pass |
| why-2 why run 7007 failed | se-why | se-where, se-proof, se-why | pass |
| why-3 where the tax rate came from | se-why | se-proof, se-why, se-where | pass |
| par-1 fan out a flakiness check | se-swarm | audit-test-quality, se-swarm, … | pass |
| par-2 three competing implementations | se-contest | se-concurrent, se-contest, … | pass (read before the limit stopped the session) |
| par-3 … ci-1 (11 prompts) | see prompts.json | — | not run: usage limit |

No completed session reported Codex's skills context budget warning.

## Results — Claude Code, 2026-11-24

**With the shipped descriptions alone, 14 of 19 prompts read an expected skill in their latest run.
With a two-sentence project instruction, all 19 did** (rounds 5 to 8, below). Rounds 1 to 4 ran 30
sessions on `opus`. No session reported a skills budget warning, and each listed 119 skills, 43 of
them from the family (`se-typescript` is conditional).

| Round | Descriptions | Prompts | Read an expected skill |
|---|---|---|---|
| 1 | as ported | all 19; 12 were stopped by the account's 5-hour usage limit | 3 of the 7 that ran |
| 2 | `se-why` and `se-swarm` rewritten | the 16 that missed or did not run | 11 of 16 |
| 3 | `se-verify`, `se-plain`, `se-prose` and `se-test-first` extended | the 4 new misses | 1 of 4 |
| 4 | as round 3 | how-1 to how-3, to check for regressions | 2 of 3 |

| Prompt | Expected | Round 1 | Round 2 | Round 3 | Round 4 | Latest |
|---|---|---|---|---|---|---|
| how-1 | se-how or se-explain | se-how | — | — | se-how | pass |
| how-2 | se-how | se-how | — | — | none | **miss** |
| how-3 | se-explain | se-explain | — | — | se-explain | pass |
| why-1 | se-why | none | se-why | — | — | pass |
| why-2 | se-why | none | se-why | — | — | pass |
| why-3 | se-why | none | se-why | — | — | pass |
| par-1 | se-swarm | none | none | — | — | **miss** |
| par-2 | se-contest | usage limit | se-contest | — | — | pass |
| par-3 | se-challenge | usage limit | se-challenge, se-contest | — | — | pass |
| ver-1 | se-harness | usage limit | se-harness, ledger-harness | — | — | pass |
| ver-2 | se-benchmark | usage limit | se-benchmark | — | — | pass |
| ver-3 | se-verify | usage limit | none | none | — | **miss** |
| wri-1 | se-writing | usage limit | se-writing | — | — | pass |
| wri-2 | se-prose | usage limit | none | none | — | **miss** |
| wri-3 | se-plain | usage limit | none | se-plain | — | pass |
| des-1 | se-playbook or se-test-first | usage limit | none | none | — | **miss** |
| des-2 | se-design | usage limit | se-design | — | — | pass |
| des-3 | se-blueprint | usage limit | se-blueprint, se-decision-log | — | — | pass |
| ci-1 | se-ci | usage limit | se-ci | — | — | pass |

Cells list the skills each session read; "none" means it loaded no skill. `ledger-harness` is the
project-local skill that `se-harness` generated during that session. Raw results:
`pstack-selection/results-claude-2026-11-24-round1.json` to `-round4.json`.

The shipped descriptions are round 2's plus the `se-plain` change from round 3. The round 3 changes
to `se-verify`, `se-prose` and `se-test-first` fixed nothing and were reverted, so `se-verify` keeps
its original wording.

### Rounds 5 to 8: with a project instruction

The five prompts that still missed (how-2, par-1, ver-3, wri-2, des-1) ran once more with the
shipped descriptions and this project `CLAUDE.md`:

> When a request matches an installed SE skill (`se-*`), load that skill before you start, and
> follow it, even when the task looks small enough to do directly. Its rules (what counts as
> evidence, the SE change baseline, what it reports) apply only when it is loaded.

**All five loaded an expected skill, each as the session's first tool call** (one run each; raw
results in `pstack-selection/results-claude-2026-11-24-round5-instruction.json`).

| Prompt | Without the instruction | With it | What changed in the work |
|---|---|---|---|
| how-2 | `se-how` once, none once | `se-how` | the same placement answer |
| par-1 | none twice | `se-swarm` | five Sonnet workers as before, now under the skill's fan-out pattern, plus a full-suite run in the lead |
| ver-3 | none twice | `se-verify` | a criterion table with PASS and FAIL states and evidence, instead of prose |
| wri-2 | none twice | `se-prose` | a similar rewrite that names each cut phrase, as one of the two runs without the skill also did |
| des-1 | none twice | `se-playbook` (its bug-fix playbook) | reproduce, fix and regression test as before; see the baseline finding below |

Round 6 re-ran des-1 after the baseline rewording (see the findings). Rounds 7 and 8 then ran the
other 14 prompts with the same instruction, to check that it breaks no route that worked. Round 7
was stopped by the account's usage limit after six prompts; par-2 had already loaded `se-contest`
when its session was stopped. Round 8 re-ran the other eight.

**All 19 prompts loaded an expected skill, each as the session's first tool call** (one run each).
No session loaded any skill before the expected one. Later loads came from the skills' own links:
`se-challenge` to `se-contest`, `se-harness` to the harness it generated and to the baseline skills,
and `se-blueprint` to `se-decision-log` and `se-playbook`. Raw results:
`results-claude-2026-11-24-round5-instruction.json`, `-round6-baseline.json`,
`results-claude-2026-11-25-round7-instruction.json` and `-round8-instruction.json`.

| Prompt | Expected | Without the instruction (latest run) | With it (latest run) | Round |
|---|---|---|---|---|
| how-1 | se-how or se-explain | se-how | se-how | 7 |
| how-2 | se-how | none | se-how | 5 |
| how-3 | se-explain | se-explain | se-explain | 7 |
| why-1 | se-why | se-why | se-why | 7 |
| why-2 | se-why | se-why | se-why | 7 |
| why-3 | se-why | se-why | se-why | 7 |
| par-1 | se-swarm | none | se-swarm | 5 |
| par-2 | se-contest | se-contest | se-contest (then stopped by the usage limit) | 7 |
| par-3 | se-challenge | se-challenge, se-contest | se-challenge, se-contest | 8 |
| ver-1 | se-harness | se-harness, ledger-harness | se-harness, ledger-harness, se-zero-trust, se-verify | 8 |
| ver-2 | se-benchmark | se-benchmark | se-benchmark | 8 |
| ver-3 | se-verify | none | se-verify | 5 |
| wri-1 | se-writing | se-writing | se-writing | 8 |
| wri-2 | se-prose | none | se-prose | 5 |
| wri-3 | se-plain | se-plain | se-plain | 8 |
| des-1 | se-playbook or se-test-first | none | se-playbook, se-verify, se-zero-trust | 6 |
| des-2 | se-design | se-design | se-design | 8 |
| des-3 | se-blueprint | se-blueprint, se-decision-log | se-blueprint, se-decision-log, se-playbook | 8 |
| ci-1 | se-ci | se-ci | se-ci | 8 |

## Findings

- **Abstract descriptions missed concrete questions (fixed).** `se-why` described "the rationale
  behind … decisions". Claude Code answered "why does this test sleep", "why did run 7007 fail" and
  "where did 0.09 come from" with Bash alone. Naming those question shapes in the description sent
  all three to `se-why`. `se-plain` covered only "the last message"; adding a passage the user quotes
  fixed wri-3.
- **Claude Code does some tasks itself instead of loading the skill (open, AC-13.2).** For par-1,
  ver-3, wri-2 and des-1 the description already names the request; par-1's "fan-out … drained into
  one consolidated report" is nearly the prompt. Claude Code still did each task directly. It
  started five Sonnet workers with its own Agent tool, checked the claim with Bash, rewrote the
  sentence, and fixed the bug test-first. The results were sound, but the skills' own rules were not
  applied. Two rounds of description changes did not move these four, so the gap is reported here
  rather than worded around. A two-sentence project instruction did move them: with it, all 19
  prompts loaded the expected skill first, and none loaded an unrelated skill (rounds 5 to 8). The
  README now recommends it as a setup step, and the validator keeps the README's copy identical to
  the tested file.
- **Baseline skills were not loaded by name (fixed).** In round 5, des-1 followed `se-playbook`'s
  bug-fix playbook and changed product code, but never loaded `se-zero-trust` or `se-verify`. The
  baseline section said "review trust **with** se-zero-trust" and "verify **with** se-verify";
  `se-ci` had the same wording and the same result until its fix 7 said "load" each skill. The
  baseline section in all 16 skills that carry it now says to load both skills by name, and the
  validator checks it (spec 001 AC-12.2). In round 6, des-1 ran again with the project instruction:
  it wrote the failing test, fixed the code, then read `se-verify` and `se-zero-trust` and reported
  each one's result (one run; `pstack-selection/results-claude-2026-11-24-round6-baseline.json`).
- **Selection varies between runs.** how-2 loaded `se-how` in round 1 and no skill in round 4, with
  the same `se-how` description. One run per prompt shows that a route can work, not how often it
  does. A selection rate needs repeated trials.
- **The two hosts miss different prompts.** With the original descriptions, Codex read `se-why` for
  all three why prompts, and Claude Code read it for none. Codex sent how-2 to `se-where`; Claude Code
  sent it to `se-how` once and answered it directly once.
- **Placement overlap (how-2).** A "where should new code live" question went to `se-where`, whose
  original description already claims "placement decisions". The merged `se-how` covers the same
  question (FR-2). Both skills can answer it, so this is an overlap rather than a wrong answer, but it
  misses the pre-registered expectation. Proposed fix, not applied because it changes an original
  skill and could not be re-tested: narrow `se-where`'s description to existing behaviour and point
  new-code placement at `se-how`.
- **Codex skills context budget.** Two `se-ci` evaluation sessions (not this test) reported
  "Exceeded skills context budget. All skill descriptions were removed and N additional skills were
  not included". The first (51 skills dropped) had the 44 skills as project skills while the 58
  original pstack skills and the old 12 SE skills were still installed globally. The second (9
  dropped) was one of three sessions with the 44 skills installed both as project skills and
  globally; the other two did not report it. With one global install, no session reported it. The
  family's 44 descriptions total about 16,300 characters, and this machine exposes about 120 other
  skills to Codex, so a crowded host can still cross the limit, and Codex then selects without any
  descriptions. Install the family once, and only the groups a project needs.

## Not done

- The remaining 11 prompts on Codex, after its usage limit resets (2026-11-25, 23:28 SGT).
- Repeated trials per prompt, to measure a selection rate rather than one route per prompt.
- Without the project instruction, the open Claude Code misses remain: par-1, ver-3, wri-2 and
  des-1, and how-2's variation between runs.
