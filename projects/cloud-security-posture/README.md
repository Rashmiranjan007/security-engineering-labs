# Cloud Security Posture and IaC Security

## Objective
Create a practical cloud security engineering lab covering secure AWS foundations, infrastructure-as-code review, identity controls, and risk-based remediation.

## Focus areas
- IAM trust policies, least privilege, and role assumption
- S3 public access and encryption controls
- Security group exposure and network boundaries
- Cloud logging, monitoring, and auditability
- KMS key policies and encryption design
- Terraform security and policy-as-code
- Vulnerability and misconfiguration prioritization

## Proposed lab structure
```text
cloud-security-posture/
  README.md
  terraform/
    secure/
    intentionally-insecure/
  policies/
  tests/
  docs/
```

## Engineering workflow
1. Define a threat model and security requirements.
2. Create isolated sample Terraform configurations.
3. Scan configurations with a policy-as-code tool.
4. Review findings for exploitability and business impact.
5. Implement secure configurations and regression tests.
6. Record evidence and remediation guidance.

## Example controls
- Block public S3 access unless explicitly approved.
- Require encryption for storage resources.
- Avoid wildcard IAM actions and resources.
- Restrict administrative access and external trust relationships.
- Limit inbound network exposure to documented sources.
- Enable appropriate audit and configuration logging.

## Risk-based remediation
Prioritize internet-exposed, exploitable, high-impact issues first. Assign each finding to an accountable owner, define a remediation due date, and require time-bound risk acceptance for exceptions.

## Roadmap
- [ ] Add intentionally insecure Terraform examples.
- [ ] Add corrected secure Terraform examples.
- [ ] Add policy checks and automated tests.
- [ ] Add architecture and data-flow diagrams.
- [ ] Add sample findings with severity rationale and remediation steps.

> Never deploy intentionally insecure examples into a production account. Use a dedicated sandbox with synthetic resources.
