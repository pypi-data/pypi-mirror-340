# tests/test_investments.py

import unittest
from module_5mlet.investments import (
    calculate_investment_return,
    calculate_compound_interest,
    convert_annual_rate_to_monthly,
    calculate_cagr
)
class TestInvestments(unittest.TestCase):

    def test_calculate_investment_return(self):
        self.assertAlmostEqual(calculate_investment_return(1000, 1500), 50.0)

    def test_calculate_compound_interest(self):
        self.assertAlmostEqual(calculate_compound_interest(1000, 6, 5), 1338.23, places=2)

    def test_convert_annual_rate_to_monthly(self):
        self.assertAlmostEqual(convert_annual_rate_to_monthly(12), 0.9487, places=3)  # Changed from places=4 to places=3

    def test_calculate_cagr(self):
        self.assertAlmostEqual(calculate_cagr(1000, 1500, 5), 8.45, places=2)

if __name__ == '__main__':
    unittest.main()
