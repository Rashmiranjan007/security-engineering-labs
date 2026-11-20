# AWS EKS AI Security Platform — Architecture and Trust Boundaries

## Trust zones

1. AWS account boundary: dedicated sandbox account and controlled IAM entry points.
2. VPC boundary: internet gateway and NAT provide routing; worker nodes and EKS API remain in private subnets.
3. EKS control-plane boundary: AWS-managed control plane with private API endpoint, control-plane logs and KMS envelope encryption for Kubernetes secrets.
4. Node boundary: managed EC2 node group with encrypted EBS root volumes and IMDSv2 required.
5. Workload boundary: restricted namespace, dedicated service account, scoped IRSA trust, quotas and pod security context.
6. AI data boundary: model artifacts must be approved and digest-verified before deployment; the sample does not download models dynamically.
7. Operations boundary: audit and runtime telemetry should be forwarded to protected central logging. This is a production design requirement, not implemented here.

## Identity path

The sample IRSA role trust policy binds both:
- audience: sts.amazonaws.com
- subject: system:serviceaccount:ai-inference:ai-inference-sa

The role has no permissions attached. Add only exact data-plane actions required by the workload, scoped to exact resources. Do not attach broad managed policies or reuse the node role for application permissions.

The node role includes EKS worker, CNI and ECR read-only policies for this managed node group. For production, consider moving CNI permissions to a dedicated service-account role and evaluate EKS Pod Identity as the organizational standard.

## Network path

- Kubernetes API endpoint is private-only.
- Nodes are in private subnets.
- One NAT Gateway is used for the sample's private-subnet default route. This is a cost simplification, not a highly available production egress architecture.
- Namespace NetworkPolicy starts with default-deny ingress and egress. DNS and gateway rules are examples; add only the flows required by the CNI and application.
- NetworkPolicy enforcement depends on deployed CNI configuration.

## AI workload controls

- Dedicated namespace with Pod Security Admission restricted.
- Non-root UID/GID, RuntimeDefault seccomp, no privilege escalation, read-only root, dropped capabilities and bounded resources.
- Image reference must be immutable and digest-pinned.
- Dedicated service account maps to a narrowly trusted IAM role.
- Model artifact provenance, signature verification, dataset access controls, prompt/data privacy and GPU node isolation remain production requirements.

## Operational detection

For production, collect CloudTrail events, EKS API/audit/authenticator/scheduler/controller logs, VPC Flow Logs, Kubernetes admission decisions, workload identity events and container runtime detections. Define ownership, severity, response SLAs, evidence retention, exception expiry and rollback procedures.

The sample does not connect to a SIEM or vendor sensor.

## Deployment gates

| Gate | Required evidence |
|---|---|
| Network | Private endpoint; subnet routes and egress reviewed |
| IAM | Trust policy limited to exact namespace/service account; no static credentials |
| Control plane | KMS encryption and required control-plane logs enabled |
| Nodes | Encrypted volumes, IMDSv2 required, supported patched AMI |
| Workloads | Restricted PSA, non-root, seccomp, read-only root, dropped capabilities |
| Admission | Digest pinning and hardened pod policy enforced |
| AI supply chain | Approved source, license, provenance, digest, signature and reviewer |
| Runtime | Audit/runtime telemetry delivered and response runbook tested |

## Limitations

Terraform formatting and static checks do not prove infrastructure security. Validate AWS API behavior, provider compatibility, policy syntax, CNI enforcement, EKS version support, quotas and organizational guardrails before use.
