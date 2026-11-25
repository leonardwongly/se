# Testing only what a change affects

Pull request CI runs the tests of the affected flows instead of the whole suite. Selection is only
safe with its safety net, so set the net up first.

## Safety net (always)

1. A change to a shared foundation runs the whole suite (see flow-map.md for the list).
2. A change whose impact can't be determined runs the whole suite: unmapped paths, generated code,
   dynamic imports, reflection, or a mapping that failed to load.
3. The default branch runs the whole suite on every push, or on a schedule if pushes are too
   frequent. A failure there that the pull request run missed is a selection miss: fix the map and
   record it.
4. Required gates run on every pull request whatever the selection says.

## Pick the simplest mechanism that works

Prefer what the platform and the project's tools already provide:

| Situation | Mechanism |
|---|---|
| Flows live in separate directories | Path rules per job (GitHub Actions: a `changes` job computing paths with `git diff`, then `if:` on flow jobs; GitLab: `rules: changes:`) |
| JavaScript monorepo with a workspace tool | `nx affected`, `turbo run --filter=...[base]`, `jest --findRelatedTests` |
| Python | Path rules from the flow map; `pytest --testmon` when the project already uses pytest |
| Go | `go list -deps` against the changed packages |
| Bazel | `bazel query 'rdeps(//..., set(<changed>))'` |

A small checked-in script that maps changed paths to flows with the flow map's affected-by table
is a fine `changes` step: it runs the same locally and in CI, so it can be tested. Add a
third-party action only when it beats that on a stated benefit, pin it to a commit SHA, and record
the simpler alternative it beat.

**GitHub Actions caution.** A workflow skipped by a workflow-level `paths:` filter leaves a
*required* status check pending forever. Keep required checks in a workflow that always runs, and
skip work inside it with job-level `if:` conditions; a skipped job reports success.

## Prove the selection

Before calling a selection change done:

1. Dry-run the mapping against at least two sample diffs: one confined to a single flow and one to
   a shared foundation. The first must select that flow and its dependents only; the second must
   select everything.
2. Run the selected tests locally and confirm they pass on the current revision.
3. Lint the pipeline with the platform's linter when available.
4. Record the expected selection for each sample diff in `CI.md`'s changelog line.

## Common misses

- Tests that import a fixture or helper from another flow: the helper is test infrastructure, so a
  shared foundation.
- Data files, migrations and schemas read at runtime: map them to the flows that read them.
- Contract tests between flows: they belong to both flows.
