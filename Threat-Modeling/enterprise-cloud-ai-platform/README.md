# Enterprise Threat Modeling & Security Architecture

**Level:** Advanced / Enterprise  
**Scenario:** Multi-tenant digital platform spanning AWS, Kubernetes, microservices, CI/CD, data services, and an AI/RAG capability.  
**Status:** Reference design and threat-model baseline; implementation exercises are intentionally separated from production deployment.

## Executive summary

This project demonstrates a repeatable, risk-driven threat-modeling practice for a complex enterprise platform. It combines system decomposition, trust-boundary analysis, STRIDE, attack trees, MITRE ATT&CK mapping, privacy analysis, risk scoring, security requirements, control ownership, and residual-risk governance.

The reference system is intentionally realistic but fictional. No real customer data, credentials, production endpoints, or internal company architecture are included.

## Business objectives and security outcomes

- Protect tenant isolation, customer data confidentiality, integrity, and availability.
- Establish zero-trust service-to-service access and workload identity.
- Secure internet-facing APIs, asynchronous event flows, and administrative operations.
- Reduce cloud, Kubernetes, CI/CD, software supply-chain, and AI/RAG attack paths.
- Make security decisions traceable to threats, controls, evidence, owners, and risk acceptance.
- Integrate threat modeling into architecture review and CI/CD change governance.

## Scope and assumptions

**In scope:** browser/mobile clients, edge WAF/CDN, API gateway, identity provider, authorization service, tenant-aware microservices, message broker, PostgreSQL, object storage, Kubernetes on AWS, private model gateway, RAG ingestion/retrieval, vector database, CI/CD, artifact registry, secrets/KMS, centralized logging/SIEM, and security operations.

**Out of scope:** provider-internal infrastructure, physical data-center controls, model-provider internals, and legal conclusions. These are tracked as external dependencies and assurance requirements.

**Assumptions:** multi-AZ deployment; private workload subnets; managed cloud services; OIDC federation for CI/CD; workload identity for pods; TLS in transit and encryption at rest; tenant identity is derived from verified claims and never trusted from a caller-controlled header.

## Architecture pack

- [Context and data-flow architecture](diagrams/01-context-and-dfd.md)
- [Deployment and trust-zone architecture](diagrams/02-deployment-and-trust-zones.md)
- [Authentication and authorization sequence](diagrams/03-authn-authz-sequence.md)
- [AI/RAG data-flow and threat boundaries](diagrams/04-ai-rag-data-flow.md)

## Threat-modeling method

1. Define business process, assets, security objectives, assumptions, and abuse cases.
2. Decompose the system into processes, data stores, external entities, and data flows.
3. Mark trust boundaries and identify where identity, privilege, or data classification changes.
4. Enumerate threats with STRIDE; use attack trees for high-impact outcomes.
5. Map relevant adversary behaviors to MITRE ATT&CK (technique mappings are hypotheses, not attribution).
6. Score inherent risk using likelihood × impact; document rationale and uncertainty.
7. Define preventive, detective, and responsive controls with accountable owners.
8. Verify controls through testable evidence; calculate residual risk after validation.
9. Obtain time-bound risk acceptance for unresolved high risks and track remediation.
10. Revisit the model on material architecture, threat, vendor, or data-classification changes.

## Risk model

Use a 1–5 likelihood and 1–5 impact scale. Inherent score = likelihood × impact.

| Score | Rating | Default treatment |
|---:|---|---|
| 1–4 | Low | Owner-managed; monitor |
| 5–9 | Moderate | Planned mitigation; documented rationale |
| 10–16 | High | Mitigation plan, security review, target date |
| 17–25 | Critical | Block release unless formally accepted by authorized executive risk owner |

Residual risk is scored only after control design and operating evidence are reviewed. A control that is merely planned does not reduce risk. Risk acceptance must name the accountable business owner, compensating controls, expiry date, and re-review trigger.

## Key security design decisions

- **Identity:** OIDC federation, short-lived credentials, MFA for privileged humans, workload identity for services, no static cloud keys in CI.
- **Authorization:** deny by default; tenant and resource authorization at the service boundary; object-level authorization on every request.
- **Network:** private subnets, restricted egress, ingress through managed edge controls, explicit service policies, private endpoints where supported.
- **Kubernetes:** least-privilege RBAC, Pod Security Standards, admission policy, signed images, restricted capabilities, read-only root filesystem, resource quotas, network policies, runtime detection.
- **Data:** classification, tenant-scoped queries, envelope encryption with KMS, managed secrets, retention/deletion controls, audited privileged access.
- **Software supply chain:** protected branches, review gates, pinned dependencies, SBOM, provenance, artifact signing, vulnerability policy, isolated build runners.
- **AI/RAG:** tenant-aware retrieval, source authorization, prompt-injection defenses, tool allowlists, output validation, sensitive-data filtering, model and prompt versioning, abuse monitoring.
- **Detection:** centralized immutable audit events, correlation IDs, cloud control-plane logs, Kubernetes audit/runtime events, API security signals, AI abuse signals, alert ownership and response runbooks.

## Repository map

| Path | Purpose |
|---|---|
| `diagrams/` | Architecture, trust boundaries, and sequence diagrams |
| `threats/` | Threat register, attack trees, STRIDE analysis |
| `controls/` | Security requirements and control-to-threat traceability |
| `governance/` | Risk methodology, RACI, review lifecycle, exception process |
| `scenarios/` | Abuse cases and validation exercises |

## How to use this project

Start with the context diagram, review the threat register, then trace each high-risk threat to a control and a verification test. Use the governance documents to run a design review. Treat all diagrams and sample scores as a worked example to be challenged—not as proof that a deployed system is secure.

## Disclaimer

This is an educational reference architecture. It does not represent the internal design of any employer or customer. Validate cloud-provider capabilities, service limits, regulatory obligations, and control effectiveness before production use.
