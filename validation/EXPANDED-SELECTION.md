# Expanded automatic selection and delegated work

**All twelve skills were observed being selected and applied across the initial
tasks and targeted reruns after routing repairs.** This is coverage of the twelve skill roles in a
bounded smoke evaluation, not a reliability percentage or universal routing claim.

On 5 November 2026 (Asia/Singapore), seven task prompts ran in fresh Codex CLI
sessions against the real repository at baseline
`c939ba3ed42783bf6502d4562c4811e37116d1e7`. Three unchanged prompts were then rerun
after targeted policy repairs: **ten top-level sessions in total**, with **six
actual delegated agents** across the two implementation-team runs and two
specialist-review runs. Each top-level task prompt omitted skill names and invocation
syntax. Expected selections were recorded before the first runs.

## Coverage and observed application

| Skill | Evidence-bearing task | Actual application and limits |
|---|---|---|
| `se-what` | Scope | Inspected installation docs/package layout; produced bounded outcomes, success/failure criteria, non-goals and unresolved partial-installation decisions. No implementation. |
| `se-why` | Rationale | Inspected current validator, tests and commit history; executed parsing examples; distinguished current behavior and recorded rationale from inferred intent. |
| `se-where` | Mechanism rerun | Located the active HTML/script bindings and playback handlers, distinguishing them from historical guide fragments. |
| `se-how` | Mechanism rerun | Traced Pause, Step, Replay, reduced-motion and visibility behavior, including a boundary case; source claims were not presented as a new browser run. |
| `se-when` | Readiness | Ran current portable checks, ordered integration/installation/release prerequisites and evidence invalidation, and kept local acceptance separate from release permission. |
| `se-who` | Expertise and team rerun | Chose actual available reviewers/workers for bounded responsibilities and assessed returned findings. No invented maintainer or authority. |
| `se-proof` | All task families | Inspected current source/evidence, used precise references and qualified claims. Skill reads alone were not accepted as comprehension. |
| `se-zero-trust` | Visual and implementation teams | Reviewed URL/path normalization, no-follow filesystem access, input/output boundaries and denied cases before code work. |
| `se-verify` | Visual and implementation teams | Executed focused and combined checks, retained failures and negative controls, and identified final source state and environment limits. |
| `se-visualise` | Visual | Built the [animated URL walkthrough](../docs/reference-walkthrough.html), verified representative Python cases and actual browser interactions, and supplied reduced-motion/text alternatives. |
| `se-swarm` | Team rerun | Launched two real workers, inspected their outputs, handled findings and integrated the stable result. |
| `se-concurrent` | Both team runs | Assigned disjoint script ownership, retained shared docs/manifest ownership with the parent, confirmed writers finished, then ran combined checks. |

The initial seven runs selected **nine distinct skills**. The mechanism task loaded
only `se-proof`, omitting `se-where` and `se-how`; the team task loaded concurrency
and baseline skills but omitted `se-swarm` and contributor-selection guidance.
The separately scoped expertise task did load `se-who`. These omissions remain
recorded; correct task output did not retroactively establish missing skill reads.

The readiness task selected `se-when` and `se-proof`, not the additional
`se-verify` anticipated by the initial matrix. Its timing skill includes direct
readiness assessment, and it reported the actual executed and unrun checks. The
application passed; this trial is not counted as a `se-verify` selection.

An independent review graded the six non-team task outcomes against their prompts,
source and tool evidence. The team outcomes additionally passed independent
black-box behavior checks. [Application grades](expanded-selection/application-grades.json)
and [selected command observations](expanded-selection/observations.json) separate
selection, instruction delivery and actual task behavior.

## Routing and delegation repairs

The global routing instructions were tightened in two steps:

1. Map each distinct requested engineering decision to its primary skill; proof
   supports that skill rather than substituting for it. Explicit team coordination
   selects swarm, contributor selection selects who, and concurrent work also
   receives ownership/integration guidance. Recover missing sections after a
   truncated skill read.
2. Require delegates to select and read relevant installed instructions in their
   own context before substantive work. An inherited parent read is not counted
   as the child's selection; inaccessible instructions must be reported honestly.

The unchanged mechanism and team prompts selected the previously omitted skills
on fresh reruns. The first read-only reviewer had inspected code but made no skill
read in its own turn. After the own-context repair, the unchanged expertise prompt
launched a new reviewer whose own first tool call delivered the complete
`se-proof` file before source analysis. The parent then independently checked its
findings. This is an observed repair on reused prompts, **not an independent
holdout evaluation. Unaffected tasks were not all repeated under the final policy;
coverage aggregates initial runs and targeted remediation reruns**.

The [portable routing policy](expanded-selection/routing-policy.md) contains the
relevant final section; merge it with existing host/project instructions rather
than replacing unrelated guidance. [Policy hashes and repair reasons](expanded-selection/routing-repair.json)
identify the tested revisions. Global backup files and full private configuration
remain local; publishing this policy does not install it on another host.

All four implementation workers performed their own baseline skill reads. Native
child turn IDs were used to exclude inherited parent history from the audit.
One initial worker's aggregate read output was truncated. In the rerun, a worker
recovered the omitted proof/verification sections before editing; independent
inspection matched the delivered source segments, including the complete
zero-trust instructions. The initial truncation is not silently treated as a
complete delivered read.

