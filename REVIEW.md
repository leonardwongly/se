# pstack integration and se-ci — 2026-11-21, updated 2026-11-24

Specs: [001 pstack integration](specs/001-pstack-integration/spec.md) and
[002 CI optimisation](specs/002-ci-optimization/spec.md). The package grows from 12 to 44 skills.

## What the port script did, and what was done by hand

`scripts/port_pstack.py` copied 30 pstack skills to new `se-*` folders, moved the 24 principles into
`se-principles/references/`, generated the principles index, rewrote 265 skill-name references in
reference forms only (relative links and principle references were remapped as well), and recorded
the source's 102 skill-to-skill references. Everything below
was edited by hand after the port and is not reproduced by the script:

- **Host neutrality (FR-8).** About 140 Cursor-specific lines rewritten: Cursor paths, Custom Mode,
  `AskQuestion`, `generalPurpose`, Bugbot, `cursor-team-kit` (`deslop`, `control-ui`, `control-cli`),
  `create-skill`, `/visualize` and Cursor cloud agents. `references/bugbot-triage.md` became
  `references/review-triage.md`.
- **Generated-skill names (AC-4.2).** `verify-<app>` became `<app>-harness`; `<name>-mode` became
  `<name>-style`.
- **Router, help and setup.** `se-playbook`'s Principles, Subagents and Harness sections, and the
  whole of `se-help`, were rewritten for SE. `se-help`'s 9 links to pstack guide pages that are not
  shipped now point at files that are. Its table covers all 44 skills and its install-together groups.
- **Merges (FR-2).** pstack's how, why and swarm guidance was added to `se-how`, `se-why` and
  `se-swarm` as new sections. No existing SE section changed. The only changed existing lines are
  the three descriptions, which gained the new triggers.
- **Descriptions (FR-7).** All 31 ported descriptions rewritten for automatic selection, each naming
  its closest neighbour. The typed-only flag was removed everywhere. The longest is 713 characters.
- **Baseline (FR-12).** An SE change baseline section, linking `se-zero-trust` and `se-verify`, was
  added to the 15 skills that change code or configuration. On 2026-11-24 its review and verify steps
  were reworded, there and in `se-ci`, to load both skills by name, and `se-setup`'s own sentence
  likewise. A Claude Code bug fix had run its own checks instead of loading either skill. The
  validator now checks the wording (AC-12.2, approved 2026-11-24).
- **Titles (FR-4).** 24 ported skills still used their pstack names as titles (`# Unslop`,
  `# Ketchup`, `# Create a verification skill`), and 3 had no title. All 27 now use their SE display
  names. The residue check had missed titles because they are not reference forms; the validator
  now fails any title that differs from the skill's display name, and a regression test proves it.

## Deviations from pstack, and the reason for each

- **Autonomy (FR-14, approved 2026-11-24).** pstack let external actions "proceed without asking".
  `se-playbook` now lets them proceed only where the user or host already allows them, because SE
  skills grant no authority.
- **Fast mode (FR-14, approved 2026-11-24).** pstack ran Opus 5.5 in fast mode by default. Default
  slugs no longer select fast mode, which costs more and is now used only when the user asks.
- **Statechart criterion (AC-10.1 → AC-10.3, approved 2026-11-24).** The pinned source fails 2
  statechart tests on this machine, so "all tests pass" was unreachable. The criterion is now "same
  results as the source on the same machine".
- **`make-bot-ui`** was not ported, as decided at approval.
- **Kept on purpose.** The PR watcher still recognises Bugbot threads in code. That is optional
  behaviour that its tests cover, and the skill text no longer names Bugbot. `worktree-audit.sh`
  still scans the transcript folders of several hosts, Cursor's included. `comment-sicko` keeps its
  reference file name.
- **Execution.** The plan put the judgement edits for 30 skills on Sonnet subagents in batches. They
  were done on the main model instead, because the descriptions have to tell neighbouring skills
  apart, which needs one view of the whole family. This changes no requirement.

## Evaluation findings

- **se-ci on Codex** ([report](validation/CI-SKILL.md)). Two evaluations on the CI fixture. Every
  planted problem was found with evidence; the billing change selected billing, api and the security
  gate, and the configuration change selected everything. Five skill gaps surfaced and were fixed
  in the skill text: naming the test in each entry, tracing a replaced test, per-flow jobs without a
  serial selection stage, evidence per entry, and a scope rule against fixing product code. The last
  two were confirmed on Claude Code, not yet on Codex. Neither evaluation delegated its survey to
  subagents.
