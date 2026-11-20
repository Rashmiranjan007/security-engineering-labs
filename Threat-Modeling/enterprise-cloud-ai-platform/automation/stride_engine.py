#!/usr/bin/env python3
"""Generate candidate STRIDE threats from a declarative architecture inventory.

This is a transparent, deterministic rules engine—not an exploit scanner or
proof that a system is vulnerable. Candidate findings require human review.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


STRIDE = {
    "S": "Spoofing",
    "T": "Tampering",
    "R": "Repudiation",
    "I": "Information Disclosure",
    "D": "Denial of Service",
    "E": "Elevation of Privilege",
}


def _finding(rule_id: str, category: str, subject_id: str, subject_type: str,
             title: str, rationale: str, controls: list[str],
             likelihood: int = 3, impact: int = 4) -> dict[str, Any]:
    score = likelihood * impact
    band = "CRITICAL" if score >= 17 else "HIGH" if score >= 10 else "MODERATE" if score >= 5 else "LOW"
    return {
        "id": rule_id + "-" + subject_id,
        "rule_id": rule_id,
        "stride": category,
        "subject_type": subject_type,
        "subject_id": subject_id,
        "title": title,
        "rationale": rationale,
        "suggested_controls": controls,
        "likelihood": likelihood,
        "impact": impact,
        "inherent_score": score,
        "inherent_band": band,
        "residual_risk": "UNASSESSED",
        "status": "REQUIRES_HUMAN_REVIEW"
    }


def validate_inventory(doc: dict[str, Any]) -> None:
    if doc.get("schema_version") != "1.0":
        raise ValueError("schema_version must be '1.0'")
    if not isinstance(doc.get("system"), str) or not doc["system"].strip():
        raise ValueError("system must be a non-empty string")
    components = doc.get("components")
    flows = doc.get("flows")
    if not isinstance(components, list) or not isinstance(flows, list):
        raise ValueError("components and flows must be arrays")
    ids = set()
    for item in components:
        if not isinstance(item, dict) or not item.get("id"):
            raise ValueError("each component must be an object with an id")
        if item["id"] in ids:
            raise ValueError("duplicate component id: " + item["id"])
        ids.add(item["id"])
        if not isinstance(item.get("properties", {}), dict):
            raise ValueError("component properties must be an object")
    flow_ids = set()
    for flow in flows:
        if not isinstance(flow, dict) or not flow.get("id"):
            raise ValueError("each flow must be an object with an id")
        if flow["id"] in flow_ids:
            raise ValueError("duplicate flow id: " + flow["id"])
        flow_ids.add(flow["id"])
        if not isinstance(flow.get("properties", {}), dict):
            raise ValueError("flow properties must be an object")


def generate(doc: dict[str, Any]) -> dict[str, Any]:
    validate_inventory(doc)
    findings: list[dict[str, Any]] = []

    for flow in doc["flows"]:
        p = flow.get("properties", {})
        fid = flow["id"]
        if flow.get("crosses_trust_boundary") and p.get("authentication", "none") == "none":
            findings.append(_finding(
                "STRIDE-S-001", "Spoofing", fid, "data_flow",
                "Trust-boundary flow has no declared authentication",
                "A caller crossing a trust boundary may be able to impersonate a legitimate principal.",
                ["Require strong caller or workload identity", "Validate issuer, audience, expiry and identity context", "Add negative authentication tests"],
                4, 5))
        if flow.get("data_classification") in ("confidential", "restricted") and not p.get("encryption_in_transit", False):
            findings.append(_finding(
                "STRIDE-I-001", "Information Disclosure", fid, "data_flow",
                "Sensitive data flow lacks declared transport encryption",
                "Sensitive data may be exposed to network observers or intermediaries.",
                ["Require TLS with approved protocol and certificate validation", "Test downgrade and certificate failure behavior"],
                3, 5))
        if flow.get("crosses_trust_boundary") and not p.get("integrity_protection", False):
            findings.append(_finding(
                "STRIDE-T-001", "Tampering", fid, "data_flow",
                "Trust-boundary flow lacks declared integrity protection",
                "Data may be altered in transit or accepted from an untrusted intermediary.",
                ["Use authenticated transport and integrity validation", "Validate message signatures or MACs where appropriate"],
                3, 4))
        if flow.get("protocol") == "messaging" and not p.get("replay_protection", False):
            findings.append(_finding(
                "STRIDE-T-002", "Tampering", fid, "data_flow",
                "Message flow lacks declared replay protection",
                "Replayed events may cause duplicate or unauthorized state transitions.",
                ["Use idempotency keys and bounded replay windows", "Validate event origin and schema", "Test duplicate and out-of-order delivery"],
                3, 4))
        if flow.get("protocol") in ("https", "http") and not p.get("rate_limited", False):
            findings.append(_finding(
                "STRIDE-D-001", "Denial of Service", fid, "data_flow",
                "HTTP flow has no declared rate limiting",
                "Unbounded requests may exhaust service capacity or create uncontrolled downstream cost.",
                ["Apply identity, tenant and route-level quotas", "Bound request size, concurrency and execution time"],
                4, 4))
        if flow.get("source") == "ai-agent" and flow.get("destination") and not p.get("tool_authorization", False):
            findings.append(_finding(
                "STRIDE-E-001", "Elevation of Privilege", fid, "data_flow",
                "AI tool flow lacks declared independent authorization",
                "A model-influenced tool request may execute beyond the user's authorized privileges.",
                ["Authorize every tool call outside the model", "Use strict tool allowlists and typed schemas", "Require human approval for sensitive actions"],
                3, 5))

    for component in doc["components"]:
        p = component.get("properties", {})
        cid = component["id"]
        tags = set(component.get("tags", []))
        if component.get("exposure") == "internet" and not p.get("rate_limiting", False):
            findings.append(_finding(
                "STRIDE-D-002", "Denial of Service", cid, "component",
                "Internet-facing component has no declared rate limiting",
                "An exposed endpoint may be abused for resource or cost exhaustion.",
                ["Configure WAF and per-tenant quotas", "Add burst limits, circuit breakers and capacity alarms"],
                4, 4))
        if component.get("data_classification") in ("confidential", "restricted") and p.get("public_access", False):
            findings.append(_finding(
                "STRIDE-I-002", "Information Disclosure", cid, "component",
                "Sensitive component declares public access",
                "Public exposure may allow unauthorized access to sensitive information.",
                ["Block public access by policy", "Use private endpoints and continuous exposure monitoring"],
                4, 5))
        if component.get("data_classification") in ("confidential", "restricted") and not p.get("audit_logging", False):
            findings.append(_finding(
                "STRIDE-R-001", "Repudiation", cid, "component",
                "Sensitive component has no declared audit logging",
                "Security-relevant actions may not be attributable or reconstructable.",
                ["Emit actor, action, resource, timestamp and correlation ID", "Forward tamper-resistant audit events to central monitoring"],
                3, 4))
        if "tenant-aware" in tags and p.get("tenant_isolation") is False:
            findings.append(_finding(
                "STRIDE-I-003", "Information Disclosure", cid, "component",
                "Tenant-aware component does not declare tenant isolation",
                "A missing tenant boundary may permit cross-tenant data access.",
                ["Enforce tenant scope server-side", "Add cross-tenant negative tests for all data operations"],
                4, 5))
        if "privileged" in tags and p.get("least_privilege") is False:
            findings.append(_finding(
                "STRIDE-E-002", "Elevation of Privilege", cid, "component",
                "Privileged component does not declare least-privilege permissions",
                "Excess permissions may increase impact after component compromise.",
                ["Scope permissions to required actions and resources", "Review effective permissions and alert on privilege changes"],
                3, 5))
        if component.get("type") == "ai_service":
            if not p.get("tool_allowlist", False):
                findings.append(_finding(
                    "STRIDE-E-003", "Elevation of Privilege", cid, "component",
                    "AI service does not declare a tool allowlist",
                    "Unbounded tool selection may expose sensitive internal capabilities.",
                    ["Allow only explicitly approved tools", "Separate model planning from deterministic authorization"]))
            if not p.get("input_screening", False):
                findings.append(_finding(
                    "STRIDE-T-003", "Tampering", cid, "component",
                    "AI input screening is not declared",
                    "Untrusted instructions or poisoned context may influence downstream model behavior.",
                    ["Treat prompts and retrieved content as untrusted", "Apply input policy and adversarial evaluations"]))
            if not p.get("output_screening", False):
                findings.append(_finding(
                    "STRIDE-I-004", "Information Disclosure", cid, "component",
                    "AI output screening is not declared",
                    "Sensitive data may be returned to an unauthorized user or downstream system.",
                    ["Apply output DLP and authorization-aware filtering", "Test secret and cross-tenant leakage cases"]))

    findings.sort(key=lambda x: (-x["inherent_score"], x["id"]))
    counts = {name: 0 for name in STRIDE.values()}
    for item in findings:
        counts[item["stride"]] += 1
    return {
        "schema_version": "1.0",
        "system": doc["system"],
        "engine": "rules-based-stride-engine",
        "disclaimer": "Candidate threats only; validate with system owners and security architects.",
        "summary": {
            "candidate_count": len(findings),
            "by_stride": counts,
            "critical": sum(x["inherent_band"] == "CRITICAL" for x in findings),
            "high": sum(x["inherent_band"] == "HIGH" for x in findings)
        },
        "findings": findings
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        doc = json.loads(args.input.read_text(encoding="utf-8"))
        result = generate(doc)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"Generated {result['summary']['candidate_count']} candidate threats -> {args.output}")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
