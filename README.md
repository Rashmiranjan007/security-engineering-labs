# Security Engineering Labs

A practical portfolio of cloud security, Kubernetes security, DevSecOps, AI application security, and defensive AI red-team engineering.

## About

I am a Principal Information Security Engineer with 12+ years of experience across cloud security, container and Kubernetes security, product security, vulnerability management, DevSecOps, and emerging AI security. This repository contains independent learning projects, reference implementations, architecture notes, and security validation examples.

## Portfolio

| Project | What it demonstrates | Current assets |
|---|---|---|
| [AWS EKS Security Engineering Platform](projects/aws-eks-ai-security-platform/README.md) | Private EKS foundation and AI workload security | Terraform VPC/EKS/KMS/IRSA, private API, managed nodes, Pod Security, NetworkPolicy, Kyverno, CI validation |
| [Cloud Security Posture](projects/cloud-security-posture/README.md) | AWS security foundations and Terraform IaC controls | Private S3 baseline, architecture, threat model, operating checklist |
| [Kubernetes Security](projects/kubernetes-security/README.md) | Workload hardening and cluster guardrails | Restricted namespace, hardened deployment, default-deny network policy, Kyverno validation example, security baseline |
| [Kubernetes AI Workload Security](projects/kubernetes-ai-workload-security/README.md) | Secure AI model-serving workloads on Kubernetes/EKS | GPU isolation, workload identity, model supply-chain controls, NetworkPolicy, Kyverno admission policy, validation tests |
| [AI Security](projects/ai-security/README.md) | Identity-aware AI/RAG application security | JWT identity, role authorization, tenant-filtered retrieval, security telemetry, API tests |
| [AI Red Team Toolkit](projects/ai-red-team-toolkit/README.md) | Structured, authorized AI security testing | Test methodology, OWASP-aligned synthetic test catalogue, catalogue validator |
| [Enterprise AI Security Architecture](projects/enterprise-ai-security-architecture/README.md) | Enterprise LLM and agent security | Architecture, threat model, RAG/identity/data controls, tool authorization policy tests |
| [Hands-on AI Agent Security Lab](projects/ai-agent-security-lab/README.md) | Runnable local LLM + RAG + agent-tool security lab | Ollama, Qdrant, FastAPI, tenant ACLs, server-side tool policy, Docker Compose |
| [Enterprise AI Security Assessment Framework](projects/ai-security-assessment-framework/README.md) | Risk-based assessment of LLM, RAG, agents, model supply chain, and runtime controls | Reference architecture, control matrix, assessment playbook, 20 synthetic tests, catalogue validator |
| [AI Runtime Security Lab](projects/ai-runtime-security-lab/README.md) | Runtime guardrails and detection simulation for AI applications and agents | Prompt-injection indicators, tenant binding, tool authorization, approval gates, abuse limits, output redaction, tests |
| [AI Model Supply Chain Security Lab](projects/ai-model-supply-chain-lab/README.md) | Verify model artifact integrity and promotion provenance | SHA-256 verification, source/license allowlists, digest-bound approval, tamper and path-traversal tests |
| [AI Red Team Automation Framework](projects/ai-red-team-automation-framework/README.md) | Execute deterministic AI security simulations against a local mock target | Prompt injection, RAG isolation, agent authorization, canary leakage, abuse throttling, risk scoring, JSON/Markdown reports, CI tests |
| [Enterprise AI Security Threat Detection Platform](projects/enterprise-ai-security-threat-detection/README.md) | Enterprise AI security architecture, detection engineering, risk operations, and governance | Reference architecture, six detection rules, synthetic event engine, risk scoring, incident reports, interactive local dashboard, simulated SOC console, EKS runtime telemetry adapter, Kubernetes detection rules, incident correlation, response playbooks, CI tests |
| [Enterprise AI Governance & GRC](projects/enterprise-ai-governance-grc/README.md) | Enterprise AI governance, risk, compliance and assurance | AI inventory, 18-control catalogue, NIST AI RMF/ISO 42001/EU AI Act mapping notes, risk engine, evidence tracking, vendor due diligence, model cards, incident playbook, local dashboard, tests |
| [Malware Analysis & Reverse Engineering](projects/malware-analysis-reverse-engineering/README.md) | Defensive static malware triage and reverse-engineering methodology | SHA-256 evidence, PE/ELF/Mach-O identification, PE import parsing, entropy, strings, optional YARA, IOC extraction, sandbox-report normalization, benign Ghidra reverse-engineering exercise, sandbox safety, ATT&CK mapping, offline tests |

