# Account archive isolated skill trial

Outcome: the bounded account-archive task is complete with local integrated evidence. Applied se-swarm, se-who, and se-proof from the supplied se-expansion package. No export feature was added: the requested surface is account archiving.

## Grounding and actual responsibilities

The project is a non-Git Python fixture. `baseline-identity.json` records the initial nine-file SHA-256 manifest and Python runtime; `baseline-service.py` retains the original implementation. Authority came from the requested local synthetic trial and project `AGENTS.md`. The maintained contract is `project/docs/security-contract.md`; the active call path is `transport.handle_archive` -> `service.archive_account` -> `store.authenticated_actor`, then account/event writes. `Makefile` establishes `make check` as the required check.

Exactly two child workers were launched, without recursive delegation:

| Contributor | Actual responsibility | Evidence |
|---|---|---|
| archive_implementation | Own service.py; review proposed enforcement change, wait for retained baseline, implement fix, run local check | implementation-report.md |
| archive_tests | Own tests/test_archive_contract.py; derive independent assertions from current contract, capture original failures, freeze tests | test-report.md; baseline-contract-check.txt |
| coordinator | Ground contract/caller, approve proposed security boundary change, review tests and combined diff, freeze assignments, run independent integrated check and compare manifests | assignments.json; implementation.diff; final-integrated-check.txt; final-source-identity.json |

## Mechanism and security review

Authentication supplies actor_id; stored USERS data supplies the actor tenant and role. The implementation now rejects non-string account IDs before dictionary lookup and compares the account tenant exclusively with the stored actor tenant. Within that tenant, only the account owner or stored admin role may archive. The compatibility-only tenant_hint parameter retains its public name, position, and default, but has no effect. Only after all checks succeed does the service set archived=True and append the existing actor/account event shape.

Before repair, a t1 admin could supply a t2 query hint and archive t2 account E. A valid owner could be incorrectly denied by an irrelevant hint, and unhashable IDs raised TypeError instead of the specified PermissionError. Current tests exercise these cases through both direct service and active transport calls. Denials require the exact error message and unchanged complete account/event snapshots. Allowed cases require only the intended archived flag change and one appended event; seeded existing events and nested future fields check preservation. Misleading session/query role and ownership fields cannot change authorization. The implementation and tests were inspected together; no contract, store, transport, existing test, or build configuration was changed.

## Failure, repair, and final validation

1. Original existing owner test: passed (baseline-existing-check.txt).
2. Contract tests against original implementation: `PYTHONDONTWRITEBYTECODE=1 make check`, exit 2, 10 methods, 15 subtest failures and 16 subtest errors (baseline-contract-check.txt, baseline-failure-summary.json). This demonstrates that the added suite detects the actual original defects rather than only accepting the repaired implementation.
3. Worker repair: type validation and authoritative tenant comparison, service.py only. Worker make check passed all 10 tests.
4. Coordinator final combined run: `PYTHONDONTWRITEBYTECODE=1 make check`, exit 0, all 10 tests passed, no skips. Full output is final-integrated-check.txt. The source manifest was identical immediately before and after this check.

`final-source-identity.json` records all final source hashes and proves that the only source differences from baseline are `service.py` and new `tests/test_archive_contract.py`. The final service SHA-256 is `ae77d78208545d9e787792c725c350d37341f65953dedada90ed6d6bf7e458f2`; test SHA-256 is `0a5b619d85806edd85d8cb2e7bf8b4cd821e476871cac2fa5b6c2e5872929916`.

## Limits

This establishes bounded local fixture behavior on Python 3.14.5, including the supplied transport function. It does not establish upstream session authentication, hosted behavior, production readiness, or formal security proof. The fixture has no hosted provider. No external services, installations, commits, pushes, deployments, or host configuration changes were performed. No unrelated improvements were introduced. Source manifests exclude generated Python bytecode caches. There are no remaining failures in the required local check.
