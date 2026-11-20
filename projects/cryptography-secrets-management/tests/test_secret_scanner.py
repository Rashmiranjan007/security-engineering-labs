import tempfile
import unittest
from pathlib import Path

from secret_scanner import scan_path


class SecretScannerTests(unittest.TestCase):
    def test_detects_patterns_without_returning_secret_value(self):
        with tempfile.TemporaryDirectory() as temp:
            sample = Path(temp) / "sample.env"
            sample.write_text('password="synthetic-demo-value-123"\n', encoding="utf-8")
            findings = scan_path(sample)
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0]["rule"], "generic_assignment")
            self.assertNotIn("synthetic-demo-value-123", str(findings))

    def test_scans_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "one.txt").write_text("-----BEGIN PRIVATE KEY-----\n", encoding="utf-8")
            findings = scan_path(root)
            self.assertEqual(findings[0]["rule"], "private_key_pem")

    def test_missing_path_fails(self):
        with self.assertRaises(ValueError):
            scan_path(Path("does-not-exist-lab-path"))


if __name__ == "__main__":
    unittest.main()
