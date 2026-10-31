import inspect
import unittest
from copy import deepcopy
from types import SimpleNamespace

import service
import store
import transport


class ArchiveContractTests(unittest.TestCase):
    def setUp(self):
        store.reset()
        self.addCleanup(store.reset)

    def prepare_state(self):
        store.reset()
        store.ACCOUNTS['A']['future_metadata'] = {'tags': ['preserve']}
        store.EVENTS.append({'actor_id': 'bob', 'account_id': 'B'})
        return deepcopy(store.ACCOUNTS), deepcopy(store.EVENTS)

    def invoke(self, route, actor_id, account_id, hint=None):
        if route == 'service':
            return service.archive_account(actor_id, account_id, hint)
        session = SimpleNamespace(actor_id=actor_id)
        query = {} if hint is None else {'tenant': hint}
        return transport.handle_archive(session, account_id, query)

    def assert_denied_unchanged(self, operation):
        accounts_before = deepcopy(store.ACCOUNTS)
        events_before = deepcopy(store.EVENTS)
        error = None
        try:
            operation()
        except Exception as caught:
            error = caught
        self.assertTrue(store.ACCOUNTS == accounts_before,
                        'Denied archive must preserve every account and field')
        self.assertTrue(store.EVENTS == events_before,
                        'Denied archive must preserve all existing events')
        self.assertIsInstance(error, PermissionError)
        self.assertEqual(error.args, ('access denied',))

    def assert_allowed_exactly(self, route, actor_id, account_id, hint=None):
        expected_accounts = deepcopy(store.ACCOUNTS)
        expected_accounts[account_id]['archived'] = True
        expected_events = deepcopy(store.EVENTS)
        expected_events.append({'actor_id': actor_id, 'account_id': account_id})
        self.invoke(route, actor_id, account_id, hint)
        self.assertTrue(store.ACCOUNTS == expected_accounts,
                        'Allowed archive must only set the selected archived flag')
        self.assertEqual(store.EVENTS, expected_events)

    def test_same_tenant_owner_and_admin_are_allowed(self):
        for route in ('service', 'transport'):
            for actor_id, account_id in (('alice', 'A'), ('bob', 'B'),
                                         ('admin', 'A'), ('admin', 'B'),
                                         ('eve', 'E')):
                with self.subTest(route=route, actor=actor_id, account=account_id):
                    self.prepare_state()
                    self.assert_allowed_exactly(route, actor_id, account_id)

    def test_nonowners_cross_tenant_and_unknown_actors_are_denied(self):
        cases = (('alice', 'B'), ('bob', 'A'), ('alice', 'E'),
                 ('admin', 'E'), ('eve', 'A'), ('eve', 'B'),
                 ('unknown', 'A'))
        for route in ('service', 'transport'):
            for actor_id, account_id in cases:
                with self.subTest(route=route, actor=actor_id, account=account_id):
                    self.prepare_state()
                    self.assert_denied_unchanged(
                        lambda: self.invoke(route, actor_id, account_id))

    def test_spoofed_tenant_hint_cannot_authorize_cross_tenant_admin(self):
        for route in ('service', 'transport'):
            for actor_id, account_id, hint in (('admin', 'E', 't2'),
                                               ('eve', 'A', 't1')):
                with self.subTest(route=route, actor=actor_id):
                    self.prepare_state()
                    self.assert_denied_unchanged(
                        lambda: self.invoke(route, actor_id, account_id, hint))

    def test_owner_relationship_does_not_override_tenant_boundary(self):
        for route in ('service', 'transport'):
            for hint in (None, 't2'):
                with self.subTest(route=route, hint=hint):
                    self.prepare_state()
                    store.ACCOUNTS['E']['owner_id'] = 'alice'
                    self.assert_denied_unchanged(
                        lambda: self.invoke(route, 'alice', 'E', hint))

    def test_irrelevant_tenant_hints_cannot_deny_authorized_archive(self):
        for route in ('service', 'transport'):
            for actor_id in ('alice', 'admin'):
                for hint in ('t2', 'unknown', '', {'tenant': 't2'}, ['t2']):
                    with self.subTest(route=route, actor=actor_id, hint=hint):
                        self.prepare_state()
                        self.assert_allowed_exactly(route, actor_id, 'A', hint)

    def test_missing_and_malformed_account_ids_are_denied_without_mutation(self):
        for route in ('service', 'transport'):
            for account_id in ('missing', '', None, [], {}, ['A'],
                               {'id': 'A'}, 0, True, ('A',)):
                with self.subTest(route=route, account_id=account_id):
                    self.prepare_state()
                    self.assert_denied_unchanged(
                        lambda: self.invoke(route, 'admin', account_id))

    def test_malformed_actor_ids_are_denied_without_mutation(self):
        for route in ('service', 'transport'):
            for actor_id in (None, '', [], {}, 0):
                with self.subTest(route=route, actor_id=actor_id):
                    self.prepare_state()
                    self.assert_denied_unchanged(
                        lambda: self.invoke(route, actor_id, 'A', 't1'))

    def test_transport_uses_authenticated_actor_not_session_hints(self):
        for actor_id, account_id, expected_allowed in (('alice', 'B', False),
                                                       ('eve', 'A', False),
                                                       ('alice', 'A', True)):
            with self.subTest(actor=actor_id, account=account_id):
                self.prepare_state()
                session = SimpleNamespace(actor_id=actor_id, tenant_id='t1',
                                          role='admin', owner_id='alice')
                operation = lambda: transport.handle_archive(
                    session, account_id, {'tenant': 't1', 'actor_id': 'admin',
                                         'role': 'admin', 'owner_id': 'alice'})
                if not expected_allowed:
                    self.assert_denied_unchanged(operation)
                else:
                    expected_accounts = deepcopy(store.ACCOUNTS)
                    expected_accounts[account_id]['archived'] = True
                    expected_events = deepcopy(store.EVENTS)
                    expected_events.append({'actor_id': actor_id,
                                            'account_id': account_id})
                    operation()
                    self.assertTrue(store.ACCOUNTS == expected_accounts)
                    self.assertEqual(store.EVENTS, expected_events)

    def test_public_signature_retains_optional_compatibility_hint(self):
        parameters = list(inspect.signature(service.archive_account).parameters.values())
        self.assertEqual([parameter.name for parameter in parameters],
                         ['actor_id', 'account_id', 'tenant_hint'])
        self.assertTrue(all(parameter.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
                            for parameter in parameters))
        self.assertIs(parameters[0].default, inspect.Parameter.empty)
        self.assertIs(parameters[1].default, inspect.Parameter.empty)
        self.assertIsNone(parameters[2].default)
