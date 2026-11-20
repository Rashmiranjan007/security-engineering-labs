# EKS-to-AI-SOC Reference Architecture

## Data flow

```text
  Synthetic EKS cluster signals
  +-----------------------------+
  | Kubernetes audit events     |
  | Admission / policy signals  |
  | Workload identity signals   |
  | Image integrity signals     |
  | Runtime sensor alerts       |
  +--------------+--------------+
                 |
                 v
       EKS telemetry adapter
       - schema validation
       - source mapping
       - workload context
       - event normalization
                 |
                 v
       Normalized SOC event API
       POST /api/events
                 |
                 v
       Detection rule engine
       - event type matching
       - severity / risk score
       - recommendation
                 |
                 v
       Correlation and incident state
       - workload + actor + 15m window
       - owner assignment
       - lifecycle + audit history
                 |
                 v
       SOC console and response playbooks
```

## Signal-to-control mapping

| Signal | Security concern | Preventive / detective control |
|---|---|---|
| Exec into AI pod | Unauthorized interactive access | Kubernetes RBAC, audit policy, break-glass governance |
| Privileged AI pod | Host escape and node access risk | Pod Security Standards, admission policy, restricted capabilities |
| Service-account token anomaly | Workload identity misuse | IRSA / EKS Pod Identity, projected tokens, audience and RBAC restrictions |
| NetworkPolicy drift | Unexpected lateral or egress paths | Default-deny policy, GitOps reconciliation, drift detection |
| Image digest mismatch | Artifact substitution or unapproved image | Digest pinning, signature/provenance verification, admission enforcement |
| Runtime threat signal | Suspicious process or behavior inside container | Runtime sensor, process ancestry, workload context, incident response |

## Production integration design notes

A production adapter should collect from authenticated and authorized sources, preserve original source IDs and timestamps, validate cluster identity, enrich namespace/pod/node metadata from trusted inventory, and deliver through a durable queue with retries and dead-letter handling. Avoid treating a workload label or event payload as proof of identity. Bind cluster and tenant identity from the authenticated collection path.

For EKS, useful source families include Kubernetes API audit logs, AWS CloudTrail for relevant AWS API activity, admission-controller decisions, policy/GitOps drift events, registry signature and digest verification results, and runtime sensor detections. Integrations must be designed and validated against the actual products and versions deployed.

## Response boundary

The SOC lab creates incidents and displays recommended actions. It does not perform containment. Real containment should be a separately authorized SOAR workflow with approval gates, scoped IAM permissions, auditable execution, rollback criteria, and human oversight for disruptive actions.
