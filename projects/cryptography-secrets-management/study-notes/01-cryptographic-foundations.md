# Module 1 — Cryptographic Foundations

## 1. What cryptography is designed to protect

Cryptography is a collection of mathematical techniques and protocols used to establish security properties in the presence of an attacker. It does not independently make an application secure. Identity, authorization, endpoint security, key custody, secure implementation, operational monitoring, and recovery remain essential.

The major security goals are:

- **Confidentiality:** only authorised parties can understand protected information.
- **Integrity:** unauthorised changes can be detected.
- **Authentication:** a party, message, or data origin can be verified.
- **Non-repudiation:** in a defined legal and operational context, a signer cannot plausibly deny a signature. Digital signatures alone do not automatically establish this; identity proofing, key custody, policy, and evidence matter.
- **Key establishment:** parties establish shared cryptographic material over an untrusted channel.
- **Forward secrecy:** compromise of a long-term authentication key does not reveal previously recorded session traffic, assuming ephemeral key exchange and correct implementation.

## 2. Security vocabulary

- **Plaintext:** data before encryption or after successful decryption.
- **Ciphertext:** encrypted representation.
- **Cipher:** the algorithm and defined transformation used to encrypt/decrypt.
- **Key:** secret or private material that controls a cryptographic operation.
- **Nonce:** a value intended to be used once within a defined key/algorithm context.
- **IV:** initialization vector; requirements vary by mode. An IV is not necessarily secret.
- **Salt:** non-secret random value used to make derived hashes unique, particularly password hashing.
- **Tag:** authentication output produced by an AEAD mode or MAC.
- **AAD:** additional authenticated data; authenticated but not encrypted.
- **Cryptoperiod:** approved period during which a key is authorised for use.
- **Key hierarchy:** relationship between root/master keys, key-encryption keys, and data-encryption keys.

## 3. Kerckhoffs's principle

A secure system should remain secure even when the attacker knows the algorithm and protocol. Security should depend on protecting the key, not hiding the algorithm. Proprietary secrecy or obscure encoding is not a substitute for sound cryptography.

## 4. Entropy and randomness

Cryptographic keys, nonces, salts, and ephemeral secrets require appropriate randomness. Operating-system cryptographic random number generators draw from entropy sources and provide a secure random interface. Do not use ordinary pseudo-random functions intended for simulations, timestamps, counters without a design, usernames, or human-selected strings as cryptographic keys.

A key with a nominal length of 256 bits does not have 256 bits of effective security if it was generated from a weak password or predictable seed.

## 5. Threat models

Cryptographic design must state what the attacker can do:

- Observe, intercept, replay, delay, reorder, or modify network traffic.
- Read a database snapshot or backup.
- Obtain an application host or container.
- Steal a credential or compromise a workload identity.
- Read logs, crash dumps, environment variables, or build artifacts.
- Influence metadata, tenant identifiers, object IDs, or AAD.
- Abuse privileged KMS permissions or compromise an administrator.

Different controls address different attacker capabilities. Encryption at rest does not protect data from a compromised application that is authorised to decrypt it.

## 6. Primitive selection overview

| Requirement | Typical mechanism |
|---|---|
| Bulk data confidentiality and integrity | AEAD such as AES-GCM or ChaCha20-Poly1305 |
| Data integrity fingerprint | SHA-256 or SHA-3 |
| Shared-secret message authentication | HMAC |
| Publicly verifiable authenticity | Digital signature |
| Password verification | Argon2id, scrypt, or PBKDF2 with unique salts |
| Secure transport | TLS 1.3 with certificate validation |
| Key wrapping and envelope encryption | KMS/HSM-backed key-encryption key |

## 7. Common misconceptions

- Base64 is an encoding, not encryption.
- A hash is not encryption and cannot be decrypted.
- Encryption without authentication can be malleable and unsafe.
- A certificate does not prove that a website or service is benevolent; it binds a public key to an identity under a trust model.
- A secret stored in a Kubernetes Secret object is not automatically protected by encryption at rest.
- Rotating a key does not automatically re-encrypt old data or erase leaked copies.
- Strong algorithms do not compensate for exposed keys, weak authorization, or insecure endpoints.

## 8. Study questions

1. Explain confidentiality, integrity, authentication, and non-repudiation with separate examples.
2. Why must cryptographic security not depend on algorithm secrecy?
3. What is the difference between a nonce, IV, salt, and key?
4. Why is encryption at rest insufficient after application host compromise?
5. Explain why Base64, hashing, encryption, and signing are different operations.
6. What does forward secrecy protect, and what does it not protect?