Delegation evidence combines native spawn results, child-specific metadata,
own-turn tool actions, scoped changes and completion/integration records. CLI
wait records alone had empty receiver lists and could not establish delegation.
Exact private handoff messages are not reproduced; child reads establish
own-context use, not metadata-only discovery independent of parent instructions.

## Real deliverables and checks

The team produced two independently owned improvements:

- Both guide HTML entry points reject any parsed `<base href>`, including empty,
  valueless and external values. A base URL changes browser resolution, which the
  static checker does not model. Target-only base elements remain allowed.
- `scripts/check_installed.py --skills-dir PATH` compares the 24 expected entrypoint
  and metadata files in all twelve packages. It emits deterministic JSON, detects
  missing/modified files, ignores unrelated packages, rejects the selected root
  or expected descendants when symlinked, and does not write or execute installed
  content or use the network. Safe operation requires POSIX descriptor/no-follow
  capabilities and a stable installation; it is not an atomic snapshot.

The visual task produced a self-contained explanation of two actual validator
paths. Its sources are explicitly pinned to the baseline revision; it illustrates
local reference processing, not the subsequently added base-tag guard or the
whole package gate. The exact final page bytes and control-script bytes were
checked against the browser preview input. Preview used `about:blank` with exact
content, not a successfully served or deployed website. Recorded checks cover
play/pause, stepping, replay, finite stopping, reduced motion, keyboard operation,
narrow DOM measurements, no-JavaScript text and print fallback.

The repaired specialist-review run also found a Markdown classification bug:
`://` anywhere in a target caused local links such as
`../../outside.css?redirect=https://example.invalid` to skip validation. It also
confirmed inconsistent handling of valid query/encoded paths. The integration
repair uses parsed URL fields and the same split/decode/resolve/contain order for
Markdown links, with focused regressions. This was a false acceptance defect,
not evidence of outside-file access or code execution.

The original team passed 27 focused tests; the independent rerun implementation
passed 26. They are distinct tested revisions, not additive coverage. Both passed
all **79 checks** in the corrected independent maintenance oracle. The final
published integration passes **35 focused tests**, **79 maintenance checks**,
and **four independent Markdown URL cases**. It also confirms read-only byte
parity for all **24 files in the actual local installation**; that is not host
activation proof. The original Markdown implementation failed all four URL
cases; [before](expanded-selection/markdown-original-results.json) and
[after](expanded-selection/markdown-repaired-results.json) results are retained.
Existing package, fixture and negative-control checks remain passing. Final commands and results are
recorded in [integration results](expanded-selection/integration-results.json).

## Preserved failures and oracle correction

- Original base-href behavior was detected by rejection assertions failing for
  the intended reason, not an import or setup error. The original team also
  repaired a special-file opening issue discovered during its parent's review.
- The first independent run recorded **76/77**, failing only an assumption that
  ancestor aliases leading to an explicitly selected installation must be
  rejected. That exceeded the task contract and would reject ordinary OS aliases.
  Independent reassessment changed it to positive acceptance while retaining all
  selected-root/expected-child symlink rejection cases. Two newline-only byte
  difference checks were also added, producing the frozen 79-case suite.
  [Initial result](expanded-selection/initial-oracle-77.json),
  [corrected initial-team result](expanded-selection/initial-team-corrected-oracle.json),
  [rerun result](expanded-selection/retry-team-results.json).
- The visual run retained an early immediate-motion assertion failure, unavailable
  cross-call variable, and screenshot-created manifest mismatch, then corrected
  its checks/artifacts and passed. File navigation/local serving and an additional
  narrow screenshot were blocked. Narrow-layout evidence is measurements, not
  that denied screenshot. Neither task routing nor browser certification is
  inferred from a screenshot.

## Reproduction and limits

From the repository root:

```sh
python3 -B -m unittest discover -s scripts -p 'test_*.py' -v
python3 -B scripts/validate.py
python3 -B validation/expanded-selection/check_maintenance.py .
python3 -B validation/expanded-selection/check_markdown.py .
python3 -B scripts/check_installed.py --skills-dir /path/to/installed/skills
```

These rerun deterministic checks, not agent selection. Repeating the ten-session
experiment requires fresh sessions, the [saved prompts and input identities](expanded-selection/inputs.json),
installed skills, the applicable policy revision, account/model access, and
inspection of actual tool events and outputs. Policy revisions and task prompts
are part of the evaluated system.

The harness was Codex CLI 0.166.0 on macOS/Python 3.14.5, with local configuration
selecting `gpt-6-astra`, high reasoning, OpenAI provider. Model identity was not
independently attested by the provider. Results do not establish statistical
reliability, other models/projects/platforms, fresh desktop-native routing,
production enforcement, accessibility certification or deployment readiness.
Swarm execution here means two bounded workers, not large-scale scheduling or a
measured speedup. The independent checker snapshots retained file bytes; it does
not prove absence of transient writes or arbitrary race resistance. Source review
and focused tests support the read-only/no-execution/network-free boundaries.

Public evidence is selected and normalized: command/path prefixes use placeholders,
private raw transcripts and encrypted handoffs are omitted, and instruction hashes
identify configuration without publishing unrelated global rules. None of the
trial workers committed, published, installed software, changed global settings or
contacted people. The supervising task applied the authorized policy repairs and
prepared the reviewed integration for publication.
