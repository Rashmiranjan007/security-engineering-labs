# Security Engineering Labs

A practical portfolio of cloud security, Kubernetes security, DevSecOps, AI application security, and defensive AI red-team engineering.

## About

I am a Principal Information Security Engineer with 12+ years of experience across cloud security, container and Kubernetes security, product security, vulnerability management, DevSecOps, and emerging AI security. This repository contains independent learning projects, reference implementations, architecture notes, and security validation examples.

## Portfolio

| Project | What it demonstrates | Current assets |
|---|---|---|
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

## How to run the portfolio

There is no single repository-wide install: each lab has its own prerequisites and safe execution steps. Open the relevant project README below and follow its **How to run** section. Most Python-only labs use Python 3.10+ and the standard library; the hands-on AI Agent lab additionally needs Docker Compose and local Ollama/Qdrant services, while the cloud and Kubernetes examples require the relevant sandbox tools and credentials.

| Lab | Run guide |
|---|---|
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
| Enterprise threat modeling | [Threat Modeling](Threat-Modeling/enterprise-cloud-ai-platform/README.md#how-to-run) |

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

GitHub Actions workflows validate the AI application lab, infrastructure examples, AI red-team catalogue, enterprise AI policy engine, and hands-on AI agent lab policy tests. The AI Red Team Automation Framework runs a local deterministic mock suite, verifies that intentionally vulnerable control profiles are detected, and executes unit tests. The Enterprise AI Security Threat Detection Platform validates synthetic telemetry, applies versioned detection rules, generates risk-ranked reports, includes a local interactive dashboard and SOC console, normalizes synthetic EKS runtime signals, and runs detection, SOC lifecycle, and adapter integration tests. See each project README for prerequisites and safe execution instructions.

## Disclaimer

These are independent portfolio and educational projects. They are not representations of employer-owned systems, proprietary architecture, or production certifications. Use the labs only on systems you own or are explicitly authorized to assess.
