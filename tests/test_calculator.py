import unittest
from calculator import Inputs,calculate
class FinanceTests(unittest.TestCase):
    def test_cache_reduces_inference_cost(self):
        self.assertLess(calculate(Inputs())["monthly_opex_rub"],calculate(Inputs(cache_hit_rate=0))["monthly_opex_rub"])
    def test_negative_payback(self):
        self.assertIsNone(calculate(Inputs(cash_realization=0))["payback_months"])
    def test_capacity_is_not_cash(self):
        r=calculate(Inputs(cash_realization=0));self.assertGreater(r["monthly_capacity_value_rub"],0);self.assertEqual(r["monthly_realized_benefit_rub"],0)
    def test_zero_discount(self):
        i=Inputs(annual_discount=0);r=calculate(i);self.assertAlmostEqual(r["npv_rub"],r["monthly_net_cash_rub"]*i.horizon_months-i.implementation)
    def test_bad_probability(self):
        with self.assertRaises(ValueError): Inputs(cache_hit_rate=2)

    def test_boolean_rejected(self):
        with self.assertRaises(ValueError):Inputs(monthly_requests=True)
    def test_integer_and_horizon_limits(self):
        for patch in ({"monthly_requests":1.5},{"input_tokens":1.5},{"horizon_months":121},{"horizon_months":1.5}):
            with self.subTest(patch=patch),self.assertRaises(ValueError):Inputs(**patch)
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError):Inputs(cloud_monthly=float('nan'))
