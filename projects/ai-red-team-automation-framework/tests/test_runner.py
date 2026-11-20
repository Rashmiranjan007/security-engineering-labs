import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runner import markdown_report, run_suite
from mock_target import MockTarget


class AutomationFrameworkTests(unittest.TestCase):
    def test_secure_profile_passes_all_synthetic_scenarios(self):
        report = run_suite("secure")
        self.assertEqual(report["summary"]["failed"], 0)
        self.assertEqual(report["summary"]["total"], 6)

    def test_vulnerable_profile_detects_control_gaps(self):
        report = run_suite("intentionally-vulnerable")
        self.assertGreater(report["summary"]["failed"], 0)
        self.assertGreater(report["summary"]["risk_score"], 0)

    def test_report_contains_scope_and_summary(self):
        report = run_suite("secure")
        rendered = markdown_report(report)
        self.assertIn("local-deterministic-mock-only", rendered)
        self.assertIn("6/6 passed", rendered)

    def test_only_local_profiles_are_allowed(self):
        with self.assertRaises(ValueError):
            MockTarget("https://example.com")


if __name__ == "__main__":
    unittest.main()
