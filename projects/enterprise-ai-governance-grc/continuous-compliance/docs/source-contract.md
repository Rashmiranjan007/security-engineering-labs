# Source Export Contract

A source snapshot is a JSON object with `schema_version`, `snapshot_id`, `generated_on` and a `sources` array.

Each source object contains `source_id`, `source_type` and a `findings` array. Each finding requires:
- `finding_id`: unique across the snapshot.
- `signal`: stable machine-readable signal key.
- `asset`: affected logical asset.
- `severity`: `critical`, `high`, `medium` or `low`.
- `status`: `open`, `in_progress`, `resolved` or `accepted`.
- `observed_at`: ISO-8601 timestamp with timezone.
- `evidence_ref`: reference to original source evidence.
- `summary`: concise sanitized description.

Resolved findings must include `resolution_evidence_ref`. Accepted findings should be supported by a separate approved exception record in the production workflow; this demo only labels the state and does not verify approvals or expiry.

Unknown signal keys are rejected unless a mapping is added. Duplicate finding IDs are rejected. Do not include secrets, raw prompts, personal data, customer content, credentials or sensitive logs in snapshots. Use opaque references to access-controlled evidence.
