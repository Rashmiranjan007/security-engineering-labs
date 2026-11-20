# Model supply-chain controls

## Trust boundaries
- Upstream publisher: source identity and original release.
- Ingestion/quarantine: downloaded bytes are untrusted until inspected.
- Review: security, ML and legal/license review.
- Promotion: only approved immutable digests move into production registry.
- Runtime: deployment verifies the same digest and records model identity.

## Minimum manifest fields
Model ID, version, publisher, source URL/identifier, artifact path, SHA-256 digest, license identifier, creation timestamp, provenance reference, approval state, reviewer and approval timestamp.

## Promotion policy
Block when any of the following is true:
- artifact digest does not match the downloaded bytes;
- source is not on the organization allowlist;
- license is absent or outside approved policy;
- model identity/version or provenance fields are missing;
- approval is absent, expired or not bound to the artifact digest;
- artifact path resolves outside the controlled artifact directory.

## Operational lifecycle
1. Ingest into quarantine with restricted write access.
2. Compute digest from the received bytes.
3. Capture source and provenance from trusted ingestion context.
4. Run format-aware static checks and isolated malware/sandbox analysis.
5. Review license, model card, intended use and data lineage.
6. Approve the exact digest and publish immutable artifact.
7. Verify digest again during deployment and emit audit event.
8. Revoke and block future pulls if compromise or license concern is discovered.

## Example control ownership
| Control | Accountable owner |
|---|---|
| Source allowlist and artifact registry | ML platform |
| Hash and signature verification | Platform security |
| License and usage review | Legal / responsible AI |
| Model card, lineage and evaluation | Model owner |
| Promotion approval | Model risk owner |
| Deployment-time verification | MLOps / platform engineering |
