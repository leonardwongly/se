from copy import deepcopy
from types import SimpleNamespace
import unittest

import store
from service import export_account
from transport import handle_export


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.users = deepcopy(store.USERS)
        store.reset()

    def tearDown(self):
        store.USERS.clear()
        store.USERS.update(self.users)
        store.reset()

    def snapshot(self):
        return deepcopy((store.USERS, store.ACCOUNTS, store.EVENTS))

    def assertUnchanged(self, before):
        # Avoid exposing protected fields in assertion diagnostics.
        self.assertTrue(before == self.snapshot(), "Store state changed")

    def assertDenied(self, actor_id, account_id):
        before = self.snapshot()
        with self.assertRaisesRegex(PermissionError, "^access denied$"):
            export_account(actor_id, account_id)
        self.assertUnchanged(before)

    def test_owner_and_same_tenant_admin_export_public_fields(self):
        cases = (
            ("alice", "A", "alice@example.invalid", "Alice"),
            ("bob", "B", "bob@example.invalid", "Bob"),
            ("admin", "A", "alice@example.invalid", "Alice"),
            ("admin", "B", "bob@example.invalid", "Bob"),
            ("eve", "E", "eve@example.invalid", "Eve"),
        )
        for actor, account, email, name in cases:
            with self.subTest(actor=actor, account=account):
                before = self.snapshot()
                result = export_account(actor, account)
                self.assertEqual(result, {"id": account, "email": email,
                                          "display_name": name})
                self.assertUnchanged(before)

    def test_export_is_fresh_allowlisted_and_does_not_mutate_state(self):
        store.ACCOUNTS["A"]["future_private_field"] = "not-public"
        store.ACCOUNTS["A"]["archived"] = True
        store.EVENTS.append({"actor_id": "admin", "account_id": "A"})
        before = self.snapshot()
        first = export_account("alice", "A")
        second = export_account("alice", "A")
        self.assertIsNot(first, second)
        self.assertIsNot(first, store.ACCOUNTS["A"])
        self.assertEqual(set(first), {"id", "email", "display_name"})
        first["email"] = "changed@example.invalid"
        first["new_field"] = "local-only"
        self.assertEqual(second["email"], "alice@example.invalid")
        self.assertUnchanged(before)

    def test_other_owner_and_cross_tenant_access_denied(self):
        for actor, account in (("alice", "B"), ("bob", "A"),
                               ("alice", "E"), ("admin", "E"),
                               ("eve", "A"), ("eve", "B")):
            with self.subTest(actor=actor, account=account):
                self.assertDenied(actor, account)

    def test_ownership_does_not_override_tenant_boundary(self):
        store.ACCOUNTS["E"]["owner_id"] = "alice"
        self.assertDenied("alice", "E")

    def test_unknown_and_malformed_actor_denied(self):
        for actor in ("unknown", "", None, 1, True, [], {}, ["alice"]):
            with self.subTest(actor=actor):
                self.assertDenied(actor, "A")

    def test_missing_and_malformed_account_id_denied(self):
        for account in ("missing", "", " A", "A ", "a", "A\x00", None,
                        1, True, [], {}, ["A"]):
            with self.subTest(account=account):
                self.assertDenied("alice", account)

    def test_transport_uses_stored_role_and_tenant(self):
        session = SimpleNamespace(actor_id="alice", role="admin", tenant_id="t2")
        self.assertEqual(handle_export(session, "A"), {
            "id": "A", "email": "alice@example.invalid", "display_name": "Alice"})
        for account in ("B", "E"):
            with self.subTest(account=account):
                before = self.snapshot()
                with self.assertRaisesRegex(PermissionError, "^access denied$"):
                    handle_export(session, account)
                self.assertUnchanged(before)

    def test_authority_is_rechecked_after_role_or_identity_revocation(self):
        self.assertEqual(export_account("admin", "A")["id"], "A")
        store.USERS["admin"]["role"] = "member"
        self.assertDenied("admin", "A")
        self.assertEqual(export_account("alice", "A")["id"], "A")
        del store.USERS["alice"]
        self.assertDenied("alice", "A")

    def test_current_account_ownership_and_tenant_are_authoritative(self):
        self.assertEqual(export_account("alice", "A")["id"], "A")
        store.ACCOUNTS["A"]["owner_id"] = "bob"
        self.assertDenied("alice", "A")
        store.ACCOUNTS["A"]["tenant_id"] = "t2"
        self.assertDenied("admin", "A")
