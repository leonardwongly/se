# CI.md template and rules

`CI.md` lives at the project root. It is the record between runs, so it holds signal, not a
transcript: what matters about this project's CI right now, and the evidence for it.

## Rules

- **Budget.** 250 lines at most, flow map included. When an update would exceed it, merge or
  retire entries before adding.
- **Evidence or nothing.** Every entry cites its own evidence: at least one of a CI run id, a file and
  line, a pull request or issue number, or a measured number with its sample size. A pointer to
  another entry ("same window", "see above") is not evidence. An entry without evidence is not
  written.
- **Name the thing.** Each entry names the test (by its id, such as `test_invoice_total`), job, step
  or file it is about, so the next run can find it and a reader can act on it.
- **One entry per thing.** Before adding, search the buckets for the same test, job or cause and
  update that entry's last-seen date and evidence instead.
- **Trace replacements.** When a run renames or replaces a test, for example to fix a flaky one,
  the entry and the changelog line name both the old and the new test.
- **Retire, don't hoard.** An entry fixed by a change, or not seen in the last 30 days or the last
  three runs, moves to a one-line changelog item and leaves its bucket.
- **Unconfirmed is a label.** A classification below 0.6 confidence keeps its entry but marks it
  `unconfirmed` until a later run confirms or retires it.
- **No secrets.** No tokens, keys, passwords, personal data or raw log dumps.

## Entry format

```
- <one-line claim> — evidence: <run id | path:line | PR #n | issue #n | number (n=…)>;
  first seen <date>; last seen <date>; impact: <what it costs or risks>; status: open|fixed|retired
```

## Skeleton

````markdown
# CI

Revision surveyed: <full or short SHA> on <date> · Run: <n> · Method: <decision model name | fallback classification>

## What matters now

1. <highest-value finding and the action it calls for>
2. <second>
3. <third>

## Survey coverage

- Surveyed: <n> source files, <n> test files, CI configuration (<paths>), <n> pull requests, <n> issues, <n> CI runs.
- Not accessible: <what, and why>, or "none".
- Reading: direct, or delegated to <n> parallel readers (first run only).

## Required gates

## Flaky

## Slow

## Low value

## Coverage gaps

## Recurring failure causes

## Infrastructure

## Flow map

```mermaid
<flow map, see flow-map.md>
```

## Proposals waiting on approval

- <test removal or hosted-setting change, with its evidence and the reviewable change that holds it>

## Changelog

- <date> <revision>: <what changed> — <before → after effect>, or "No new signal."
````

An empty bucket keeps its heading with `- None observed.` so the next run sees it was checked.
