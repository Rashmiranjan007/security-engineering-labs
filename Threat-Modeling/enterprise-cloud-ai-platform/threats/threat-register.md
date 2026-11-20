# Threat register

This is a worked example. Scores are illustrative and must be recalibrated with business impact, exposure, exploitability, and control evidence.

**Scoring:** Likelihood (L) 1–5 × Impact (I) 1–5 = inherent risk. Residual score is intentionally marked TBD until controls are tested.

| ID | STRIDE | Scenario / asset | L | I | Inherent | Priority | Mitigation and evidence |
|---|---|---|---:|---:|---:|---|---|
| TM-001 | Spoofing | Forged identity headers bypass user identity at gateway | 4 | 5 | 20 | Critical | Strip untrusted headers; validate OIDC at service; gateway spoofing tests |
| TM-002 | Elevation | Broken object-level authorization exposes another tenant's record | 4 | 5 | 20 | Critical | Tenant-scoped policy checks on every operation; cross-tenant negative tests |
| TM-003 | Tampering | Event payload changed or replayed to alter business state | 3 | 5 | 15 | High | Signed/validated event origin, schema validation, idempotency, replay controls |
| TM-004 | Information Disclosure | Public object-store policy exposes customer documents | 3 | 5 | 15 | High | Block public access, policy-as-code, access analyzer, exposure alert |
| TM-005 | Denial of Service | Unbounded API, queue, or model requests exhaust capacity/cost | 4 | 4 | 16 | High | Per-tenant quotas, rate/token budgets, back-pressure, autoscaling bounds |
| TM-006 | Elevation | CI OIDC role can assume broad production administrator role | 3 | 5 | 15 | High | Repo/ref-bound trust, least privilege, environment approval, CloudTrail alert |
| TM-007 | Tampering | Compromised build runner publishes malicious image | 3 | 5 | 15 | High | Ephemeral isolated runners, provenance, signing, digest pinning, admission verify |
| TM-008 | Information Disclosure | RAG retrieval returns another tenant's document chunk | 4 | 5 | 20 | Critical | Server-side tenant + ACL filters; namespace isolation; adversarial retrieval tests |
| TM-009 | Elevation | Prompt injection induces privileged tool execution | 3 | 5 | 15 | High | Tool broker authorization, allowlist, argument validation, human approval |
| TM-010 | Tampering | Poisoned document contaminates RAG corpus | 3 | 4 | 12 | High | Ingestion scanning, source provenance, quarantine, review, corpus rollback |
| TM-011 | Information Disclosure | Secrets appear in prompts, logs, traces, or model output | 3 | 5 | 15 | High | Secret isolation, DLP/redaction, retention control, output screening |
| TM-012 | Repudiation | Admin changes policy or access without attributable audit record | 3 | 4 | 12 | High | Immutable centralized audit, actor/session/correlation IDs, alert on log gaps |
| TM-013 | Elevation | Kubernetes workload obtains node or cloud credentials | 3 | 5 | 15 | High | Workload identity, IMDS restrictions, pod hardening, RBAC and runtime detection |
| TM-014 | Denial of Service | Queue poison message causes retry storm and worker saturation | 3 | 4 | 12 | High | DLQ, bounded retries, poison-message handling, queue-age alarms |
| TM-015 | Information Disclosure | Excessive telemetry stores tokens or personal data | 3 | 4 | 12 | High | Structured logging allowlist, redaction tests, retention and access policy |
| TM-016 | Tampering | Dependency confusion or compromised package enters build | 3 | 5 | 15 | High | Trusted registries, lockfiles, provenance, SBOM, SCA and review |
| TM-017 | Spoofing | Service accepts token from untrusted issuer or wrong audience | 3 | 5 | 15 | High | Exact issuer/audience/algorithm validation; negative JWT tests |
| TM-018 | Repudiation | Security event dropped or altered before SIEM ingestion | 3 | 4 | 12 | High | Durable buffering, integrity checks, delivery SLO, gap detection |
| TM-019 | Tampering | Unauthorized database migration changes schema/data | 2 | 5 | 10 | High | Separate migration identity, reviewed migration, backup, approval and audit |
| TM-020 | Elevation | Break-glass role remains active after emergency | 2 | 5 | 10 | High | JIT expiry, session recording, alerting, post-use review and credential rotation |

## Risk treatment record

Every High/Critical threat must have:
- named service owner and security control owner;
- treatment decision (mitigate, avoid, transfer, accept);
- target date and measurable acceptance criteria;
- verification artifact (test, policy result, log, configuration, or exercise);
- residual likelihood/impact with rationale;
- exception ID and expiry if accepted.

## Release gates

- Any open Critical risk blocks production release unless an explicitly authorized executive risk owner accepts it under documented policy.
- High risks require security architecture approval and a funded remediation plan.
- A planned control does not count as implemented.
- A compensating control must be independently testable and monitored.
