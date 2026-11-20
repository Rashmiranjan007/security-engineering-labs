# Threat-model validation plan

Run only against local labs, isolated test accounts, or explicitly authorized environments. Do not test production systems without written authorization and a defined change window.

| Test ID | Scenario | Expected secure behavior | Evidence |
|---|---|---|---|
| VT-01 | Change object ID to another tenant's record | 403/404; no data leakage; security event emitted | API test output |
| VT-02 | Submit forged tenant / role headers | Headers ignored or rejected; verified identity remains authoritative | Gateway and service test |
| VT-03 | Wrong issuer / audience / expired JWT | Request rejected before business logic | Auth test report |
| VT-04 | Replay duplicate event | Idempotent handling; no duplicate state transition | Broker/worker test |
| VT-05 | Attempt public object storage configuration | Policy blocks deployment or alerts before exposure | IaC policy result |
| VT-06 | Deploy unsigned or untrusted image | Admission controller rejects workload | Admission event |
| VT-07 | CI job from untrusted ref requests production role | OIDC trust denies role assumption | Cloud audit event |
| VT-08 | Retrieved document contains indirect prompt injection | No unauthorized tool call; content treated as untrusted | AI evaluation trace |
| VT-09 | Tenant A asks RAG for tenant B document | No cross-tenant result, citation, or metadata leakage | Retrieval test |
| VT-10 | Model attempts tool call with invalid or excessive arguments | Schema and policy layer rejects call | Tool broker audit |
| VT-11 | Prompt contains secrets / sensitive data | Data policy blocks or redacts before external processing | DLP evidence |
| VT-12 | High-rate API / model request | Quotas and budgets enforce bounded consumption | Load test and metrics |
| VT-13 | Queue receives poison message | Bounded retries; DLQ; no retry storm | Queue metrics |
| VT-14 | Disable or interrupt log forwarder | Gap alert fires; events are buffered or loss is surfaced | SIEM alert and pipeline SLO |
| VT-15 | Restore database from backup | Recovery meets agreed RTO/RPO and integrity checks pass | Restore exercise report |

## Exit criteria

- All Critical test cases pass.
- High-risk failures have documented remediation or approved time-bound exception.
- Evidence is attached to the relevant threat and control IDs.
- Re-test is completed after remediation.
- Model owner, engineering owner, and security reviewer approve the updated residual risk.
