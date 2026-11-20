# Defensive AI Red Team Toolkit

A structured catalogue and validation starter for assessing AI application security in an authorized lab. The initial version focuses on test design quality and repeatability; it does not send attack payloads to public services or claim to assess a live model.

## Included

- Versioned JSON catalogue of synthetic AI security test cases
- Direct prompt-injection, RAG tenant-isolation, excessive-agency, and unbounded-input scenarios
- Required-field, severity, and duplicate-ID validation
- Test methodology, evidence expectations, and authorization guardrails
- Unit tests for catalogue validation

## How to run

Requires Python 3.10+ and uses only the Python standard library.

```bash
cd projects/ai-red-team-toolkit
python validate_cases.py
python -m unittest -v
```

Expected output:

```text
Validated 4 AI security test cases.
```

## Test case format

Each case records a stable ID, risk category, scenario, preconditions, synthetic input, expected safe behavior, severity, and control references. Add new cases to `test-cases/llm-security-cases.json` and run the validator before submitting a change.

## Current coverage

| Test ID | Risk area | Expected security property |
|---|---|---|
| LLM-PI-001 | Direct prompt injection | Trusted policy remains authoritative |
| LLM-RAG-001 | RAG tenant isolation | Retrieval cannot cross authenticated tenant boundary |
| LLM-AG-001 | Excessive agency | Tool independently authorizes role and resource |
| LLM-DO-001 | Unbounded input | Request is rejected before expensive processing |

## Roadmap

- [ ] Add a local mock target adapter and deterministic attack/defense integration tests.
- [ ] Add indirect prompt-injection cases in synthetic retrieved documents.
- [ ] Add structured Markdown/JSON assessment reports.
- [ ] Add optional integration against a user-owned local endpoint with explicit scope and rate limits.
- [ ] Expand coverage across OWASP LLM application risks.

## Guardrails

- Run only against applications you own or have explicit permission to assess.
- Use synthetic prompts, documents, identities, and canary values.
- Apply strict request, token, concurrency, and time limits.
- Do not store real credentials or personal data in test output.

See [Test Methodology](docs/TEST-METHODOLOGY.md).

> This is a defensive testing starter, not a complete red-team scanner or a guarantee of AI application security.
