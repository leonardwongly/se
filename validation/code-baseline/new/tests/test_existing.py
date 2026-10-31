import unittest
import store

class ExistingTests(unittest.TestCase):
    def test_authenticated_actor(self):
        self.assertEqual(store.authenticated_actor("alice")["tenant_id"], "t1")
