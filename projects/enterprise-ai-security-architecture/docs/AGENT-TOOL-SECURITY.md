# Agent and Tool Security

## Mandatory controls

- Explicit tool allowlist; no dynamic tool discovery from model output.
- Strict argument schemas with length, type, enum, and range constraints.
- Bind user identity and tenant from verified claims, never model arguments.
- Authorize tool, action, target resource, and parameters in trusted code.
- Use narrowly scoped workload identity for each tool.
- Require human approval for high-impact or irreversible actions.
- Bind approval to a canonical action digest, approver identity, expiry, and one-time use.
- Apply timeouts, rate limits, idempotency, and output size limits.
- Treat tool output as untrusted input to subsequent model turns.

## Risk tiers

| Tier | Example | Control |
|---|---|---|
| Low | Read a public internal catalogue | Read scope and resource ACL |
| Medium | Read tenant business records | Tenant and document ACL, audit |
| High | Modify cloud configuration or ticket state | Explicit policy and human approval |
| Critical | Delete production data, rotate privileged credentials | Out-of-band approval, dual control, break-glass governance; avoid autonomous execution |

## Lab implementation

src/tool_gateway.py demonstrates an allowlist, role checks, tenant/resource ownership, strict arguments, and an approval requirement for high-impact actions. It simulates execution and returns a decision; it does not call cloud APIs, execute shell commands, or mutate real systems.

## Production note

A boolean approval flag from an API request is not a valid approval workflow. Use a trusted approval service that authenticates approvers, records immutable evidence, expires approvals, prevents replay, and verifies that the approved action digest matches the executed action.
