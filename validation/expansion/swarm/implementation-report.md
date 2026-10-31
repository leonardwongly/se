# Archive implementation report

Scope: isolated, non-Git Python fixture at `validation/expansion/swarm/project`. Edited only `service.py`; tests were maintained by another worker and left unchanged.

Read `AGENTS.md`, maintained `docs/security-contract.md`, `service.py`, `store.py`, `transport.py`, and the documented check target in `Makefile`. Proposed the change before editing and waited for the parent to confirm baseline capture.

## Changes

- Validate that `account_id` is a string before dictionary lookup; malformed non-string values now raise `PermissionError('access denied')`, including unhashable values.
- Compare the account tenant exclusively with the authenticated actor's stored tenant. The retained compatibility argument `tenant_hint=None` is unused and cannot grant or deny access.
- Preserve same-tenant owner/admin authorization, the public signature, and archive/event mutations after authorization succeeds.

## Validation

Executed `make check` after the fix: exit 0, 10 tests passed in 0.003 seconds. Tests covered authorized owners/admins, tenant hints, cross-tenant and non-owner denials, unknown/malformed actors, missing/malformed account IDs, unchanged state on denial, signature preservation, and the transport caller.

Source identity (SHA-256 of `service.py`, not Git evidence):

- Before: `a28565411d66f5353909f6eb51bfc80d4bce3b30117b27bc80f5d7f7a15f9ecc`
- After: `ae77d78208545d9e787792c725c350d37341f65953dedada90ed6d6bf7e458f2`

This is local fixture validation only. No hosted service, external call, dependency installation, commit, or deployment was involved. No changes were made to tests, store, transport, documentation, or other project files by this implementation worker. Parent retains responsibility for combined integration evidence.
