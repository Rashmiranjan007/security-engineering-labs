# Automated STRIDE Threat Identification Engine

## Objective

Convert a structured architecture inventory into a repeatable set of candidate STRIDE threats. The engine is a rules-based decision-support tool: it accelerates threat discovery, preserves traceability to components and data flows, and produces a reviewable JSON report. It does not replace architecture review or human risk judgment.

## Pipeline

```mermaid
flowchart LR
  A[Architecture inventory JSON] --> B[Schema and input validation]
  B --> C[Component and flow normalization]
  C --> D[STRIDE rule engine]
  D --> E[Candidate threat records]
  E --> F[Risk scoring and control mapping]
  F --> G[JSON report + review queue]
  G --> H[Security architect validation]
  H --> I[Approved threat register]
```

## Inputs

The inventory declares:
- system name and environment;
- components with type, trust zone, data classification, exposure, and security properties;
- data flows with source, destination, protocol, authentication, encryption, and trust-boundary crossing;
- optional tags such as `tenant-aware`, `internet-facing`, `privileged`, `ai-enabled`, and `event-driven`.

See [sample-architecture.json](sample-architecture.json).

## Run locally

Requires Python 3.10+ and no third-party packages.

```bash
cd Threat-Modeling/enterprise-cloud-ai-platform/automation
python stride_engine.py --input sample-architecture.json --output generated-threats.json
python -m unittest -v
```

## Rule design

| STRIDE category | Example trigger | Candidate concern |
|---|---|---|
| Spoofing | Internet-facing flow without declared authentication | Unauthenticated caller or forged identity |
| Tampering | Event-driven flow without integrity/replay controls | Message alteration or replay |
| Repudiation | Sensitive component without audit logging | Unattributable privileged or data action |
| Information Disclosure | Restricted data store with public exposure or weak access declaration | Unauthorized data access |
| Denial of Service | Internet-facing component without rate limiting | Resource or cost exhaustion |
| Elevation of Privilege | Privileged component with broad permissions or untrusted input | Privilege escalation |

The engine emits candidate threats with rule IDs, affected component/flow IDs, rationale, suggested controls, and default inherent score. A trigger indicates a review question, not proof of a vulnerability.

## Governance and safe use

- Validate inventory completeness before interpreting output.
- Review false positives and false negatives with service owners.
- Never auto-close or auto-accept threats from generated output.
- Do not lower residual risk until controls have operating evidence.
- Version the architecture input and generated report together.
- Use fictional or sanitized architecture data in public repositories.
- Treat generated descriptions as untrusted input if reports are passed to other automation.

## Extending the engine

Add new rules as small deterministic functions with stable IDs and unit tests. Require each rule to specify its STRIDE category, trigger logic, rationale, and actionable control guidance. Introduce schema versioning before making breaking changes.
