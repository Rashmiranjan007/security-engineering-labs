# AI Application Security Lab

A dependency-free Python lab demonstrating practical security controls for LLM and RAG applications. This is a defensive engineering portfolio project, not a production security library.

## Implemented
- Prompt-injection phrase screening (a detection signal, not a complete defense)
- Tenant-isolated document retrieval in trusted application code
- Tool allowlisting and human approval for high-impact actions
- Strict structured-output validation
- Secret-like value redaction for demonstration logs
- Automated regression tests and GitHub Actions CI

## Run locally
Requires Python 3.10+.

```bash
cd projects/ai-security
python -m unittest discover -s tests -v
python -m app.demo
```

No API key, external model, or third-party Python dependency is required.

## Architecture
```text
User Request
    |
    v
Trusted Application Layer ---> Input screening (signal only)
    |
    +----> Tenant authorization ---> Retrieval store
    |
    +----> Model adapter (future extension; untrusted output)
                  |
                  v
          Output schema validation
                  |
                  v
          Policy-controlled tool dispatcher
                  |
          Human approval for high-impact actions
                  |
                  v
              Tool execution

Logs: minimize data -> redact known secrets -> retention controls
```

## Important design decisions
1. Prompt screening is only a detection signal. Regexes cannot reliably identify all prompt injection.
2. Tenant authorization is deterministic and happens outside the model.
3. The model cannot grant itself tool permissions.
4. Each real tool must independently authorize its operation and resource.
5. Schema validation checks shape, not truthfulness or safety.

## Next milestones
- [ ] Add a mock RAG API with authenticated tenant context.
- [ ] Add indirect-injection tests in synthetic retrieved documents.
- [ ] Add policy tests for tool arguments and resource ownership.
- [ ] Add Docker and container hardening checks.
- [ ] Add dependency and secret scanning to CI.
- [ ] Map controls to OWASP LLM Top 10.

See [Threat Model](docs/THREAT-MODEL.md) for scope, trust boundaries, threats, controls, and residual risks.

> Use synthetic data and authorized lab systems only. Never commit real secrets or customer data.
