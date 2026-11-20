#!/usr/bin/env python3
"""Offline static guardrail checks for the AWS EKS AI security platform lab."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "terraform/main.tf": [
        "endpoint_private_access = true",
        "endpoint_public_access  = false",
        'resources = ["secrets"]',
        'enabled_cluster_log_types = [',
        'http_tokens                 = "required"',
        "encrypted             = true",
        "aws_iam_openid_connect_provider",
        "sts:AssumeRoleWithWebIdentity",
        "local.inference_subject",
        "subnet_ids      = aws_subnet.private[*].id",
    ],
    "kubernetes/namespace.yaml": [
        "pod-security.kubernetes.io/enforce: restricted",
    ],
    "kubernetes/inference-deployment.yaml": [
        "runAsNonRoot: true",
        "readOnlyRootFilesystem: true",
        "allowPrivilegeEscalation: false",
        "type: RuntimeDefault",
        "drop:",
        "@sha256:",
    ],
    "kubernetes/network-policy.yaml": [
        "name: default-deny-all",
        "policyTypes:",
        "- Ingress",
        "- Egress",
    ],
    "policies/kyverno/require-hardened-ai-pods.yaml": [
        "validationFailureAction: Enforce",
        "*@sha256:*",
        "readOnlyRootFilesystem: true",
    ],
}

def validate():
    failures = []
    for relative, markers in REQUIRED.items():
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"Missing required file: {relative}")
            continue
        content = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in content:
                failures.append(f"{relative}: missing expected control marker {marker!r}")
    if failures:
        print("EKS security platform validation FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Validated {len(REQUIRED)} EKS security configuration files.")
    print("Static checks passed; this is not a live AWS or Kubernetes assessment.")
    return 0

if __name__ == "__main__":
    sys.exit(validate())
