from fastapi import FastAPI, HTTPException
from .rag import retrieve
from .runtime import RuntimeMonitor
from .schemas import ChatRequest, ChatResponse
from .security import inspect_untrusted_text, redact_secrets

app = FastAPI(title="AI Security Engineering Lab",
              description="Defensive demo of RAG isolation, input screening, and runtime telemetry.",
              version="1.0.0")
monitor = RuntimeMonitor()

@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_mode": "deterministic-demo"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    inspection = inspect_untrusted_text(request.message)
    if not inspection.allowed:
        monitor.record("prompt_injection_signal", "high", request.tenant_id,
                       "Potential prompt injection phrase detected")
        raise HTTPException(status_code=400, detail="Request blocked by input security policy")
    docs = retrieve(request.tenant_id, request.message)
    if not docs:
        monitor.record("retrieval_empty", "low", request.tenant_id,
                       "No tenant-scoped documents matched")
        answer = "I could not find a matching document in your authorized lab knowledge base."
    else:
        answer = "Relevant authorized lab notes: " + " ".join(doc["text"] for doc in docs)
    monitor.record("chat_request", "info", request.tenant_id,
                   "Completed deterministic RAG demo request")
    return ChatResponse(answer=redact_secrets(answer),
                        citations=[doc["id"] for doc in docs],
                        security_status="screened")

@app.get("/admin/security/events")
def security_events() -> dict:
    """Unauthenticated local-demo endpoint; add auth before deployment."""
    return monitor.snapshot()
