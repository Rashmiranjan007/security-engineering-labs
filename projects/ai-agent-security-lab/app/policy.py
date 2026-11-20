from dataclasses import dataclass
from enum import Enum
from typing import Any
from .identity import Principal


class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRES_APPROVAL = "requires_approval"


@dataclass(frozen=True)
class ToolDecision:
    decision: Decision
    reason: str


TOOL_RULES = {
    "read_ticket": {
        "action": "read", "roles": {"analyst", "ticket_operator", "admin"},
        "args": {"ticket_id"}, "approval": False,
    },
    "update_ticket": {
        "action": "update", "roles": {"ticket_operator", "admin"},
        "args": {"ticket_id", "status"}, "approval": True,
    },
}

# Trusted synthetic resource inventory. Never accept resource ownership from the API caller.
DEMO_RESOURCE_TENANTS = {
    "ticket-100": "tenant-a",
    "ticket-200": "tenant-b",
}


def authorize_tool(principal: Principal, tool: str, action: str, resource_id: str,
                   arguments: dict[str, Any], approval_ref: str | None = None) -> ToolDecision:
    rule = TOOL_RULES.get(tool)
    if not rule or action != rule["action"]:
        return ToolDecision(Decision.DENY, "Tool or action is not allowlisted")
    resource_tenant = DEMO_RESOURCE_TENANTS.get(resource_id)
    if resource_tenant is None or resource_tenant != principal.tenant_id:
        return ToolDecision(Decision.DENY, "Resource is unknown or outside the principal tenant")
    if not principal.roles.intersection(rule["roles"]):
        return ToolDecision(Decision.DENY, "Role is not authorized")
    if not isinstance(arguments, dict) or set(arguments) != rule["args"]:
        return ToolDecision(Decision.DENY, "Arguments do not match strict schema")
    if arguments.get("ticket_id") != resource_id:
        return ToolDecision(Decision.DENY, "Argument resource does not match authorized resource")
    if any(not isinstance(v, str) or not v.strip() or len(v) > 128 for v in arguments.values()):
        return ToolDecision(Decision.DENY, "Invalid argument value")
    if tool == "update_ticket" and arguments["status"] not in {"open", "in_progress", "resolved"}:
        return ToolDecision(Decision.DENY, "Unsupported ticket status")
    if rule["approval"] and approval_ref != "DEMO-APPROVED":
        return ToolDecision(Decision.REQUIRES_APPROVAL, "High-impact action requires approval")
    return ToolDecision(Decision.ALLOW, "Policy checks passed")
