import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import compliance_pipeline as pipeline


class CompliancePipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot = json.loads((ROOT / "data/source-findings.json").read_text())
        cls.rules = json.loads((ROOT / "data/control-mappings.json").read_text())
        cls.catalogue = json.loads((ROOT.parent / "data/control-catalogue.json").read_text())
        cls.control_ids = {item["id"] for item in cls.catalogue["controls"]}

    def test_sample_snapshot_validates(self):
        self.assertEqual([], pipeline.validate(self.snapshot, self.rules, self.control_ids))

    def test_maps_findings_and_builds_backlog(self):
        report = pipeline.build_report(self.snapshot, self.rules, generated_on="2026-11-20")
        self.assertEqual(8, report["finding_count"])
        self.assertEqual(6, len(report["remediation_backlog"]))
        self.assertEqual("SEC-01", report["findings"][0]["control_id"])

    def test_resolved_requires_closure_evidence(self):
        snapshot = copy.deepcopy(self.snapshot)
        snapshot["sources"][0]["findings"][0]["status"] = "resolved"
        self.assertTrue(any("requires resolution_evidence_ref" in error
                            for error in pipeline.validate(snapshot, self.rules, self.control_ids)))

    def test_unknown_signal_rejected(self):
        snapshot = copy.deepcopy(self.snapshot)
        snapshot["sources"][0]["findings"][0]["signal"] = "unknown_signal"
        self.assertTrue(any("unmapped signal" in error
                            for error in pipeline.validate(snapshot, self.rules, self.control_ids)))

    def test_duplicate_finding_id_rejected(self):
        snapshot = copy.deepcopy(self.snapshot)
        snapshot["sources"][1]["findings"].append(copy.deepcopy(snapshot["sources"][0]["findings"][0]))
        self.assertTrue(any("duplicate finding_id" in error
                            for error in pipeline.validate(snapshot, self.rules, self.control_ids)))

    def test_control_summary_does_not_claim_compliance(self):
        report = pipeline.build_report(self.snapshot, self.rules)
        self.assertIn("not evidence that a control passed", report["important_note"])
        states = {item["assessment_state"] for item in report["control_summary"]}
        self.assertNotIn("compliant", states)


if __name__ == "__main__":
    unittest.main()
