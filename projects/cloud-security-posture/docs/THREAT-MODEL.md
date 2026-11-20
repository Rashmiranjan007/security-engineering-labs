# Cloud Security Posture Lab — Threat Model

## Assets
- Objects stored in the S3 bucket
- Bucket policy and public-access configuration
- Encryption configuration and key material
- Terraform state and deployment credentials

## Trust boundaries
- Engineer workstation to CI runner
- CI runner to AWS API
- AWS identity to S3 control plane
- Terraform state backend to authorized operators

## Threat scenarios

| Scenario | Potential impact | Preventive / detective control | Validation |
|---|---|---|---|
| Bucket accidentally made public | Data disclosure | S3 public-access block; policy review | Inspect all four public-access block settings |
| Object stored without default encryption | Data exposure at rest | Bucket default encryption | Inspect bucket encryption configuration |
| Accidental overwrite or deletion | Data loss | Versioning | Confirm versioning status is Enabled |
| CI credential theft | Unauthorized cloud changes | Short-lived federated identity; least privilege | Review trust policy and CI permissions |
| Terraform state disclosure | Infrastructure metadata / secret exposure | Encrypted, access-controlled remote state | Review backend controls; never commit state |

## Residual risks

Public-access blocking does not replace a least-privilege bucket policy. Versioning is not a backup strategy by itself. SSE-S3 may not meet every regulated workload's customer-managed key requirement. Terraform state can contain sensitive values even when source files do not.

## Review questions

- Who can assume the deployment role, and under what conditions?
- Is access limited to the intended account, region, and resources?
- Is state encrypted and access-logged?
- Are data retention and deletion requirements documented?
- Are alerts configured for public-access or policy changes?
