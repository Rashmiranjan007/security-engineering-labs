# AI Data Protection

## Data lifecycle

| Stage | Risks | Controls |
|---|---|---|
| User input | PII, credentials, regulated data | Classification, DLP, minimization, policy-based rejection or masking |
| Retrieval | Unauthorized or over-classified content | Tenant and document ACLs, classification filters |
| Model provider | Provider retention/training, residency, exposure | Approved endpoint, contractual review, data residency, no-training settings where applicable |
| Model output | Secrets, personal data, unsafe instructions | Output DLP, schema validation, policy checks |
| Tool calls | Excessive data sharing and unauthorized changes | Per-tool scopes, argument filtering, authorization |
| Telemetry | Prompt/response over-collection | Structured events, redaction, minimization, retention controls |

## Design requirements

- Define data classes and allowed model/provider destinations.
- Avoid sending secrets, credentials, or unnecessary personal data to model context.
- Prefer tokenization or redaction before inference where feasible.
- Enforce output checks before displaying or forwarding model-generated content.
- Do not assume regex-based redaction is complete.
- Encrypt data in transit and at rest; manage keys separately from application data.
- Define retention, deletion, legal hold, and access review requirements.
- Prevent prompts, responses, and tokens from entering unrestricted logs or analytics.

## Incident response

For suspected AI data exposure: stop the affected workflow, revoke relevant credentials/tokens, preserve minimized audit evidence, identify impacted tenants/documents/providers, assess downstream tool actions, notify privacy/security stakeholders under applicable policy, and validate remediation with negative access tests.
