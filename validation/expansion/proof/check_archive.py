"""Read-only fixture execution against its maintained authorization contract."""
import copy
import json
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2] / 'code-baseline/original-update'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
import store
from transport import handle_archive

cases = [
    ('owner own tenant', 'alice', 'A', {}, True),
    ('admin own tenant', 'admin', 'B', {}, True),
    ('member other owner', 'alice', 'B', {}, False),
    ('admin cross tenant without hint', 'admin', 'E', {}, False),
    ('admin cross tenant with target hint', 'admin', 'E', {'tenant': 't2'}, False),
    ('owner with irrelevant hint', 'alice', 'A', {'tenant': 't2'}, True),
    ('unknown actor', 'unknown', 'A', {}, False),
    ('missing account', 'alice', 'missing', {}, False),
    ('list account id', 'alice', [], {}, False),
    ('dict account id', 'alice', {}, {}, False),
]

results = []
for name, actor, account, query, should_allow in cases:
    store.reset()
    before = copy.deepcopy((store.ACCOUNTS, store.EVENTS))
    exception = None
    try:
        handle_archive(SimpleNamespace(actor_id=actor), account, query)
    except Exception as exc:
        exception = {'type': type(exc).__name__, 'message': str(exc)}
    changed_accounts = [key for key in store.ACCOUNTS if store.ACCOUNTS[key] != before[0][key]]
    events_changed = store.EVENTS != before[1]
    if should_allow:
        expected_accounts = copy.deepcopy(before[0])
        expected_accounts[account]['archived'] = True
        passed = exception is None and store.ACCOUNTS == expected_accounts and store.EVENTS == [{'actor_id': actor, 'account_id': account}]
    else:
        passed = exception == {'type': 'PermissionError', 'message': 'access denied'} and (store.ACCOUNTS, store.EVENTS) == before
    results.append({'case': name, 'expected': 'allow' if should_allow else 'deny without state changes', 'exception': exception, 'changed_accounts': changed_accounts, 'events': copy.deepcopy(store.EVENTS), 'events_changed': events_changed, 'contract_pass': passed})

print(json.dumps({'cases': results, 'passed': sum(r['contract_pass'] for r in results), 'total': len(results)}, indent=2))
sys.exit(0 if all(r['contract_pass'] for r in results) else 1)
