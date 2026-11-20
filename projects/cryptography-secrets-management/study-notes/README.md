# Cryptography and Secrets Management — Study Notes

These notes are a theory-first learning path. They are deliberately separate from the executable lab. Study the concepts, design trade-offs, threat models, and enterprise operating practices before using the practical exercises.

## Recommended sequence

1. [Module 1 — Cryptographic foundations](01-cryptographic-foundations.md)
2. [Module 2 — Symmetric encryption and authenticated encryption](02-symmetric-and-aead.md)
3. [Module 3 — Asymmetric cryptography and key exchange](03-asymmetric-cryptography.md)
4. [Module 4 — Hashing, MACs, signatures and password storage](04-hashes-macs-signatures-passwords.md)
5. [Module 5 — PKI, certificates and TLS](05-pki-certificates-and-tls.md)
6. [Module 6 — Enterprise key management and KMS/HSM](06-enterprise-key-management.md)
7. [Module 7 — Secrets management for cloud, Kubernetes and CI/CD](07-enterprise-secrets-management.md)
8. [Module 8 — Cryptographic attacks, failures and post-quantum transition](08-attacks-and-post-quantum.md)
9. [Module 9 — Enterprise architecture, governance and interview review](09-architecture-governance-and-interview-review.md)

## How to study

- First understand the security property being provided: confidentiality, integrity, authenticity, non-repudiation, identity, or key establishment.
- For each primitive, learn its inputs, outputs, trust assumptions, failure modes, and correct use cases.
- Draw the data flow and key flow. Ask where plaintext, keys, credentials, and metadata exist at every step.
- Compare designs rather than memorising algorithm names.
- Use the review questions at the end of each module to test understanding.

## Scope

These are educational technical notes, not implementation instructions for a production cryptographic system, a legal interpretation, or a certification guide. Production systems should use vetted libraries, managed cryptographic services, current standards, and independent security review.
