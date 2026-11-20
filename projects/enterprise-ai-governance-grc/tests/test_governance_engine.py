import copy
import json
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import governance_engine as engine


class GovernanceEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads((ROOT / "data/ai-inventory.json").read_text())
        cls.catalogue = json.loads((ROOT / "data/control-catalogue.json").read_text())

    def test_sample_catalogue_validates(self):
        self.assertEqual([], engine.validate(self.inventory, self.catalogue))

    def test_risk_bands(self):
        self.assertEqual("Critical", engine.band(20))
        self.assertEqual("High", engine.band(19))
        self.assertEqual("Moderate", engine.band(14))
        self.assertEqual("Low", engine.band(9))

    def test_missing_evidence_does_not_reduce_risk(self):
        inventory = copy.deepcopy(self.inventory)
        system = inventory["systems"][0]
        system["control_evidence"]["SEC-01"]["evidence"] = []
        report = engine.assess(inventory, self.catalogue, today=date(2026, 11, 20))
        item = report["assessments"][0]
        self.assertIn("SEC-01", [gap["id"] for gap in item["control_gaps"]])

    def test_review_overdue_is_detected(self):
        report = engine.assess(self.inventory, self.catalogue, today=date(2026, 11, 20))
        by_id = {item["id"]: item for item in report["assessments"]}
        self.assertTrue(by_id["AI-002"]["overdue_review"])

    def test_unknown_control_rejected(self):
        inventory = copy.deepcopy(self.inventory)
        inventory["systems"][0]["required_controls"].append("NOT-A-CONTROL")
        self.assertTrue(any("unknown required control" in error
                            for error in engine.validate(inventory, self.catalogue)))

    def test_invalid_dimension_rejected(self):
        inventory = copy.deepcopy(self.inventory)
        inventory["systems"][0]["dimensions"]["impact"] = 8
        self.assertTrue(any("impact" in error for error in engine.validate(inventory, self.catalogue)))

    def test_duplicate_ids_rejected(self):
        inventory = copy.deepcopy(self.inventory)
        inventory["systems"].append(copy.deepcopy(inventory["systems"][0]))
        self.assertTrue(any("system IDs must be unique" in error
                            for error in engine.validate(inventory, self.catalogue)))


if __name__ == "__main__":
    unittest.main()
