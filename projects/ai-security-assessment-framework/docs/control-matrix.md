# AI Security Control Matrix

The matrix defines expected control outcomes and evidence. Tailor applicability to the system's model type, data sensitivity, autonomy, deployment, and regulatory scope.

| ID | Domain | Control objective | Example evidence | Priority |
|---|---|---|---|---|
| GOV-01 | Governance | Named business, system, model, and data owners | Inventory, RACI, approved use case | P1 |
| GOV-02 | Governance | Risk tier and prohibited-use boundaries documented | AI impact assessment, policy | P1 |
| DATA-01 | Data | Training/fine-tuning data provenance and rights are traceable | Dataset manifest, approvals | P1 |
| DATA-02 | Data | PII and secrets are detected/minimized before indexing or training | DLP results, pipeline policy | P1 |
| DATA-03 | Data | Retention, deletion, and subject-rights workflows cover derived stores | Deletion test evidence, runbook | P1 |
| MOD-01 | Model supply chain | Model source, version, hash, license, and publisher are recorded | Model card, artifact manifest | P1 |
| MOD-02 | Model supply chain | Model weights/adapters are access-controlled and integrity-verified | Registry ACL, signature verification | P1 |
| MOD-03 | Model supply chain | Dependencies and serving images are scanned and pinned | SBOM, scan report, image digest | P1 |
| PROM-01 | Prompt/context | User and retrieved content are treated as untrusted instructions | Design review, adversarial test | P1 |
| PROM-02 | Prompt/context | System prompt and secrets are not treated as authorization controls | Negative tests, code review | P1 |
| RAG-01 | RAG | Tenant/document ACLs enforced before context assembly | Cross-tenant test, query logs | P0 |
| RAG-02 | RAG | Ingestion validates provenance, content type, malware, and classification | Pipeline evidence | P1 |
| RAG-03 | RAG | Cache and vector filters are tenant-aware and fail closed | Cache-key review, isolation tests | P0 |
| AGT-01 | Agents | Tool calls are allowlisted and schema-validated | Tool registry, schema tests | P0 |
| AGT-02 | Agents | Each action is independently authorized for user, resource, and operation | Authorization tests, policy logs | P0 |
| AGT-03 | Agents | High-impact actions require human approval and idempotency controls | Approval workflow, audit trail | P1 |
| AGT-04 | Agents | Tool execution has bounded time, retries, recursion, and egress | Runtime config, network policy | P1 |
| IAM-01 | Identity | API validates issuer, audience, expiry, signature, and tenant claims | Auth tests, configuration | P0 |
| IAM-02 | Identity | Service identities are short-lived and least privilege | IAM policy review, token TTL | P1 |
| API-01 | API | Rate limits and quotas resist abuse and cost exhaustion | Gateway policy, load tests | P1 |
| API-02 | API | Tenant/resource authorization is checked on every request | Negative authorization suite | P0 |
| RUN-01 | Runtime | Model and tool services are isolated with restricted egress | Network policy, cloud rules | P1 |
| RUN-02 | Runtime | Abuse, anomalous tool use, and sensitive output are monitored | Alert rules, detection tests | P1 |
| RUN-03 | Runtime | Logs redact secrets and minimize sensitive prompt retention | Logging config, sample events | P1 |
| EVAL-01 | Evaluation | Security regression suite runs on model/prompt/data/tool changes | CI run, evaluation report | P1 |
| EVAL-02 | Evaluation | Drift, fallback, and human escalation are defined | SLOs, incident runbook | P2 |
| IR-01 | Response | AI-specific incident scenarios and kill switches are tested | Tabletop, runbook, exercise results | P1 |

## Priority interpretation

- **P0:** foundational authorization/isolation control; block production exposure when absent.
- **P1:** required before production for most enterprise use cases; documented exception only with accountable risk owner.
- **P2:** maturity control or conditional requirement based on use case.

## Evidence quality

Prefer configuration exports, automated test results, access-control policies, signed manifests, logs with correlation IDs, and observed operating evidence. A policy document alone is not evidence that a control is effective. Capture test date, environment, build/model version, reviewer, result, and artifact location.
