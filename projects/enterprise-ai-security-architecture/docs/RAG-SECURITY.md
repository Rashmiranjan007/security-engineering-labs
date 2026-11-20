# RAG Security: Retrieval, Ingestion, and Poisoning

## Secure ingestion pipeline

1. Authenticate uploader and authorize the target tenant/collection.
2. Validate file type, size, parser behavior, and malware policy.
3. Extract text in a sandbox; do not execute embedded content.
4. Attach immutable provenance: source ID, owner, tenant, uploader, timestamp, classification, and content hash.
5. Apply DLP/classification and content safety checks.
6. Quarantine suspicious or untrusted sources for review.
7. Chunk and embed only approved content.
8. Preserve ACL metadata on every chunk and enforce it at query time.
9. Support revocation, deletion, and re-indexing when source permissions change.

## Retrieval-time controls

- Bind tenant and user identity from verified server context.
- Apply document-level ACL filters before top-k results are returned.
- Re-check authorization after retrieval and before context assembly where appropriate.
- Limit result count, chunk size, and total context tokens.
- Return provenance with every chunk.
- Treat retrieved content as untrusted data, never as trusted system instructions.
- Prevent retrieval from crossing tenants, classification levels, or data residency boundaries.

## Poisoning and indirect injection

A document may contain misleading instructions, hidden text, or requests to exfiltrate data. Content scanning can flag suspicious patterns but cannot prove content is safe. Use source trust levels, provenance, human review for high-impact sources, and strict separation between content and system policy.

## Operational controls

Monitor ingestion anomalies, source ownership changes, retrieval-denial spikes, and high-risk content access. Retain source hashes and ingestion decisions for investigation. Provide a way to revoke a source and purge all derived chunks/embeddings.
