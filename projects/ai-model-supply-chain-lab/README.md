# AI Model Supply Chain Security Lab

A defensive, offline lab for validating model artifacts before promotion into an AI platform. It focuses on model provenance, artifact integrity, source and license policy, approval gates, and tamper detection.

## What it demonstrates
- SHA-256 verification of model artifact bytes against a reviewed manifest.
- Required provenance fields: model identity, version, source, publisher, creation time, license and artifact digest.
- Allowlist policy for approved model sources and licenses.
- Explicit promotion approval and reviewer metadata.
- Safe path handling so a manifest cannot point outside the lab artifact directory.
- Negative tests for tampering, unapproved sources, missing approval and path traversal.

## Flow
Model publisher / upstream source -> quarantine download -> hash and provenance capture -> security/license review -> approval -> offline verification -> controlled model registry promotion -> deployment pipeline.

## Run
Python 3.10+; standard library only:

    python -m unittest discover -s projects/ai-model-supply-chain-lab/tests -v
    python projects/ai-model-supply-chain-lab/tools/verify_model.py --manifest projects/ai-model-supply-chain-lab/manifests/sample-model.json

The sample artifact is synthetic text, not a real model. The manifest is intentionally marked approved for demonstration.

## Production design recommendations
1. Store model artifacts in a private, access-controlled registry or object store.
2. Generate provenance at ingestion; do not trust metadata supplied only by an unverified uploader.
3. Use cryptographic signatures backed by managed KMS/HSM keys and verify them in the promotion pipeline. This lab verifies SHA-256 integrity and policy metadata; it does not implement digital signatures.
4. Bind approval to the exact artifact digest, model version, environment and reviewer identity.
5. Scan serialized model formats in an isolated, resource-limited environment. Avoid loading untrusted pickle-based artifacts in privileged processes.
6. Record immutable audit events for upload, scan, approval, promotion, rollback and revocation.
7. Re-verify the digest at deployment time; do not rely only on an ingestion-time check.
8. Maintain an inventory of model owners, use cases, licenses, dependencies, training-data lineage and expiry/review dates.

## Threats addressed
Artifact substitution, tampering, unapproved upstream source, license-policy violation, missing provenance, approval bypass and unsafe artifact path references.

## Limitations
This is an educational control demonstrator, not a complete model scanner, malware detector, license legal opinion, provenance attestation verifier or production signing system. SHA-256 proves byte equality with the supplied digest; it does not prove that a model is safe, unbiased, non-poisoned or trustworthy. Production signing should use an established signing and attestation ecosystem with managed private keys.
