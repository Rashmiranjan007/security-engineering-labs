# AI Application Threat Model

## Scope
A toy multi-tenant retrieval-augmented generation (RAG) service with an LLM, a document store, and optional tools. The lab uses synthetic data and deterministic mock behavior; no external model API is called.

## Assets
- Tenant documents and metadata
- System/developer instructions
- Model and service credentials
- Tool capabilities and downstream systems
- Security logs and test evidence

## Trust boundaries
1. User to application API
2. Application to model provider
3. Retrieval service to document store
4. Model output to tool dispatcher
5. Application to logging/monitoring

## Abuse cases and controls
| Threat | Control demonstrated | Residual risk |
|---|---|---|
| Direct prompt injection | Suspicious-input screening | Pattern screening is bypassable; never treat it as the primary security boundary |
| Indirect injection in retrieved text | Treat retrieved content as untrusted; enforce policy in application code | Model may still be influenced by malicious context |
| Cross-tenant data exposure | Tenant filter in trusted retrieval code | Production systems need identity-bound authorization and datastore-level isolation |
| Excessive agency | Tool allowlist and approval gate | Tool implementation must independently authorize every action |
| Unsafe model output | Strict response contract | Schema validity does not prove semantic safety |
| Secret leakage in logs | Redaction example | Redaction patterns are incomplete; minimize and classify logs at source |

## Security assumptions
- The caller's tenant identity is authenticated by trusted middleware.
- The model is not an authorization authority.
- Tool implementations re-check authorization at execution time.
- Synthetic data is used throughout this lab.

## Out of scope
Production-grade prompt-injection prevention, model training, real cloud credentials, and third-party service testing.
