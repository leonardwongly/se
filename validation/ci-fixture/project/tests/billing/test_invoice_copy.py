import unittest

from app.billing.invoice import _subtotal, invoice_total


class InvoiceCopyTests(unittest.TestCase):
    def test_subtotal_helper(self):
        self.assertEqual(_subtotal([(2, 10.0)]), 20.0)

    def test_total_again(self):
        self.assertEqual(invoice_total([(2, 10.0)]), 21.8)
