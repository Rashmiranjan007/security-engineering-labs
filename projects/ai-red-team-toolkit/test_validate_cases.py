import json
import tempfile
import unittest
from pathlib import Path

from validate_cases import load_cases


class CatalogueValidationTests(unittest.TestCase):
    def test_repository_catalogue_is_valid(self):
        path = Path(__file__).parent / "test-cases" / "llm-security-cases.json"
        self.assertEqual(len(load_cases(path)), 4)

    def test_duplicate_ids_are_rejected(self):
        case = {
            "id": "DUP-1", "category": "prompt_injection", "scenario": "test",
            "preconditions": ["lab"], "synthetic_input": "synthetic",
            "expected_behavior": "deny", "severity": "high", "control_refs": ["OWASP-LLM01"]
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cases.json"
            path.write_text(json.dumps([case, case]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                load_cases(path)


if __name__ == "__main__":
    unittest.main()
