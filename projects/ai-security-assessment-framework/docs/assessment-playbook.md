# AI Security Assessment Playbook

## 1. Intake and scoping

Record:
- Business capability and intended users.
- Business owner, technical owner, model owner, data owner, security contact.
- Model/provider, model version, hosting region, inference path, fallback.
- Data classes in prompts, retrieved context, training/fine-tuning, logs, and outputs.
- RAG sources, vector stores, caches, tools, plugins, APIs, and downstream systems.
- Autonomy level and maximum consequence of an action.
- Internet exposure, tenant model, identities, and third-party dependencies.

## 2. Risk tiering

Assess impact across confidentiality, integrity, availability, privacy, financial loss, safety, and legal/regulatory exposure. Consider scale, affected population, reversibility, and degree of autonomy. Assign an accountable risk owner. High-impact autonomous actions require stronger controls and human review.

## 3. Architecture and threat modeling

Draw data flows and trust boundaries. Identify assets (prompts, context, embeddings, model weights, API keys, tool credentials, outputs, audit events), entry points, privileged operations, external dependencies, and failure modes. Apply STRIDE to services and data flows; add AI-specific abuse cases such as prompt injection, retrieval poisoning, model extraction, sensitive data leakage, unsafe tool use, and resource exhaustion.

## 4. Validation workstreams

### Identity and API
- Reject invalid signature, issuer, audience, expired, and not-yet-valid tokens.
- Verify tenant identity is derived from trusted claims, not caller-controlled headers.
- Attempt cross-tenant object access using synthetic accounts.
- Verify per-user and per-tenant quotas and abuse controls.

### Prompt and context
- Test direct and indirect prompt injection with harmless synthetic instructions.
- Verify retrieved content cannot override system policy or invoke tools by itself.
- Test system prompt disclosure and secret canaries using non-production synthetic values.
- Confirm output is treated as untrusted and safely rendered/consumed.

### RAG and data
- Upload synthetic documents with different tenant ACLs and classifications.
- Verify unauthorized documents never enter the model context, citations, caches, or logs.
- Test document deletion across source, chunk, embedding, cache, and backup lifecycle.
- Validate ingestion provenance, parser limits, content scanning, and poison-content handling.

### Agent and tools
- Attempt disallowed tool names, malformed arguments, parameter overreach, and unauthorized resource IDs.
- Verify authorization occurs in the broker and downstream service, not in model instructions.
- Verify approval gates for irreversible or high-impact operations.
- Confirm timeouts, recursion limits, rate limits, idempotency, and egress restrictions.

### Model and supply chain
- Verify model publisher, version, hash, license, source, and approval.
- Verify model artifacts, adapters, tokenizers, and dependencies are integrity-checked.
- Scan build images and dependencies; retain SBOM and provenance.
- Restrict access to model registries and deployment credentials.

### Runtime, monitoring, and response
- Test inference quotas, concurrency, token limits, and graceful degradation.
- Generate synthetic abuse signals and verify alert routing and triage.
- Verify logs avoid raw secrets and unnecessary sensitive content.
- Exercise model/provider disablement, tool kill switch, key rotation, and incident escalation.

## 5. Findings and risk decisions

For each finding record:
- Unique ID, affected component, threat scenario, and business consequence.
- Reproduction conditions using synthetic data and authorized environment.
- Evidence and exact model/prompt/build version.
- Likelihood (1–5), impact (1–5), inherent score, and rationale.
- Required control, owner, remediation milestone, and retest criteria.
- Residual risk only after implementation and evidence review.
- Exception owner, compensating controls, expiry, and reapproval trigger.

## 6. Release gates

Suggested minimum gates:
- No unresolved P0 authorization or tenant-isolation failures.
- All P1 controls implemented or covered by time-bound, formally approved exceptions.
- Security regression tests run against the exact model, prompt, dataset, and tool configuration intended for release.
- Monitoring, incident ownership, and kill switches verified.
- Model/provider/data changes trigger reassessment proportional to their impact.

## 7. Change-triggered reassessment

Reassess when changing model/provider/version, system prompt, retrieval corpus, embedding model, vector schema, tenant logic, tools, plugin permissions, API scopes, data classification, hosting region, or model-serving infrastructure.

## 8. Report template

| Field | Entry |
|---|---|
| System / version | |
| Business and technical owner | |
| Assessment date / assessor | |
| Scope and exclusions | |
| Data classification | |
| Model/provider and deployment | |
| Autonomy / impact tier | |
| Critical findings | |
| P0/P1 control status | |
| Residual risk and exceptions | |
| Release recommendation | |
| Retest date | |
