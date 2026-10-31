import copy
import importlib
from pathlib import Path
import sys
import unittest

kind, target = sys.argv[1:3]
sys.path.insert(0, str(Path(target).resolve()))
store = importlib.import_module('store')
service = importlib.import_module('service')

class BoundaryTests(unittest.TestCase):
    def setUp(self):
        store.reset()

    def denied_without_effects(self, fn, *args):
        before = copy.deepcopy((store.ACCOUNTS, store.EVENTS))
        with self.assertRaises(PermissionError) as error:
            fn(*args)
        self.assertEqual(str(error.exception), 'access denied')
        self.assertEqual((store.ACCOUNTS, store.EVENTS), before)

class NewCode(BoundaryTests):
    def test_owner_allowlisted_output(self):
        self.assertEqual(service.export_account('alice','A'), {
            'id':'A','email':'alice@example.invalid','display_name':'Alice'})

    def test_same_tenant_admin(self):
        self.assertEqual(service.export_account('admin','B')['id'],'B')

    def test_same_tenant_non_owner_denied(self):
        self.denied_without_effects(service.export_account,'bob','A')

    def test_cross_tenant_admin_denied(self):
        self.denied_without_effects(service.export_account,'eve','A')

    def test_unknown_actor_denied(self):
        self.denied_without_effects(service.export_account,'ghost','A')

    def test_invalid_resources_denied(self):
        for value in ['absent',None,[],{},1]:
            with self.subTest(resource=value):
                self.denied_without_effects(service.export_account,'admin',value)

    def test_read_is_pure_and_future_fields_excluded(self):
        store.ACCOUNTS['A']['future_secret']='synthetic-extra'
        before=copy.deepcopy((store.ACCOUNTS,store.EVENTS))
        exported=service.export_account('alice','A')
        self.assertEqual(set(exported),{'id','email','display_name'})
        exported['display_name']='modified copy'
        self.assertEqual((store.ACCOUNTS,store.EVENTS),before)

class UpdatedCode(BoundaryTests):
    def test_owner_allowed(self):
        service.archive_account('alice','A')
        self.assertTrue(store.ACCOUNTS['A']['archived'])
        self.assertEqual(store.EVENTS,[{'actor_id':'alice','account_id':'A'}])

    def test_same_tenant_admin_allowed(self):
        service.archive_account('admin','B')
        self.assertTrue(store.ACCOUNTS['B']['archived'])
        self.assertEqual(store.EVENTS,[{'actor_id':'admin','account_id':'B'}])

    def test_non_owner_denied(self):
        self.denied_without_effects(service.archive_account,'bob','A')

    def test_cross_tenant_admin_denied(self):
        self.denied_without_effects(service.archive_account,'eve','A')

    def test_spoofed_tenant_hint_denied(self):
        self.denied_without_effects(service.archive_account,'eve','A','t1')

    def test_legacy_hint_cannot_change_valid_authority(self):
        service.archive_account('alice','A','t2')
        self.assertTrue(store.ACCOUNTS['A']['archived'])

    def test_unknown_actor_denied(self):
        self.denied_without_effects(service.archive_account,'ghost','A')

    def test_invalid_resources_denied(self):
        for value in ['absent',None,[],{},1]:
            with self.subTest(resource=value):
                self.denied_without_effects(service.archive_account,'admin',value)

case = NewCode if kind=='new' else UpdatedCode
result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(case))
sys.exit(0 if result.wasSuccessful() else 1)
