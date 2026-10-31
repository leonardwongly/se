import store

def archive_account(actor_id, account_id, tenant_hint=None):
    actor = store.authenticated_actor(actor_id)
    account = store.ACCOUNTS.get(account_id)
    if account is None or account['tenant_id'] != (tenant_hint or actor['tenant_id']):
        raise PermissionError('access denied')
    if actor['role'] != 'admin' and account['owner_id'] != actor_id:
        raise PermissionError('access denied')
    account['archived'] = True
    store.EVENTS.append({'actor_id': actor_id, 'account_id': account_id})
