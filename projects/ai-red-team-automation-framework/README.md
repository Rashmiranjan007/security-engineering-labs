# AI Red Team Automation Framework

A deterministic, local-only automation harness for exercising AI application security controls against a synthetic mock target. This project extends the catalogue in [AI Red Team Toolkit](../ai-red-team-toolkit/README.md): that project validates test-case quality; this one executes safe simulations, evaluates outcomes, scores risk, and produces evidence reports.

## What it tests

- Direct and indirect prompt-injection handling
- RAG tenant-isolation enforcement
- Agent tool authorization and approval boundaries
- Sensitive-output / canary disclosure controls
- Abuse throttling for repeated requests

## Architecture

```text
Synthetic test catalogue (JSON)
          |
          v
     Test runner  -------> Scope guard (local mock only)
          |                            |
          v                            v
   Mock AI target <------------ Control profile
          |
          v
   Assertions + risk scoring
          |
          +------> JSON evidence report
          +------> Markdown summary
```

## Run

Python 3.10+; standard library only.

```bash
cd projects/ai-red-team-automation-framework
python runner.py
python runner.py --profile intentionally-vulnerable
python -m unittest discover -s tests -v
```

The secure profile should pass all scenarios. The intentionally vulnerable profile disables selected mock controls so the harness can demonstrate that it detects control failures; its non-zero exit status is expected.

Reports are written to `reports/latest.json` and `reports/latest.md`. These are generated outputs and are not committed by the workflow.

## Safety and scope

- The runner has no HTTP client, network access, model API integration, shell execution, or external target option.
- Inputs, identities, retrieved documents, tool calls, and canary values are synthetic.
- The mock target is deliberately small and deterministic; it is not a substitute for testing a real application.
- Any future live-target adapter must be a separate, opt-in extension with explicit authorization, a fixed allowlisted endpoint, rate limits, timeouts, and data-handling controls.
- Do not use this project against systems you do not own or have explicit permission to assess.

## Interpretation

A passing run means only that the simulated controls behaved as expected for this catalogue. It does not prove that an LLM is secure, that prompt injection is solved, or that production controls are effective. Heuristic and synthetic tests have limited coverage.

## Portfolio value

Demonstrates a repeatable security-engineering workflow: scenario-as-code, deterministic execution, control assertions, severity-weighted risk scoring, machine-readable evidence, unit tests, and CI validation.
