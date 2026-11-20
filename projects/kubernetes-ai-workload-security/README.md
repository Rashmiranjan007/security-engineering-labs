# Kubernetes AI Workload Security Architecture

A defensive reference architecture for model-serving workloads on Kubernetes and Amazon EKS. It connects AI-specific risks to enforcement across the model supply chain, cluster, workload, identity, network and runtime.

## Why this is separate
The existing Kubernetes Security project covers general cluster hardening; the AI Runtime Security Lab simulates application-level guardrails. This project focuses on operating AI inference workloads safely on Kubernetes, including GPU scheduling, model artifact integrity, cloud workload identity and isolation.

## Security objectives
1. Admit only approved, signed and scanned workload images.
2. Treat model weights, tokenizers and adapters as supply-chain assets with provenance and integrity checks.
3. Isolate inference services from training jobs, management planes and unrelated tenants.
4. Use dedicated workload identities and short-lived credentials; avoid static cloud keys in pods.
5. Constrain GPU workloads with explicit scheduling, quotas and node isolation.
6. Protect prompts, retrieved data and outputs at application/data boundaries.
7. Collect Kubernetes audit, application and runtime telemetry for response.

## Reference architecture
Engineering -> CI (tests, SAST, dependency and image scans) -> SBOM + provenance -> image signing -> private OCI registry -> admission verification -> restricted inference pod -> isolated GPU node pool.
Model registry -> review, checksum and provenance verification -> controlled artifact promotion -> read-only model mount.
Inference pod -> workload identity -> scoped cloud services. NetworkPolicy -> approved gateway -> external APIs/data. Runtime and audit telemetry -> SIEM/SOC.

## Contents
- docs/architecture.md — trust boundaries, control design and operating model.
- manifests/namespace.yaml — restricted namespace defaults.
- manifests/service-account.yaml — dedicated service account.
- manifests/inference-deployment.yaml — hardened inference workload with GPU request.
- manifests/network-policy.yaml — default-deny with narrow ingress/egress.
- manifests/resource-quota.yaml — capacity and abuse guardrails.
- policies/kyverno/require-approved-ai-workloads.yaml — admission policy examples.
- tools/validate.py and tests/test_validate.py — offline static checks.

## Run the offline checks
Requires Python 3.10+ and uses only the standard library:
- python -m unittest discover -s projects/kubernetes-ai-workload-security/tests -v
- python projects/kubernetes-ai-workload-security/tools/validate.py

## EKS and GPU implementation notes
- Use a dedicated managed GPU node group or node pool with taints, tolerations, node affinity and separate IAM permissions.
- A GPU label alone is not a security boundary. Restrict who can create pods with GPU tolerations and who can modify node labels.
- Prefer EKS Pod Identity or IRSA with a dedicated service account and least-privilege IAM role. Add platform-specific identity annotations in an environment overlay.
- Promote model artifacts through a controlled workflow recording source, version, checksum, license and reviewer. Production should not download arbitrary models at runtime.
- Use Secrets Manager / Parameter Store through a supported integration or CSI driver; never bake secrets into images or Git.
- Separate training, fine-tuning, evaluation and production inference identities and namespaces.

## Production rollout gates
| Gate | Evidence |
|---|---|
| Image | Approved base, scan results, SBOM, signature and immutable digest |
| Model | Source/version, checksum, provenance, license review and approval |
| Identity | Dedicated service account, scoped cloud role, no static credentials |
| Runtime | Non-root, read-only root filesystem, dropped capabilities, seccomp |
| Network | Default-deny verified; documented dependencies only |
| GPU | Dedicated pool, quota, scheduling restrictions and node patch process |
| Data | Tenant isolation, encryption, retention and sensitive-data controls |
| Detection | Audit/runtime telemetry, alert owner and tested response runbook |

## Limitations
The validator performs simple offline static checks; it is not a Kubernetes API server, YAML parser, policy engine, image scanner, signature verifier or proof of runtime isolation. Validate Kyverno syntax and API compatibility against your deployed versions. NetworkPolicy requires a compatible CNI. The sample image digest and platform-specific identity integration must be replaced before deployment.

## Safety
Educational defensive reference only. It does not deploy to a cluster or access cloud accounts. Use only in environments you own or are authorized to administer.
