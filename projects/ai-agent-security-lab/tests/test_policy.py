import unittest
from app.identity import Principal
from app.policy import Decision, authorize_tool


class ToolPolicyTests(unittest.TestCase):
    def setUp(self):
        self.analyst = Principal("alice", "tenant-a", frozenset({"analyst"}))
        self.operator = Principal("bob", "tenant-a", frozenset({"ticket_operator"}))

    def test_allowlisted_read(self):
        result = authorize_tool(self.analyst, "read_ticket", "read", "ticket-100", {"ticket_id": "ticket-100"})
        self.assertEqual(result.decision, Decision.ALLOW)

    def test_unknown_tool_denied(self):
        result = authorize_tool(self.analyst, "shell", "execute", "ticket-100", {})
        self.assertEqual(result.decision, Decision.DENY)

    def test_cross_tenant_resource_denied(self):
        result = authorize_tool(self.analyst, "read_ticket", "read", "ticket-200", {"ticket_id": "ticket-200"})
        self.assertEqual(result.decision, Decision.DENY)

    def test_unknown_resource_denied(self):
        result = authorize_tool(self.analyst, "read_ticket", "read", "ticket-999", {"ticket_id": "ticket-999"})
        self.assertEqual(result.decision, Decision.DENY)

    def test_resource_argument_mismatch_denied(self):
        result = authorize_tool(self.analyst, "read_ticket", "read", "ticket-100", {"ticket_id": "ticket-200"})
        self.assertEqual(result.decision, Decision.DENY)

    def test_unauthorized_role_denied(self):
        result = authorize_tool(self.analyst, "update_ticket", "update", "ticket-100",
                                {"ticket_id": "ticket-100", "status": "resolved"}, "DEMO-APPROVED")
        self.assertEqual(result.decision, Decision.DENY)

    def test_high_impact_requires_approval(self):
        result = authorize_tool(self.operator, "update_ticket", "update", "ticket-100",
                                {"ticket_id": "ticket-100", "status": "resolved"})
        self.assertEqual(result.decision, Decision.REQUIRES_APPROVAL)

    def test_unexpected_argument_denied(self):
        result = authorize_tool(self.analyst, "read_ticket", "read", "ticket-100",
                                {"ticket_id": "ticket-100", "tenant_id": "tenant-b"})
        self.assertEqual(result.decision, Decision.DENY)

    def test_invalid_status_denied(self):
        result = authorize_tool(self.operator, "update_ticket", "update", "ticket-100",
                                {"ticket_id": "ticket-100", "status": "delete"}, "DEMO-APPROVED")
        self.assertEqual(result.decision, Decision.DENY)


if __name__ == "__main__":
    unittest.main()
