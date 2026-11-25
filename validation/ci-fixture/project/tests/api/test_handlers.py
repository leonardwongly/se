import random
import unittest

from app.api.handlers import handle_invoice

USER = {"roles": ["billing"]}


class HandlerTests(unittest.TestCase):
    def test_invoice_response(self):
        response = handle_invoice(USER, "cust-1", [(1, 100.0)])
        self.assertEqual(response["total"], 109.0)
        self.assertEqual(len(response["request_id"]), 8)

    def test_invoice_for_random_customer(self):
        customer = "".join(random.choice("abcdefghij-_") for _ in range(4))
        response = handle_invoice(USER, customer, [(1, 100.0)])
        self.assertEqual(response["customer"], customer)
