import store


def export_account(actor_id, account_id):
    actor = store.authenticated_actor(actor_id)
    if not isinstance(account_id, str) or account_id not in store.ACCOUNTS:
        raise PermissionError("access denied")

    account = store.ACCOUNTS[account_id]
    if actor["tenant_id"] != account["tenant_id"] or (
        actor["role"] != "admin" and account["owner_id"] != actor["id"]
    ):
        raise PermissionError("access denied")

    return {field: account[field] for field in ("id", "email", "display_name")}
