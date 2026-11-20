#!/usr/bin/env python3
"""Deterministic AI runtime guard simulator; standard library only.

Evaluates synthetic request/tool events. It does not call an LLM, execute tools,
scan networks, or interact with external systems.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

PATTERNS = {
    "PROMPT_INJECTION": [
        re.compile(r"ignore (all )?(previous|prior) instructions", re.I),
        re.compile(r"reveal (the )?(system prompt|hidden instructions)", re.I),
        re.compile(r"act as (the )?system", re.I),
        re.compile(r"disregard (the )?safety (rules|policy)", re.I),
    ],
    "SECRET_EXFILTRATION": [
        re.compile(r"(?i)\b(api[_ -]?key|password|secret|access[_ -]?token)\b\s*[:=]\s*\S+"),
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ],
}

DEFAULT_POLICY = {
    "allowed_tools": ["search_public_docs", "get_ticket_status"],
    "high_impact_tools": ["close_ticket", "rotate_credential", "delete_record"],
    "max_prompt_chars": 12000,
    "max_output_chars": 8000,
    "max_requests_per_subject": 5,
    "max_tool_calls_per_request": 3,
    "require_approval_for_high_impact": True,
}


def redact(text: str) -> str:
    text = re.sub(r"(?i)(api[_ -]?key|password|secret|access[_ -]?token)(\s*[:=]\s*)\S+", r"\1\2[REDACTED]", text)
    text = re.sub(r"\bAKIA[0-9A-Z]{16}\b", "[REDACTED_AWS_ACCESS_KEY]", text)
    text = re.sub(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----.*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "[REDACTED_PRIVATE_KEY]", text, flags=re.S)
    return text


class RuntimeGuard:
    def __init__(self, policy: dict[str, Any] | None = None):
        self.policy = {**DEFAULT_POLICY, **(policy or {})}
        self.request_counts: dict[str, int] = defaultdict(int)
        self.events: list[dict[str, Any]] = []

    def _event(self, subject: str, event_type: str, decision: str, reasons: list[str], details: dict[str, Any] | None = None):
        record = {
            "subject": subject,
            "event_type": event_type,
            "decision": decision,
            "reasons": reasons,
            "details": details or {},
        }
        self.events.append(record)
        return record

    def evaluate_request(self, event: dict[str, Any]) -> dict[str, Any]:
        subject = str(event.get("subject", "anonymous"))
        prompt = str(event.get("prompt", ""))
        retrieved = str(event.get("retrieved_context", ""))
        combined = prompt + "\n" + retrieved
        reasons: list[str] = []
        self.request_counts[subject] += 1

        if len(prompt) > int(self.policy["max_prompt_chars"]):
            reasons.append("PROMPT_SIZE_LIMIT")
        if self.request_counts[subject] > int(self.policy["max_requests_per_subject"]):
            reasons.append("REQUEST_RATE_LIMIT")
        for category, patterns in PATTERNS.items():
            if any(pattern.search(combined) for pattern in patterns):
                reasons.append(category)
        if event.get("tenant_id") != event.get("resource_tenant_id"):
            reasons.append("TENANT_CONTEXT_MISMATCH")
        decision = "BLOCK" if reasons else "ALLOW"
        return self._event(subject, "inference_request", decision, reasons, {
            "prompt_chars": len(prompt),
            "retrieved_context_chars": len(retrieved),
            "prompt_preview": redact(prompt[:160]),
        })

    def evaluate_tool_call(self, event: dict[str, Any]) -> dict[str, Any]:
        subject = str(event.get("subject", "anonymous"))
        tool = str(event.get("tool", ""))
        reasons: list[str] = []
        if tool not in self.policy["allowed_tools"] and tool not in self.policy["high_impact_tools"]:
            reasons.append("TOOL_NOT_ALLOWLISTED")
        if not event.get("user_authorized", False):
            reasons.append("USER_NOT_AUTHORIZED")
        if not event.get("resource_authorized", False):
            reasons.append("RESOURCE_NOT_AUTHORIZED")
        if tool in self.policy["high_impact_tools"]:
            if self.policy["require_approval_for_high_impact"] and not event.get("human_approved", False):
                reasons.append("HUMAN_APPROVAL_REQUIRED")
        if int(event.get("tool_calls_in_request", 1)) > int(self.policy["max_tool_calls_per_request"]):
            reasons.append("TOOL_CALL_BUDGET_EXCEEDED")
        decision = "BLOCK" if reasons else "ALLOW"
        return self._event(subject, "tool_invocation", decision, reasons, {"tool": tool})

    def evaluate_output(self, event: dict[str, Any]) -> dict[str, Any]:
        subject = str(event.get("subject", "anonymous"))
        output = str(event.get("output", ""))
        reasons: list[str] = []
        if len(output) > int(self.policy["max_output_chars"]):
            reasons.append("OUTPUT_SIZE_LIMIT")
        if any(pattern.search(output) for pattern in PATTERNS["SECRET_EXFILTRATION"]):
            reasons.append("SENSITIVE_OUTPUT_DETECTED")
        decision = "BLOCK" if reasons else "ALLOW"
        return self._event(subject, "model_output", decision, reasons, {
            "output_chars": len(output),
            "redacted_preview": redact(output[:160]),
        })

    def report(self) -> dict[str, Any]:
        counts = {"ALLOW": 0, "BLOCK": 0}
        for event in self.events:
            counts[event["decision"]] += 1
        return {
            "summary": {"events": len(self.events), "allowed": counts["ALLOW"], "blocked": counts["BLOCK"]},
            "events": self.events,
            "note": "Heuristic simulation only. Review alerts and tune patterns; this is not a production DLP or prompt-injection detector."
        }


def run_scenarios(path: str) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    guard = RuntimeGuard(data.get("policy"))
    for event in data.get("events", []):
        kind = event.get("type")
        if kind == "request":
            guard.evaluate_request(event)
        elif kind == "tool":
            guard.evaluate_tool_call(event)
        elif kind == "output":
            guard.evaluate_output(event)
        else:
            raise ValueError(f"Unsupported event type: {kind}")
    return guard.report()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Synthetic event scenario JSON")
    parser.add_argument("--output", help="Write JSON report to file; stdout if omitted")
    args = parser.parse_args()
    result = json.dumps(run_scenarios(args.input), indent=2)
    if args.output:
        Path(args.output).write_text(result + "\n", encoding="utf-8")
    else:
        print(result)


if __name__ == "__main__":
    main()
