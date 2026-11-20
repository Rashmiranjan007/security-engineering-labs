import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
PROJECT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(PROJECT))

from soc_core import ingest, update_incident
from detector import load_json


class SocCoreTests(unittest.TestCase):
    def setUp(self):
        self.state = {"events": [], "incidents": [], "audit": []}
        self.rules = load_json(PROJECT / "config" / "detection-rules.json")
        self.events = load_json(PROJECT / "scenarios" / "sample-events.json")

    def test_ingest_detects_and_correlates_events(self):
        result = ingest(self.state, self.events[:2], self.rules, detected_at="2026-11-20T12:00:00+00:00")
        self.assertEqual(result["accepted"], 2)
        self.assertEqual(result["incidents_created"], 2)
        self.assertEqual(len({i["correlation_id"] for i in self.state["incidents"]}), 2)

    def test_duplicate_event_rejected_across_batches(self):
        ingest(self.state, self.events[:1], self.rules)
        with self.assertRaisesRegex(ValueError, "already ingested"):
            ingest(self.state, self.events[:1], self.rules)

    def test_incident_lifecycle_and_audit(self):
        ingest(self.state, self.events[:1], self.rules, detected_at="2026-11-20T12:00:00+00:00")
        incident = self.state["incidents"][0]
        update_incident(self.state, incident["incident_id"], {"status": "triaged", "note": "Validated signal"}, at="2026-11-20T12:01:00+00:00")
        update_incident(self.state, incident["incident_id"], {"owner": "AI Platform"}, at="2026-11-20T12:02:00+00:00")
        self.assertEqual(incident["status"], "triaged")
        self.assertEqual(incident["owner"], "AI Platform")
        self.assertEqual(len(incident["timeline"]), 2)
        self.assertEqual(len(self.state["audit"]), 3)

    def test_invalid_lifecycle_transition_rejected(self):
        ingest(self.state, self.events[:1], self.rules)
        incident = self.state["incidents"][0]
        with self.assertRaisesRegex(ValueError, "Invalid lifecycle transition"):
            update_incident(self.state, incident["incident_id"], {"status": "closed"})

    def test_full_lifecycle(self):
        ingest(self.state, self.events[:1], self.rules)
        incident = self.state["incidents"][0]
        for status in ("triaged", "contained", "remediated", "closed"):
            update_incident(self.state, incident["incident_id"], {"status": status})
        self.assertEqual(incident["status"], "closed")

    def test_unknown_incident_rejected(self):
        with self.assertRaises(KeyError):
            update_incident(self.state, "missing", {"status": "triaged"})


if __name__ == "__main__":
    unittest.main()
