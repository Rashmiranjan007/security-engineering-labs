# Enterprise Key Management Lifecycle

## Key hierarchy and envelope encryption

- Key Encryption Key (KEK): held and operated by KMS/HSM; protects data keys.
- Data Encryption Key (DEK): generated for a data object or bounded data set; encrypts payload with authenticated encryption.
- Persist ciphertext, nonce, algorithm/version metadata, required AAD context, and the encrypted DEK. Do not persist plaintext DEKs.
- Separate key administrators, key users, auditors, and application operators. Enforce least privilege and separation of duties.

## Lifecycle

1. **Design:** classify data, define cryptoperiod, algorithm, key purpose, region, recovery requirements, and ownership.
2. **Generate:** use approved KMS/HSM or cryptographically secure random generation. Never derive production keys from passwords or timestamps.
3. **Distribute:** use authenticated channels and workload identity. Never send keys in source code, chat, tickets, or logs.
4. **Store:** use KMS/HSM or a managed secrets platform; restrict decrypt and administration separately.
5. **Use:** bind encryption context/AAD to tenant, resource, or data classification. Audit sensitive operations.
6. **Rotate:** define periodic and event-driven rotation. Re-encrypt or re-wrap data keys as required; retain old decrypt capability for approved data-retention windows.
7. **Revoke/disable:** immediately restrict compromised or unneeded keys; assess affected ciphertext, backups, snapshots, and replicas.
8. **Backup/recover:** document quorum, dual control, restore testing, and regional recovery. Protect backups at least as strongly as originals.
9. **Destroy:** follow retention, legal hold, and crypto-erasure requirements; require approvals and evidence.

## Rotation is not retroactive protection

Rotating a key prevents future use of the old key only when systems stop accepting it. It does not automatically re-encrypt old data, remove copies, invalidate leaked plaintext, or revoke already-issued credentials. Build a migration and verification plan.

## KMS/HSM control checklist

- Key policies and IAM policies both reviewed; no wildcard principals or broad decrypt grants.
- Separate key creation, policy administration, and data-use permissions.
- Restrict cross-account use and encryption context.
- Enable immutable/audited key-use logs and alert on unusual decrypt volume or geography.
- Define deletion windows, pending deletion protections, break-glass access, and recovery.
- Inventory keys, owners, purpose, algorithm, region, rotation setting, dependencies, and last review.
- Test restore and rotation in non-production before rollout.

## Incident response: suspected key compromise

Contain access, disable or restrict the key where safe, preserve audit evidence, identify affected ciphertext and principals, rotate/reissue dependent secrets, re-encrypt data where needed, investigate exfiltration, validate consumers, and document residual exposure. Coordinate with service owners before disabling shared production keys to avoid uncontrolled outages.