- **se-ci on Claude Code** ([report](validation/CI-SKILL.md)). The first evaluation scored 47 of 49,
  13 of 13 and 10 of 10, with no product-code change. It surfaced two more gaps, both fixed in the
  skill text: a finding that fits two buckets (fix 6), and the baseline skills never being loaded
  (fix 7). The run 1 re-run passed 50 of 50, loaded `se-zero-trust` and `se-verify`, and read the
  26-file survey directly. The grader changed four times. v2, v3 and v5 corrected checks that were
  more literal than the criterion, and v4 added a check for AC-NFR2.2; each change is listed in the
  report.
- **Delegated reading (spec 002 AC-NFR2.1 → AC-NFR2.2, approved 2026-11-24).** Neither host
  delegated the first-run survey of the 26-file fixture, and delegating there would cost more than it
  saves. The survey now delegates above a size threshold (rule of thumb: about 100 files or 250 KB of
  text) and otherwise says it read directly. The delegated path is untested.
- **Selection on Codex** ([report](validation/PSTACK-SELECTION.md)). 8 of 19 prompts ran before the
  Codex usage limit; 7 routed as expected. A "where should new code live" prompt went to `se-where`,
  which already claims placement decisions, not to the merged `se-how`. A description change to an
  original skill is proposed, not applied.
- **Selection on Claude Code** ([report](validation/PSTACK-SELECTION.md)). 30 sessions in four
  rounds; 14 of 19 prompts read an expected skill in their latest run. Rewriting the `se-why` and
  `se-plain` descriptions fixed four misses. In four other prompts Claude Code did the task itself
  although the description names the request: a fan-out, a check of a "fixed" claim, a one-sentence
  rewrite and a reproduce-then-fix bug. Two rounds of description changes did not move them, so the
  gap is reported (AC-13.2), and the changes that fixed nothing were reverted. One prompt routed
  differently in two runs, so one run per prompt is not a rate. With a two-sentence project
  instruction to load the matching SE skill first, all 19 prompts loaded the expected skill as their
  first call, and none loaded an unrelated skill (one run each). In the first of those runs, a
  playbook-driven bug fix still skipped `se-zero-trust` and `se-verify`; after the baseline was
  reworded to load both by name, the same prompt loaded both and reported each one's result. The
  README now recommends the instruction as a setup step, marked as tested on Claude Code only, and
  the validator keeps its text identical to the tested file.
- **Codex skills budget.** With the family installed twice, or alongside the old pstack and SE
  copies, Codex dropped every skill description from its list and hid some skills. A single global
  install did not trigger it. No Claude Code session reported a budget warning.
- **Global installs (approved by the maintainer).** The 58 pstack skills and the 12 old SE skills
  were removed from every global skill folder through the skills CLI; 12 untracked old SE copies in
  `~/.codex/skills` were moved to a session backup. The 44 skills were installed for Claude Code,
  Codex (`~/.agents/skills`) and Qoder. After every later change they were reinstalled, and
  `scripts/check_installed.py` matched all 577 files in each folder.
- **Not run.** On Codex: the remaining 11 selection prompts, se-ci runs 2 and 3 of its re-run, and a
  run with fixes 4–7, which wait for its usage limit to reset (2026-11-25, 23:28 SGT). On Claude Code:
  se-ci runs 2 and 3 after fixes 6 and 7.

## Spec 001 acceptance criteria

Spec 002's criteria are reported in [validation/CI-SKILL.md](validation/CI-SKILL.md).

