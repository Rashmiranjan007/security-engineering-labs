# AI Runtime Monitoring and Response

## Security telemetry

Capture structured events with correlation ID, timestamp, actor pseudonymous ID, tenant, model/provider identifier, policy decision, tool name, resource reference, approval reference, and outcome. Avoid logging raw prompts/responses by default; use controlled evidence capture only when justified.

## Detection use cases

| Detection | Signal | Response |
|---|---|---|
| Prompt injection attempts | Policy violation / suspicious content score | Block or constrain request; preserve minimal evidence |
| Cross-tenant access attempt | ACL denial, tenant mismatch | Deny, alert on repeated attempts, investigate identity |
| Excessive tool use | Tool-call rate or budget exceeded | Stop agent run, throttle, alert owner |
| Privileged tool attempt | High-risk action proposed | Require approval or deny |
| Sensitive output | DLP classification hit | Block/redact response; incident workflow if confirmed |
| RAG poisoning indicator | Untrusted source or ingestion anomaly | Quarantine source, revoke derived chunks |
| Cost/DoS anomaly | Token, concurrency, latency, or spend threshold | Rate limit, circuit break, notify service owner |

## Operational requirements

- Centralize protected audit events in the enterprise SIEM.
- Define severity, alert owner, escalation path, and response SLA.
- Correlate user request, retrieval, model invocation, tool proposal, approval, and execution.
- Monitor false positives and false negatives; tune with approved test data.
- Protect telemetry from tampering and restrict access.
- Define retention and deletion according to data classification and policy.

## Incident playbook

1. Stop or isolate the affected agent/tool workflow.
2. Revoke or rotate exposed credentials and tokens.
3. Determine tenant, data, model, tool, and resource scope.
4. Review approvals and tool execution records.
5. Contain unauthorized access or changes and restore from trusted state.
6. Preserve appropriate evidence and notify stakeholders.
7. Add regression tests and verify the control before restoring service.
