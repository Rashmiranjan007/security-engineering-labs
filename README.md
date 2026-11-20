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
.github/workflows/
```

## Validation

GitHub Actions workflows validate the AI application lab, infrastructure examples, AI red-team catalogue, enterprise AI policy engine, and hands-on AI agent lab policy tests. See each project README for prerequisites and safe execution instructions.

## Disclaimer

These are independent portfolio and educational projects. They are not representations of employer-owned systems, proprietary architecture, or production certifications. Use the labs only on systems you own or are explicitly authorized to assess.
