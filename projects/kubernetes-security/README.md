# Kubernetes and Container Security Baseline

Practical baseline examples for Kubernetes and EKS workloads.

## Included manifests
- Namespace with Pod Security Admission labels set to restricted
- Hardened non-root Deployment with seccomp, dropped capabilities, read-only root filesystem, resource limits, and disabled service-account token mounting
- Default-deny ingress and egress NetworkPolicy

## How to run
Requires kubectl and a cluster with a compatible CNI that enforces NetworkPolicy.

```bash
kubectl apply --dry-run=client -f manifests/namespace.yaml
kubectl apply --dry-run=client -f manifests/default-deny-network-policy.yaml
kubectl apply --dry-run=client -f manifests/secure-deployment.yaml
```

For a live lab only, inspect every manifest and apply in order:

```bash
kubectl apply -f manifests/namespace.yaml
kubectl apply -f manifests/default-deny-network-policy.yaml
kubectl apply -f manifests/secure-deployment.yaml
kubectl -n security-lab rollout status deployment/hardened-demo
```

The default-deny policy blocks all ingress and egress until explicit allow rules are added. Add required DNS and application flows before expecting workloads to communicate. NetworkPolicy behavior depends on CNI support.

## Operational checklist
- Review image provenance and pin production images by digest.
- Add explicit ingress and egress allow policies.
- Validate the image supports non-root and read-only filesystem operation.
- Test probes and writable paths for the actual workload.
- Review RBAC, workload identity, audit logging, and runtime monitoring.

> These are illustrative lab manifests. Test compatibility before production use.
