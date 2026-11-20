# Security Engineering Labs

A public, hands-on portfolio of cloud security, Kubernetes security, AI security, and AI red-team engineering projects.

## About

I am a Principal Information Security Engineer focused on cloud security, container and Kubernetes security, DevSecOps, product security, vulnerability management, and AI security. My work spans AWS and GCP environments, Kubernetes/EKS, infrastructure as code, CI/CD security, runtime protection, and security automation.

## Portfolio projects

| Project | Focus | Planned implementation |
|---|---|---|
| [Cloud Security Posture](projects/cloud-security-posture/README.md) | AWS IAM, S3, Terraform | Secure-by-default infrastructure examples, policy checks, threat scenarios, and remediation guidance |
| [Kubernetes Security](projects/kubernetes-security/README.md) | EKS, admission control, container hardening | Workload security baseline, admission policies, image controls, runtime considerations, and validation |
| [AI Security](projects/ai-security/README.md) | Prompt injection, RAG, model and API security | Threat model, attack/defense labs, secure architecture, and evaluation tests |
| [AI Red Team Toolkit](projects/ai-red-team-toolkit/README.md) | LLM application testing | Repeatable tests for OWASP LLM risks, reporting, and CI integration |

## Engineering principles

- Demonstrate risks only in isolated, intentionally vulnerable lab environments.
- Prefer reproducible tests, clear threat models, and actionable remediation.
- Never commit credentials, tokens, customer data, or proprietary company material.
- Keep examples vendor-neutral unless a project explicitly documents a product integration.

## Repository structure

```text
projects/
  cloud-security-posture/
  kubernetes-security/
  ai-security/
  ai-red-team-toolkit/
.github/workflows/
docs/
```

## Disclaimer

These projects are for education and defensive security engineering. Use the labs only on systems you own or are explicitly authorized to test.
