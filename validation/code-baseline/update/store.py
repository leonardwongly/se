from copy import deepcopy

USERS = {
    'alice': {'id': 'alice', 'tenant_id': 't1', 'role': 'member'},
    'bob': {'id': 'bob', 'tenant_id': 't1', 'role': 'member'},
    'admin': {'id': 'admin', 'tenant_id': 't1', 'role': 'admin'},
    'eve': {'id': 'eve', 'tenant_id': 't2', 'role': 'admin'},
}
INITIAL = {
    'A': {'id': 'A', 'owner_id': 'alice', 'tenant_id': 't1', 'email': 'alice@example.invalid', 'display_name': 'Alice', 'api_key': 'synthetic-key-A', 'archived': False},
    'B': {'id': 'B', 'owner_id': 'bob', 'tenant_id': 't1', 'email': 'bob@example.invalid', 'display_name': 'Bob', 'api_key': 'synthetic-key-B', 'archived': False},
    'E': {'id': 'E', 'owner_id': 'eve', 'tenant_id': 't2', 'email': 'eve@example.invalid', 'display_name': 'Eve', 'api_key': 'synthetic-key-E', 'archived': False},
}
ACCOUNTS = deepcopy(INITIAL)
EVENTS = []

def reset():
    ACCOUNTS.clear()
    ACCOUNTS.update(deepcopy(INITIAL))
    EVENTS.clear()

def authenticated_actor(actor_id):
    if not isinstance(actor_id, str) or actor_id not in USERS:
        raise PermissionError('access denied')
    return USERS[actor_id]
