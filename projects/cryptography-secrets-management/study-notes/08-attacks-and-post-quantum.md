# Module 8 — Cryptographic Attacks, Implementation Failures and Post-Quantum Transition

## 1. Attacks against cryptographic systems

Cryptographic failures often target the protocol, implementation, key handling, or surrounding application rather than breaking the mathematical algorithm.

### Brute force and weak keys
Attackers try candidate keys or passwords. High-entropy keys, appropriate key sizes, memory-hard password hashing, rate limits, and protected key custody raise the cost.

### Replay attacks
An attacker records a valid request or token and resubmits it. Bind authentication to freshness using timestamps, nonces, sequence numbers, short lifetimes, and server-side replay detection where required.

### Man-in-the-middle
An attacker intercepts and relays traffic while impersonating endpoints. Authenticated key exchange, certificate validation, hostname checks, and secure trust-store management prevent unauthenticated substitution.

### Padding oracle
An application reveals whether decrypted padding is valid. Different error messages or timing can allow adaptive ciphertext attacks against vulnerable CBC constructions. Use authenticated encryption and avoid exposing distinguishable decryption errors.

### Nonce reuse
Reusing a nonce with the same key in modes such as GCM can cause severe confidentiality and authenticity failures. Nonce management is a protocol and distributed-systems design requirement, not merely a random-number detail.

### Side-channel attacks
Timing, cache behaviour, power consumption, electromagnetic leakage, and fault behaviour may reveal information about secret operations. Use constant-time implementations and hardware protections where relevant; application code should rely on vetted libraries.

### Downgrade and algorithm confusion
An attacker may cause peers to negotiate weaker algorithms or exploit inconsistent algorithm/key handling. Enforce approved protocol versions, algorithm allowlists, strong parameter validation, and authenticated negotiation.

### Key theft and authorization abuse
A stolen key or overly broad KMS permission can bypass the mathematical strength of the algorithm. Least privilege, HSM/KMS protections, workload identity, audit, and rapid revocation are critical.

## 2. Implementation and operational failures

- Hard-coded or shared keys.
- Secrets in source history, logs, crash dumps, backups, or container layers.
- Disabled certificate verification.
- Weak random generation.
- Unauthenticated encryption.
- Incorrect serialization or canonicalization.
- Unbounded decrypt endpoints and error oracles.
- Incorrect key rotation that breaks old ciphertext or leaves compromised keys active.
- Weak recovery processes that bypass normal controls.
- Missing inventory of certificates and keys.

## 3. Cryptographic agility

Cryptographic agility is the ability to change algorithms, key sizes, protocols, certificates, and key formats without redesigning every application. Build versioned ciphertext envelopes, algorithm identifiers, key IDs, policy-driven allowlists, automated inventory, and migration testing. Agility does not mean accepting arbitrary algorithms from untrusted input.

## 4. Quantum computing and cryptography

A sufficiently capable fault-tolerant quantum computer would threaten widely used public-key systems based on integer factorization and discrete logarithms, including RSA and ECC. Grover's algorithm can reduce the effective search complexity of brute-force symmetric key search, but does not make modern symmetric encryption instantly obsolete.

Post-quantum cryptography (PQC) develops algorithms intended to resist known classical and quantum attacks. NIST has standardised key encapsulation and signature algorithms, including ML-KEM, ML-DSA, and SLH-DSA. Organisations should track current standards and implementation guidance rather than inventing hybrid protocols.

## 5. Harvest now, decrypt later

An attacker may collect encrypted traffic or data today and attempt to decrypt it in the future when quantum capabilities improve. This is most relevant for information with long confidentiality lifetimes, such as sensitive intellectual property, personal data, strategic records, and long-lived secrets.

Risk assessment should consider data lifetime, exposure, storage location, protocol use, migration complexity, and attacker incentives.

## 6. PQC migration planning

1. Inventory cryptographic algorithms, certificates, libraries, protocols, key lengths, and data flows.
2. Identify dependencies on RSA, ECDH, ECDSA, and vulnerable key-establishment mechanisms.
3. Classify information by confidentiality lifetime and impact.
4. Track vendor and cloud-provider PQC roadmaps.
5. Test supported standards and interoperability in non-production.
6. Plan certificate, protocol, hardware, HSM, and performance upgrades.
7. Preserve cryptographic agility and monitor standards updates.
8. Validate migration, rollback, and incident response.

## 7. Study questions

1. Explain replay, downgrade, MITM, and padding-oracle attacks.
2. Why can a cryptographically strong algorithm still fail due to a side channel?
3. What is cryptographic agility?
4. Which classes of public-key cryptography are threatened by a large-scale quantum computer?
5. Explain harvest-now-decrypt-later risk.
6. What should be inventoried before a PQC migration?
