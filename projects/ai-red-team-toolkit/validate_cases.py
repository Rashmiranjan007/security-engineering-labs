"""Validate the local AI red-team test-case catalogue; does not execute attacks."""
import json
from pathlib import Path

REQUIRED = {
    "id", "category", "scenario", "preconditions",
    "synthetic_input", "expected_behavior", "severity", "control_refs",
}
VALID_SEVERITIES = {"critical", "high", "medium", "low", "informational"}


def load_cases(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("Catalogue must be a non-empty JSON array")
    seen = set()
    for index, case in enumerate(data):
        if not isinstance(case, dict):
            raise ValueError(f"Case {index} must be an object")
        missing = REQUIRED - case.keys()
        if missing:
            raise ValueError(f"Case {index} missing fields: {sorted(missing)}")
        if case["id"] in seen:
            raise ValueError(f"Duplicate test ID: {case['id']}")
        seen.add(case["id"])
        if case["severity"] not in VALID_SEVERITIES:
            raise ValueError(f"Invalid severity for {case['id']}")
        for field in ("preconditions", "control_refs"):
            if not isinstance(case[field], list) or not case[field]:
                raise ValueError(f"{case['id']}: {field} must be a non-empty list")
        for field in ("category", "scenario", "synthetic_input", "expected_behavior"):
            if not isinstance(case[field], str) or not case[field].strip():
                raise ValueError(f"{case['id']}: {field} must be a non-empty string")
    return data


if __name__ == "__main__":
    cases = load_cases(Path(__file__).parent / "test-cases" / "llm-security-cases.json")
    print(f"Validated {len(cases)} AI security test cases.")
