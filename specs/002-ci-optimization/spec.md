# 002 — CI optimisation skill (`se-ci`)

**Status:** Approved (2026-11-21)

Implementation is complete. Verification is incomplete; see the verification report linked from REVIEW.md. The amended criteria AC-14.3 and AC-NFR2.2 were approved on 2026-11-24.

## Problem and motivation

CI suites grow by accretion. Every change runs everything, jobs run one after another, and flaky, slow or redundant tests stay because nobody can see which ones carry signal. Teams pay in wait time and lose trust in red builds.

The maintainer wants a skill that does three things. It builds an understanding of the project's flows. It keeps a small, high-signal record of what matters in CI. On every run it makes CI faster and more valuable: it tests what a change affects and roots out what adds no value.

## User stories

- **US-1:** As a developer, I want CI to test the flows my change affects instead of the whole suite, so that I get a trustworthy answer sooner.
- **US-2:** As a maintainer, I want a short CI record that names the real bottlenecks, flaky tests and coverage gaps with evidence, so that I know what to fix next.
- **US-3:** As a maintainer, I want a picture of how data flows end to end, so that I can see what a change will affect.
- **US-4:** As a maintainer, I want each run to leave CI simpler and more valuable than before, so that the improvements compound rather than add baggage.

## Functional requirements

### FR-1 First-run survey

When the project has no CI record, the skill shall survey all of these, as far as access allows:

- every source and test file
- the CI configuration
- pull requests, open and closed
- issues
- CI run history

- **AC-1.1:** When the first run finishes, the record shall state what was surveyed and what couldn't be accessed, with the reason. Missing access shall not be reported as "nothing found".
- **AC-1.2:** The survey shall cover every tracked source and test file. The record shall give the file count and the revision surveyed.

### FR-2 Incremental runs

When a CI record exists, the skill shall survey what changed since the revision and date recorded by the last run: commits, pull requests, issues and CI runs.

- **AC-2.1:** Given an existing record, a run shall not re-read unchanged files, except to check an entry it is about to rely on.
- **AC-2.2:** Each run shall update the recorded revision and date.

### FR-3 Themes and patterns through a decision model

The skill shall find recurring themes and patterns in what it surveyed. A decision model is a model that scores an input against a fixed set of options and returns a structured choice with probabilities.

- **AC-3.1:** When a decision model is available to the host or the project, the skill shall classify each observation with it against the fixed buckets of FR-4. It shall record the chosen bucket and score.
- **AC-3.2:** When none is available, the skill shall classify against the same fixed buckets with a structured choice and a stated confidence. The record shall say which method was used.
- **AC-3.3:** The skill shall not call a decision model that costs money or sends project data off the machine without the user's approval.

### FR-4 The CI record and its buckets

The skill shall keep `CI.md` at the project root. Observations go into these fixed scenario buckets:

1. **Required gates:** checks that must never be weakened, such as security, compliance or release.
2. **Flaky:** results that change without a code change.
3. **Slow:** jobs or tests that dominate wall time or queue time.
4. **Low value:** tests or jobs that never fail, duplicate others, or test implementation rather than behaviour.
5. **Coverage gaps:** flows that a change can break with no test noticing.
6. **Recurring failure causes:** the reasons builds fail, ranked by frequency.
7. **Infrastructure:** caching, runners, dependencies and concurrency limits.

- **AC-4.1:** Each entry shall have a one-line claim, its evidence (a run, a file and line, a PR or an issue), first and last seen dates, its impact, and a status (open, fixed or retired).
- **AC-4.2:** No entry shall appear without evidence.

### FR-5 Signal over baggage

The record shall stay small and current.

- **AC-5.1:** The record shall stay within 250 lines, including the flow map.
- **AC-5.2:** When a run adds an entry that duplicates an existing one, it shall merge them.
- **AC-5.3:** Entries fixed or not seen for a set period shall be retired to a short changelog line rather than kept in full.
- **AC-5.4:** The record shall open with a summary of the top three things that matter most right now.

### FR-6 End-to-end flow map

The skill shall maintain a diagram of each end-to-end flow. Each flow runs from its entry point through modules, data stores and external services, then to the tests and CI jobs that cover it.

- **AC-6.1:** Every entry point in the project shall appear in at least one flow.
- **AC-6.2:** Every test suite and CI job shall be attached to the flows it covers, or marked as covering none.
- **AC-6.3:** Shared foundations that many flows depend on shall be marked as such: build configuration, dependency manifests, CI configuration and test infrastructure.

