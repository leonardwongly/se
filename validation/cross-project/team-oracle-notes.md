# Independent team CLI oracle

Frozen before reading the team implementation. Design inputs: `team.prompt.txt`, `ACCEPTANCE.md`, `matrix.json`, and baseline audit modules at `4a50ea995c37132bcfee5c64fd908d35ca0cef96`. The implementation under evaluation was not inspected.

## Frozen identity

- Checker: `check_team.py`
- SHA-256: `43a2870c98858bade479c2bbffc3e831cd8db32d51859bdbb25017892494c1c8`
- Freeze UTC: `2026-11-05T02:07:40.151618+00:00`
- Runtime: Node `v26.13.0`, Python `3.14.5`
- Own-context skills read: se-proof, se-zero-trust, se-verify. The truncated tail of the initial zero-trust read was read separately.

## Acceptance coverage

38 cases execute copied real entrypoints with disposable, synthetic local fixtures. Both CLIs have JSON valid/finding/error coverage; missing and symlink input; malformed JSON or rendered HTML; original human valid/finding output; export preservation and import-without-running; ten invalid argument forms including unknown/positional arguments, `--`, `--json=1`, duplicate JSON flags and JSON both before/after invalid arguments. Reading also has wrong top-level JSON shape and unsafe cover traversal.

The oracle uses explicit expected values for the synthetic content. Performance reports and inventory use frozen budget values and known fixture byte counts, not the candidate's exported result as the oracle. Existing exported names are required, additional exports are allowed.

The invalid-argument cases preload a core-fs guard for read/open/stat/list/access operations against project inputs. Exit 97 with `ORACLE_INPUT_ACCESS` demonstrates wrong ordering. Script/module loads remain permitted. This is instrumented real-Node process evidence, not a universal OS-level read audit. Every run compares file hashes, symlink targets, modes and modification timestamps before/after; it checks no persistent mutations inside the disposable project. It cannot prove absence of transient writes, arbitrary writes outside that tree, every fs API, or network effects. No network is requested by this checker.

## Original baseline result

Command:

```sh
python3 check_team.py $TRIAL_ROOT/baseline team-oracle-before.json
```

Checker exits 1: **6/38 pass, 32/38 fail**. Both human pass/finding controls and both import/export controls pass. JSON valid cases reach the audit successfully and exit 0 but output human text, so JSON failures are not fixture/setup failures. Original finding and error cases reach their intended code paths but violate JSON channel/shape expectations. All invalid-argument cases attempt project-input access and the guard terminates them with 97 instead of the required 2, demonstrating the intended ordering defect. Raw stdout, stderr, exit, assertions, source hashes and runtime identity are retained in `team-oracle-before.json`.

## Harness boundary review

The checker writes only disposable temporary synthetic projects and the explicitly provided evidence output. It runs structured subprocess argument lists, with no shell interpolation, no dependencies, no installation and no publication. NODE_OPTIONS is cleared for deterministic subprocess startup. It compares source hashes at start/end and rejects a changed source snapshot. Its project argument is an authorized local test subject, not arbitrary untrusted server input. It removes only its own temporary directories through TemporaryDirectory cleanup.

## Pending integration

Run the exact same frozen checker once the implementation writers have finished, preserving `team-oracle-before.json` and writing a new after result. Project-wide test execution and final diff/ownership review belong to the coordinating evaluation and implementation agents. This checker gives bounded local CLI behavior evidence, not full security, network, release or production proof.

## Completed implementation run

At 2026-11-05T02:14:25.521726+00:00, after the coordinator confirmed both writers had ended, the exact frozen checker was run against the stable team checkout:

```sh
python3 check_team.py $TRIAL_ROOT/team team-oracle-after.json
```

Result: **38/38 passed**, checker exit 0, unchanged SHA-256 `43a2870c98858bade479c2bbffc3e831cd8db32d51859bdbb25017892494c1c8`. The original **6/38 pass, 32 intended failures** remain in `team-oracle-before.json`. Only after this run was the candidate diff inspected. No material contract/security regression found: runtime changes are confined to CLI argument/output handling and preserve audit logic and exports. Final source hashes are in `application-grades.json` and script hashes also in the raw oracle result.

The team's retained focused combined test run passes 41/41. Its unfiltered operations suite remains recorded as 27 passes/1 startup failure due to missing `yaml`; this prerequisite blocker is not erased by the focused pass. Parent separately owns dependency-backed immutable-copy validation. No full release, hosted or production claim is made.
