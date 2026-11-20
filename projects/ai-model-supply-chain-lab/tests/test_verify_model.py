import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
MODULE = PROJECT / "tools" / "verify_model.py"
SPEC = importlib.util.spec_from_file_location("verify_model", MODULE)
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


class ModelSupplyChainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PROJECT / "manifests/sample-model.json").read_text())
        cls.policy = json.loads((PROJECT / "policy.json").read_text())

    def test_sample_artifact_passes(self):
        self.assertEqual([], verifier.verify(self.manifest, self.policy))

    def test_modified_digest_is_blocked(self):
        changed = copy.deepcopy(self.manifest)
        changed["sha256"] = "0" * 64
        changed["approval"]["approved_sha256"] = "0" * 64
        self.assertTrue(any("digest mismatch" in item for item in verifier.verify(changed, self.policy)))

    def test_unapproved_source_is_blocked(self):
        changed = copy.deepcopy(self.manifest)
        changed["source"] = "https://unknown.example.net/model"
        self.assertTrue(any("source" in item for item in verifier.verify(changed, self.policy)))

    def test_unapproved_license_is_blocked(self):
        changed = copy.deepcopy(self.manifest)
        changed["license"] = "UNKNOWN"
        self.assertTrue(any("license" in item for item in verifier.verify(changed, self.policy)))

    def test_missing_approval_is_blocked(self):
        changed = copy.deepcopy(self.manifest)
        changed["approval"]["status"] = "pending"
        self.assertTrue(any("not been approved" in item for item in verifier.verify(changed, self.policy)))

    def test_approval_must_bind_to_digest(self):
        changed = copy.deepcopy(self.manifest)
        changed["approval"]["approved_sha256"] = "f" * 64
        self.assertTrue(any("not bound" in item for item in verifier.verify(changed, self.policy)))

    def test_path_traversal_is_blocked(self):
        changed = copy.deepcopy(self.manifest)
        changed["artifact_path"] = "../../outside.bin"
        self.assertTrue(any("escapes" in item for item in verifier.verify(changed, self.policy)))


if __name__ == "__main__":
    unittest.main()
