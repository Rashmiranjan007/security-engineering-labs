# AWS EKS Security Engineering Platform

A defense-in-depth reference implementation for a private Amazon EKS platform hosting security-sensitive and AI inference workloads. It combines AWS foundation controls, Kubernetes hardening, workload identity, network isolation, admission policy, and automated checks.

> Deployment warning: Terraform creates billable AWS resources if applied. CI never deploys this lab. Begin with offline checks, review the plan, and use a disposable AWS account only if you choose to deploy it.

## Architecture

~~~mermaid
flowchart TB
  OP[Operator via approved VPN] --> API[Private EKS API]
  subgraph VPC["Dedicated AWS VPC"]
    subgraph PUB["Public subnets"]
      NAT[NAT Gateway]
    end
    subgraph PRIV["Private subnets"]
      CP[EKS control plane ENIs]
      NG[Managed worker nodes]
      AI[AI inference namespace]
      NG --> AI
      CP --> NG
    end
    KMS[KMS secrets encryption] --> CP
    OIDC[OIDC / IRSA] --> AI
    REG[Private image registry] --> NG
  end
  AI -->|restricted egress| NAT
  POLICY[Kyverno admission policy] --> AI
  AI --> SOC[Central SOC / logging - future integration]
~~~

The diagram is a logical reference. Terraform provisions the VPC, private EKS cluster, managed node group, KMS encryption, and a dedicated IRSA role. Public ingress, SIEM, GPU node groups, and production runtime telemetry are not provisioned.

## Security controls

| Layer | Controls |
|---|---|
| AWS network | VPC, public/private subnets, NAT egress, private EKS API, no public API endpoint |
| EKS control plane | KMS envelope encryption for Kubernetes secrets; API, audit, authenticator, controller-manager and scheduler logs |
| IAM | Separate cluster/node roles; OIDC provider; IRSA role scoped to one service account |
| Worker nodes | Managed node group in private subnets; encrypted root volume; IMDSv2 required |
| Kubernetes | Restricted Pod Security Admission; non-root; read-only root; dropped capabilities; seccomp; quotas |
| Network | Default-deny ingress/egress; explicit DNS and gateway allowances |
| Admission | Kyverno example requiring digest-pinned images and hardened pod settings |
| AI workload | Dedicated namespace and service account; immutable image placeholder; GPU scheduling extension points |

## Repository contents

- terraform/ — VPC, private EKS cluster, KMS, IAM, IRSA and managed node group.
- kubernetes/ — namespace, service account, inference deployment, NetworkPolicy and quota.
- policies/kyverno/ — admission policy example.
- tools/validate.py and tests/ — offline static checks and unit tests.
- .github/workflows/aws-eks-ai-security-platform.yml — formatting and Python validation only.

## How to run

### 1. Offline validation (no AWS credentials required)

Requires Python 3.10+ and Terraform 1.5+ for formatting.

From the repository root:

~~~bash
python projects/aws-eks-ai-security-platform/tools/validate.py
python -m unittest discover -s projects/aws-eks-ai-security-platform/tests -v
terraform -chdir=projects/aws-eks-ai-security-platform/terraform fmt -check -recursive
~~~

### 2. Optional Terraform review in an isolated AWS sandbox

Prerequisites: AWS CLI configured with a dedicated sandbox identity, Terraform 1.5+, and permission to create VPC, EKS, IAM, KMS and EC2 resources. Use short-lived SSO/assumed-role credentials; never put access keys in files or GitHub.

~~~bash
cd projects/aws-eks-ai-security-platform/terraform
cp terraform.tfvars.example terraform.tfvars
# Edit region, cluster name and CIDR values.
terraform init
terraform validate
terraform plan
~~~

Review the plan. This configuration creates a NAT Gateway, EKS control plane, EC2 worker nodes, networking and KMS resources that can incur ongoing charges. Only apply if you explicitly approve the plan in your own sandbox:

~~~bash
terraform apply
~~~

The EKS API endpoint is private-only. Use an approved VPN or controlled in-VPC administration host to reach it. Do not make the API public for convenience.

When finished, review and run:

~~~bash
terraform destroy
~~~

Keep Terraform state private and encrypted. Never commit state, plan files or sensitive tfvars.

### 3. Optional Kubernetes deployment

After provisioning and configuring kubectl through an approved private network path, replace the placeholder image digest and IRSA role ARN. Install a compatible Kyverno version before applying the ClusterPolicy.

~~~bash
kubectl apply -f projects/aws-eks-ai-security-platform/kubernetes/namespace.yaml
kubectl apply -f projects/aws-eks-ai-security-platform/kubernetes/service-account.yaml
kubectl apply -f projects/aws-eks-ai-security-platform/kubernetes/resource-quota.yaml
kubectl apply -f projects/aws-eks-ai-security-platform/kubernetes/network-policy.yaml
kubectl apply -f projects/aws-eks-ai-security-platform/kubernetes/inference-deployment.yaml
kubectl apply -f projects/aws-eks-ai-security-platform/policies/kyverno/require-hardened-ai-pods.yaml
~~~

NetworkPolicy requires a compatible CNI. Default-deny blocks traffic until the necessary flows are explicitly allowed.

## Production engineering decisions

1. Use separate AWS accounts for development, staging and production.
2. Add VPC endpoints for required AWS services and minimize NAT egress.
3. Use EKS access entries and centrally managed identity groups; avoid long-lived IAM users.
4. Evaluate EKS Pod Identity as an organizational standard; this lab demonstrates IRSA.
5. Use dedicated GPU node groups with taints, tolerations, node affinity, quotas and restricted scheduling permissions.
6. Pull images by immutable digest and verify signatures/provenance in admission.
7. Quarantine, scan, approve and digest-verify model weights, tokenizers, adapters and datasets.
8. Forward CloudTrail, EKS control-plane, VPC Flow, Kubernetes audit, admission and runtime events to protected central logging.
9. Integrate the approved runtime sensor and incident response process; this lab does not install Falcon or another vendor sensor.
10. Test upgrades, node replacement, policy rollout, restore and incident response.

## Limitations

- CI does not run terraform init, plan or apply and has no AWS credentials.
- This is a reference starter; review AWS quotas, AZ availability, pricing, provider versions and organization guardrails.
- One NAT Gateway keeps the example simpler but is not a multi-AZ production egress design.
- No public ingress, GPU node group, SIEM or vendor runtime sensor is provisioned.
- The Kubernetes image digest and IRSA role ARN are deliberate placeholders.
- The Kyverno example is not a complete image signature/provenance verification implementation.
- Static checks are not a Terraform plan scanner or live cluster assessment.

## Safety

Use only AWS accounts and Kubernetes clusters you own or are explicitly authorized to administer. Never commit credentials, Terraform state, plan files, production logs, model artifacts or customer data.
