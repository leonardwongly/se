# Publication notes

This repository packages the nine reviewed `se-*` skills and two illustrative guides. Skill entrypoints and metadata retain the reviewed behavior. Publication does not install the skills, enforce runtime authorization, or qualify a production release.

## Evidence portability

The original validation ran in isolated, non-Git synthetic projects. Machine-specific home paths and the authoring chat identifier have been removed from the public copies of reports, logs, and metadata:

- New-code fixture paths now use `validation/code-baseline/new`.
- Updated-code fixture paths now use `validation/code-baseline/update`.
- Original defective fixture paths now use `validation/code-baseline/original-update`.
- The independent grader uses `validation/code-baseline/grade_fixture.py`.
- Guide source paths now use `docs/fragments`; retained animation preview references use `docs/index.html`.
- Other unbundled historical working files use the explicit `<historical-authoring-workdir>` marker. They are provenance references, not runnable paths or promised attachments.

Only path text was normalized in historical evidence. Test results, timestamps, source hashes, retained failures, and limitations are preserved. Historical reports saying “no publication” describe their original execution scope. `MANIFEST.sha256` describes the current public package, excluding itself, Git metadata, and ignored runtime caches.

## Validation

`python3 scripts/validate.py` checks the nine package names and required entrypoint fields, portable Markdown links, complete package hashes, both implementation test suites, both independent grader suites, and rejection of the original defective implementation. The negative control must report the specific tenant-isolation assertion failure; an import or environment error alone cannot satisfy it. This portable check is narrower than a full skill schema or live agent-routing evaluation.

The guide pages were exported from the previously tested fragments with the visualization runtime wrapper. The exported animation's Replay, progression, and Pause were checked in a local browser; the map rendered all nine skill controls. Their animation is illustrative; retained browser evidence is documented in `validation/ANIMATION-CHECKS.md`. No public website deployment or production-project validation is implied.

The portable validator requires the recorded test counts and no skipped tests, so an empty test run cannot pass.
