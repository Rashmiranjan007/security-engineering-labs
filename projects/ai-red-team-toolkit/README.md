# Defensive AI Red Team Toolkit

## Objective
Create a repeatable test harness for evaluating LLM application security in an authorized lab. The toolkit focuses on detecting weaknesses and producing actionable reports, not attacking third-party services.

## Initial test categories
- Prompt injection: direct and indirect instruction override attempts
- Sensitive information disclosure: synthetic secrets and canary values
- Insecure output handling: malformed or adversarial model output
- Excessive agency: unauthorized tool invocation attempts
- RAG security: document access control and retrieval isolation
- Denial of service: bounded tests for oversized input and resource exhaustion
- Supply chain: dependency and model artifact provenance checks

## Proposed layout
```text
ai-red-team-toolkit/
  README.md
  test-cases/
  harness/
  reports/
  docs/
```

## Test record format
Each test should capture:
- Test ID and risk category
- Preconditions and lab configuration
- Synthetic input/payload
- Expected safe behavior
- Actual result
- Severity and evidence
- Recommended mitigation

## Guardrails
- Run only against applications you own or have explicit permission to assess.
- Use synthetic prompts, documents, and secrets.
- Apply strict request, token, and time limits.
- Do not store real credentials or personal data in test output.

## Roadmap
- [ ] Define a versioned JSON test-case schema.
- [ ] Build a local test runner with a mock model adapter.
- [ ] Add deterministic pass/fail assertions.
- [ ] Generate Markdown and JSON reports.
- [ ] Add CI workflow for the local test suite.
- [ ] Map cases to OWASP Top 10 for LLM Applications.

## Deliverable
A reproducible assessment workflow that helps developers identify, prioritize, fix, and retest LLM application risks.
