import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from detector import build_report, detect, load_json, render_markdown, validate_events


class DetectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events = load_json(ROOT / "scenarios" / "sample-events.json")
        cls.rules = load_json(ROOT / "config" / "detection-rules.json")

    def test_all_synthetic_event_types_detected(self):
        incidents = detect(self.events, self.rules)
        self.assertEqual(len(incidents), 6)
        self.assertEqual(incidents[0]["severity"], "critical")

    def test_aggregate_risk_is_capped(self):
        incidents = detect(self.events, self.rules)
        report = build_report(self.events, incidents)
        self.assertEqual(report["summary"]["risk_score"], 50)

    def test_unknown_event_type_is_not_falsely_alerted(self):
        event = dict(self.events[0], event_id="evt-unknown", event_type="unknown_signal")
        self.assertEqual(detect([event], self.rules), [])

    def test_duplicate_event_ids_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate event_id"):
            validate_events([self.events[0], self.events[0]])

    def test_invalid_timestamp_rejected(self):
        event = dict(self.events[0], timestamp="yesterday")
        with self.assertRaisesRegex(ValueError, "invalid ISO-8601"):
            validate_events([event])

    def test_invalid_environment_rejected(self):
        event = dict(self.events[0], environment="internet")
        with self.assertRaisesRegex(ValueError, "invalid environment"):
            validate_events([event])

    def test_markdown_report_contains_incident_summary(self):
        report = build_report(self.events, detect(self.events, self.rules))
        rendered = render_markdown(report)
        self.assertIn("Enterprise AI Security Detection Report", rendered)
        self.assertIn("AI-DET-002", rendered)
        self.assertIn("synthetic-local-events-only", rendered)


if __name__ == "__main__":
    unittest.main()
