# Kubernetes Workload Security Baseline

| Area | Baseline | Validation evidence |
|---|---|---|
| Namespace | Pod Security Admission restricted | Namespace labels and admission result |
| Identity | Non-root UID/GID; no unnecessary service-account token | Pod securityContext and automount setting |
| Privileges | No privilege escalation; drop ALL capabilities | Container securityContext |
| System calls | seccomp RuntimeDefault | Pod securityContext |
| Filesystem | Read-only root filesystem; explicit writable volumes | Container mounts and securityContext |
| Resources | CPU/memory requests and limits | Container resources |
| Network | Default-deny ingress and egress; explicit allow rules | NetworkPolicy inventory and connectivity tests |
| Image | Approved registry, digest pinning, vulnerability assessment | Image metadata and scanner report |
| Secrets | External secret management where appropriate; avoid plaintext manifests | Secret references and repository scanning |
| Runtime | Runtime detection, alert routing, response ownership | Runtime policy and incident runbook |
| Governance | Owner labels, exception expiry, remediation SLA | Workload inventory and ticket evidence |

## Exception process

An exception must include affected namespace/workload, risk statement, business justification, compensating controls, accountable service owner, security approver, expiry date, and remediation plan. Reassess at expiry or after material workload changes.

## Applicability

This baseline is a starting point, not a universal production policy. Adapt probes, filesystem mounts, network flows, identity integration, and resource limits to each workload and cluster distribution.
