# Updated-code exercise: archive_account

Gate: **PASS for the isolated local fixture's archive contract**. This is not a production, hosted-provider, or full security-audit claim. No exceptions or outstanding required checks.

## Scope and source grounding

- Root: `validation/code-baseline/update`.
- Non-Git source identity, as required by `AGENTS.md:8` and `docs/security-contract.md:3`; no branch/revision or commit claim.
- Read this project's instructions, maintained contract, active transport, service, store, existing tests, Makefile, and manifest before changing behavior. Did not read sibling fixtures, parent grader, or archived design material.
- Authority: `docs/security-contract.md:6-12` requires stored identity, same-tenant ownership/admin permission, uniform denial, and no denial effects. Lines 17-20 preserve the signature and define archive/event effects. Historical documents are explicitly non-authoritative at lines 3-4.
- Active caller: `transport.py:3-4` takes the actor ID from the authenticated session and passes the untrusted query tenant as `tenant_hint`.
- Runtime: Python 3.14.5, macOS 27.2 arm64. Initial observation `2026-10-31T00:29:30+08:00`; final snapshot `2026-10-31T00:30:51+08:00`. See `code-fixtures/update/evidence/environment.txt`.
- Applied current skills `se-how`, `se-zero-trust`, `se-verify` from `outputs/se-skills`, not historical validation reports.

## Observed defect and implemented change

The original service accepted a caller-supplied tenant in its authorization comparison. A tenant-t1 admin could archive tenant-t2 account E by supplying `tenant_hint='t2'`. A valid owner could also be denied solely because of an unrelated hint. Unhashable account IDs reached dictionary lookup and raised TypeError instead of the required PermissionError.

`service.py:3-13` now authenticates through `store.authenticated_actor`, rejects non-string account IDs, looks up the account, compares its tenant only to the authoritative stored actor tenant, enforces admin/ownership permission, then mutates the archive flag and appends the event. `tenant_hint` remains accepted with its original default and has no authority. Missing string IDs use the existing uniform denial path.

Changed implementation: `service.py` only. Added behavioral tests: `tests/test_archive_contract.py`. Contract, transport, store, existing tests, Makefile, and manifest remain unchanged by digest comparison. Evidence files are under this project's `evidence/`; this report is the only authored file outside the fixture.

## Acceptance and zero-trust baseline

| Criterion / boundary | Enforcer and evidence | Result |
|---|---|---|
| Authenticate stored actor; unknown/malformed actors denied | `store.py:22-25`, called at `service.py:4`; invalid-actor test lines 55-59 | PASS |
| IDs are untrusted; malformed/missing inputs use uniform denial | `service.py:5-9`; malformed-account test lines 49-53, including lists/dicts/bytes/booleans | PASS |
| Owners and admins restricted to their own tenant | `service.py:8-11`; fixed independent allow-set matrix at test lines 25-47; owner across tenant at lines 61-64 | PASS |
| Query hints neither grant nor remove authority | 75 matrix combinations across 5 actors, 3 accounts, and 5 hints; active transport denial and success at test lines 66-74 | PASS |
| Denial produces no protected side effects | Shared helper at test lines 16-23 compares complete accounts and event snapshots after the expected exact exception; matrix includes a preexisting event | PASS |
| Success changes only target archive flag and appends the specified event | Matrix compares complete expected account state and event sequence; existing owner test also retained | PASS |
| Public signature preserved | `service.py:3`; signature test at test lines 76-78 | PASS |
| New tests exercise the real boundary, with a useful independent oracle | Tests invoke the actual service/transport and actual in-memory store, not a stub authorization service; expected allow-set comes from contract and fixture identities | PASS |

Sensitive account data remains in the store. The change adds no output or log sink and archive still returns None. Full-state assertions deliberately avoid printing account values on failure, preserving synthetic credential confidentiality. No new dependencies, commands, network calls, credentials, migrations, or policy changes were introduced.

