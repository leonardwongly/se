# Publication notes

This repository packages twelve `se-*` skills and two illustrative guides. The original nine-skill evidence remains historical; the proof, visualise, swarm and specialist-selection update has its own [review record](validation/EXPANSION-REVIEW.md). Publication does not install the skills, enforce runtime authorization, or qualify a production release.

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

`python3 scripts/validate.py` checks the twelve package names and required entrypoint fields, portable Markdown links, complete package hashes, both implementation test suites, both independent grader suites, and rejection of the original defective implementation. The negative control must report the specific tenant-isolation assertion failure; an import or environment error alone cannot satisfy it. This portable check is narrower than a full skill schema or live agent-routing evaluation.

The current guide uses a custom standalone interface with local CSS and JavaScript. README PNG/GIF previews are captured from that interface. Original inline fragments remain historical sources; their older export and browser records do not establish the current UI's behavior. See [custom guide validation](validation/CUSTOM-GUIDE.md) for the current checks and media provenance. All animations are illustrative. No public website deployment or production-project validation is implied.

The portable validator requires the recorded test counts and no skipped tests, so an empty test run cannot pass.

The same command checks local `src` and `href` references in `docs/index.html` and
`docs/skill-map.html`. Paths are relative to the HTML
file, with query/fragment components removed before percent decoding. Resolved
targets must stay inside the repository and exist. URLs with a scheme or network
host, and references with no path (including fragment-only links), need no local
target; the check makes no network requests. This is a static reference check, not
browser validation: it does not check fragment IDs, CSS URLs, `srcset`, meta
refresh, JavaScript-generated references, or `<base>` URL behavior.

Run the HTML reference regressions with
`python3 -B -m unittest discover -s scripts -p test_validate.py -v`. This separate
suite creates temporary symlinks to exercise escape rejection; the portable
validator itself does not need permission to create symlinks.

## Automatic-selection evidence

The [two-task CLI evaluation](validation/AUTOMATIC-SELECTION.md) is a separate observed trial, not a capability of the portable validator. Its public record includes task prompts, selected command observations, source hashes, an independent checker and original/repaired results. Machine-specific command prefixes and result-source labels are normalized; full private traces and global configuration remain local. Running the portable validator does not rerun agent selection.
