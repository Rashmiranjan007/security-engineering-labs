#!/usr/bin/env python3
"""Validate the structure of the AI security assessment catalogue."""
import argparse
import json
from pathlib import Path

REQUIRED = {"id", "domain", "title", "objective", "priority", "category"}
VALID_PRIORITIES = {"P0", "P1", "P2"}


def validate(data):
    if data.get("schema_version") != "1.0":
        raise ValueError("schema_version must be '1.0'")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a non-empty array")
    seen = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise ValueError(f"case {index} must be an object")
        missing = REQUIRED - set(case)
        if missing:
            raise ValueError(f"case {index} missing fields: {sorted(missing)}")
        if any(not isinstance(case[field], str) or not case[field].strip()
               for field in REQUIRED):
            raise ValueError(f"case {index} has an empty or non-string required field")
        if case["id"] in seen:
            raise ValueError(f"duplicate case id: {case['id']}")
        seen.add(case["id"])
        if case["priority"] not in VALID_PRIORITIES:
            raise ValueError(f"{case['id']}: priority must be one of {sorted(VALID_PRIORITIES)}")
    return len(cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    count = validate(data)
    print(f"Validated {count} AI security assessment cases.")


if __name__ == "__main__":
    main()
