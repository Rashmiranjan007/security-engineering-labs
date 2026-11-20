# AI Application Security Lab

## Objective
Build a practical, defensive reference implementation for securing LLM-powered applications, including model access, prompts, retrieval-augmented generation (RAG), tools, and data flows.

## Threat model
Assets: system prompts, user data, retrieved documents, model/API credentials, tool permissions, and generated outputs.

Trust boundaries:
1. User input to application
2. Application to model provider
3. Retrieval service to document store
4. Model/tool router to external tools
5. Application logs and monitoring pipeline

Threats include direct and indirect prompt injection, sensitive information disclosure, insecure output handling, excessive agency, data poisoning, denial of service, and supply-chain compromise.

## Security controls
- Treat user prompts and retrieved content as untrusted data.
- Keep authorization decisions outside the model; enforce them in deterministic application code.
- Apply least privilege to tools and service identities.
- Enforce tenant-aware retrieval filters before context reaches the model.
- Redact secrets and sensitive data before logging; define retention controls.
- Validate model output against schemas before downstream use.
- Add rate limits, token budgets, timeouts, and abuse monitoring.
- Store API keys in a secrets manager; never commit credentials.
- Use human approval for high-impact actions.

## Lab plan
- [ ] Create a minimal toy RAG application with synthetic documents.
- [ ] Demonstrate direct and indirect prompt injection safely.
- [ ] Test cross-tenant retrieval isolation.
- [ ] Add output schema validation and tool authorization.
- [ ] Add secret redaction and security event logging.
- [ ] Document tests, findings, and mitigations.

## Validation scenarios
| Scenario | Expected secure behavior |
|---|---|
| Prompt asks for system prompt | No confidential prompt or secret is disclosed |
| Retrieved document contains hostile instructions | Content is treated as untrusted data |
| User requests another tenant's document | Retrieval authorization denies access |
| Model proposes an unauthorized tool action | Application policy blocks execution |
| Output contains malformed JSON | Schema validation rejects it |

## Success criteria
Every test has a reproducible input, expected result, observed result, and remediation note.

> Use synthetic data and isolated local environments only. This project is for defensive testing and education.
