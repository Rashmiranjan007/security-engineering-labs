import os

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .rag import retrieve
from .runtime import RuntimeMonitor
from .schemas import ChatRequest, ChatResponse
from .security import inspect_untrusted_text, redact_secrets

app = FastAPI(
    title="AI Security Engineering Lab",
    description="Defensive demo of JWT identity, RAG isolation, input screening, and runtime telemetry.",
    version="1.1.0",
)
monitor = RuntimeMonitor()
bearer = HTTPBearer(auto_error=False)
JWT_ISSUER = "ai-security-lab"
JWT_AUDIENCE = "ai-security-api"


def authenticated_identity(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> dict:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    secret = os.getenv("JWT_SECRET", "")
    if len(secret.encode("utf-8")) < 32:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="JWT verification is not configured securely",
        )
    try:
        claims = jwt.decode(
            credentials.credentials,
            secret,
            algorithms=["HS256"],
            issuer=JWT_ISSUER,
            audience=JWT_AUDIENCE,
            options={"require": ["exp", "iat", "sub", "tenant_id", "role", "iss", "aud"]},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not isinstance(claims.get("sub"), str) or not isinstance(claims.get("tenant_id"), str):
        raise HTTPException(status_code=401, detail="Invalid identity claims")
    if not claims["sub"] or not claims["tenant_id"]:
        raise HTTPException(status_code=401, detail="Invalid identity claims")
    if claims.get("role") not in {"user", "admin"}:
        raise HTTPException(status_code=403, detail="Unsupported role")
    return claims


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_mode": "deterministic-demo"}


@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    identity: dict = Depends(authenticated_identity),
) -> ChatResponse:
    tenant_id = identity["tenant_id"]
    inspection = inspect_untrusted_text(request.message)
    if not inspection.allowed:
        monitor.record(
            "prompt_injection_signal",
            "high",
            tenant_id,
            "Potential prompt injection phrase detected",
        )
        raise HTTPException(status_code=400, detail="Request blocked by input security policy")
    docs = retrieve(tenant_id, request.message)
    if not docs:
        monitor.record(
            "retrieval_empty",
            "low",
            tenant_id,
            "No tenant-scoped documents matched",
        )
        answer = "I could not find a matching document in your authorized lab knowledge base."
    else:
        answer = "Relevant authorized lab notes: " + " ".join(doc["text"] for doc in docs)
    monitor.record(
        "chat_request",
        "info",
        tenant_id,
        "Completed deterministic RAG demo request",
    )
    return ChatResponse(
        answer=redact_secrets(answer),
        citations=[doc["id"] for doc in docs],
        security_status="screened",
    )


@app.get("/admin/security/events")
def security_events(identity: dict = Depends(authenticated_identity)) -> dict:
    if identity["role"] != "admin":
        raise HTTPException(status_code=403, detail="Administrator role required")
    return monitor.snapshot()
