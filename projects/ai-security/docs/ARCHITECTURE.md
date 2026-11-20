# AI Security Lab Architecture

Client -> FastAPI schema validation -> input screening -> tenant-scoped retrieval -> deterministic mock response -> secret-like value redaction -> response with synthetic citations.

Suspicious input produces a blocked response and a runtime security event. Runtime events are stored in a bounded in-memory buffer.

## Security boundaries
- Tenant ID is supplied by the caller in this demo. Production must derive it from authenticated claims, never trust a client-supplied tenant identifier.
- The event endpoint is unauthenticated for local use only.
- Retrieval uses a tiny in-memory synthetic corpus, not a vector database.
- The deterministic response adapter is a placeholder for a model gateway with separate policy enforcement.

## Production hardening
Add authentication and authorization, tenant identity from verified tokens, datastore-level isolation, rate limiting, request size limits, audit retention, encrypted storage, secret management, network controls, and authenticated administrative telemetry.
