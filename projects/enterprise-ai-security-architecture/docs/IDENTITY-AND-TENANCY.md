# Identity and Tenant Security

## Identity source

Use an enterprise OIDC provider. Validate token signature, issuer, audience, expiry, not-before, authorized client, and required scopes. Prefer asymmetric signatures and JWKS-based key rotation. Do not accept tenant ID, user ID, role, or group membership from request bodies or arbitrary headers.

## Authorization model

- Derive subject, tenant, roles, and scopes from verified claims and trusted entitlement services.
- Use deny-by-default authorization.
- Apply authorization to every API, retrieval, document, and tool operation.
- Re-check authorization at execution time; do not rely on an earlier model decision.
- Use separate service identities for retrieval, model access, and each downstream tool.

## Multi-tenant retrieval

Every retrieval request must carry a server-derived tenant context. Enforce tenant and document ACL filters in the datastore query, not only in application post-processing. Consider namespace separation for high-sensitivity tenants. Test positive and negative access cases, including guessed document IDs and metadata filters.

## Session and token controls

Use short-lived access tokens, secure refresh-token handling, revocation strategy, key rotation, and secure transport. Do not log bearer tokens. Avoid shared long-lived API keys and broad service principals.

## Validation tests

- User from tenant A cannot retrieve tenant B documents.
- User cannot set or override tenant claims via request parameters.
- A regular user cannot invoke admin-only APIs.
- A revoked or expired identity cannot start new operations.
- Tool execution re-checks current authorization and target ownership.