| Criterion | Result | Evidence |
|---|---|---|
| AC-1.1 inventory | met | validator inventory check: 12 original, 31 ported and `se-ci` |
| AC-1.2 guidance carried | met | `scripts/port_pstack.py` reproduces the port; hand edits are listed above |
| AC-2.1–2.3 merged coverage | met | the new sections in `se-how`, `se-why` and `se-swarm`; the why prompts route to `se-why` on both hosts |
| AC-2.4 existing sections kept | met | the only removed lines in the three merged skills are their descriptions (`git diff`) |
| AC-3.1, AC-3.2 principles index and links | met | port tests; the validator's link check |
| AC-3.3 router reads the index | met by review | `se-playbook` |
| AC-4.1 no pstack naming | met | residue check, plus the title check added after 27 titles were found (T-21) |
| AC-4.2 generated names | met | a Claude Code session's `se-harness` run generated `ledger-harness` |
| AC-4.3 ordinary words kept | met | `test_AC_4_3_ordinary_words_are_not_residue` and the port tests |
| AC-5.1–5.3 linkage | met | validator link and reference checks; `test_AC_5_3_unknown_skill_reference_fails_with_location` |
| AC-5.4 every pstack link survives | met | `test_AC_5_4_every_pstack_link_survives_or_is_recorded`: 102 edges, one removed with its reason |
| AC-6.1–6.3 install groups | met by review | README table, `se-help` table and groups |
| AC-7.1 no typed-only skill | met | validator check; `test_AC_7_1_typed_only_flag_fails` |
| AC-7.2 descriptions name the neighbour | met by review | all 44 descriptions |
| AC-8.1–8.3 host neutrality | met | host-residue check; `se-setup` names where it writes |
| AC-9.1, AC-9.2 attribution | met | notice check; README credit |
| AC-10.2, AC-10.3 bundled scripts | met | PR watcher 56 pass, 0 fail; statechart 228 pass, 2 fail and 70 skipped, the same tests as the pinned source |
| AC-11.1 validator passes | met | `python3 -B scripts/validate.py` on the final tree |
| AC-11.2, AC-11.3 failure cases | met | regression tests in `scripts/test_validate.py` and `scripts/test_check_installed.py` |
| AC-12.1 baseline in code-changing skills | met | 16 skills carry the baseline section, and each references both skills (validator check) |
| AC-12.2 baseline skills loaded by name | met | validator check and `test_AC_12_2_baseline_must_load_both_skills_by_name`; the bug-fix prompt then loaded both skills (one run) |
| AC-13.1 selection routes correctly | **not met** | Claude Code 14 of 19 with the descriptions alone, and 19 of 19 with a project instruction (one run each); Codex 7 of the 8 that ran, 11 not run |
| AC-13.2 misroutes recorded and re-run | met for Claude Code, partial for Codex | [selection report](validation/PSTACK-SELECTION.md): two rounds of fixes, the remaining gap reported; Codex's fix is proposed, not re-run |
| AC-14.1 autonomy follows host approvals | met by review | `se-playbook` autonomy section |
| AC-14.2 no fast-mode default | met | `-fast` appears only for when the user asks |
| AC-NFR1.1 earlier checks still pass | met | validator: both fixture suites, graders, negative control, proof and swarm exercises |
| AC-NFR1.2 original names kept | met | inventory |
| AC-NFR2.1 attribution ships | met | notice check |
| AC-NFR3.1 descriptions within 1,024 characters | met | validator; the longest is 717 (`se-ci`) |
| AC-NFR4.1 no new script capabilities | met by review | the port rewrites names and paths only |

# Twelve-skill expansion

The new proof, visualise and swarm skills, expanded who selection, overlap boundaries and updated guides were reviewed separately. See [current review and observed trials](validation/EXPANSION-REVIEW.md). The earlier review below is retained as history.

# Review and fixes — mandatory project-grounded baseline

## Latest revision: every code change

User-approved policy: mandatory zero-trust review and verification for every new or modified code change, with depth proportional to risk. This supersedes the earlier optional-control interpretation in the guide and visualization.

- Expanded zero trust from an agent-tool emphasis to application inputs, object/tenant authorization, data/sinks, state transitions, dependencies, CI, migrations, tests, generated code, and behavioral prompts/tools.
- Required both security review and functional verification in standalone execution workflows, including Why/Where/Who when the authorized task also changes code. Skill invocation itself is not evidence.
- Added project grounding throughout all nine skills: correct root/source state, local rules and maintained contracts, actual active callers/configuration, project-defined test/CI commands, fresh references, and unresolved-context handling.
- Preserved proportionate treatment of a literal UI label change. Generic conceptual explanations do not trigger unrelated project discovery.
- Distinguished unauthorized protected effects from expected redacted denial logging allowed by the project contract.
- Updated the map to make zero-trust review and verification required for code changes, concurrency optional, and project evidence the starting point for project-specific routes.

