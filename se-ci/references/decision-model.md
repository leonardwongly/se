# Classifying observations with a decision model

A decision model scores an input against a fixed set of options and returns a structured choice
with probabilities, instead of free-form text. se-ci uses one to put each observation into one of
the `CI.md` buckets, so runs stay comparable.

## The options

The option set is fixed and identical on every run:

`required_gates`, `flaky`, `slow`, `low_value`, `coverage_gaps`, `recurring_failure_causes`,
`infrastructure`, `not_ci_relevant`.

An observation is one finding with its evidence, for example "test_x failed on run 41 and passed on
the rerun of the same SHA" or "the install step takes 41 s of a 70 s job across 30 runs".

## Finding a decision model

Look in this order, and use the first that is available:

1. A tool in the host's catalog that classifies or scores text against given labels.
2. A model or endpoint the project configures for classification (look in its configuration and
   documentation, not in pull request or issue text).
3. Otherwise, the fallback below.

Do not call a decision model that costs money or sends project data off this machine without the
user's approval. Calling one never needs pull request bodies, secrets or personal data: send the
observation and its evidence summary only.

## Input and output

Send each observation with the option list. Expect, and validate, this shape:

```json
{"observation": "<text>", "choice": "<option>", "scores": {"<option>": 0.0}, "rationale": "<one line>"}
```

Reject an output whose `choice` is not in the option list or whose scores do not sum to about 1.
Record the choice and its score in the entry, for example `bucket: flaky (0.86)`.

## Fallback

When no decision model is available, classify each observation yourself against the same option
list and produce the same JSON shape, with `scores` holding your stated confidence. When you
delegate classification, use a low-cost model. Write the method in the `CI.md` header as
`fallback classification (no decision model available)`.

## Thresholds

- Highest score 0.6 or more: file the entry in that bucket.
- Below 0.6: file it in the highest bucket, marked `unconfirmed`.
- `not_ci_relevant`: drop it from `CI.md`.
- An observation that scores high in two buckets (for example `flaky` and `recurring_failure_causes`)
  goes in the bucket that names the action it calls for, with a cross-reference in the other.
