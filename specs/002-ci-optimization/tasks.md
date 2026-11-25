# 002 — Tasks

- [x] T-1 Build the fixture project: the three flows and shared config, the serial workflow, the planted problems, the recorded history JSON and the offline `gh` shim. (FR-1, FR-11, FR-12)
- [x] T-2 Write `grade_ci.py` with all checks from the plan's test strategy. Confirm it fails on an empty output directory. (all ACs)
- [x] T-3 [P] Write `references/ci-md-template.md` and `references/decision-model.md`. (FR-3, FR-4, FR-5, AC-3.1–3.3)
- [x] T-4 [P] Write `references/flow-map.md` and `references/affected-tests.md`. (FR-6, FR-7, FR-9)
- [x] T-5 [P] Write `references/ci-shape.md`, `references/bottlenecks.md` and `references/pruning.md`. (FR-8, FR-10, FR-11, FR-12)
- [x] T-6 Write `se-ci/SKILL.md`: the run loop, links with fallbacks, the baseline and the safety rules. Write `agents/openai.yaml`. (FR-1, FR-2, FR-13, FR-14, NFR-1–4)
- [x] T-7 Add `se-ci` to the validator inventory, the README tables and the install group. Regenerate the manifest and run the validator. (spec 001 FR-6, FR-11)
- [ ] T-8 Run evaluation runs 1–3 on Claude Code and Codex. Grade them, fix the skill text and re-run the failures. (all ACs) — partial: Codex ran two evaluations (five gaps fixed); its last re-run waits for its usage limit. Claude Code scored 47/49, 13/13 and 10/10, two more gaps were fixed (fixes 6 and 7), and the run 1 re-run passed 50/50 under grader v5; runs 2 and 3 were not repeated.
- [ ] T-9 Write `validation/CI-SKILL.md` with AC-by-AC results and limits. Set the spec Status to `Implemented`. (all) — report covers both hosts; Status stays Approved until T-8 closes.
- [x] T-10 Apply the AC-NFR2.2 amendment: the size rule in the skill's survey step and the CI.md template, a grader check that the record says how the survey was read, and the reference answer. Run the grader self-test. (AC-NFR2.2)
