# Module 9 — Enterprise Architecture, Governance and Interview Review

## 1. Enterprise reference architecture

A mature enterprise design separates data encryption, key custody, identity, authorization, secret delivery, and audit.

Conceptual components:
- Applications and workloads encrypt data using vetted AEAD libraries.
- A KMS/HSM protects KEKs and performs key wrapping or cryptographic operations.
- A secrets platform stores application credentials and supports versioning/rotation.
- Workload identity authenticates services without embedding long-lived cloud keys.
- Policy controls which principals can use which keys or secrets and for what operations.
- Central audit collects KMS, identity, secret-store, cloud, Kubernetes, and application events.
- Detection and response teams monitor anomalous use and credential exposure.

## 2. Enterprise design principles

- **Least privilege:** grant only the necessary operation, resource, context, and duration.
- **Separation of duties:** distinguish key administration, key usage, approval, and audit.
- **Purpose separation:** distinct keys for encryption, signing, authentication, and environments.
- **Data minimisation:** do not collect or retain secrets or plaintext unnecessarily.
- **Short-lived identity:** prefer federation and workload identity over static credentials.
- **Defence in depth:** combine KMS policy, IAM, network controls, application authorization, and audit.
- **Recoverability:** test backup, restore, rotation, and disaster-recovery processes.
- **Crypto agility:** plan for algorithm deprecation and post-quantum migration.
- **Evidence:** retain key inventory, access reviews, rotation evidence, exceptions, and incident records.

## 3. Principal-level design scenario: multi-account AWS and EKS

Assume hundreds of Kubernetes clusters across multiple AWS accounts. Each workload needs database credentials, object storage access, and encryption for sensitive application records.

A defensible architecture should:
1. Use per-workload identity rather than shared node credentials.
2. Scope service-account trust to the intended cluster and namespace identity.
3. Use separate roles for secret retrieval, data encryption, and application runtime operations.
4. Use envelope encryption with account/environment-appropriate KMS keys.
5. Apply resource and key policies that restrict cross-account access and encryption context.
6. Deliver secrets at runtime through a managed store or CSI integration.
7. Enable encryption at rest for Kubernetes data and tightly scope Secret RBAC.
8. Centralise audit and detect anomalous secret reads, decrypt volume, and policy changes.
9. Automate rotation and verify application reload without service interruption.
10. Maintain an inventory of keys, secrets, certificates, owners, dependencies, and exceptions.
11. Test break-glass, recovery, regional failure, and key-compromise scenarios.
12. Define clear ownership among platform, application, cloud security, IAM, and SOC teams.

## 4. Governance and control evidence

Useful evidence includes:
- Approved cryptographic standard and algorithm allowlist.
- Key inventory with owner, purpose, location, status, cryptoperiod, and dependencies.
- KMS/HSM access policy reviews and access logs.
- Key rotation and revocation records.
- Secret inventory, ownership, expiry, and rotation status.
- Certificate inventory and renewal metrics.
- CI/CD secret scanning results and remediation tickets.
- Workload identity adoption and static key reduction.
- Incident records for key or credential compromise.
- Tested backup, restore, and disaster-recovery procedures.
- Documented cryptographic exceptions with expiry and risk acceptance.

## 5. Security metrics

- Percentage of production data stores encrypted with approved algorithms.
- Percentage of keys with accountable owners and current reviews.
- Percentage of secrets with automatic rotation and expiry.
- Number of long-lived static cloud credentials.
- Mean time to revoke and replace exposed credentials.
- Number of privileged decrypt operations and anomalous decrypt alerts.
- Certificate renewal success and certificates expiring within defined windows.
- Percentage of workloads using federated identity.
- Number and age of cryptographic exceptions.
- PQC inventory and migration coverage.

Metrics should have clear definitions, owners, scope, and data sources. A high encryption coverage percentage does not prove good key custody or authorization.

## 6. Interview questions and answer prompts

**Q: Encryption versus hashing?** Encryption is reversible with the correct key and is used for confidentiality. Hashing is a one-way digest operation used for integrity fingerprints and other constructions; it does not provide confidentiality or origin authentication by itself.

**Q: AES-GCM versus CBC?** GCM is AEAD and authenticates ciphertext and AAD. CBC provides confidentiality only and requires a separate correctly designed MAC; error handling can create padding-oracle risk. Prefer approved AEAD for new application designs.

**Q: What is envelope encryption?** A DEK encrypts data, while a KMS/HSM-protected KEK wraps the DEK. The application stores ciphertext and wrapped DEK, not plaintext key material.

**Q: How do you protect secrets in EKS?** Use workload identity, external secret delivery where appropriate, encryption at rest, least-privilege RBAC, restricted mounts, audit logging, and rotation. Do not treat base64 as encryption or commit populated Secret manifests.

**Q: How do you handle a leaked API key?** Treat it as compromised, identify scope and consumers, revoke it, issue a replacement through the managed platform, update and validate consumers, inspect logs and source history, investigate misuse, and record evidence.

**Q: How would you design KMS access at scale?** Establish account and environment boundaries, delegated administration, scoped key policies, workload-specific roles, cross-account controls, central audit, key inventory, rotation standards, and break-glass procedures.

**Q: What does rotation achieve?** It limits future use of old key material after consumers migrate. It does not automatically re-encrypt historic data, remove copies, invalidate leaked plaintext, or revoke already issued tokens.

**Q: How do you prepare for post-quantum cryptography?** Inventory algorithms and dependencies, prioritise long-lived confidential data, track standards and vendor support, test interoperable implementations, and design an orderly migration with agility and rollback.

## 7. Final self-assessment

You should be able to:
- Select appropriate primitives for each security requirement.
- Explain AES-GCM nonce and AAD requirements.
- Design hybrid encryption and envelope encryption.
- Explain RSA, ECC, ECDH, signatures, HMAC, and password hashing.
- Explain PKI, certificate validation, TLS, and mTLS.
- Design enterprise KMS/HSM key lifecycle and separation of duties.
- Secure secrets in AWS, EKS, Kubernetes, CI/CD, and AI workloads.
- Threat-model cryptographic failures and credential compromise.
- Define governance evidence, operational metrics, and incident runbooks.
- Explain cryptographic agility and PQC migration.
