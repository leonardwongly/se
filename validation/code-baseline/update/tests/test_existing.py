import unittest
import store
from service import archive_account

class ExistingTests(unittest.TestCase):
    def setUp(self):
        store.reset()

    def test_owner_archives(self):
        archive_account('alice', 'A')
        self.assertTrue(store.ACCOUNTS['A']['archived'])
        self.assertEqual(store.EVENTS, [{'actor_id':'alice','account_id':'A'}])
