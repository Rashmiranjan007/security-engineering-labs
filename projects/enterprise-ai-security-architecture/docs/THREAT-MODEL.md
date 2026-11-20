# Enterprise AI Application Threat Model

## Scope and assets

Scope: enterprise assistant with RAG, model gateway, and agent tools. Assets include confidential documents, tenant boundaries, user identity, system instructions, model/provider credentials, tool credentials, business data, approval records, and security telemetry.

## Threat scenarios

| Threat | Attack path | Impact | Required controls |
|---|---|---|---|
| Direct prompt injection | User content attempts to override policy | Policy bypass, data disclosure | Treat user text as untrusted; enforce policy outside model |
| Indirect prompt injection | Retrieved document contains adversarial instructions | Tool misuse or data leakage | Content provenance, trust labels, context isolation, tool authorization |
| Cross-tenant RAG exposure | Retrieval query omits tenant/document ACL | Confidentiality breach | Identity-bound tenant and document ACL filters at data layer |
| RAG poisoning | Attacker uploads malicious or misleading content | Incorrect answers or unsafe actions | Ingestion authorization, provenance, scanning, review, rollback |
| Excessive agency | Model requests privileged tool | Unauthorized action | Tool allowlist, schema validation, resource authorization, approval |
| Insecure output handling | Model output used as SQL/HTML/command | Injection or execution | Context-aware output encoding; parameterized operations; no shell interpolation |
| Sensitive data disclosure | Prompt, retrieval, output, or logs expose secrets/PII | Confidentiality and compliance impact | DLP, minimization, redaction, access controls, retention |
| Model supply-chain compromise | Untrusted model/provider/plugin or dependency | Backdoor, data exposure | Approved sources, artifact provenance, version pinning, vendor review |
| Denial of service / cost abuse | Large inputs, loops, repeated tool calls | Availability and financial impact | Input/token/concurrency/time budgets, quotas, circuit breakers |
| Audit tampering | Events altered or over-collected | Loss of evidence or privacy breach | Append-only audit, access control, integrity protection, minimization |

## Abuse cases and security invariants

- A user cannot read a document unless the document ACL authorizes that user.
- A model cannot grant permissions, alter tenant context, or approve its own tool call.
- Every tool call is authorized at execution time against the actual target resource.
- An approval is valid only for the exact action, parameters, principal, and time window approved.
- Retrieved text cannot modify system policy or tool permissions.
- Sensitive data is not sent to an unapproved provider or written to unrestricted logs.

## Risk assessment

Prioritize by data sensitivity, exposure, exploitability, blast radius, and business impact. Treat cross-tenant access, privileged tool execution, and secret disclosure as critical until proven otherwise.

## Residual risk

No prompt-injection filter can guarantee that a model will ignore adversarial content. The architecture therefore assumes model behavior can be manipulated and relies on independent authorization, constrained tools, least privilege, and human review for high-impact actions.
