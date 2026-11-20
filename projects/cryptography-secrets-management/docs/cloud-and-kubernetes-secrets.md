# Cloud, Kubernetes, and CI/CD Secrets Patterns

## AWS

- Prefer IAM roles and workload identity (EKS IRSA or EKS Pod Identity) over static access keys.
- Scope trust relationships to the exact cluster, namespace, service account, and audience/subject claims where applicable.
- Use AWS Secrets Manager or Systems Manager Parameter Store for application secrets; use KMS key policies and IAM conditions to restrict access.
- Keep secret retrieval at runtime; avoid baking values into container images, Terraform state, user data, or CI logs.
- Treat Terraform state as sensitive. Use encrypted remote state, strict access, locking, audit, and secret-free plans where possible.

## Kubernetes / EKS

- Kubernetes Secret values are base64-encoded, not encrypted by base64. Configure encryption at rest for the backing datastore.
- Apply least-privilege RBAC; avoid broad list/watch permissions on Secrets and avoid mounting secrets into unrelated containers.
- Prefer external secret stores or CSI driver integrations with workload identity where suitable.
- Use namespace boundaries, admission policies, pod security controls, and audit logging.
- Do not expose secrets as environment variables unnecessarily; mounted files and short-lived retrieval may reduce accidental disclosure but still require process and filesystem protection.
- Never commit populated Secret manifests. Use placeholders and external secret references.

## CI/CD

- Prefer OIDC federation to cloud roles with short-lived credentials.
- Scope pipeline permissions by repository, branch, environment, and job.
- Mask values, disable shell tracing around sensitive commands, and avoid printing environment or debug dumps.
- Protect release environments with approvals and provenance checks.
- Rotate credentials after suspected exposure and invalidate old sessions/tokens.

## AI and model-serving workloads

- Keep model-provider API keys in a managed secret store; do not put them in prompts, notebooks, model artifacts, logs, or frontend bundles.
- Use distinct credentials per service and environment; scope provider keys to minimum capabilities and budgets.
- Avoid passing secrets to tools or retrieval contexts. Redact telemetry and traces.
- Bind access to tenant/workload identity, not model-generated claims.
- Monitor secret retrieval, anomalous use, unexpected egress, and provider spend.

## Reference flow

1. Pod receives identity from the platform.
2. Application authenticates to the secrets service using workload identity.
3. Policy authorizes only named secret paths and versions.
4. Secret is delivered at runtime with short cache lifetime.
5. Access is audited; secret values are never logged.
6. Rotation updates the managed version and application reload is verified.
