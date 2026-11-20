# AI Security Lab Architecture

Client -> JWT verification -> identity and role authorization -> request schema validation -> input screening -> tenant-scoped retrieval -> deterministic mock response -> secret-like value redaction -> response with synthetic citations.

Suspicious input produces a blocked response and a runtime security event. Runtime events are stored in a bounded in-memory buffer. The administrative event endpoint requires a verified JWT with the `admin` role.

## Identity and authorization boundary

- The caller sends only the message in the chat body. The API derives the user and tenant from signed JWT claims; client-supplied tenant/user fields are rejected.
- JWTs must be signed with HS256 and include `sub`, `tenant_id`, `role`, `iat`, `exp`, `iss`, and `aud` claims.
- The verification secret is read from `JWT_SECRET`; the service refuses to verify tokens if it is missing or shorter than 32 bytes.
- The expected issuer is `ai-security-lab` and audience is `ai-security-api`.
- Only `user` and `admin` roles are accepted. The admin telemetry endpoint requires `admin`.
- The included tests mint synthetic tokens with a test-only key. There is intentionally no public token-issuing endpoint.

## Remaining demo limitations

- This is a local engineering lab, not a production identity service. Production should use an enterprise OIDC provider and validate asymmetric signatures, key rotation, issuer, audience, scopes, and token revocation policy.
- Retrieval uses a tiny in-memory synthetic corpus, not a vector database. Production tenant isolation must also be enforced in the datastore/query layer.
- The response adapter is deterministic and does not call a real LLM.
- Input screening is a basic demonstration, not robust prompt-injection prevention.
- Runtime events are in-memory and are lost on restart.

## Production hardening

Use enterprise OIDC/JWKS validation, short-lived tokens, least-privilege scopes, rate limiting, request size limits, durable tamper-evident audit storage, encrypted storage, managed secrets, network controls, and datastore-enforced tenant isolation. Treat model output and retrieved documents as untrusted data; enforce authorization outside the model.