## How to run the portfolio

There is no single repository-wide install: each lab has its own prerequisites and safe execution steps. Open the relevant project README below and follow its **How to run** section. Most Python-only labs use Python 3.10+ and the standard library; the hands-on AI Agent lab additionally needs Docker Compose and local Ollama/Qdrant services, while the cloud and Kubernetes examples require the relevant sandbox tools and credentials.

| Lab | Run guide |
|---|---|
| AWS EKS security platform | [AWS EKS Security Engineering Platform](projects/aws-eks-ai-security-platform/README.md#how-to-run) |
| Cloud / Terraform | [Cloud Security Posture](projects/cloud-security-posture/README.md#how-to-run) |
| Kubernetes hardening | [Kubernetes Security](projects/kubernetes-security/README.md#how-to-run) |
| Kubernetes AI workloads | [Kubernetes AI Workload Security](projects/kubernetes-ai-workload-security/README.md#how-to-run) |
| AI application security | [AI Security](projects/ai-security/README.md#how-to-run) |
| AI agent + RAG | [Hands-on AI Agent Security](projects/ai-agent-security-lab/README.md#how-to-run) |
| AI architecture and policy | [Enterprise AI Security Architecture](projects/enterprise-ai-security-architecture/README.md#how-to-run) |
| AI runtime controls | [AI Runtime Security](projects/ai-runtime-security-lab/README.md#how-to-run) |
| AI red-team catalogue | [AI Red Team Toolkit](projects/ai-red-team-toolkit/README.md#how-to-run) |
| AI red-team automation | [AI Red Team Automation](projects/ai-red-team-automation-framework/README.md#how-to-run) |
| Model supply chain | [AI Model Supply Chain](projects/ai-model-supply-chain-lab/README.md#how-to-run) |
| AI assessment framework | [AI Security Assessment](projects/ai-security-assessment-framework/README.md#how-to-run) |
| Enterprise AI SOC + EKS | [Threat Detection Platform](projects/enterprise-ai-security-threat-detection/README.md#how-to-run) |
| Interactive dashboard | [Dashboard run guide](projects/enterprise-ai-security-threat-detection/dashboard/README.md#how-to-run) |
| Local SOC console/API | [SOC lab run guide](projects/enterprise-ai-security-threat-detection/soc-lab/README.md#how-to-run) |
| EKS runtime simulation | [EKS simulation run guide](projects/enterprise-ai-security-threat-detection/eks-runtime-simulation/README.md#how-to-run) |
| Enterprise AI governance and GRC | [Enterprise AI Governance & GRC](projects/enterprise-ai-governance-grc/README.md#quick-start) |
| Malware analysis and reverse engineering | [Malware Analysis & Reverse Engineering](projects/malware-analysis-reverse-engineering/README.md#how-to-run) |
| Enterprise threat modeling | [Threat Modeling](Threat-Modeling/enterprise-cloud-ai-platform/README.md#how-to-run) |

### Run the dashboard, SOC console, and EKS telemetry simulation together

This is the main end-to-end local demo for the Enterprise AI Security Threat Detection Platform. It needs Python 3.10+ and three terminals. No AWS account, cluster, model, or external service is contacted.

**Terminal 1 — start the local SOC API and console**

```bash
cd projects/enterprise-ai-security-threat-detection/soc-lab
python server.py
```

Keep this terminal running. The console is at [http://127.0.0.1:8765](http://127.0.0.1:8765).

**Terminal 2 — generate and view the dashboard report**

```bash
cd projects/enterprise-ai-security-threat-detection
python detector.py
python -m http.server 8000
```

Open [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/). The dashboard reads the local `reports/latest.json` generated by `detector.py`.

**Terminal 3 — simulate EKS runtime events into the SOC**

```bash
cd projects/enterprise-ai-security-threat-detection/eks-runtime-simulation
python simulate.py --dry-run
python simulate.py
```

Refresh the SOC console at [http://127.0.0.1:8765](http://127.0.0.1:8765) to inspect the generated EKS incidents and playbooks. Use a new `--batch-id` for repeat ingestion; duplicate event IDs are rejected.

The dashboard report and SOC incident queue are separate local views: the dashboard visualizes the detector's sample-event report, while the EKS simulator posts synthetic EKS events to the SOC API. Stop each server with Ctrl+C. The SOC's local state is stored in `soc-lab/state.json`; stop the SOC server and delete that file manually if you want to reset the demo.

Start with a local/offline validation command before deploying any manifest or Terraform plan. Review every plan and manifest, use disposable environments, and never commit credentials or production telemetry.

## Engineering approach

- Threat-model trust boundaries, assets, abuse cases, and residual risk.
- Enforce authorization in trusted application and infrastructure layers.
- Prefer reproducible tests, secure defaults, policy-as-code, and clear remediation guidance.
- Use synthetic data and isolated environments for security testing.
- Document limitations; a passing lab test is not proof of production security.

## Repository structure

```text
projects/
  aws-eks-ai-security-platform/
    terraform/
    kubernetes/
    policies/kyverno/
    tools/
    tests/
  cloud-security-posture/
    terraform/secure/
    docs/
  kubernetes-security/
    manifests/
    policies/kyverno/
    docs/
  ai-security/
    app/
    tests/
    docs/
  ai-red-team-toolkit/
    test-cases/
    docs/
  ai-security-assessment-framework/
    docs/
    test-cases/
    tools/
  ai-red-team-automation-framework/
    test-cases/
    tests/
    reports/ (generated)
  enterprise-ai-governance-grc/
    governance/ (policy and RACI)
    risk-management/ (assessment methodology)
    data/ (synthetic AI inventory and controls)
    compliance/ (framework mapping notes)
    model-governance/ (model card template)
    third-party-risk/ (supplier questionnaire)
    audit/ (synthetic evidence register)
    incident-management/ (AI incident playbook)
    tools/ and tests/ (offline risk engine and validation)
    dashboard/ (local GRC report viewer)
  malware-analysis-reverse-engineering/
    tools/ (static triage and advanced analysis)
    ghidra-case-study/ (benign C training program and Ghidra exercises)
  enterprise-ai-security-threat-detection/
    config/
    docs/
    scenarios/
    tests/
    reports/ (generated)
    dashboard/ (local HTML dashboard)
    soc-lab/ (local SOC API, console, playbooks, tests)
    eks-runtime-simulation/ (synthetic EKS event adapter and tests)
.github/workflows/
```

## Validation

GitHub Actions workflows validate the AWS EKS security platform configuration (formatting and offline checks only; no cloud deployment), the AI application lab, infrastructure examples, AI red-team catalogue, enterprise AI policy engine, and hands-on AI agent lab policy tests. The AI Red Team Automation Framework runs a local deterministic mock suite, verifies that intentionally vulnerable control profiles are detected, and executes unit tests. The Enterprise AI Security Threat Detection Platform validates synthetic telemetry, applies versioned detection rules, generates risk-ranked reports, includes a local interactive dashboard and SOC console, normalizes synthetic EKS runtime signals, and runs detection, SOC lifecycle, and adapter integration tests. The Malware Analysis & Reverse Engineering lab runs offline static triage tests against a benign text fixture and generates JSON/Markdown reports; it does not execute samples. The Enterprise AI Governance & GRC module validates a synthetic AI inventory and control catalogue, calculates explainable risk scores, flags control evidence gaps and overdue reviews, and renders a local dashboard; it does not certify compliance or provide legal advice. See each project README for prerequisites and safe execution instructions.

## Disclaimer

These are independent portfolio and educational projects. They are not representations of employer-owned systems, proprietary architecture, or production certifications. Use the labs only on systems you own or are explicitly authorized to assess.
