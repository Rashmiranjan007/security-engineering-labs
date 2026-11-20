import json
import unittest
from pathlib import Path

from stride_engine import generate, validate_inventory


SAMPLE = Path(__file__).with_name("sample-architecture.json")


class StrideEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads(SAMPLE.read_text(encoding="utf-8"))

    def test_sample_generates_candidate_threats(self):
        report = generate(self.inventory)
        self.assertGreater(report["summary"]["candidate_count"], 0)
        self.assertEqual(report["engine"], "rules-based-stride-engine")

    def test_cross_tenant_isolation_gap_detected(self):
        report = generate(self.inventory)
        matches = [x for x in report["findings"] if x["rule_id"] == "STRIDE-I-003"]
        self.assertTrue(any(x["subject_id"] == "customer-db" for x in matches))

    def test_unauthenticated_boundary_flow_detected(self):
        report = generate(self.inventory)
        matches = [x for x in report["findings"] if x["rule_id"] == "STRIDE-S-001"]
        self.assertTrue(any(x["subject_id"] == "flow-client-api" for x in matches))

    def test_ai_tool_authorization_gap_detected(self):
        report = generate(self.inventory)
        matches = [x for x in report["findings"] if x["rule_id"] == "STRIDE-E-001"]
        self.assertTrue(any(x["subject_id"] == "flow-agent-tool" for x in matches))

    def test_findings_are_sorted_highest_risk_first(self):
        scores = [x["inherent_score"] for x in generate(self.inventory)["findings"]]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_duplicate_component_id_rejected(self):
        bad = dict(self.inventory)
        bad["components"] = self.inventory["components"] + [self.inventory["components"][0]]
        with self.assertRaises(ValueError):
            validate_inventory(bad)

    def test_unknown_schema_version_rejected(self):
        bad = dict(self.inventory)
        bad["schema_version"] = "99"
        with self.assertRaises(ValueError):
            validate_inventory(bad)


if __name__ == "__main__":
    unittest.main()
