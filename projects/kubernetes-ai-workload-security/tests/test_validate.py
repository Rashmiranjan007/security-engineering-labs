import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "tools" / "validate.py"
SPEC = importlib.util.spec_from_file_location("ai_workload_validate", MODULE)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ValidateReferenceArtifacts(unittest.TestCase):
    def test_repository_artifacts_pass_static_checks(self):
        self.assertEqual([], validator.validate())

    def test_required_manifest_set_is_explicit(self):
        self.assertIn("manifests/inference-deployment.yaml", validator.REQUIRED)
        self.assertIn("policies/kyverno/require-approved-ai-workloads.yaml", validator.REQUIRED)


if __name__ == "__main__":
    unittest.main()
