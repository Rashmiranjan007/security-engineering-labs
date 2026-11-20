# Continuous Compliance and Security Findings Integration

This extension connects synthetic exports from the portfolio's AI security, EKS/cloud posture and model supply-chain labs to the Enterprise AI GRC control catalogue. It normalizes findings, maps them to governance controls, creates an evidence-linked remediation backlog and summarizes control-level attention.

## Run

From this directory:

```bash
python tools/compliance_pipeline.py --sources data/source-findings.json --rules data/control-mappings.json --output-dir reports
python -m unittest discover -s tests -v
python -m http.server 8001
```

Open http://localhost:8001/dashboard/. The dashboard reads `reports/latest.json`; run the pipeline first.

## Current simulated source adapters

- AI security threat detection: prompt-injection, cross-tenant retrieval, unauthorized tool use and model integrity signals.
- EKS/cloud posture: privileged workload, image digest drift, workload identity anomaly and network policy drift.
- AI model supply chain: artifact digest mismatch, unapproved source and missing promotion approval.

The sample events are synthetic snapshots. The pipeline reads JSON files only. It does not connect to AWS, Kubernetes, CrowdStrike, Prisma Cloud, Wiz, GitHub APIs, a SIEM, a ticketing system or any external service. Source adapters are deliberately represented as export contracts so real integrations can be added behind approved credentials and APIs later.

## Important compliance semantics

- A finding is a risk signal, not proof that a control is ineffective or that a legal requirement has been breached.
- No mapped findings in a snapshot does **not** mean a control passed or the organization is compliant.
- A finding marked resolved remains visible in the report; closure requires evidence reference and human validation.
- Accepted risk is shown separately and is not counted as remediation closure.
- Control mappings are portfolio examples. Validate applicability, control ownership and regulatory interpretation with accountable teams.

See [integration architecture](docs/integration-architecture.md) and [source contract](docs/source-contract.md).
