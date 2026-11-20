# Module 2 — Symmetric Encryption and Authenticated Encryption

## 1. Symmetric cryptography

Symmetric encryption uses the same secret key, or directly related secret material, for encryption and decryption. It is efficient for large data volumes and is therefore commonly used for files, databases, object storage, backups, and network session traffic.

The central operational problem is not only choosing an algorithm. It is securely generating, distributing, storing, authorising, rotating, backing up, and retiring the shared key.

## 2. Block ciphers and AES

AES is a standardised block cipher with a 128-bit block size and key sizes of 128, 192, or 256 bits. AES transforms fixed-size blocks; a mode of operation defines how to safely process messages of arbitrary length.

AES is not itself a complete file-encryption protocol. Mode selection, nonce/IV generation, authentication, padding rules where applicable, metadata handling, and key management are all part of the design.

## 3. Modes of operation

- **ECB:** encrypts blocks independently and reveals repeated patterns. Do not use for general data encryption.
- **CBC:** uses an IV and requires separate integrity protection. Incorrect padding/error handling can create padding-oracle vulnerabilities.
- **CTR:** turns a block cipher into a stream-like construction. Counter/nonce reuse under the same key is catastrophic.
- **GCM:** an authenticated encryption mode that provides confidentiality and integrity when used correctly.
- **XTS:** designed for storage-sector encryption; it is not a general-purpose authenticated messaging format.

The correct mode depends on the use case. Prefer an approved AEAD construction for application messages and records.

## 4. Authenticated encryption with associated data (AEAD)

AEAD provides confidentiality and authenticity for plaintext while also authenticating selected metadata.

Conceptual inputs:
- Secret key
- Nonce
- Plaintext
- Optional AAD

Outputs:
- Ciphertext
- Authentication tag

Decryption verifies the tag before releasing plaintext. If the key, nonce, ciphertext, tag, or AAD is wrong or modified, authentication must fail. Applications should fail closed and must not process unauthenticated plaintext.

### AES-GCM

AES-GCM is widely used and efficient, with hardware acceleration on many platforms. A 96-bit nonce is the common recommended size. Nonce uniqueness under a given key is essential. Reuse can undermine both confidentiality and authentication.

Random nonces reduce coordination complexity but still require a sound collision-risk analysis at high volume. Counter-based allocation can provide uniqueness but needs robust distributed coordination, persistence, and rollback protection. A key rotation or per-message/per-object key design may be part of the risk reduction strategy.

### ChaCha20-Poly1305

ChaCha20-Poly1305 is another widely used AEAD construction. It can perform well where AES hardware acceleration is unavailable. Nonce requirements still apply; use vetted libraries and their documented APIs.

## 5. AAD and context binding

AAD is visible metadata that is authenticated alongside ciphertext. Examples include tenant ID, object ID, record type, schema version, or data classification. AAD can prevent a valid ciphertext from being moved into a different logical context if the decrypting service independently supplies and verifies the expected context.

Do not blindly trust context values supplied by an untrusted caller. The trusted application should derive expected AAD from authenticated identity and server-side object metadata.

## 6. Envelope encryption

Envelope encryption uses two layers:

1. A data-encryption key (DEK) encrypts application data using AEAD.
2. A key-encryption key (KEK), usually managed by a KMS/HSM, protects the DEK.

The application stores ciphertext, nonce, AAD metadata, algorithm/version information, and the encrypted DEK. It should not store the plaintext DEK. Decryption requires an authorised KMS unwrap/decrypt operation followed by local data decryption.

Benefits include efficient bulk encryption, separation of key administration from data storage, scoped KMS policy, and re-wrapping data keys without necessarily re-encrypting all data.

## 7. Design failure modes

- Reusing a GCM nonce under the same key.
- Using ECB or custom modes.
- Encrypting but not authenticating.
- Releasing plaintext before tag verification.
- Storing the DEK beside the data in plaintext.
- Using caller-controlled AAD without trusted context binding.
- Logging plaintext, keys, or authentication failures with sensitive details.
- Failing to version ciphertext formats and key identifiers.
- Losing old keys before retained data has been migrated or expired.

## 8. Study questions

1. Why is AES a block cipher rather than a complete encryption solution?
2. Compare ECB, CBC, CTR, GCM, and XTS.
3. What security properties does AEAD provide?
4. Why is GCM nonce reuse dangerous?
5. Explain AAD with a multi-tenant database example.
6. Walk through envelope encryption and identify where each key exists.
7. What should an application do when AEAD authentication fails?
