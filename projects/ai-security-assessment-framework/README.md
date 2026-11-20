# Enterprise AI Security Assessment Framework

**Level:** Principal / Staff Security Engineer  
**Scope:** Enterprise LLM, RAG, AI agents, model lifecycle, inference APIs, and AI-enabled business workflows.  
**Status:** Reference assessment methodology with synthetic test cases and control evidence guidance.

## Executive objective

Provide a repeatable, risk-based way to assess AI systems across design, build, deployment, and runtime. The framework focuses on security properties that traditional application reviews can miss: untrusted model context, retrieval authorization, tool autonomy, model and dataset provenance, output handling, and probabilistic behavior.

This is a fictional reference framework. It does not represent an employer or customer environment.

## Assessment coverage

| Domain | What to assess |
|---|---|
| Governance and inventory | Use case, business owner, data classification, model/system inventory, risk tier |
| Data and privacy | Training/fine-tuning data provenance, consent/legal basis, PII, retention, deletion, leakage |
| Model supply chain | Model source, weights, signatures/hashes, tokenizer, adapters, dependencies, artifact access |
| Prompt and context | Direct/indirect prompt injection, instruction hierarchy, system prompt exposure, context poisoning |
| RAG and vector stores | Tenant/document ACLs, ingestion trust, retrieval filters, embedding leakage, index isolation |
| Agent and tool security | Tool allowlists, per-action authorization, least privilege, approval gates, SSRF/egress, secrets |
| API and identity | AuthN/AuthZ, tenant binding, quotas, replay protection, service identity, key management |
| Inference/runtime | Abuse detection, resource exhaustion, model endpoint isolation, output validation, telemetry |
| Evaluation and resilience | Adversarial evaluations, regression tests, drift, fallback, human escalation, incident response |

## Repository guide

- [Reference architecture](docs/reference-architecture.md)
- [Control matrix and evidence requirements](docs/control-matrix.md)
- [Assessment playbook](docs/assessment-playbook.md)
- [Synthetic assessment test catalogue](test-cases/assessment-catalogue.json)
- [Catalogue validator](tools/validate_catalogue.py)
- [Validator unit tests](tools/test_validate_catalogue.py)

## How to run

Requires Python 3.10+ and the standard library.

```bash
cd projects/ai-security-assessment-framework
python tools/validate_catalogue.py --input test-cases/assessment-catalogue.json
python -m unittest discover -s tools -v
```

The catalogue validator checks structure and required fields. It does not execute prompts, call models, or test a live target. Use the playbook to conduct authorized reviews and record evidence.

## Assessment workflow

1. Register the system, business owner, data classes, model/provider, deployment pattern, and intended users.
2. Map data flows, trust boundaries, retrieval sources, model endpoints, tools, and human approval points.
3. Select controls and tests based on system risk, not merely the presence of an LLM.
4. Validate identity, data isolation, model provenance, tool authorization, and abuse protections.
5. Record evidence, gaps, likelihood, impact, accountable owner, remediation date, and residual risk.
6. Re-test after model, prompt, dataset, tool, provider, or architecture changes.

## Risk rating

Use likelihood and impact from 1–5; inherent risk = likelihood × impact. Suggested bands: 1–4 Low, 5–9 Moderate, 10–16 High, 17–25 Critical. The score supports prioritization; it is not a probability or a substitute for documented rationale. Do not reduce residual risk until the control is implemented and operating evidence is reviewed.

## Design principles

- Treat model output and retrieved content as untrusted data.
- Keep authorization outside the model; never rely on prompt instructions as an access-control boundary.
- Authorize every tool action server-side using the initiating user's identity and scoped service identity.
- Enforce tenant and document ACLs before content reaches the model context.
- Separate system instructions, user content, retrieved content, and tool results.
- Use least privilege, bounded execution, explicit egress, and human approval for consequential actions.
- Log security-relevant events without storing secrets or unnecessary sensitive prompts.
- Evaluate behavior continuously; one successful test run does not establish safety.

## Related portfolio projects

This assessment framework complements the [AI Security Application](../ai-security/README.md), [AI Red Team Toolkit](../ai-red-team-toolkit/README.md), [Enterprise AI Security Architecture](../enterprise-ai-security-architecture/README.md), and [Hands-on AI Agent Security Lab](../ai-agent-security-lab/README.md).

## Disclaimer

Use only with systems you own or are explicitly authorized to assess. Test cases are synthetic assessment prompts and review scenarios, not instructions to attack third-party systems. Validate regulatory and legal requirements with appropriate specialists.
