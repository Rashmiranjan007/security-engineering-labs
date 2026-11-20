# EKS Runtime Security Telemetry Simulation

A synthetic integration bridge that maps Kubernetes audit, EKS identity, admission/policy, image-integrity, and container-runtime signals into the existing AI Security SOC event schema.

## What this demonstrates

- Synthetic EKS cluster, namespace, pod, node, and workload metadata
- Kubernetes API audit signals such as exec into an AI inference pod
- Privileged workload admission/runtime signals
- Service-account token and workload-identity anomalies
- NetworkPolicy drift
- Container image digest mismatch
- Runtime threat alert from a generic container runtime sensor
- Normalization into the SOC detection engine and incident lifecycle

## How to run

Terminal 1 — start the SOC API and console:

```bash
cd projects/enterprise-ai-security-threat-detection/soc-lab
python server.py
```

Terminal 2 — preview the normalized EKS events without sending them:

```bash
cd projects/enterprise-ai-security-threat-detection/eks-runtime-simulation
python simulate.py --dry-run
```

Terminal 2 — ingest them into the local SOC:

```bash
python simulate.py
```

Open [http://127.0.0.1:8765](http://127.0.0.1:8765), refresh the queue, and inspect the EKS incidents and their playbooks. Use a new `--batch-id` for another run, because the SOC rejects duplicate event IDs.

## Supported synthetic signal types

| Source signal | Normalized event | Default severity |
|---|---|---|
| Kubernetes audit exec | `k8s_exec_into_ai_pod` | High |
| Admission/runtime privileged pod | `privileged_ai_workload` | Critical |
| Service-account token anomaly | `service_account_token_anomaly` | Critical |
| Network policy change/drift | `network_policy_drift` | High |
| Image digest mismatch | `container_image_digest_mismatch` | Critical |
| Container runtime sensor alert | `runtime_threat_detection` | Critical |

## Design and trust boundaries

See [architecture](docs/architecture.md). The simulator deliberately separates source telemetry from the normalized SOC event contract. In a real deployment, adapters would need authenticated collection, source-specific schema validation, immutable event provenance, clock synchronization, workload identity, RBAC, durable queues, and tenant-aware access control.

## Safety and limitations

- The fixture is entirely synthetic. No EKS cluster, AWS account, Kubernetes API, CrowdStrike tenant, or external endpoint is contacted.
- The sender accepts only loopback API destinations (`127.0.0.1` or `localhost`).
- This is not an EKS collector, Falcon integration, CloudTrail integration, or production runtime detector.
- The runtime alert is a simulated source signal; it does not execute malware or create a real threat.
- The adapter does not execute containment, delete pods, change IAM, modify NetworkPolicies, or alter clusters.
- Do not ingest production logs, credentials, tokens, or employer telemetry into this public lab.
