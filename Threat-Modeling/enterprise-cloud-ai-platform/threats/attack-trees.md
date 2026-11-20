# Attack trees and adversary paths

## AT-01 — Exfiltrate tenant data

**Goal:** obtain data belonging to another tenant.

```mermaid
flowchart TD
  G[Exfiltrate tenant data] --> A[Exploit application authorization]
  G --> B[Exploit identity/session]
  G --> C[Exploit data or backup exposure]
  G --> D[Exploit AI/RAG retrieval]
  A --> A1[Change object ID]
  A --> A2[Change tenant claim/header]
  A --> A3[Abuse export endpoint]
  B --> B1[Steal token]
  B --> B2[Abuse weak admin MFA]
  C --> C1[Public object storage]
  C --> C2[Overprivileged DB identity]
  D --> D1[Cross-tenant vector query]
  D --> D2[Prompt injection + unsafe tool]
```

**Control strategy:** object-level authorization, tenant-bound claims, phishing-resistant MFA, short-lived tokens, private storage, scoped DB identities, tenant-aware retrieval, tool broker authorization, DLP, and exfiltration detection.

## AT-02 — Compromise production through CI/CD

```mermaid
flowchart TD
  G[Deploy malicious workload] --> A[Compromise source]
  G --> B[Compromise build]
  G --> C[Abuse deployment identity]
  A --> A1[Malicious dependency]
  A --> A2[Unreviewed code change]
  B --> B1[Runner compromise]
  B --> B2[Artifact substitution]
  C --> C1[Overbroad OIDC trust]
  C --> C2[Unprotected production environment]
  B1 --> D[Malicious image reaches registry]
  B2 --> D
  C1 --> D
  C2 --> D
```

**Control strategy:** protected branches, CODEOWNERS, dependency pinning, isolated ephemeral runners, SBOM, provenance attestations, image signing, digest pinning, OIDC subject restrictions, protected environments, deployment approval, admission signature verification, and runtime monitoring.

## AT-03 — Abuse AI agent capabilities

```mermaid
flowchart TD
  G[Cause unauthorized agent action] --> A[Prompt injection]
  G --> B[Tool authorization weakness]
  G --> C[Data poisoning]
  A --> A1[Direct user prompt]
  A --> A2[Retrieved document instruction]
  B --> B1[Tool lacks per-user authorization]
  B --> B2[Unsafe argument accepted]
  C --> C1[Untrusted upload]
  C --> C2[Compromised ingestion source]
  A1 --> D[Unauthorized tool invocation]
  A2 --> D
  B1 --> D
  B2 --> D
```

**Control strategy:** deterministic policy enforcement outside the model, strict tool allowlists, typed schemas, per-action authorization, human approval for high-impact operations, source provenance, quarantine, and full tool-call audit.

## ATT&CK mapping (hypothesis for detection engineering)

| Attack path | Relevant ATT&CK behavior to investigate | Defensive telemetry |
|---|---|---|
| Stolen credentials | Valid Accounts | IdP sign-in, token anomalies, MFA events |
| Cloud privilege abuse | Cloud account / permission discovery and privilege escalation behaviors | Cloud audit, IAM changes, role assumption |
| Container compromise | Container administration and escape-related behaviors | Kubernetes audit, runtime process and syscall telemetry |
| CI/CD compromise | Compromise software supply chain | SCM audit, runner events, artifact provenance |
| Data exfiltration | Exfiltration over web service / cloud storage | API logs, object access, egress, DLP |
| Service disruption | Network denial of service / resource exhaustion | WAF, API quotas, queue depth, model token/cost metrics |

Technique IDs should be confirmed against the current MITRE ATT&CK knowledge base before use in a formal detection catalog. This project does not claim observed adversary activity.
