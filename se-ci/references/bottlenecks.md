# Finding bottlenecks and low-value checks

Each run measures, ranks and records. Numbers come from CI history where it exists; a local run is
a fallback and is labelled as such.

## Where to read

| Need | GitHub Actions | Other sources |
|---|---|---|
| Runs, durations, conclusions | `gh run list --json databaseId,headSha,conclusion,createdAt,updatedAt,event` | the platform's run API; exported history files |
| Per-job and per-step timing | `gh run view <id> --json jobs` | job logs with timestamps |
| Per-test duration and outcome | JUnit XML artifacts; `pytest --durations=0`; `go test -json`; `jest --json` | test reports |
| Queue time | job `startedAt` minus run `createdAt` | runner logs |
| Cache hits | cache step output (`cache-hit`) | install step duration spread |

## Metrics

- **Duration.** Median and 90th percentile per job, per step and per test, with the sample size.
- **Queue time.** Time waiting for a runner, separate from execution.
- **Cache hit rate.** Hits over restores; a slow install step with no cache step is a miss by
  construction.
- **Flake rate.** A test is flaky when the same SHA both passed and failed it, including reruns.
  Rate = flaky failures over runs of that test.
- **Catch value.** How often a check's failure was a real defect: failures that led to a code fix
  before merge, divided by its runs. A check that never failed in a long history, or only ever
  failed alongside another check on the same cause, adds little signal.

## Ranking

Rank by cost to the people waiting:

1. Wall time on the pull request critical path (median), then queue time.
2. Flake rate × runs per week (reruns and lost trust).
3. Run time spent on checks with near-zero catch value.

Write the top items into the slow, flaky, low value and infrastructure buckets with their numbers.

## Vetting a number

Before you report a speedup or a regression: state the sample size and spread, use the same
runner type before and after, rule out caching or queue effects, and name what limits the number.
**se-benchmark** has the full checklist.
