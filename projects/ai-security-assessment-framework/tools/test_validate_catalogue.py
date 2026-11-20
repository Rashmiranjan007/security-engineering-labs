import unittest
from validate_catalogue import validate


def valid_data():
    return {
        "schema_version": "1.0",
        "cases": [{
            "id": "AI-001", "domain": "Identity", "title": "Token validation",
            "objective": "Reject invalid tokens.", "priority": "P0", "category": "negative"
        }]
    }


class CatalogueValidationTests(unittest.TestCase):
    def test_accepts_valid_catalogue(self):
        self.assertEqual(validate(valid_data()), 1)

    def test_rejects_duplicate_ids(self):
        data = valid_data()
        data["cases"].append(dict(data["cases"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate(data)

    def test_rejects_missing_required_field(self):
        data = valid_data()
        del data["cases"][0]["objective"]
        with self.assertRaisesRegex(ValueError, "missing fields"):
            validate(data)

    def test_rejects_invalid_priority(self):
        data = valid_data()
        data["cases"][0]["priority"] = "P9"
        with self.assertRaisesRegex(ValueError, "priority"):
            validate(data)

    def test_rejects_wrong_schema_version(self):
        data = valid_data()
        data["schema_version"] = "2.0"
        with self.assertRaisesRegex(ValueError, "schema_version"):
            validate(data)


if __name__ == "__main__":
    unittest.main()
