# Module 4 — Hashes, MACs, Signatures and Password Storage

## 1. Cryptographic hash functions

A cryptographic hash maps arbitrary-length input to a fixed-length digest. Important properties include:
- **Preimage resistance:** given a digest, finding an input that produces it should be computationally infeasible.
- **Second-preimage resistance:** given one input, finding a different input with the same digest should be infeasible.
- **Collision resistance:** finding any two different inputs with the same digest should be infeasible.

SHA-256 and SHA-3 are widely used hash families. A digest can detect accidental or unauthorised changes only when the expected digest is itself protected. An attacker who can replace both a file and its unsigned digest can replace both consistently.

## 2. Hashing is not authentication

A plain hash has no secret key. Anyone can calculate a digest. To authenticate a message, use a MAC with a shared secret or a digital signature with an asymmetric key pair.

## 3. HMAC

HMAC combines a cryptographic hash function with a secret key. It is commonly used for API request authentication, webhook verification, and message integrity between parties that share a secret.

Security requirements:
- Generate high-entropy keys.
- Keep the key confidential and limit access.
- Include relevant message context in the authenticated bytes.
- Define canonical serialization so sender and receiver sign exactly the same representation.
- Include timestamps/nonces or sequence identifiers when replay resistance is required.
- Compare tags in constant time.
- Rotate shared keys and support a controlled overlap period where appropriate.

HMAC does not provide non-repudiation because both parties possess the same secret and can create tags.

## 4. Digital signatures

Digital signatures use a private signing key and public verification key. They are useful for software release signing, document integrity, firmware authenticity, and provenance.

A robust signature system must define:
- Approved algorithms and parameters.
- Exact data serialization and canonicalization.
- Key identity and trust chain.
- Key protection and access approvals.
- Signature format and metadata.
- Expiry, revocation, and key rollover.
- Verification policy and failure behaviour.

A valid signature only says that the corresponding private key signed the data. It does not establish that the data is benign, approved, or free of vulnerabilities.

## 5. Password storage

Passwords are low-entropy human secrets. Fast general-purpose hashes are unsuitable for password storage because attackers can test guesses at high speed.

Use a dedicated password hashing/KDF scheme:
- Argon2id is a strong modern default where supported and approved.
- scrypt is memory-hard and can be suitable.
- PBKDF2 may be required in some regulated or compatibility contexts with reviewed iteration parameters.

Each password should have a unique random salt. Store algorithm and parameter metadata with the resulting verifier so the system can upgrade parameters over time. A pepper may add protection if stored separately, but it creates a separate high-value secret and recovery dependency.

Never store plaintext passwords, reversible encrypted passwords, or fast SHA-256 password digests.

## 6. Replay and canonicalization

A valid HMAC or signature can still be replayed if the protocol does not bind freshness. Include a timestamp, nonce, request ID, or monotonic sequence where appropriate, and enforce a replay window or one-time-use record.

Canonicalization matters because JSON field ordering, whitespace, Unicode normalization, URL encoding, and header ordering can change byte representation. Define precisely which bytes are authenticated.

## 7. Study questions

1. Explain preimage, second-preimage, and collision resistance.
2. Why does a SHA-256 digest not prove who produced a file?
3. Compare HMAC and digital signatures.
4. Why should MAC comparison be constant time?
5. What is a replay attack and how can a signed request still be replayed?
6. Why are Argon2id and scrypt preferred over SHA-256 for passwords?
7. Explain salt versus pepper and their storage requirements.
