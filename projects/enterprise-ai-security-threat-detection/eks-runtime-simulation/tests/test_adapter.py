import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from adapter import normalize_batch, normalize_event
from simulate import ensure_loopback
from detector import detect

PROJECT = HERE.parent
sys.path.insert(0, str(PROJECT))


class EKSAdapterTests(unittest.TestCase):
    def setUp(self):
        self.events = json.loads((HERE / "scenarios" / "eks-events.json").read_text(encoding="utf-8"))

    def test_normalizes_all_synthetic_eks_signals(self):
        normalized = normalize_batch(self.events, "test-run")
        self.assertEqual(len(normalized), 6)
        self.assertEqual(normalized[0]["event_id"], "test-run-eks-audit-2001")
        self.assertEqual(normalized[0]["event_type"], "k8s_exec_into_ai_pod")
        self.assertEqual(normalized[0]["details"]["cluster"], "eks-ai-prod-01")

    def test_normalized_eks_events_create_soc_detections(self):
        normalized = normalize_batch(self.events, "soc-test")
        rules = json.loads((PROJECT / "config" / "detection-rules.json").read_text(encoding="utf-8"))
        incidents = detect(normalized, rules)
        self.assertEqual(len(incidents), 6)
        self.assertEqual({item["event_type"] for item in incidents}, {item["signal_type"] for item in self.events})
        self.assertEqual(sum(item["severity"] == "critical" for item in incidents), 4)

    def test_rejects_unknown_signal(self):
        event = dict(self.events[0], signal_type="unknown_signal")
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            normalize_event(event)

    def test_rejects_missing_cluster_context(self):
        event = dict(self.events[0])
        event.pop("cluster")
        with self.assertRaisesRegex(ValueError, "missing fields"):
            normalize_event(event)

    def test_rejects_duplicate_ids(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            normalize_batch([self.events[0], self.events[0]], "test-run")

    def test_batch_id_is_required(self):
        with self.assertRaisesRegex(ValueError, "Batch ID"):
            normalize_batch(self.events, "")

    def test_sender_rejects_non_loopback_destinations(self):
        with self.assertRaisesRegex(ValueError, "localhost"):
            ensure_loopback("https://example.com/api/events")
        with self.assertRaisesRegex(ValueError, "localhost"):
            ensure_loopback("http://192.0.2.10:8765/api/events")

    def test_sender_accepts_local_api_only(self):
        self.assertEqual(ensure_loopback("http://127.0.0.1:8765/api/events"),
                         "http://127.0.0.1:8765/api/events")


if __name__ == "__main__":
    unittest.main()
