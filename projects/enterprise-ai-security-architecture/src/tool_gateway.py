"""Local policy demonstration for safe agent tool dispatch.

No real tool is executed. A model proposal is treated as untrusted input.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any


class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRES_APPROVAL = "requires_approval"


@dataclass(frozen=True)
class Principal:
    subject: str
    tenant_id: str
    roles: frozenset[str]


@dataclass(frozen=True)
class ToolProposal:
    tool: str
    action: str
    resource_id: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class PolicyResult:
    decision: Decision
    reason: str


TOOL_POLICIES = {
    "read_ticket": {
        "actions": {"read"},
        "roles": {"analyst", "admin"},
        "required_args": {"ticket_id"},
        "allowed_args": {"ticket_id"},
    },
    "update_ticket": {
        "actions": {"update"},
        "roles": {"ticket_operator", "admin"},
        "required_args": {"ticket_id", "status"},
        "allowed_args": {"ticket_id", "status"},
    },
}
HIGH_IMPACT_ACTIONS = {("update_ticket", "update")}


def authorize_tool_call(
    principal: Principal,
    proposal: ToolProposal,
    *,
    resource_tenant_id: str | None,
    approval_valid: bool = False,
) -> PolicyResult:
    """Evaluate a proposal. Never execute the proposed operation here."""
    policy = TOOL_POLICIES.get(proposal.tool)
    if policy is None:
        return PolicyResult(Decision.DENY, "Tool is not allowlisted")
    if proposal.action not in policy["actions"]:
        return PolicyResult(Decision.DENY, "Action is not allowed for this tool")
    if not principal.subject or not principal.tenant_id:
        return PolicyResult(Decision.DENY, "Missing authenticated principal context")
    if resource_tenant_id is None or resource_tenant_id != principal.tenant_id:
        return PolicyResult(Decision.DENY, "Resource is outside the principal tenant")
    if not principal.roles.intersection(policy["roles"]):
        return PolicyResult(Decision.DENY, "Principal lacks required role")
    if not isinstance(proposal.arguments, dict):
        return PolicyResult(Decision.DENY, "Arguments must be an object")
    if set(proposal.arguments) - policy["allowed_args"]:
        return PolicyResult(Decision.DENY, "Unexpected tool argument")
    if not policy["required_args"].issubset(proposal.arguments):
        return PolicyResult(Decision.DENY, "Required tool argument missing")
    for key, value in proposal.arguments.items():
        if not isinstance(value, str) or not value.strip() or len(value) > 128:
            return PolicyResult(Decision.DENY, f"Invalid argument: {key}")
    if proposal.tool == "update_ticket":
        if proposal.arguments.get("status") not in {"open", "in_progress", "resolved"}:
            return PolicyResult(Decision.DENY, "Ticket status is not an allowed value")
    if (proposal.tool, proposal.action) in HIGH_IMPACT_ACTIONS and not approval_valid:
        return PolicyResult(Decision.REQUIRES_APPROVAL, "High-impact action requires trusted approval")
    return PolicyResult(Decision.ALLOW, "Policy checks passed; downstream executor must re-authorize")
