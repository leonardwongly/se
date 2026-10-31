# Account export exercise

Gate: **PASS for the isolated local account-export implementation**. No production, hosted-provider, concurrency, or full-security-audit claim is made.

## Grounding and scope

- Project: `validation/code-baseline/new`; maintained contract declares it non-Git (`docs/security-contract.md:3`). Source identity is SHA-256 rather than an enclosing repository revision.
- Read `AGENTS.md`, maintained `docs/security-contract.md`, active caller `transport.py`, `Makefile`, `pyproject.toml`, `service.py`, `store.py` (synthetic keys redacted before displaying), and the original test. No historical archive, sibling fixture, or parent grader was read.
- Used the requested current `se-how`, `se-zero-trust`, and `se-verify` skills under `outputs/se-skills`. No installation, network request, commit, deploy, credential change, or external service action occurred.
- `docs/security-contract.md:6-15` establishes actor lookup, tenant/owner/admin policy, uniform denial, public-field allowlisting, and no state changes. `transport.py:3-4` supplies only the authenticated session actor ID and requested account ID. `Makefile:1-2` prescribes `make check`, invoking `python3 -m unittest discover -s tests -v`. The manifest requires Python >=3.10; the actual interpreter was Python 3.14.5 on macOS arm64.
- Initial `service.py` only raised `NotImplementedError`. Its initial SHA-256 was `f6f82a712ce997096454e4c8be4091fffc82e01431c03d36e497d0fe4e81c30a`. The original test checked actor lookup only; it did not establish export acceptance.
- The archive paragraph is not an instruction to implement another API in this export-only task. No archive operation or transport interface was added or changed.

## Implementation and zero-trust baseline

- Changed `service.py:4-15`: retrieve authoritative actor using `store.authenticated_actor`, reject non-string or absent account IDs with `PermissionError('access denied')`, require matching stored tenants, then require stored admin role or stored ownership. Return a fresh dict constructed from exactly `id`, `email`, `display_name`.
- Added `tests/test_export.py` with nine behavioral tests (including subcases), retaining the original test unchanged. Tests call the real service and active transport function with the real in-memory store; no authorization stub substitutes for enforcement.
- Untrusted input: account ID; identity supplied by the fixture's already-authenticated transport. Authority: current `store.USERS` actor plus `store.ACCOUNTS` resource metadata. Session role/tenant hints are not consumed. Enforcement: `service.py:5-13`, before public data construction at line 15.
- Sensitive fields remain in the fixture store; the returned dict is an explicit allowlist so unknown future fields cannot escape. Both success and denial tests compare deep snapshots of USERS, ACCOUNTS, and EVENTS; mutation diagnostics avoid printing protected store values. Export itself contains no store mutation, logging, file, network, subprocess, or persistence sink.
- Invalid/unhashable identifiers are rejected before dictionary lookup. Existing actor validation is reused. Authorization is evaluated on every call; tests cover role revocation, identity deletion, changed account ownership, and changed account tenant.
- Reviewed the full resulting source and tests plus caller and contract. No dependency, runtime-config, migration, authentication-provider, or CI change was introduced. Final source comparison is retained in `evidence/implementation.patch`; unchanged file hashes match the initial observation. In-memory mutation testing did not write a modified service to disk.

## Acceptance and executed checks

All paths below are relative to the project root.

| Criterion | Check / oracle | Result |
|---|---|---|
| Owners and same-tenant admins export | `tests/test_export.py:33-47`, independently specified public dicts for five valid actor/account pairs | PASS |
| Wrong owner and cross-tenant access denied | `tests/test_export.py:64-73`, exact exception and unchanged state, including owner match across tenants | PASS |
| Unknown/malformed actor and missing/malformed account IDs denied | `tests/test_export.py:75-84`, including list/dict/null/bool/int and ambiguous strings | PASS |
| Exactly public fields, fresh result, unchanged store | `tests/test_export.py:49-62`, future private field, archived account, preexisting event, two calls, then caller mutation | PASS |
| Caller hints do not grant authority | `tests/test_export.py:86-95`, real transport with forged session role/tenant hints | PASS |
| Current identity/resource authorization used | `tests/test_export.py:97-110`, role/identity revocation and resource metadata changes | PASS |
| Existing behavior retained | Original `tests/test_existing.py` retained and run | PASS |
| Tests reach missing implementation | Before implementation, `make check` exited 2; 10 tests ran, 36 subcase errors from the intentional `NotImplementedError` | Expected baseline failure retained |
| Authorization tests detect an actual bypass | In-memory removal of tenant condition caused four intended `PermissionError not raised` failures; valid control still passed; no execution/setup errors | Negative control PASS |
| Project-required final validation | `make check` exited 0; 10 tests, no skips, no errors or failures | PASS |

Exact principal commands, run with cwd equal to the project root:

```sh
make check
make check > evidence/before-implementation.log 2>&1
make check > evidence/final-check.log 2>&1
```

The final verification additionally invoked `subprocess.run(['make', 'check'], capture_output=True, text=True)` from Python, saved its combined output, and compared SHA-256 hashes of all nine source/configuration/instruction files before and after that command. It passed with identical hashes at `2026-10-31T00:30:48.511133+08:00`.

The negative control command was `python3 - <<'PY' > evidence/authorization-negative-control.log 2>&1` with this body (no disk source mutation):

```python
from pathlib import Path
import sys
import unittest
import service
sys.path.insert(0, str(Path('tests').resolve()))
source = Path('service.py').read_text()
original = 'actor["tenant_id"] != account["tenant_id"] or ('
assert original in source
mutated = source.replace(original, 'False or (', 1)
exec(compile(mutated, '<in-memory-tenant-check-disabled>', 'exec'), service.__dict__)
from test_export import ExportTests
suite = unittest.TestSuite([
    ExportTests('test_owner_and_same_tenant_admin_export_public_fields'),
    ExportTests('test_ownership_does_not_override_tenant_boundary'),
    ExportTests('test_other_owner_and_cross_tenant_access_denied'),
])
result = unittest.TextTestRunner(verbosity=2).run(suite)
assert not result.errors, 'Negative control failed during setup/execution'
assert len(result.failures) == 4, 'Expected ownership tenant failure and three cross-tenant admin failures'
print('NEGATIVE CONTROL PASS: removing tenant enforcement causes four intended denial assertions to fail; positive control still passes.')
```

## Evidence and limits

- `evidence/before-implementation.log`: retained initial failing run; failure was missing implementation, not environment setup.
- `evidence/authorization-negative-control.log`: intended mutation failures, harness exit 0 because all expected failures were observed.
- `evidence/final-check.log`: final passing required project check.
- `evidence/final-source.json`: exact root, timestamp/timezone, Python/OS, command, exit status, unchanged-during-check assertion, per-file SHA-256.
- `evidence/implementation.patch`: reviewed source/test delta. Final service SHA-256: `cd7c575e3e92f985628295365a6c94f28812c55e79da1825f126c4c4c63f0d16`; new tests: `e932af23283003e699cd5f061920a5d538c9dbae0a749f6d8b76e56dd6177b86`.

All evidence is local synthetic Python execution. The fixture declares no hosted provider, so hosted verification is not part of this acceptance scope. Authentication session establishment is assumed as explicitly specified by the project contract; this task validates service authorization and transport consumption, not a real identity provider. Trusted store schemas, scalar public fields, and the fixture's sequential in-memory execution model remain assumptions; no production database atomicity or concurrent revocation claim is made. No coverage percentage, benchmark, deployment, release approval, or security certification is claimed. No required local checks remain blocked or unrun and no exceptions were granted.
