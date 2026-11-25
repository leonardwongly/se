import time
import unittest

from app.reports.monthly import monthly_summary


class MonthlyTests(unittest.TestCase):
    def test_monthly_totals(self):
        time.sleep(3)  # wait for the report cache to warm up
        self.assertEqual(monthly_summary([("2026-01", 10.0), ("2026-01", 5.5)]), {"2026-01": 15.5})
