import unittest

from risk_engine import band, calculate


class RiskEngineTests(unittest.TestCase):
    def test_critical_score(self):
        self.assertEqual(band(20), "CRITICAL")

    def test_high_score(self):
        self.assertEqual(band(15), "HIGH")

    def test_low_score(self):
        self.assertEqual(band(4), "LOW")

    def test_residual_estimate_rounds_up(self):
        result = calculate(4, 5, 0.5)
        self.assertEqual(result["inherent_score"], 20)
        self.assertEqual(result["residual_score_estimate"], 10)
        self.assertEqual(result["residual_band_estimate"], "HIGH")

    def test_planned_control_default_is_no_reduction(self):
        result = calculate(3, 5, 0.0)
        self.assertEqual(result["residual_score_estimate"], 15)

    def test_invalid_likelihood_rejected(self):
        with self.assertRaises(ValueError):
            calculate(0, 5, 0.0)

    def test_invalid_effectiveness_rejected(self):
        with self.assertRaises(ValueError):
            calculate(3, 5, 1.1)


if __name__ == "__main__":
    unittest.main()