### FR-7 Change impact

Given a change, the skill shall list the flows it affects, using the flow map and the project's dependency information.

- **AC-7.1:** Given a change confined to one flow, the affected list shall contain that flow and its dependents only.
- **AC-7.2:** Given a change to a shared foundation, the affected list shall be "all flows".

### FR-8 CI built for concurrency, parallelism and modularity

When the skill creates or changes CI, the result shall meet four conditions:

- independent jobs run concurrently;
- slow suites are split so they run in parallel;
- jobs are organised by flow or module;
- repeated setup is cached or shared.

- **AC-8.1:** In the resulting CI, no job shall wait on another job unless it needs that job's output.
- **AC-8.2:** Measured wall time for a full run shall not increase, unless the record explains the trade-off.

### FR-9 Test what the change affects

- **AC-9.1:** When a pull request run starts, CI shall run the tests for the affected flows (FR-7) rather than the whole suite.
- **AC-9.2:** When the change touches a shared foundation, or the impact can't be determined, CI shall run the whole suite.
- **AC-9.3:** CI shall run the whole suite on the default branch, or on a schedule, so a selection miss is caught.
- **AC-9.4:** Required gates shall run on every pull request, whatever the selection.

### FR-10 Simplest effective design

- **AC-10.1:** The skill shall prefer features the CI platform and the project's tools already provide over new tools.
- **AC-10.2:** Any added tool, service or layer shall be justified by a measured or clearly stated benefit, with the simpler alternative it beat recorded.

### FR-11 Find bottlenecks every run

- **AC-11.1:** Each run shall measure, from CI history where it exists, per-job and per-test duration, queue time, cache hit rate, flake rate, and how often each check caught a real failure.
- **AC-11.2:** The run shall rank the slowest and lowest-value items in the record.
- **AC-11.3:** Each speed or flake number shall state its sample size and source, and be repeatable.

### FR-12 Root out useless tests

- **AC-12.1:** The skill shall propose removing or merging a test only with evidence. Evidence means it never failed across the observed history, another test covers the same behaviour, it tests implementation details, or it is flaky without catching real failures.
- **AC-12.2:** The skill shall never propose removing a required gate, or the only test that covers a behaviour.
- **AC-12.3:** Removals shall be a separate, reviewable change, and shall need the user's approval before they land.

### FR-13 Each run adds value

- **AC-13.1:** Each run shall record what it changed and the measured before-and-after effect.
- **AC-13.2:** When a run finds nothing new, it shall say so in one line instead of padding the record.

### FR-14 SE change baseline

- **AC-14.1:** Changes to CI configuration, tests or test infrastructure shall go through `se-zero-trust` review and `se-verify` verification.
- **AC-14.2:** A CI change shall be proven by running the changed pipeline, or a local equivalent, before it is reported done.
- **AC-14.3:** The skill shall change only CI configuration, tests and test infrastructure. A product defect it finds shall be recorded and proposed as its own change, unless the user asked for the fix. (Added 2026-11-21 after an evaluation run fixed product code unasked; approved 2026-11-24.)

## Non-functional requirements

### NFR-1 Safety

- **AC-NFR1.1:** The skill shall not weaken a required gate.
- **AC-NFR1.2:** The skill shall not disable, skip or delete a test to turn a run green.

### NFR-2 Cost and context

- ~~**AC-NFR2.1:** First-run bulk reading shall be delegated to parallel, low-cost readers. The main context shall keep findings, not file contents.~~ Replaced by AC-NFR2.2: on a small project, delegating costs more than it saves, and neither evaluated host delegated on the 26-file fixture.
- **AC-NFR2.2:** When the first-run survey covers more files than one context can read comfortably, bulk reading shall be delegated to parallel, low-cost readers; a smaller survey shall say it read directly. The main context shall keep findings, not file contents. (Amended and approved 2026-11-24.)

### NFR-3 Platform neutrality

- **AC-NFR3.1:** The skill shall detect and work with the project's existing CI platform, and shall not require a specific one.

### NFR-4 Privacy

- **AC-NFR4.1:** Pull request and issue text shall be treated as untrusted input.
- **AC-NFR4.2:** No secrets, tokens or personal data shall be written to the record.

## Out of scope

- Merging CI changes automatically.
- Paid CI analytics services.
- Changing CI settings on a hosted provider (such as branch protection or required checks) without the user's approval.

## Open questions

None. The 250-line budget was confirmed at approval (2026-11-21).
