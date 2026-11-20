# Kubernetes and Container Security Baseline

## Objective
Document and validate a practical security baseline for Kubernetes workloads, with emphasis on AWS EKS and portable Kubernetes controls.

## Security domains
1. Cluster and control-plane configuration
2. Identity, RBAC, and service accounts
3. Network segmentation and egress control
4. Pod and container hardening
5. Image provenance, vulnerability scanning, and admission
6. Secrets and encryption
7. Runtime detection and response
8. Audit logging, monitoring, and incident readiness

## Workload baseline
- Run as non-root wherever possible.
- Set read-only root filesystems where compatible.
- Drop Linux capabilities and avoid privileged containers.
- Disallow host PID, IPC, and network namespaces unless justified.
- Define CPU and memory requests/limits.
- Use seccomp and AppArmor profiles where supported.
- Pin images by immutable digest for production workloads.
- Apply Kubernetes Pod Security Standards and admission policy.
- Restrict service-account token mounting when not required.

## Identity and network
- Use least-privilege RBAC; avoid wildcard permissions.
- Prefer workload identity over static cloud credentials.
- Apply default-deny NetworkPolicies and explicitly allow required flows.
- Protect secrets with encryption at rest and controlled access.

## Validation checklist
- [ ] Review cluster and node configuration.
- [ ] Identify privileged and root-running workloads.
- [ ] Detect host namespace and hostPath usage.
- [ ] Validate image provenance and scan results.
- [ ] Test admission policies in audit mode before enforcement.
- [ ] Review RBAC and service-account permissions.
- [ ] Verify audit log collection and runtime alert routing.

## Governance model
Prioritize findings using severity, exploitability, exposure, and business criticality. Define remediation SLAs with service owners. Exceptions should include a documented risk, compensating controls, accountable approver, and expiry date.

## Roadmap
- [ ] Add sample hardened Deployment manifests.
- [ ] Add example admission policies.
- [ ] Add CI checks for Kubernetes manifests.
- [ ] Add a threat model and architecture diagram.
- [ ] Add a sample remediation and exception workflow.

> Examples are for controlled lab environments. Validate compatibility before applying controls to production clusters.
