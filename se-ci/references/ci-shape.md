# CI shape: concurrency, parallelism and modules

Shape the pipeline so the answer arrives sooner without losing signal.

## Rules

- **Concurrency by default.** Independent jobs run at the same time. A job waits on another
  (`needs:` in GitHub Actions and GitLab) only when it consumes that job's output, such as the
  `changes` job's selection or a build artifact.
- **Modules.** One job per flow or module, named after it, running that flow's tests. A failure
  then names the flow that broke.
- **Split the slow.** Shard a suite that dominates wall time (by file or by recorded duration) and
  run the shards in parallel. Shard only when the suite is the bottleneck: each shard repeats
  setup.
- **Share setup.** Cache dependency installs keyed on the lockfile or manifest (GitHub Actions:
  `actions/setup-<lang>` with `cache:`, or `actions/cache`; GitLab: `cache:` keyed on the lockfile).
  Build once and pass artifacts instead of rebuilding in every job.
- **Cancel stale runs.** Cancel in-progress runs for the same branch when a new push arrives
  (GitHub Actions: a `concurrency:` group with `cancel-in-progress: true` for pull requests; never
  cancel default-branch runs mid-flight).
- **Required gates stand alone.** Keep each required gate as its own always-running job, so
  selection and sharding can never skip it.
- **Fail fast, report fully.** Put the fast, high-signal checks first; let flow jobs finish
  independently (`fail-fast: false` in a matrix) so one failure doesn't hide another.

## Selection without a serial planning stage

A separate `changes` job that every flow job `needs` adds a second queue wait before any test
starts. When queue time is a large share of the run (compare it with execution time in the
history), let each flow job decide for itself instead:

```yaml
  flows:
    strategy:
      fail-fast: false
      matrix:
        flow: [billing, api, reports]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - id: select          # writes run=true or run=false; no base (a push) means run=true
        env:
          FLOW: ${{ matrix.flow }}
          BASE: ${{ github.event.pull_request.base.sha }}
        run: python ci/affected.py --flow "$FLOW" --base "${BASE:-}" >> "$GITHUB_OUTPUT"
      - if: steps.select.outputs.run == 'true'
        run: python -m unittest discover -s "tests/${{ matrix.flow }}" -t . -v
```

Each matrix entry is its own concurrently running job, named after its flow, and an unaffected
flow finishes in seconds with success. Pass event values to scripts through `env:`, never by
pasting `${{ }}` expressions into a script body. Keep the separate `changes` job when queue time is small or
when several jobs share one expensive selection step.

## GitHub Actions sketch

```yaml
on:
  pull_request:
  push:
    branches: [main]
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
jobs:
  changes:            # computes affected flows; full run on shared foundations or on main
  security-gate:      # required: always runs, no if:
  billing:
    needs: changes
    if: contains(needs.changes.outputs.flows, 'billing')
```

## Before and after

Measure the full-suite wall time before and after the change on the same runner type, with the
sample size stated. A change that makes the full run slower needs a stated trade-off in `CI.md`
(for example, more parallel jobs cost a little more total compute but return the pull request
answer sooner).