Human permission to edit this fixture was not treated as application-user authority. Runtime permission remains checked on every call against the stored actor/account. Validation precedes both writes. The existing in-memory mutation/event sequence is not a database transaction; concurrency, process crashes, and durable persistence are outside this fixture's documented environment and are not certified by these tests.

## Executed verification and retained failures

All commands ran in the fixture root. Required command comes directly from `AGENTS.md:4` and `Makefile:1-2`: `make check`, expanding to `python3 -m unittest discover -s tests -v`.

| Run | Command | Actual outcome / exit | Evidence |
|---|---|---|---|
| Existing-suite baseline | `make check` | 1 test passed; exit 0 | Tool-observed before edits; baseline source digest below |
| Test-the-tests on original service | `make check > evidence/known-defect.log 2>&1` | 8 tests executed; 5 failures, 14 errors; make exit 2 | `evidence/known-defect.log`, written `2026-10-31T00:30:27+08:00` |
| Required combined check on fixed service | `make check > evidence/final-check.log 2>&1` | All 8 tests passed, no skips; exit 0 | `evidence/final-check.log`, written `2026-10-31T00:30:34+08:00` |
| Stable final source validation | `shasum -a 256 -c evidence/source.sha256` | All 9 entries OK; exit 0 | Final source manifest |

The failing run is intentional defect-detection evidence, retained rather than hidden by a retry. Failures arose from unauthorized success (PermissionError not raised), authorized requests denied by hints, and malformed IDs raising TypeError. They were behavior failures in the real changed path, not environment/setup errors. The implementation change resolved those failures with the identical test suite. No temporary production mutation or bypass was needed.

Reviewed final diff: `evidence/final.diff`. Source files were unchanged after the final passing run; all manifest digests were checked. No coverage percentage, benchmark, independent audit, hosted CI, real authentication-provider integration, deployment, or release-readiness claim is made. No provider exists in this fixture per its contract; a hosted-provider check is not an applicable local-fixture gate. No network installations, Git commits, deployment, or external service access occurred.

## Exact identities

Original `service.py` SHA-256: `a28565411d66f5353909f6eb51bfc80d4bce3b30117b27bc80f5d7f7a15f9ecc`.

Final source SHA-256 values are retained in `evidence/source.sha256`, including:

- `service.py`: `ae77d78208545d9e787792c725c350d37341f65953dedada90ed6d6bf7e458f2`
- `tests/test_archive_contract.py`: `e82a4de0698ffa621a4418616b4a0874ceebc7cd3314703f40912a59f638c088`
- `docs/security-contract.md`: `b821dfca7631ca0ef60ba3501fde7407f0aa79591c490dc12dee6fcb2e765e8c`
- `evidence/source.sha256`: `c0fb659b2e71ffc328a9d31d1fffa1029ec847111e02be25659d888c2e18abc4`
- `evidence/final.diff`: `cf39f7bb8b6a0d328e968c5e9474ffeceaa9512fc04a0ab4e50db2c3bb3a6b1f`
- `evidence/known-defect.log`: `2bbc282ab2bb6dd39d0b41a972fa4bb98089110e5874dbcce590c13604d9dbaa`
- `evidence/final-check.log`: `f0675439b891a5dc9f3a22e940fcfb8ac992d348debfcf29c821909b808b8d0f`

Applied skill SHA-256 values:

- `se-how/SKILL.md`: `2adbb13c30fa416eb94238bbc3cfd3fa9493fb63eef3c340df36a1aeafc8abfd`
- `se-zero-trust/SKILL.md`: `f9cfa2302923509f038c300d8a761ab07f4a85e4236c848fc949ff47af50df7c`
- `se-verify/SKILL.md`: `cba26212492f47feef0524249b47e05b0ee8c83fde7f1ee41e64f74fe3622911`

To reproduce: `cd validation/code-baseline/update && make check`.
