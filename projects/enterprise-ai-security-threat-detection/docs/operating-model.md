# AI Security Operating Model

## Ownership

| Function | Accountability |
|---|---|
| AI Product Owner | Business impact, product risk, remediation funding |
| AI Engineering | Application controls, prompt/context boundaries, tool broker |
| Data / ML Platform | Dataset and model provenance, registry, evaluation pipeline |
| Cloud / Kubernetes Platform | Workload identity, cluster isolation, network and admission controls |
| Product Security / AI Security | Threat model, security requirements, detection rules, risk review |
| SOC | Alert triage, correlation, incident coordination, evidence handling |
| Privacy / Legal | Data exposure assessment, regulatory and notification advice |
| Risk Owner / Executive | Residual-risk acceptance within delegated authority |

## Incident workflow

1. **Detect:** Generate an alert with rule ID, severity, asset, evidence, and recommended action.
2. **Triage:** Confirm authenticity, scope, business criticality, and whether the action was blocked.
3. **Contain:** Revoke or constrain affected sessions/tools, isolate compromised artifacts, or disable unsafe retrieval paths.
4. **Investigate:** Trace identity, tenant, model version, prompt/context provenance, tool calls, and deployment changes.
5. **Remediate:** Fix the root control gap and add regression coverage.
6. **Validate:** Re-run relevant tests and obtain control-owner confirmation.
7. **Close:** Record evidence, residual risk, owner, timestamps, and lessons learned.

## Suggested response targets

These are example internal targets, not external standards. Set contractual and regulatory requirements separately.

| Severity | Initial triage target | Containment / action plan |
|---|---:|---:|
| Critical | 15 minutes | Immediate containment; executive/security escalation |
| High | 1 hour | Same business day |
| Medium | 1 business day | 5 business days |
| Low | 5 business days | 30 calendar days |

## Governance metrics

- Critical/high AI security alerts by workload and tenant
- Mean time to acknowledge, contain, and remediate
- Repeat findings and control regression rate
- Model artifacts failing integrity/provenance validation
- Unauthorized agent tool attempts and approval bypasses
- Tenant-isolation violations and data exposure assessments
- Policy drift age and remediation SLA adherence
- Exceptions by owner, expiry date, and residual risk

## Exception management

Exceptions must identify the affected asset, business justification, compensating controls, risk owner, approver, expiry date, and remediation milestone. No permanent or ownerless exceptions. Reassess on material architecture or threat changes.
