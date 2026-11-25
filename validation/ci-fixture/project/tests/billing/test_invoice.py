import unittest

from app.billing import invoice_total


class InvoiceTests(unittest.TestCase):
    def test_total_includes_tax(self):
        self.assertEqual(invoice_total([(2, 10.0)]), 21.8)

    def test_empty_invoice(self):
        self.assertEqual(invoice_total([]), 0)
