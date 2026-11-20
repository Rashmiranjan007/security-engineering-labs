# Module 6 — Enterprise Key Management, KMS and HSM

## 1. Why key management dominates cryptographic security

Strong algorithms can fail operationally when keys are exposed, over-authorised, copied, retained indefinitely, or lost. Enterprise key management defines who can create, use, administer, rotate, recover, revoke, and destroy keys, and how those actions are monitored.

## 2. Key types and hierarchy

- **Root/master key:** protects lower-level keys or establishes a hierarchy.
- **KEK:** key-encryption key; wraps or encrypts DEKs.
- **DEK:** data-encryption key; encrypts application data.
- **Signing key:** private key used to sign code, artifacts, or messages.
- **TLS private key:** proves service identity during authenticated transport.
- **Secret/token:** credential used for authentication or authorization; not necessarily a cryptographic key.

Do not reuse one key across unrelated purposes. Key separation limits blast radius and avoids cross-protocol misuse.

## 3. KMS versus HSM

A Key Management Service provides managed key lifecycle, access policy, cryptographic operations, audit, and integration with cloud services. A Hardware Security Module is a specialised hardware security boundary for generating, storing, and using cryptographic keys.

A cloud KMS may be backed by HSM infrastructure, but service design, tenancy model, assurance, key exportability, region, and compliance scope vary. Evaluate the actual service guarantees rather than assuming all KMS offerings have identical properties.

## 4. Key lifecycle

1. **Planning:** identify data classification, key purpose, algorithm, ownership, cryptoperiod, availability, and recovery.
2. **Generation:** use approved cryptographic random generation or KMS/HSM generation.
3. **Activation:** record owner, metadata, policy, and permitted operations.
4. **Distribution:** securely deliver access through workload identity or controlled channels.
5. **Use:** authorise only required operations; audit key use and context.
6. **Rotation:** rotate based on cryptoperiod, compromise, policy, algorithm changes, or ownership changes.
7. **Suspension/revocation:** stop use when compromised or no longer trusted.
8. **Recovery:** use documented, tested backup and dual-control procedures.
9. **Destruction:** securely retire keys when retention and recovery obligations permit.

## 5. Rotation models

- **Automatic rotation:** service rotates key material under a managed policy.
- **Manual rotation:** operator creates and promotes a replacement through an approved workflow.
- **Re-wrapping:** decrypt or unwrap a DEK under an old KEK and wrap it under a new KEK; bulk data need not always be re-encrypted.
- **Re-encryption:** decrypt data and encrypt with a new DEK/key where cryptographic migration or compromise response requires it.

Rotation does not mean the old key can always be immediately deleted. Historical ciphertext, backups, archives, legal retention, and disaster recovery may still depend on old key material.

## 6. Separation of duties and access control

Separate:
- Key administrators who configure policy and lifecycle.
- Key users/workloads that perform encrypt/decrypt/sign/verify operations.
- Auditors who review activity.
- Break-glass operators who follow exceptional approval and evidence processes.

Avoid broad wildcard permissions. Restrict by principal, operation, resource, environment, region, encryption context, and other service-supported conditions. A workload that only encrypts should not automatically receive decrypt rights.

## 7. Cloud KMS architecture considerations

For AWS KMS, understand key policies, IAM policies, grants, encryption context, aliases, multi-Region keys, automatic rotation support by key type, imported material, deletion windows, CloudTrail integration, and service integrations. The effective permission model can involve both key policy and IAM authorization; review the complete policy path.

For multi-account environments, define key ownership, cross-account trust, delegated administration, central logging, regional strategy, and account recovery. Cross-account decrypt should be narrowly scoped and explicitly justified.

## 8. Incident response for key compromise

Identify the key and dependent systems, contain access, preserve audit events, assess the scope and time window, rotate or revoke credentials, re-wrap or re-encrypt data as appropriate, update consumers, inspect backups and replicas, and verify the new trust state. Coordinate key disablement with application owners to avoid unplanned outages.

## 9. Study questions

1. Explain KEK and DEK and why envelope encryption scales.
2. Compare KMS and HSM.
3. What is the difference between rotation, re-wrapping, and re-encryption?
4. Why is separation of duties important?
5. What is encryption context and how can it constrain misuse?
6. What must be considered before disabling a compromised key?
7. How would you design key management across hundreds of cloud accounts?
