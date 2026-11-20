# Cloud Security Posture and IaC Security

Hands-on Terraform examples for secure AWS foundations, identity controls, and risk-based remediation.

## Included
- Private S3 bucket with public access blocks
- Server-side encryption and versioning
- Terraform provider and variable configuration

## How to run
Requires Terraform 1.5+ and AWS credentials configured through a secure local profile or environment-based identity. Never commit credentials.

```bash
cd projects/cloud-security-posture/terraform/secure
terraform init
terraform fmt -check
terraform validate
terraform plan
```

Review the plan before any apply. This example may incur cloud charges if deployed. Destroy lab resources when finished.

## Planned extensions
- [ ] Add IAM least-privilege examples and policy tests.
- [ ] Add intentionally insecure fixtures for static analysis only.
- [ ] Add Checkov/tfsec scanning in CI.
- [ ] Add architecture and threat-model diagrams.

> Do not deploy intentionally insecure configurations to production. Use a dedicated sandbox account.
