# Enterprise AI Security Reference Architecture

## Trust boundaries

1. User to API: authenticate the caller and validate request size, content type, and rate.
2. API to orchestrator: pass only verified identity context; do not trust client-supplied tenant or role fields.
3. Orchestrator to model gateway: use an approved model endpoint and centrally enforced policy.
4. RAG service to data store: apply tenant and document ACLs before returning content.
5. Model output to tool gateway: treat all proposed actions and arguments as untrusted.
6. Tool gateway to executor: independently authorize the principal, operation, target, and parameters.
7. Application to telemetry: minimize sensitive data and protect audit integrity.

## Core design principles

- The model is a probabilistic component, not a policy decision point.
- Identity and authorization live in trusted application services.
- Tool calls are proposals; policy code decides whether they can execute.
- Retrieval must enforce document-level access before context construction.
- Prompt screening is defense in depth, not a security boundary.
- Human approval must be bound to a specific action, resource, parameters, and expiry.
- Observability must support investigations without indiscriminately logging prompts or secrets.

## Logical sequence

```text
Request -> OIDC validation -> Gateway policy -> Orchestrator
       -> authorized RAG retrieval -> model inference
       -> output checks -> tool proposal
       -> tool/resource authorization -> approval if required
       -> isolated executor -> audit event
```

## Production architecture decisions

- Use an enterprise OIDC provider and asymmetric token validation through trusted issuer metadata/JWKS.
- Use a gateway that supports model allowlisting, quotas, provider routing, data residency, and policy enforcement.
- Keep vector database namespaces and document ACLs bound to verified tenant/user claims.
- Use separate workload identities and narrowly scoped credentials for each tool.
- Place high-risk tools behind a dedicated approval and execution service.
- Send structured security events to a protected audit/SIEM platform.
