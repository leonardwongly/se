# Automatic skill selection: two observed tasks

**Result: both tasks passed the scoped routing evaluation.** On 5 November 2026
(Asia/Singapore), two fresh Codex CLI agents selected and read relevant installed
skills without skill names in either task prompt. No routing-policy or installed-skill
change was required. The implementation task repaired a real validator gap.

This is an observed smoke evaluation of one configured host, not a success-rate
estimate or a guarantee about future tasks.

## Setup and evidence

Both runs used `codex exec --ephemeral --json`, the existing global `AGENTS.md`, and
the twelve installed skills from baseline commit
`b0033264ab4f84af01ef0ab18a66f690acaa53e9`. The implementation session used a
`workspace-write` sandbox in an isolated clone; the explanation session used a
`read-only` sandbox against the original clean repository. Neither received
follow-up coaching or a list of skills to use in its task prompt.

The global routing instructions intentionally named the skill responsibilities:
proof for substantive claims, zero-trust review and verification for all code
changes, and task-appropriate selection of the remaining skills. Thus this tests
**global routing instructions plus installed-skill selection**, not metadata-only
discovery with those instructions removed.

Harness: Codex CLI 0.166.0 on macOS; configured model `gpt-6-astra`, reasoning effort
`high`, provider `openai`, with no model override. Model identity is from local
configuration, not independently attested server metadata. Python checks used
3.14.5. Global instructions and all twelve installed skill entrypoint hashes
remained unchanged throughout the trials.

| Task | Actual selection | Observed use | Result |
|---|---|---|---|
| Add local HTML reference checking to the portable validator | `se-proof`, `se-zero-trust`, `se-verify` | Successful file-read event `item_4` preceded first edit `item_12`; inspected revision and implementation, reviewed path normalization/containment, added meaningful tests, checked the final diff and package, and demonstrated old failures versus repaired behavior | PASS |
| Explain what a passing portable validator establishes | `se-proof` | Successful file-read event `item_4`; inspected source and maintained documentation, ran package and JavaScript syntax checks, preserved the clean repository, and distinguished retained browser evidence from a new browser run | PASS |

The evaluator inspected completed tool events and resulting artifacts rather than
accepting the agents' declarations alone. Neither worker committed, published,
installed anything, or changed global settings. The parent subsequently integrated
the reviewed fix. Publication of that fix is separate from the trial scope.

Portable evidence:

- Exact [implementation prompt](automatic-selection/code-task.txt) and
  [explanation prompt](automatic-selection/analysis-task.txt), with no skill names.
- [Selected command observations and source hashes](automatic-selection/observations.json).
- Independent [original results](automatic-selection/original-results.json) and
  [repaired results](automatic-selection/repaired-results.json).
- Reusable [independent checker](automatic-selection/check_html_references.py).

Displayed command home prefixes and result-source paths are normalized; this is a
selected evidence record, not a complete public transcript. Raw local traces and
unrelated MCP diagnostics are not distributed. The instruction hashes identify the
tested configuration; the author's complete global instructions are not bundled.

## Validator gap and fix

The original checker hashed HTML files but did not inspect local `src` or `href`
references. A refreshed manifest could pass even with missing files or links
escaping the repository. The fix uses the standard-library HTML parser, removes
query/fragment components before percent decoding, resolves paths, and checks
repository containment before target existence. It covers `docs/index.html` and
`docs/skill-map.html`; the existing integrity and synthetic behavior gates remain.

An independent agent designed the black-box checker before reading the worker's
implementation. It runs the actual validator in temporary copies and independently
regenerates manifests, so a stale hash cannot masquerade as HTML-reference detection.
Outside-repository cases point to existing harmless fixture files. Original and
repaired runs left their source packages unchanged.

| Validation | Original | Repaired |
|---|---|---|
| Independent acceptance checks | 11 passed; 10 failed because broken/escaping references were accepted | 21 passed; zero failed |
| Root-relative URL observation | Recorded separately, not an acceptance gate | Recorded separately, not an acceptance gate |
| Focused HTML regressions | Not present | 9 passed |
| Full package and synthetic checks | Passed despite the HTML gap | Passed with the new check |
| Final diff whitespace check | Not a trial acceptance result | Passed |

Coverage includes both entry points; missing images, scripts and stylesheets;
query/fragment handling; encoded filenames and traversal; existing outside targets;
ignored external/data/fragment references; and retained hash/inventory rejection.
The focused regressions also cover symlink escapes and malformed paths. The
independent guard records and blocks Python network attempts; none were observed.

## Reproduce deterministic checks

From the repository root:

```sh
python3 -B -m unittest discover -s scripts -p test_validate.py -v
python3 -B scripts/validate.py
python3 -B validation/automatic-selection/check_html_references.py .
```

The independent checker creates temporary copies; it does not mutate the supplied
source package. It requires subprocess execution and writable temporary storage.
The focused regression suite also needs permission to create temporary symlinks.

To reproduce the old failure, provide a separate checkout of the baseline commit
to the current checker. Its full acceptance mode should exit 1 with ten failed
cases. `--expect-known-gap` instead exits 0 when the original missing-image defect
is successfully reproduced; that mode is not an acceptance pass for the old code.

These commands rerun deterministic validator checks, **not the live agent trials**.
Repeating the latter requires installed skills, the described routing policy, a
configured Codex account/model, fresh sessions, the saved prompts, and inspection
of actual tool events and results. Outcomes may vary.

## Limitations and recovery

- Two purposively selected tasks do not establish reliability across all twelve
  skills, unrelated projects, models or future tasks. Only three distinct skills
  were observed; selecting all twelve on every task is not the intended behavior.
- The harness was Codex CLI. Desktop-native selection, delegated skill inheritance
  and swarm orchestration were not tested by these two workers.
- The implementation worker recovered from probing a nonexistent CI directory by
  finding the documented project command. Unrelated configured MCP servers logged
  startup warnings; neither task depended on them. They were not counted as
  successful tool use or repaired as part of this bounded task.
- Static HTML checking does not exercise browser behavior, fragment IDs, CSS URLs,
  `srcset`, meta refresh, JavaScript-generated references or `<base>` behavior.
  Root-relative references use filesystem absolute-path semantics, not site-root
  mapping. References with a scheme or network host are not fetched or checked for
  availability or safety.
- The network guard observes Python socket operations, not arbitrary native
  subprocess traffic. Other Python versions, operating systems, hosted CI and
  production environments were not exercised. No deployment or release-readiness
  claim follows from these results.
