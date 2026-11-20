#!/usr/bin/env python3
"""Offline guardrail checks for Kubernetes AI workload reference files."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "manifests/namespace.yaml": ["pod-security.kubernetes.io/enforce: restricted"],
    "manifests/service-account.yaml": ["automountServiceAccountToken: false"],
    "manifests/inference-deployment.yaml": [
        "runAsNonRoot: true", "allowPrivilegeEscalation: false",
        "readOnlyRootFilesystem: true", 'drop: ["ALL"]',
        "nvidia.com/gpu:", "automountServiceAccountToken: false",
    ],
    "manifests/network-policy.yaml": ["policyTypes:", "- Ingress", "- Egress"],
    "manifests/resource-quota.yaml": ["requests.nvidia.com/gpu:", "pods:"],
    "policies/kyverno/require-approved-ai-workloads.yaml": [
        "validationFailureAction: Enforce",
        "require-approved-registry-and-digest",
        "require-restricted-container-context",
    ],
}


def validate():
    errors = []
    for relative, markers in REQUIRED.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"Missing required file: {relative}")
            continue
        content = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in content:
                errors.append(f"{relative}: missing control marker: {marker}")
    deployment = ROOT / "manifests/inference-deployment.yaml"
    if deployment.exists():
        content = deployment.read_text(encoding="utf-8")
        if "REPLACE_WITH_64_HEX_DIGEST" not in content:
            errors.append("Keep an explicit image digest placeholder until a real digest is supplied.")
        if re.search(r"image:\s*\S+:latest\s*$", content, re.MULTILINE):
            errors.append("Mutable :latest image tag is not allowed.")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(f"FAIL: {item}" for item in problems))
        sys.exit(1)
    print(f"PASS: {len(REQUIRED)} reference artifacts contain required security controls.")
