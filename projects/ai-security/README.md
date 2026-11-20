# AI Application Security Lab

A defensive engineering lab for securing an AI/RAG application. It demonstrates identity-aware tenant isolation, request screening, security telemetry, and automated regression testing. It is a learning/portfolio project, not a production security product.

## Implemented controls

- JWT bearer-token verification with required issuer, audience, expiry, and identity claims
- Tenant and user identity derived from signed claims, not request-body fields
- Role-based access control for the administrative security-event endpoint
- Strict request schema validation
- Tenant-filtered retrieval over a synthetic in-memory corpus
- Prompt-injection signal detection and security-event recording
- Secret-like value redaction in generated responses
- Bounded in-memory runtime event telemetry
- Automated API/regression tests, GitHub Actions CI, and a non-root Docker image

## How to run

Requires Python 3.10+.

```bash
cd projects/ai-security
python -m pip install -r requirements.txt
export JWT_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
python -m unittest discover -s tests -v
```

Start the API in one terminal:

```bash
uvicorn app.main:app --reload
```

Mint a five-minute synthetic user token in another terminal (same `JWT_SECRET`):

```bash
python scripts/mint_demo_token.py --tenant tenant-a --user analyst-1 --role user
```

Copy the token into `TOKEN`, then call the API:

```bash
export TOKEN="<paste-token-here>"
curl -s http://127.0.0.1:8000/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Kubernetes workloads"}'
```

To inspect security events, mint a token with `--role admin` and use that token on `GET /admin/security/events`. Regular users receive HTTP 403. The health endpoint is public.

The token-minting script is strictly for local demonstrations. In a real deployment, integrate with an enterprise OIDC identity provider; do not expose a shared-secret token issuer.

## Architecture

```text
Client
  |
  v
JWT verification (signature, issuer, audience, expiry)
  |
  v
Identity + role authorization
  |
  v
Strict request validation
  |
  v
Input screening (signal only)
  |
  v
Tenant-scoped retrieval
  |
  v
Deterministic demo response -> secret-like value redaction
  |
  v
Response + synthetic citations

Admin JWT (role=admin) -> security-event endpoint
```

## Known limitations

- The response is deterministic; no real LLM provider is connected.
- Retrieval is keyword-based and in-memory; no vector database is connected.
- The demo uses HS256 shared-secret JWTs. Production should use OIDC/JWKS asymmetric verification, key rotation, and least-privilege scopes.
- Tenant isolation is demonstrated in application logic with synthetic data. Production must enforce tenant filters at the datastore boundary too.
- Prompt-injection screening is basic phrase detection, not a complete defense against direct or indirect prompt injection.
- Runtime events are in-memory and disappear on restart.
- No production token issuer, durable audit store, rate limiter, or distributed session/revocation system is included.

## Security principles

1. Authorization is enforced in trusted application code, never delegated to the model.
2. Tenant identity comes from verified claims, not caller-controlled request fields.
3. Retrieved content and model output must be treated as untrusted.
4. Every real tool must independently authorize its operation and target resource.
5. Schema validation checks structure, not truthfulness or safety.

See [Architecture](docs/ARCHITECTURE.md), [Threat Model](docs/THREAT-MODEL.md), and [Red-Team Test Plan](RED-TEAM-TEST-PLAN.md).

> Use synthetic data and authorized lab systems only. Never commit real secrets or customer data.
