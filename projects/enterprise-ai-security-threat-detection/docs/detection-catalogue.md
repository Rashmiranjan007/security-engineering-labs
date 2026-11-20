# Detection Catalogue

The executable rule data is maintained in `config/detection-rules.json`.

| Rule | Event type | Severity | Required response |
|---|---|---|---|
| AI-DET-001 | `prompt_injection` | High | Review source, isolate untrusted content, tune prompt/context boundaries |
| AI-DET-002 | `cross_tenant_retrieval` | Critical | Block retrieval, contain affected session, investigate tenant ACL path |
| AI-DET-003 | `unauthorized_tool_call` | Critical | Deny action, suspend affected agent credential if warranted, inspect tool broker |
| AI-DET-004 | `sensitive_output` | High | Suppress response, assess exposure, rotate affected secrets if real |
| AI-DET-005 | `model_integrity_failure` | Critical | Quarantine artifact/deployment, verify provenance and promotion chain |
| AI-DET-006 | `policy_drift` | Medium | Reconcile approved policy, identify unauthorized changes, validate rollout |

## Required event fields

- `event_id`: unique event identifier
- `timestamp`: ISO-8601 timestamp
- `event_type`: one of the supported event types
- `workload`: emitting AI service or platform workload
- `environment`: development, staging, or production
- `actor`: pseudonymous user/service identity
- `resource`: affected resource or tool
- `outcome`: allow, deny, or detect
- `details`: event-specific metadata; do not place secrets or raw sensitive prompts here

## Triage principles

1. Validate event authenticity and correlation context.
2. Establish affected tenant, workload, model, and time window.
3. Confirm whether a preventive control blocked the action.
4. Assess data exposure and downstream side effects.
5. Contain first when tenant isolation, privileged tools, or model integrity are implicated.
6. Preserve minimal evidence and record the owner, decision, and follow-up.
