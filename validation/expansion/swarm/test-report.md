# Archive contract test report

Added only `project/tests/test_archive_contract.py`: nine independent behavioral test methods plus the existing owner test. Tests are frozen following baseline capture.

Evidence source: isolated non-Git local project at `validation/expansion/swarm/project`; maintained `docs/security-contract.md`, active `transport.py`, `store.py`, original `service.py`, and existing test. No historical docs, external services, installs, commits, or host changes were used.

Frozen test SHA-256: `0a5b619d85806edd85d8cb2e7bf8b4cd821e476871cac2fa5b6c2e5872929916`.

Coverage includes direct service and active transport calls for same-tenant owners/admins, nonowners, cross-tenant actors, unknown/malformed actors, missing/malformed account IDs including lists/dicts, spoofed tenant hints, irrelevant hints on permitted requests, and owner relationships that cannot override tenant boundaries. Transport tests also supply misleading session/query authorization fields. Public argument names, positional compatibility, and optional hint default are checked.

Denied operations require exact `PermissionError('access denied')` and compare the complete account collection and event list with deep snapshots. Allowed operations compare all account fields against precisely one intended `archived=True` update and require exactly one appended actor/account event. Existing events and nested future metadata are seeded to detect destructive replacement or unintended mutation; assertions avoid printing account credentials.

Baseline command, before implementation edits:

```sh
PYTHONDONTWRITEBYTECODE=1 make check
```

Result: exit 2; 10 test methods ran in 0.012s; **15 subtest failures and 16 subtest errors**. Full output is `baseline-contract-check.txt`.

- Seven failures demonstrate unauthorized cross-tenant account mutation through spoofed hints (including a stored ownership relationship and active transport).
- Eight failures demonstrate list/dict IDs raising `TypeError` rather than the required denial.
- Sixteen errors demonstrate irrelevant hints incorrectly rejecting otherwise authorized owner/admin actions.

The existing owner test, legitimate owner/admin cases, malformed actor rejection, ordinary denials, and signature check passed against the baseline. This report establishes the baseline only; the parent agent owns combined post-implementation validation.
