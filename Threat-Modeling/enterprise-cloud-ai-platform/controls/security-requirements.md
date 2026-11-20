# Security requirements and control traceability

Controls are requirements until implementation and evidence are demonstrated.

| Control ID | Requirement | Threats addressed | Owner | Verification evidence |
|---|---|---|---|---|
| SEC-IAM-01 | Validate token signature, issuer, audience, expiry, nbf, and algorithm | TM-001, TM-017 | IAM / AppSec | Automated negative JWT test suite |
| SEC-IAM-02 | Enforce object-level authorization and tenant binding at every data operation | TM-002, TM-008 | Product Engineering | Cross-tenant API integration tests |
| SEC-IAM-03 | Require phishing-resistant MFA and JIT privileged access | TM-020, TM-012 | IAM | IdP policy export, access review, session evidence |
| SEC-API-01 | Rate-limit by tenant, identity, route, and cost-sensitive operation | TM-005 | API Platform | Load test, gateway policy, quota alerts |
| SEC-DATA-01 | Block public storage and require encryption with managed keys | TM-004, TM-011 | Cloud Platform | Policy-as-code and cloud configuration evidence |
| SEC-DATA-02 | Use parameterized queries and scoped database identities | TM-002, TM-019 | Data Platform | Code review, DB grants, integration tests |
| SEC-EVT-01 | Validate event schema, origin, idempotency, and replay window | TM-003, TM-014 | Platform Engineering | Replay and poison-message tests |
| SEC-K8S-01 | Enforce restricted pod security, RBAC least privilege, and network policies | TM-013 | Container Security | Admission tests, RBAC review, network test |
| SEC-SC-01 | Generate SBOM and provenance; sign and verify release artifacts | TM-007, TM-016 | DevSecOps | Attestation, signature verification, CI logs |
| SEC-CICD-01 | Restrict OIDC trust to exact repository, branch/ref, audience, and environment | TM-006 | Cloud IAM | Trust policy review and negative assume-role test |
| SEC-AI-01 | Apply tenant and source ACL filters server-side to every retrieval | TM-008, TM-010 | AI Platform | Adversarial retrieval isolation tests |
| SEC-AI-02 | Authorize every tool call independently of model output | TM-009 | AI Platform / AppSec | Tool authorization test suite |
| SEC-AI-03 | Screen uploads, track provenance, and quarantine suspicious documents | TM-010 | Data / AI Platform | Ingestion test and quarantine audit |
| SEC-AI-04 | Apply prompt/output DLP, retention limits, and model-provider governance | TM-011 | Privacy / AI Governance | DLP tests, provider assessment, retention config |
| SEC-LOG-01 | Centralize tamper-resistant audit events with delivery-gap alerting | TM-012, TM-018 | Detection Engineering | SIEM event test and pipeline SLO |
| SEC-LOG-02 | Redact secrets and sensitive data before logs/traces are persisted | TM-015 | Platform / Privacy | Automated log scanning and sample review |
| SEC-RES-01 | Set bounded retries, dead-letter queues, circuit breakers, and resource budgets | TM-005, TM-014 | SRE | Failure-injection and load test |
| SEC-BCP-01 | Test backup restore and recovery against service RTO/RPO | Availability | SRE / Data | Restore exercise report |

## Security acceptance criteria

- Every Critical threat has a validated mitigation or formally approved exception.
- Every High threat has an owner, target date, and verification plan.
- No production deployment can bypass artifact verification and environment protection.
- Cross-tenant authorization tests run on every release and fail closed.
- AI tool authorization tests include direct and indirect prompt injection attempts.
- Audit events are searchable within the agreed detection SLO and sensitive values are redacted.
- Exceptions expire automatically or trigger escalation; indefinite exceptions are prohibited.

## Evidence quality

Preferred evidence: automated tests, policy evaluation output, signed attestations, cloud configuration exports, access review records, SIEM event samples, and approved exercise reports. Screenshots alone are weak evidence unless accompanied by source configuration and date/context.
