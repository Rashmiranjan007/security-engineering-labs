# Threat Model and Operational Runbooks

## Assets

Encryption keys, DEKs, API credentials, database passwords, signing keys, certificates, encrypted data, KMS policies, secret-store policies, CI/CD identity tokens, audit records.

## Threat scenarios

| Threat | Impact | Preventive controls | Detection / response |
|---|---|---|---|
| Key committed to Git | Data compromise | Secret scanning, pre-commit hooks, short-lived credentials | Revoke/rotate, investigate history and consumers |
| Overbroad decrypt permission | Bulk data exposure | Least privilege, encryption context, separation of duties | Alert on anomalous decrypt operations |
| AES-GCM nonce reuse | Confidentiality/integrity failure | Library-generated unique nonce; key usage design | Rotate key and assess affected ciphertext |
| Secret leaked in logs | Credential abuse | Redaction, structured logging, no debug dumps | Search logs, revoke and reissue |
| Kubernetes Secret read by excessive RBAC | Workload credential theft | Namespace RBAC, encryption at rest, external store | Audit API reads and rotate exposed values |
| CI token exfiltration | Cloud/repository compromise | OIDC, short-lived scoped tokens, protected environments | Revoke sessions, inspect workflow and cloud audit |
| Certificate expiry or private-key theft | Service outage / impersonation | Inventory, renewal automation, protected key storage | Alert, revoke, replace and validate trust |

## Secret exposure runbook

1. Treat the credential as compromised; do not test it by using it.
2. Identify owner, scope, permissions, environments, and dependent services.
3. Revoke or disable it; issue a replacement through the approved secret platform.
4. Update consumers and validate service health.
5. Review Git history, CI logs, build artifacts, images, caches, logs, backups, and downstream copies.
6. Review identity, KMS, provider, and application audit events for misuse.
7. Remove exposed copies where possible, while recognizing Git history may persist in clones/forks.
8. Record timeline, blast radius, rotation evidence, owner, and lessons learned.

## Operational metrics

- Percentage of secrets with an accountable owner and expiry/rotation policy.
- Static credentials replaced by workload identity.
- Mean time to revoke and rotate exposed credentials.
- KMS decrypt anomalies investigated within target.
- Key inventory coverage and overdue key reviews.
- Certificate expiry coverage and renewal success.
- Secret findings by age, severity, and remediation SLA.

## Validation scenarios

- Modify ciphertext and confirm AES-GCM authentication fails.
- Supply incorrect AAD and confirm decryption fails.
- Verify HMAC rejects altered messages.
- Add synthetic credential patterns and confirm scanner reports only metadata.
- Test key rotation and consumer reload in a disposable environment.
- Verify a workload cannot read another workload's secret.
