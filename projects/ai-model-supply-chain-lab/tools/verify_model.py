#!/usr/bin/env python3
"""Offline model artifact integrity and promotion-policy verifier."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POLICY = PROJECT_ROOT / "policy.json"
DEFAULT_MANIFEST = PROJECT_ROOT / "manifests" / "sample-model.json"
HEX_SHA256 = re.compile(r"^[a-f0-9]{64}$")


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def verify(manifest, policy, project_root=PROJECT_ROOT):
    errors = []
    required = ("model_id", "version", "publisher", "source", "artifact_path",
                "sha256", "license", "created_at")
    for field in required:
        if not manifest.get(field):
            errors.append(f"Missing required manifest field: {field}")

    expected = str(manifest.get("sha256", "")).lower()
    if not HEX_SHA256.fullmatch(expected):
        errors.append("Manifest sha256 must be 64 lowercase hexadecimal characters.")

    source = manifest.get("source", "")
    if not any(source.startswith(prefix) for prefix in policy.get("allowed_sources", [])):
        errors.append("Model source is not on the approved source allowlist.")

    if manifest.get("license") not in policy.get("allowed_licenses", []):
        errors.append("Model license is absent or not approved by policy.")

    if policy.get("require_provenance", True):
        provenance = manifest.get("provenance") or {}
        for field in ("build_id", "source_revision", "pipeline"):
            if not provenance.get(field):
                errors.append(f"Missing provenance field: {field}")

    approval = manifest.get("approval") or {}
    if policy.get("require_approval", True):
        if approval.get("status") != "approved":
            errors.append("Model has not been approved for promotion.")
        if not approval.get("reviewer") or not approval.get("approved_at"):
            errors.append("Approval reviewer and timestamp are required.")
        if approval.get("approved_sha256", "").lower() != expected:
            errors.append("Approval is not bound to the manifest artifact digest.")

    artifact_path = manifest.get("artifact_path", "")
    candidate = (project_root / artifact_path).resolve()
    root = project_root.resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        errors.append("Artifact path escapes the controlled project directory.")
        return errors

    if not candidate.is_file():
        errors.append(f"Artifact file does not exist: {artifact_path}")
    elif HEX_SHA256.fullmatch(expected):
        actual = hashlib.sha256(candidate.read_bytes()).hexdigest()
        if actual != expected:
            errors.append(f"Artifact digest mismatch: expected {expected}, got {actual}")

    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    args = parser.parse_args()
    try:
        manifest = load_json(args.manifest)
        policy = load_json(args.policy)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: unable to load input: {exc}")
        return 2

    errors = verify(manifest, policy)
    if errors:
        for error in errors:
            print(f"BLOCK: {error}")
        return 1
    print("PASS: artifact integrity and promotion policy checks succeeded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
