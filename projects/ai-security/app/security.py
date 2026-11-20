"""Defensive guardrails for a toy LLM application.

This module demonstrates deterministic controls around an LLM. It does not
claim that regex-based prompt-injection detection can secure a model by itself.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


INJECTION_PATTERNS = (
    re.compile(r"ignore (all )?(previous|prior) instructions", re.I),
    re.compile(r"reveal (the )?(system prompt|hidden prompt)", re.I),
    re.compile(r"act as (an? )?(administrator|system)", re.I),
    re.compile(r"disregard (all )?(rules|policies)", re.I),
)


@dataclass(frozen=True)
class SecurityDecision:
    allowed: bool
    reason: str


def inspect_untrusted_text(text: str) -> SecurityDecision:
    """Flag common suspicious strings for review; not a complete classifier."""
    for pattern in INJECTION_PATTERNS:
        if pattern.search(text):
            return SecurityDecision(False, "Potential prompt injection detected")
    return SecurityDecision(True, "No known injection pattern detected")


def retrieve_for_tenant(
    documents: list[dict[str, Any]], tenant_id: str, query: str
) -> list[dict[str, Any]]:
    """Return only documents owned by the caller's tenant.

    Authorization is enforced in application code, not delegated to the model.
    The query match is intentionally simple for this demonstration.
    """
    needle = query.casefold()
    return [
        doc for doc in documents
        if doc.get("tenant_id") == tenant_id
        and needle in str(doc.get("text", "")).casefold()
    ]


ALLOWED_TOOLS = {"search_public_docs", "get_ticket_status"}
HIGH_IMPACT_TOOLS = {"disable_account", "issue_refund", "delete_resource"}


def authorize_tool_call(
    tool_name: str, *, user_role: str, human_approved: bool = False
) -> SecurityDecision:
    """Apply an allowlist and require explicit approval for high-impact actions."""
    if tool_name in HIGH_IMPACT_TOOLS:
        if user_role != "admin" or not human_approved:
            return SecurityDecision(False, "High-impact action requires admin and human approval")
        return SecurityDecision(True, "Approved high-impact action")
    if tool_name not in ALLOWED_TOOLS:
        return SecurityDecision(False, "Tool is not on the application allowlist")
    return SecurityDecision(True, "Tool is allowlisted")


def validate_structured_output(value: Any) -> SecurityDecision:
    """Validate a tiny example response contract before downstream use."""
    if not isinstance(value, dict):
        return SecurityDecision(False, "Output must be a JSON object")
    if set(value) != {"answer", "confidence"}:
        return SecurityDecision(False, "Unexpected or missing output fields")
    if not isinstance(value["answer"], str) or len(value["answer"]) > 2000:
        return SecurityDecision(False, "Answer must be a string of at most 2000 characters")
    confidence = value["confidence"]
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
        return SecurityDecision(False, "Confidence must be numeric")
    if not 0 <= confidence <= 1:
        return SecurityDecision(False, "Confidence must be between 0 and 1")
    return SecurityDecision(True, "Output matches schema")


SECRET_PATTERNS = (
    re.compile(r"(?i)\b(api[_-]?key|token|password)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
)


def redact_secrets(text: str) -> str:
    """Redact common secret-like values before demo logging."""
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted
