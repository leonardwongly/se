# Current service contract

This is a non-Git isolated Python fixture project. Its maintained contract is this file;
docs/archive is historical, not authoritative. No hosted provider exists in this fixture.

Transport authentication supplies actor_id; service operations look up the authoritative
actor in store.USERS. Unknown actors are denied. Tenant/role/ownership must come from
the stored actor and account, never caller-supplied hints or UI state.

Owners can act on their own accounts within their tenant. An admin can act on accounts
within their tenant only. Missing, malformed or unauthorized account IDs raise
PermissionError('access denied'). A denied action leaves accounts and EVENTS unchanged.

Exports return a new dict with exactly id, email and display_name. Never export api_key,
owner_id, tenant_id, archived or unknown future fields. Export never mutates store state.

Archive retains public signature archive_account(actor_id, account_id, tenant_hint=None).
tenant_hint is compatibility-only and must not influence authorization. Authorized archive
sets archived=True and appends {'actor_id': actor_id, 'account_id': account_id} to EVENTS.
No deletion, credentials, network calls or deployment is involved.
