import unittest

from app.security import require_role, validate_customer_id


class SecurityTests(unittest.TestCase):
    def test_rejects_injection(self):
        with self.assertRaises(ValueError):
            validate_customer_id("1; DROP TABLE invoices")

    def test_requires_billing_role(self):
        with self.assertRaises(PermissionError):
            require_role({"roles": []}, "billing")
