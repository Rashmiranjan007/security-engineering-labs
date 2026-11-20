# Cryptography Fundamentals

## Security goals and primitives

| Goal | Primitive | Typical use | Important limitation |
|---|---|---|---|
| Confidentiality + integrity | Authenticated encryption (AES-GCM, ChaCha20-Poly1305) | Protect data at rest/in transit | Nonce requirements and key management remain critical |
| Integrity + shared-key authenticity | HMAC-SHA-256 | Webhook or message authentication | Any holder of the shared key can create a valid MAC |
| Integrity / fingerprints | SHA-256 | File digest, artifact identity | A hash alone does not authenticate origin |
| Public-key signatures | Ed25519 or ECDSA/RSA-PSS | Verify signed artifacts and messages | Protect private keys; define algorithm and key lifecycle |
| Key agreement | ECDH | Establish shared secrets | Requires authenticated peer identity and safe key derivation |
| Password storage | Argon2id, scrypt, PBKDF2 | Store password verifiers | Use unique salts and reviewed cost parameters |

## Symmetric vs asymmetric cryptography

- Symmetric cryptography uses the same secret key to encrypt and decrypt. It is efficient for bulk data.
- Asymmetric cryptography uses a public/private key pair. It supports signatures and key establishment; it is not a reason to encrypt large files directly with RSA.
- Hybrid/envelope encryption combines both: a data key encrypts application data, while a KMS/HSM-protected key encrypts the data key.

## Hash vs MAC vs digital signature

- A cryptographic hash is unkeyed; anyone can compute it.
- A MAC uses a shared secret; only key holders can generate/verify valid tags.
- A digital signature uses a private signing key and a public verification key. It supports third-party verification, subject to identity and key governance.

## TLS and PKI

TLS 1.3 provides authenticated key establishment and protected transport when correctly configured. Certificate validation must check trust chain, hostname, validity, usage, and revocation policy where applicable. Private keys must not be embedded in images or source repositories.

## Common design failures

- ECB mode, custom ciphers, unauthenticated encryption, hard-coded keys.
- Reusing AES-GCM nonces under one key.
- Treating Base64 as encryption or SHA-256 as password hashing.
- Ignoring certificate validation or disabling TLS verification.
- Logging secrets, plaintext, tokens, or key material.
- Using deprecated algorithms or weak key sizes without a migration plan.

Use vetted libraries and current NIST/OWASP guidance. Do not invent cryptographic protocols.
