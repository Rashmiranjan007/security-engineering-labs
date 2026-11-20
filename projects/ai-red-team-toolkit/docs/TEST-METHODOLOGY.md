# AI Red Team Toolkit — Test Methodology

## Purpose

Define repeatable, authorized tests for AI-enabled applications. The initial deliverable is a versioned test-case catalogue; it does not send payloads to public services or claim to assess a live model.

## Test lifecycle

1. Define scope, owner, target environment, and written authorization.
2. Identify the trust boundary and relevant AI application component.
3. Select a test case and record preconditions.
4. Use synthetic prompts, documents, identities, and canary values.
5. Execute in an isolated environment with request/time/token limits.
6. Capture minimal evidence and expected-versus-observed behavior.
7. Assign severity based on impact, exploitability, and exposure.
8. Recommend a control, owner, and retest date.
9. Retest after remediation and retain the result.

## Test case fields

Each JSON case includes a stable ID, risk category, scenario, preconditions, synthetic input, expected behavior, severity, and control references. Keep payloads benign and bounded; do not include real secrets or customer information.

## Initial coverage

| Risk family | Example test objective |
|---|---|
| Prompt injection | Verify untrusted instructions cannot override trusted policy |
| Sensitive information disclosure | Verify synthetic canary values are not disclosed across boundaries |
| RAG data isolation | Verify retrieval respects the authenticated tenant |
| Excessive agency | Verify tool calls are independently authorized |
| Insecure output handling | Verify untrusted output is schema-validated and safely rendered |
| Denial of service | Verify input, token, concurrency, and time limits |
| Supply chain | Verify dependency and model artifact provenance |

## Reporting

Report scope, build/version, test IDs, pass/fail/blocked status, evidence references, severity, residual risk, remediation owner, and retest outcome. Distinguish a blocked test from a passing control test.
