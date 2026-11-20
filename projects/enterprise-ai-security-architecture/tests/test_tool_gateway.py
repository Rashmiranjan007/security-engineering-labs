import unittest

from src.tool_gateway import Decision, Principal, ToolProposal, authorize_tool_call


class ToolGatewayPolicyTests(unittest.TestCase):
    def setUp(self):
        self.analyst = Principal("user-1", "tenant-a", frozenset({"analyst"}))
        self.operator = Principal("user-2", "tenant-a", frozenset({"ticket_operator"}))

    def test_unknown_tool_is_denied(self):
        result = authorize_tool_call(
            self.analyst, ToolProposal("shell", "execute", "host-1", {}),
            resource_tenant_id="tenant-a",
        )
        self.assertEqual(result.decision, Decision.DENY)

    def test_read_tool_allowed_for_authorized_tenant(self):
        result = authorize_tool_call(
            self.analyst,
            ToolProposal("read_ticket", "read", "ticket-1", {"ticket_id": "ticket-1"}),
            resource_tenant_id="tenant-a",
        )
        self.assertEqual(result.decision, Decision.ALLOW)

    def test_cross_tenant_resource_denied(self):
        result = authorize_tool_call(
            self.analyst,
            ToolProposal("read_ticket", "read", "ticket-2", {"ticket_id": "ticket-2"}),
            resource_tenant_id="tenant-b",
        )
        self.assertEqual(result.decision, Decision.DENY)

    def test_missing_role_denied(self):
        result = authorize_tool_call(
            self.analyst,
            ToolProposal("update_ticket", "update", "ticket-1",
                         {"ticket_id": "ticket-1", "status": "resolved"}),
            resource_tenant_id="tenant-a", approval_valid=True,
        )
        self.assertEqual(result.decision, Decision.DENY)

    def test_high_impact_action_requires_approval(self):
        proposal = ToolProposal(
            "update_ticket", "update", "ticket-1",
            {"ticket_id": "ticket-1", "status": "resolved"},
        )
        result = authorize_tool_call(
            self.operator, proposal, resource_tenant_id="tenant-a"
        )
        self.assertEqual(result.decision, Decision.REQUIRES_APPROVAL)

    def test_approved_high_impact_action_passes_policy(self):
        proposal = ToolProposal(
            "update_ticket", "update", "ticket-1",
            {"ticket_id": "ticket-1", "status": "resolved"},
        )
        result = authorize_tool_call(
            self.operator, proposal, resource_tenant_id="tenant-a", approval_valid=True
        )
        self.assertEqual(result.decision, Decision.ALLOW)

    def test_unexpected_arguments_denied(self):
        result = authorize_tool_call(
            self.analyst,
            ToolProposal("read_ticket", "read", "ticket-1",
                         {"ticket_id": "ticket-1", "tenant_id": "tenant-b"}),
            resource_tenant_id="tenant-a",
        )
        self.assertEqual(result.decision, Decision.DENY)

    def test_invalid_enum_value_denied(self):
        result = authorize_tool_call(
            self.operator,
            ToolProposal("update_ticket", "update", "ticket-1",
                         {"ticket_id": "ticket-1", "status": "delete"}),
            resource_tenant_id="tenant-a", approval_valid=True,
        )
        self.assertEqual(result.decision, Decision.DENY)


if __name__ == "__main__":
    unittest.main()
