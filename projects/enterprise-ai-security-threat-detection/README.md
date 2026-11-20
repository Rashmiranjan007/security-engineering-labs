# Enterprise AI Security Architecture & Threat Detection Platform

A portfolio-grade reference platform for governing and detecting security risks across enterprise AI applications, RAG pipelines, AI agents, model artifacts, and Kubernetes-hosted inference services.

This project is the enterprise operating layer for the repository's focused labs. It does not replace them: it demonstrates how architecture guardrails, security telemetry, detection logic, risk prioritization, incident response, and governance fit together.

## Capabilities

- Enterprise reference architecture and trust-boundary documentation
- Synthetic security-event schema and detection-rule catalogue
- Deterministic detection engine for AI-specific and platform security events
- Severity-weighted risk scoring and recommended response actions
- JSON evidence output and Markdown executive/operations report
- Governance model, ownership, escalation, and response playbook
- Local SOC simulation with synthetic ingestion, alert correlation, incident lifecycle, audit trail, and playbooks
- EKS runtime telemetry adapter, six Kubernetes/runtime detection rules, and end-to-end SOC integration tests
- Unit tests and GitHub Actions validation

## Architecture

```text
  AI applications / RAG / agents / model registry / Kubernetes
                         |
                  Trusted telemetry
                         |
              Event normalization layer
                         |
               Detection & policy engine
                         |
            +------------+-------------+
            |                          |
       Risk scoring              Evidence store
            |                          |
       Alert routing                 Reports
            |
     SOC / AI Security / Platform owners
            |
   Triage -> Contain -> Remediate -> Validate
            |
        Governance & metrics
```

See [reference architecture](docs/reference-architecture.md), [detection catalogue](docs/detection-catalogue.md), and [operating model](docs/operating-model.md).

## Detection coverage

| Detection | Example signal | Default severity |
|---|---|---|
| Prompt injection | Untrusted instruction override indicator | High |
| RAG tenant boundary violation | Retrieved resource tenant differs from caller tenant | Critical |
| Agent privilege misuse | Tool invocation without authorization or approval | Critical |
| Sensitive output | Synthetic secret/canary appears in model output | High |
| Model integrity failure | Artifact digest differs from approved digest | Critical |
| AI policy drift | Runtime policy version differs from approved version | Medium |

## How to run

Python 3.10+; standard library only.

```bash
cd projects/enterprise-ai-security-threat-detection
python detector.py --input scenarios/sample-events.json
python -m unittest discover -s tests -v
```

The JSON and Markdown reports are written to `reports/latest.json` and `reports/latest.md`. The sample data is synthetic.

## Local dashboard

A dependency-free browser dashboard provides incident KPIs, severity distribution, workload exposure, searchable and filterable detections, and a selectable incident investigation panel. See [dashboard instructions](dashboard/README.md). Generate the local report first, then serve the project directory with Python's built-in HTTP server.

## Local SOC simulation

A loopback-only SOC console adds simulated telemetry ingestion, workload/actor/time-window correlation, incident ownership, an audited lifecycle, and event-specific response playbooks. See [SOC lab instructions](soc-lab/README.md). Start it with `python soc-lab/server.py` from this project directory. The service is bound to localhost and is not a production integration.

## EKS runtime-to-SOC integration

The [EKS runtime simulation](eks-runtime-simulation/README.md) normalizes synthetic Kubernetes audit, admission, workload identity, NetworkPolicy drift, image-integrity, and runtime-sensor signals into the SOC event schema. It feeds the same local API and detection rules, creating incidents and response playbooks. This is a local simulation only; it does not connect to AWS, EKS, or a runtime security vendor.

## Risk scoring

Each matched event receives a severity and a configurable risk score from the rule catalogue. The aggregate score is capped at 100 for dashboard presentation. This is a prioritization aid, not a probability of compromise or a compliance score. Tune weights against business impact, exposure, exploitability, and asset criticality before production use.

## Production integration considerations

A real deployment would require authenticated telemetry ingestion, schema validation, tenant-aware access control, durable storage, event integrity, alert deduplication, SIEM/SOAR integration, secrets management, privacy controls, and operational SLOs. Enforce authorization at the source system; never rely on a detection pipeline as the only preventive control.

## Safety and limitations

- This implementation reads local JSON files and generates local reports only.
- It does not connect to an LLM, cloud account, SIEM, registry, cluster, or external endpoint. The EKS adapter uses synthetic fixtures and sends only to the loopback SOC API.
- All event data is synthetic. No credentials, personal data, or employer telemetry should be committed.
- Detection rules are deterministic examples, not a complete AI threat detector.
- A clean report does not prove that an AI system is secure.

## Portfolio positioning

Demonstrates Principal-level security engineering across architecture, threat modeling, detection engineering, risk governance, security operations, and automation—not just individual security checks.
