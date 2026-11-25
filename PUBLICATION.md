# Publication notes

This repository packages 44 `se-*` skills (twelve core skills, thirty-one adapted from pstack, and `se-ci`) and two illustrative guides. The original nine-skill evidence remains historical; the proof, visualise, swarm and specialist-selection update has its own [review record](validation/EXPANSION-REVIEW.md). Publication does not install the skills, enforce runtime authorization, or qualify a production release.

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

`python3 scripts/validate.py` checks the 44 package names and required entrypoint fields (including description length and that no skill is typed-only), portable Markdown links, references between skills, the absence of pstack naming and Cursor-only features inside skill folders, the pstack attribution notice, complete package hashes, both implementation test suites, both independent grader suites, and rejection of the original defective implementation. The negative control must report the specific tenant-isolation assertion failure; an import or environment error alone cannot satisfy it. This portable check is narrower than a full skill schema or live agent-routing evaluation.

The current guide uses a custom standalone interface with local CSS and JavaScript. README PNG/GIF previews are captured from that interface. Original inline fragments remain historical sources; their older export and browser records do not establish the current UI's behavior. See [custom guide validation](validation/CUSTOM-GUIDE.md) for the current checks and media provenance. All animations are illustrative. No public website deployment or production-project validation is implied.

The portable validator requires the recorded test counts and no skipped tests, so an empty test run cannot pass.

The same command checks local `src` and `href` references in `docs/index.html` and
`docs/skill-map.html`. Paths are relative to the HTML
file, with query/fragment components removed before percent decoding. Resolved
targets must stay inside the repository and exist. URLs with a scheme or network
host, and references with no path (including fragment-only links), need no local
target; the check makes no network requests. This is a static reference check, not
browser validation: it does not check fragment IDs, CSS URLs, `srcset`, meta
refresh, or JavaScript-generated references. A `<base>` element with any `href`
attribute is rejected with its entry point and line number, including external,
empty, and valueless attributes: browser base-URL resolution is not modeled.
A `<base target="...">` without `href` is allowed.

Run the HTML reference regressions with
`python3 -B -m unittest discover -s scripts -p test_validate.py -v`. This separate
suite creates temporary symlinks to exercise escape rejection; the portable
validator itself does not need permission to create symlinks.

## Installed-file comparison

`python3 -B scripts/check_installed.py --skills-dir /path/to/installed/skills`
compares every file of each of the 44 repository packages (entry files, playbooks,
references and bundled scripts) against that explicitly selected directory. Comparison is
byte-for-byte, including line endings; unrelated installed skills and extra files
are ignored. The command never writes installed files, executes their contents,
or uses the network. It verifies file parity, not host discovery or skill behavior.

JSON output has `status`, `files`, and `errors` fields. File records are sorted by
repository-relative `path`, with a `status` such as `match`, `missing`, `modified`,
or `symlink`. Exit status is 0 for a complete match, 1 for installation differences,
and 2 for unusable arguments, installation root, repository source, or platform.

The installation root itself and expected descendant paths must not be symlinks;
normal aliases in ancestors of the explicitly selected root (such as macOS `/tmp`)
are permitted. Component-by-component descriptor-relative opens with no-follow
flags prevent expected-path symlinks from redirecting reads. Nonregular files are
rejected, and reads are bounded by the corresponding repository file's size plus
one byte. This requires POSIX no-follow and descriptor-relative file operations;
unsupported platforms fail closed. Use a quiescent installation for a coherent
comparison: individual safe reads do not provide an atomic snapshot of the whole tree.

Run its focused regressions with
`python3 -B -m unittest discover -s scripts -p test_check_installed.py -v`.
Run all focused script suites with
`python3 -B -m unittest discover -s scripts -p 'test_*.py' -v`, then run
`python3 -B scripts/validate.py` for package integrity and the bundled synthetic
exercises. These checks use temporary installations and do not validate a real
host installation unless one is explicitly selected in a separate invocation.

## Automatic-selection evidence

The [two-task CLI evaluation](validation/AUTOMATIC-SELECTION.md) is a separate observed trial, not a capability of the portable validator. Its public record includes task prompts, selected command observations, source hashes, an independent checker and original/repaired results. Machine-specific command prefixes and result-source labels are normalized; full private traces and global configuration remain local. Running the portable validator does not rerun agent selection.

## Expanded selection and integration

The [expanded ten-session evaluation](validation/EXPANDED-SELECTION.md) separately records all-twelve role coverage, delegated own-context reads, initial misses and policy repairs. Its prompts and selected observations are portable; full private traces and unrelated global instructions are not distributed. Coverage is not a success-rate estimate.

Markdown targets now use parsed URL fields, split query/fragment components before one strict percent-decode, and enforce resolved repository containment before existence. A URL appearing only in a local target's query no longer skips validation. Link extraction remains the existing bounded regex, not a complete Markdown parser; fragment IDs and remote availability are not checked. Run all focused script regressions with `python3 -B -m unittest discover -s scripts -p 'test_*.py' -v`.

## Second-project final-policy evaluation

The [ProjectPortfolio evaluation](validation/CROSS-PROJECT-SELECTION.md) publishes eight fresh task prompts, policy/skill identities, sanitized instruction-read receipts, independent application grades and deterministic checkers. All tasks use one unchanged final policy; initial project findings and post-trial remediation remain distinct. Raw sessions, unrelated global configuration and private session identifiers stay local.

The maintenance and scanner patches apply only to a disposable ProjectPortfolio checkout at the pinned revision. They were not merged into that project's original checkout or deployed. The HTML explanation is preserved byte-for-byte; its relative source links target its original project location, and hosted playback is unverified. The portable package validator checks the skills package and existing guide entrypoints; it does not execute this external-project evaluation or all exported HTML artifacts.

## pstack port

Thirty-one skills are adapted from pstack (MIT, Lauren Tan) at commit
`c3464c11c60b1352d5e8f5f0428a3a6943837568`; see [third-party notices](THIRD_PARTY_NOTICES.md)
and [spec 001](specs/001-pstack-integration/spec.md). `scripts/port_pstack.py` re-creates the
renamed folders from a checkout of that commit and records the source's skill-to-skill
references in `validation/pstack-port/source-edges.json`. Hand edits made after the port
(host-neutral wording, descriptions, merges, the change baseline) are listed in
[REVIEW.md](REVIEW.md). To sync a later upstream commit, port the old and the new commit
into two scratch directories with `--any-commit`, diff them, and apply that diff here.

`python3 -B -m unittest discover -s scripts -p 'test_*.py' -v` includes the port tests, which
prove that every pstack reference survives in the SE package or is recorded with a reason in
`validation/pstack-port/removed-edges.json`.

The bundled scripts keep their own suites, which `validate.py` does not run because they need
JavaScript runtimes. Copy the scripts folder out of the repository first, so no
`node_modules` lands in the package:

- PR watcher: `bun install --frozen-lockfile && bun test watch-pr` in a copy of
  `se-playbook/scripts`. 56 tests pass, as on the pinned source.
- Statechart pipeline: `npm install && npm test` in a copy of `se-states/scripts`. On the
  reference machine the pinned source and the port give the same 300 results: 228 pass, 70
  are skipped because `TLA2TOOLS` does not point at `tla2tools.jar`, and the same 2 fail before
  and after the port (a symlinked-launcher test and `render.test.ts`). The 2 failures depend on
  the environment and are not caused by the port.

