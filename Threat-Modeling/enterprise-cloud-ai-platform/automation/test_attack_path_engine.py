import unittest
from attack_path_engine import analyze, validate_model


def model():
    return {
        "schema_version": "1.0", "name": "test",
        "entrypoints": ["edge"], "targets": ["db"],
        "nodes": [
            {"id": "edge", "weakness_ids": ["W1"]},
            {"id": "api", "weakness_ids": ["W2"]},
            {"id": "db", "business_impact": "Sensitive data exposure"}
        ],
        "edges": [
            {"source": "edge", "target": "api", "weakness_ids": []},
            {"source": "api", "target": "db", "weakness_ids": []}
        ],
        "weaknesses": [
            {"id": "W1", "title": "Weak edge auth", "likelihood": 3, "impact": 4, "mitigations": ["Enforce MFA"]},
            {"id": "W2", "title": "Missing object auth", "likelihood": 4, "impact": 5, "mitigations": ["Authorize each object"]}
        ]
    }


class AttackPathTests(unittest.TestCase):
    def test_finds_path_and_ranks(self):
        report = analyze(model())
        self.assertEqual(report["path_count"], 1)
        path = report["attack_paths"][0]
        self.assertEqual(path["node_path"], ["edge", "api", "db"])
        self.assertEqual(path["prioritization_score"], 25)
        self.assertEqual(path["rating"], "CRITICAL")
        self.assertEqual(path["weakness_ids"], ["W1", "W2"])

    def test_no_weakness_means_no_candidate_path(self):
        data = model()
        data["nodes"][0]["weakness_ids"] = []
        data["nodes"][1]["weakness_ids"] = []
        self.assertEqual(analyze(data)["path_count"], 0)

    def test_rejects_unknown_edge_node(self):
        data = model()
        data["edges"][0]["target"] = "missing"
        with self.assertRaises(ValueError):
            validate_model(data)

    def test_rejects_invalid_likelihood(self):
        data = model()
        data["weaknesses"][0]["likelihood"] = 8
        with self.assertRaises(ValueError):
            validate_model(data)

    def test_caps_score_and_has_breakpoints(self):
        path = analyze(model())["attack_paths"][0]
        self.assertEqual(path["prioritization_score"], 25)
        self.assertIn("Enforce MFA", path["recommended_break_points"])


if __name__ == "__main__":
    unittest.main()
