# Module 3 — Asymmetric Cryptography and Key Exchange

## 1. Public/private key model

Asymmetric cryptography uses a mathematically related key pair:
- The **private key** is protected and used for operations such as signing or private-key decryption in schemes designed for it.
- The **public key** can be distributed and used to verify signatures or participate in key-establishment/encryption schemes.

The public key is not confidential, but its authenticity matters. If an attacker substitutes their public key, a protocol may establish a secure channel with the attacker instead of the intended service. Certificates, trust stores, fingerprints, and authenticated protocols address this problem.

## 2. Main use cases

- Digital signatures and verification.
- Authenticated key establishment.
- Certificate-based identity.
- Secure software and artifact signing.
- Establishing symmetric session keys for efficient data encryption.

Asymmetric algorithms are generally not used to encrypt large application payloads directly. Hybrid cryptography uses asymmetric techniques to establish or protect symmetric keys, then uses AEAD for bulk data.

## 3. RSA

RSA security is based on the difficulty of factoring large composite integers, under current classical computing assumptions. RSA can be used for encryption schemes and signatures, but the schemes and padding matter.

- For encryption, use a secure padding scheme such as RSA-OAEP, not textbook RSA.
- For signatures, use RSA-PSS rather than legacy or ad hoc constructions.
- Key sizes and parameter choices should follow current standards and organisational policy.
- RSA private keys require strong access control, backup, and rotation governance.

RSA is not a key-exchange protocol by itself in modern TLS 1.3; TLS 1.3 removed static RSA key exchange.

## 4. Elliptic-curve cryptography

ECC provides security based on elliptic-curve discrete logarithm problems. It can offer strong security with smaller keys and efficient operations.

Common families include:
- **ECDH:** elliptic-curve Diffie-Hellman key agreement.
- **ECDSA:** elliptic-curve digital signatures.
- **EdDSA / Ed25519:** signature schemes designed for simpler and safer implementations in supported contexts.

Do not confuse ECDH key agreement with ECDSA signatures. They solve different problems.

## 5. Diffie-Hellman key agreement

Diffie-Hellman allows two parties to derive a shared secret over a channel observed by an attacker. It does not, by itself, authenticate the parties. Without authentication, a man-in-the-middle can establish separate secrets with each endpoint.

Authenticated protocols combine key agreement with certificates, signatures, pre-shared keys, or another trusted authentication mechanism.

Ephemeral Diffie-Hellman keys provide forward secrecy when correctly negotiated and discarded after use.

## 6. Hybrid encryption and key derivation

A common conceptual flow:
1. Sender obtains or validates the recipient's public key.
2. A key-establishment mechanism derives shared secret material.
3. A KDF such as HKDF derives purpose-specific symmetric keys.
4. AEAD encrypts the actual payload.
5. Recipient performs the corresponding key agreement and derives the same symmetric key.
6. AEAD verifies and decrypts the payload.

A KDF is important because raw shared secrets should not simply be reused for arbitrary purposes. Context labels and protocol transcript information help separate keys and prevent cross-protocol confusion.

## 7. Digital signatures

A signer computes a signature over a message or digest using a private key. A verifier uses the corresponding public key. Signatures provide integrity and evidence that the holder of the private key authorised the signed data, subject to key custody and identity trust.

A signature does not encrypt the content. Anyone with access to the signed content and public key can verify it. Signature verification also does not prove that the signed content is safe.

## 8. Private-key protection

- Use KMS/HSM or hardware-backed storage for high-value signing keys.
- Separate signing permission from key administration.
- Restrict which build/release identities can invoke signing.
- Use approval gates and immutable audit logs for production release signing.
- Rotate, revoke, and replace compromised keys and publish updated trust metadata.
- Never put private keys in source code, container images, logs, or ordinary CI variables where protected key services are available.

## 9. Study questions

1. Why is a public key's authenticity important?
2. Explain RSA-OAEP versus RSA-PSS.
3. Compare ECDH, ECDSA, and Ed25519.
4. Why does unauthenticated Diffie-Hellman permit a man-in-the-middle attack?
5. Explain forward secrecy using ephemeral key exchange.
6. Why use a KDF after deriving a shared secret?
7. What does a digital signature prove, and what does it not prove?