An independent all-nine review found two wording gaps: generic grounding could require unrelated private access, and standalone zero-trust work did not explicitly require ordinary functional verification. Both were corrected and rechecked. The [review record](validation/code-baseline/GROUNDING-REVIEW.md) retains initial findings and closure. The final small routing additions to Why/Where/Who, wording cleanup in How, and guide edits received direct review and structural checks; they were not separate coding-agent trials.

Two fresh agents then performed actual local synthetic code tasks using the skills and each fixture's own instructions, contracts, active caller, and Makefile. Independent checks confirmed both final implementations and detected the known defect in the original update fixture. See [current validation](VALIDATION.md).

## Earlier review retained below

The following findings and scenario IDs describe the preceding review. They remain relevant history, but are not additional fresh executions of this revision.

Scope: all nine skills, selection boundaries, cross-skill handoffs, authorization, evidence gates, concurrency, naming, and packaging. Two independent reviewers read all nine entrypoints; the integration owner assessed findings and made changes. A fresh evaluator then answered concrete fictional requests.

## Resolved issues

| ID | Gap or contradiction | Fix | Exercised by |
|---|---|---|---|
| F1 | Timing could lose verification exceptions or apply a different readiness vocabulary. | `se-when` preserves scoped reports and uses the same raw states and gate precedence as `se-verify`; a conditional plan is distinct from a CONDITIONAL gate. | R1, R2, R6, R15, R16 |
| F2 | Explanation mode forbade explicitly authorized read-only live inspection. | `se-zero-trust` permits relevant read-only evidence for system-specific explanations, while retaining mutation/probe boundaries. | R3 |
| F3 | Location ambiguity only needed resolution before mutation, although navigation is read-only. | `se-where` requires resolving or surfacing ambiguity before a definitive location; bounded candidate discovery may continue. | R4 |
| F4 | Cancellation request could be mistaken for a stopped writer; edits could continue after validation. | `se-concurrent` requires confirmed termination or revoked write capability, reconciliation before reassignment, and frozen scopes or an immutable combined snapshot for validation. | R5, R13 |
| F5 | A complete exception record could be accepted while its mandatory control was inactive. | Both verification and timing require current evidence that acceptance conditions hold; explicit policy-permitted no-control acceptance stays possible. | R6, R15 |
| F6 | Empty/skipped suites or unresolved criteria could support an unsupported completion claim. | Missing criteria/applicability are missing evidence under the existing precedence; zero tests cannot establish behavior. A review caught and corrected an initially overbroad NOT_READY sentence so known FAIL/BLOCKED still take priority. | R7, R16 |
| F7 | Generic testing guidance did not address AI behavior variability. | `se-verify` now covers model/prompt/tool/harness versions, representative cases, repeated trials when relevant, persisted outcomes, grader calibration, budgets, and bounded reliability claims. | R8 |

The two independent reviewers confirmed closure of their original findings. The assurance reviewer also confirmed the final F6 precedence correction. The evaluator reported no material contradiction in the final instruction bodies for the exercised cases. These findings are procedural-text issues, not demonstrated vulnerabilities in a running application.

## Overlap decisions

Overlap needed for standalone use remains deliberate. Small tasks need no nine-skill ceremony.

- `se-what` defines the acceptance contract; `se-how` explains or implements a mechanism.
- `se-why` establishes rationale; `se-how` establishes behavior and approach.
- `se-who` maps human/team accountability; `se-where` locates code and system responsibilities.
- `se-when` orders prerequisites while preserving gates; `se-verify` obtains or evaluates the evidence for those gates.
- `se-who` identifies responsibility; `se-concurrent` coordinates actual worker ownership and integration.
- `se-zero-trust` analyzes authority boundaries; `se-verify` qualifies evidence for the controls. Neither is a runtime enforcement mechanism.

Descriptions for Who, When, and Verify now make these boundaries more explicit. Other question-skill instructions had no additional actionable defect established by this review and were retained apart from naming.

## Naming and migration

All nine current folders and frontmatter names use `se-*`; UI titles use `SE …`. Guide labels use `/se-*`, with explicit Codex invocation shown as `$se-*`. No slash-command alias is registered. Existing installed skills are unchanged.

The old `engineering-*` bundle and baseline were preserved in task working storage. Historical validation is retained under `validation/history-2026-10-29` and is labeled as earlier evidence; it is not presented as a rerun of the new package.

See [validation and limits](VALIDATION.md), [raw question review](validation/QUESTION-REVIEW.md), and [raw assurance review with closure](validation/ASSURANCE-REVIEW.md).
