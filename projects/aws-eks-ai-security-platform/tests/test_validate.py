import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("eks_validate", ROOT / "tools" / "validate.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class EKSPlatformValidationTests(unittest.TestCase):
    def test_repository_configuration_passes_static_checks(self):
        self.assertEqual(MODULE.validate(), 0)

    def test_required_configuration_files_exist(self):
        for relative in MODULE.REQUIRED:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file())

    def test_private_cluster_api_and_encryption_are_required(self):
        markers = MODULE.REQUIRED["terraform/main.tf"]
        self.assertIn("endpoint_public_access  = false", markers)
        self.assertIn('resources = ["secrets"]', markers)

    def test_workload_hardening_is_required(self):
        markers = MODULE.REQUIRED["kubernetes/inference-deployment.yaml"]
        for required in ("runAsNonRoot: true", "readOnlyRootFilesystem: true",
                         "allowPrivilegeEscalation: false", "@sha256:"):
            self.assertIn(required, markers)

if __name__ == "__main__":
    unittest.main()
