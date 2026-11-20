# Architecture and operating model

## Assets and trust boundaries
| Asset | Key risk | Control owner |
|---|---|---|
| Container image | Vulnerable or tampered runtime | Platform / product security |
| Model weights, tokenizer, adapters | Poisoning, substitution, unlicensed artifact | ML platform |
| Prompts, embeddings, retrieved records | Tenant leakage and sensitive-data exposure | AI application owner |
| GPU node and device plugin | Cross-workload exposure and privileged access | Kubernetes platform |
| Service account / cloud role | Credential theft and privilege escalation | Cloud IAM |
| Inference API | Unauthorized use and resource exhaustion | Application owner |
| Registry and artifact pipeline | Untrusted promotion or mutable tags | Supply-chain owner |
| Telemetry | Missing evidence or sensitive-data leakage | SOC / platform |

Trust boundaries include source/build, image registry, model registry, Kubernetes control plane, node/GPU pool, pod, application/data gateway, external dependency and observability platform.

## Deployment flow
1. Build from approved base images; run unit, SAST, dependency and image scans.
2. Generate SBOM and provenance; sign the immutable image digest.
3. Promote model artifacts through a controlled workflow recording source, version, checksum, license and reviewer.
4. Store artifacts in approved private registries. Production must not pull arbitrary public images or models at runtime.
5. Admission validates registry, digest pinning, namespace and required security context. Implement actual signature verification with Kyverno verifyImages or an equivalent verified admission integration.
6. Deploy with dedicated service account, scoped workload identity, restricted pod security and explicit resource limits.
7. Route ingress and egress through approved paths; enforce tenant authorization in the application and data gateway.
8. Collect Kubernetes audit, API, application and runtime telemetry; map alerts to owners and response SLAs.

## Workload hardening
- Run as non-root; set allowPrivilegeEscalation false.
- Use readOnlyRootFilesystem true, drop all Linux capabilities and use RuntimeDefault seccomp.
- Avoid hostPath, hostNetwork, hostPID, hostIPC, privileged mode and container-runtime socket mounts.
- Use a dedicated service account with token automount disabled unless Kubernetes API access is required.
- Set CPU, memory, ephemeral-storage requests/limits and explicit GPU requests. Cap concurrency at the inference gateway.
- Use health probes that do not disclose secrets or model internals.
- Keep model files read-only; place writable scratch data in bounded ephemeral volumes.

GPU device plugins may require host-level components. Keep those components platform-managed and isolated; do not grant inference containers privileged access to install or manage drivers.

## Network and data boundaries
Start with default-deny ingress and egress. Add only required flows: ingress from the approved ingress gateway; DNS to cluster DNS; egress to approved model/data endpoints through a gateway; telemetry to an approved collector. Kubernetes NetworkPolicy is L3/L4 and does not provide FQDN policy or application-layer tenant authorization. Validate CNI support and add an egress gateway, service mesh or cloud firewall where needed. Enforce tenant and object-level authorization in the application/data service.

## Identity and secrets
For EKS, prefer EKS Pod Identity or IRSA, with a dedicated IAM role per workload or trust domain. Restrict trust to the exact cluster, namespace and service account. Scope permissions to required model objects and APIs. Monitor role use and avoid node-role credential inheritance. Use Secrets Manager / Parameter Store through a supported integration or CSI driver; do not commit secret values.

## Governance and response
| Event | Response |
|---|---|
| Image/model provenance failure | Block promotion, quarantine artifact and investigate source |
| Critical image CVE | Block rollout or require a documented time-bound exception |
| Unexpected egress | Contain workload, preserve telemetry and validate destination |
| Cross-tenant access indicator | Disable affected path, preserve evidence and notify data owner |
| GPU exhaustion / inference abuse | Rate-limit at gateway, apply quota and investigate caller |
| Runtime compromise | Isolate workload/node per incident plan and rotate credentials |

Exceptions require named owner, business justification, compensating controls, expiry and risk approval. Reassess after image, model, cluster-version or trust-boundary changes.

## Validation checklist
- [ ] Admission rejects mutable image tags and unapproved registries.
- [ ] Signature verification is tested with valid and invalid signatures.
- [ ] Model checksum and provenance are verified during promotion.
- [ ] Namespace enforces restricted Pod Security Standards.
- [ ] Inference pod has no privileged mode, host namespaces or hostPath.
- [ ] Workload identity is dedicated and least-privileged.
- [ ] NetworkPolicy is enforced by the CNI and tested from a live pod.
- [ ] GPU node pool is isolated and quota-controlled.
- [ ] Audit and runtime events reach monitoring.
- [ ] Incident and exception workflows have owners and expiry dates.
