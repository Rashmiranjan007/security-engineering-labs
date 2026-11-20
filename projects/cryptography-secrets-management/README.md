# Cryptography & Secrets Management Engineering Lab

A practical, security-focused lab covering application cryptography, key management, secrets hygiene, and cloud-native secret delivery.

## Learning objectives

- Select the right cryptographic primitive for confidentiality, integrity, authenticity, and password storage.
- Use authenticated encryption (AES-256-GCM) with unique nonces and authenticated associated data (AAD).
- Use HMAC-SHA-256 for message integrity and authenticity; compare MACs in constant time.
- Understand key generation, storage, rotation, revocation, backup, recovery, and destruction.
- Detect common hard-coded secret patterns in an explicitly selected source tree.
- Design secure secrets delivery for AWS, Kubernetes, CI/CD, and AI workloads.

## Lab contents

| Path | Purpose |
|---|---|
| `crypto_lab.py` | AES-GCM authenticated encryption, HMAC signing/verification, strict key parsing |
| `secret_scanner.py` | Local, read-only scanner for common credential patterns |
| `tests/` | Unit tests for tampering, AAD mismatch, key validation, and scanner findings |
| `fixtures/` | Synthetic examples only; never real credentials |
| `docs/cryptography-fundamentals.md` | Symmetric/asymmetric crypto, hashes, MACs, signatures, TLS, PKI |
| `docs/key-management-lifecycle.md` | Enterprise KMS/HSM and key lifecycle |
| `docs/cloud-and-kubernetes-secrets.md` | AWS, EKS, Kubernetes, CI/CD and workload identity patterns |
| `docs/threat-model-and-runbooks.md` | Threat scenarios, incident response, operational controls |

## Quick start

Python 3.10+ is required.

```bash
cd projects/cryptography-secrets-management
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

### Authenticated encryption demo

Generate a fresh 256-bit key for this local demo. Keep it in the current shell only; do not commit it or use it as a production key.

```bash
python -c "import secrets,base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"
```

Set the generated value as an environment variable, then run:

```bash
export LAB_AES_KEY_B64='PASTE_FRESH_DEMO_KEY_HERE'
python crypto_lab.py encrypt --text "confidential demo payload" --aad "tenant=demo"
python crypto_lab.py encrypt --text "confidential demo payload" --aad "tenant=demo" --out envelope.json
python crypto_lab.py decrypt --input envelope.json --aad "tenant=demo"
```

The CLI never writes the key to disk. The JSON envelope contains a random nonce, ciphertext and algorithm metadata, not the encryption key. For PowerShell, use `$env:LAB_AES_KEY_B64="..."`.

### Secret scanning demo

```bash
python secret_scanner.py fixtures
```

The scanner is read-only and reports file paths, line numbers, and rule names; it does not print matched secret values. Scan only directories you are authorized to inspect. Treat results as leads for review, not proof that a credential is valid.

## Security design notes

- AES-GCM provides authenticated encryption. A 96-bit nonce is generated randomly for each encryption under a key. Never reuse a nonce with the same AES-GCM key.
- AAD is authenticated but not encrypted. It can bind ciphertext to context such as tenant, record ID, or schema version.
- HMAC is for message authentication with a shared secret; it is not a digital signature and does not provide non-repudiation.
- Passwords must use a dedicated password-hashing/KDF scheme such as Argon2id, scrypt, or PBKDF2 with a unique salt and reviewed parameters—not fast SHA-256.
- Store production keys in a managed KMS/HSM or secrets platform. Do not store keys beside ciphertext or in source control.
- Prefer workload identity and short-lived credentials over long-lived static cloud keys.
- Kubernetes Secret objects are base64-encoded data, not encryption by themselves. Enable encryption at rest and tightly scope RBAC.
- Never log secrets, access tokens, private keys, plaintext sensitive payloads, or cryptographic key material.

## Production architecture patterns

1. Application requests a data-encryption key from a KMS envelope-encryption workflow.
2. KMS protects the data key under a key-encryption key (KEK); the application encrypts data locally using a data-encryption key (DEK).
3. Persist ciphertext, nonce, AAD metadata, and the encrypted DEK. Do not persist plaintext DEKs.
4. Restrict decrypt permissions to the workload identity and required encryption context.
5. Audit key use, alert on anomalous decrypt activity, and rotate/revoke keys through a controlled process.
6. For Kubernetes, use external secret stores or CSI integrations with workload identity where possible; avoid broad cluster-wide secret access.

## Safety and limitations

This is an educational implementation, not a production KMS, HSM, password vault, certificate authority, or compliance assessment. The CLI is a local demonstration. The scanner uses heuristic patterns and cannot guarantee discovery of all secrets or validate credentials. Do not use real production secrets in fixtures or tests. Do not deploy sample keys or configurations to production.

## Further reading

- NIST SP 800-57: Recommendation for Key Management
- NIST SP 800-38D: Galois/Counter Mode (GCM)
- NIST SP 800-63B: Digital Identity Guidelines
- OWASP Cryptographic Storage Cheat Sheet
- OWASP Secrets Management Cheat Sheet
