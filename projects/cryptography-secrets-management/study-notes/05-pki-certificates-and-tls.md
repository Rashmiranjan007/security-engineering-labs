# Module 5 — PKI, Certificates and TLS

## 1. Public Key Infrastructure

PKI is the people, policies, processes, systems, and cryptographic components used to create, distribute, validate, renew, revoke, and trust digital certificates.

A certificate binds an identity to a public key through a signature from a trusted Certificate Authority (CA). The relying party validates the certificate chain and checks whether the identity matches the intended service.

## 2. X.509 certificate concepts

Important fields include:
- Subject and Subject Alternative Name (SAN): identities represented by the certificate.
- Issuer: CA that signed the certificate.
- Public key and algorithm information.
- Validity period: not-before and not-after.
- Key Usage and Extended Key Usage: permitted purposes.
- Basic Constraints: whether the certificate can act as a CA.
- Serial number and signature algorithm.

For TLS server authentication, hostname validation against SAN is essential. A certificate with a valid chain but the wrong hostname must not be accepted.

## 3. Certificate chain validation

A typical chain is:
- Leaf/server certificate.
- One or more intermediate CA certificates.
- Trusted root CA in the client's trust store.

The client validates signatures, chain constraints, validity, key usage, identity, and applicable revocation policy. Trust anchors are configured by the client or operating environment. An attacker-controlled root CA in a trust store can undermine TLS identity checks.

## 4. Certificate lifecycle

Inventory certificates, assign owners, automate issuance and renewal, protect private keys, monitor expiry, revoke compromised certificates, and validate replacements. Expiry is a reliability and security risk; emergency manual renewal is not a sustainable lifecycle process.

## 5. TLS 1.3 high-level handshake

A simplified view:
1. Client sends supported versions, cipher suites, key shares, and extensions.
2. Server selects parameters and responds with its key share and certificate-based authentication.
3. Parties derive handshake and traffic secrets from key agreement and transcript data.
4. Server proves possession of its certificate private key by signing handshake context.
5. Client validates certificate chain and service identity.
6. Both sides derive traffic keys and protect application data with AEAD.

The actual TLS 1.3 protocol is more precise and includes transcript binding and key schedule details. Study the standard for exact message sequencing and security properties.

## 6. TLS security properties and limitations

TLS can provide transport confidentiality, integrity, and server authentication; mutual TLS can also authenticate clients. TLS does not automatically provide application-level authorization, protect compromised endpoints, encrypt data after it reaches the application, or prevent an authorised user from accessing data.

Use modern TLS versions and approved cipher suites. Disable obsolete protocols and weak configurations. Do not disable certificate validation to resolve connectivity problems.

## 7. Mutual TLS

In mTLS, both client and server present certificates. It is useful for service-to-service authentication, workload identity, and zero-trust service meshes. Certificate issuance and identity mapping must be tightly governed; possession of any certificate from a broad CA should not automatically grant broad access.

## 8. Study questions

1. What problem does PKI solve?
2. Explain leaf, intermediate, and root certificates.
3. Why is SAN validation essential?
4. What happens if a root CA is compromised?
5. Explain the high-level TLS 1.3 handshake.
6. Compare TLS server authentication and mutual TLS.
7. Why does TLS not replace application authorization?
