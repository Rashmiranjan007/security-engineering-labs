import logging
import uuid
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from .identity import Principal, get_demo_principal
from .model import generate_answer
from .policy import Decision, authorize_tool
from .retrieval import ingest_document, retrieve

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-agent-security-lab")
app = FastAPI(title="AI Agent Security Lab", version="0.1.1")


class IngestRequest(BaseModel):
    document_id: str = Field(min_length=1, max_length=100)
    text: str = Field(min_length=1, max_length=12000)
    allowed_users: list[str] = Field(min_length=1, max_length=50)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ToolRequest(BaseModel):
    tool: str = Field(min_length=1, max_length=80)
    action: str = Field(min_length=1, max_length=40)
    resource_id: str = Field(min_length=1, max_length=100)
    arguments: dict = Field(default_factory=dict)
    approval_ref: str | None = None


@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-agent-security-lab"}


@app.post("/ingest")
def ingest(body: IngestRequest, principal: Principal = Depends(get_demo_principal)):
    try:
        ingest_document(body.document_id, body.text, principal, body.allowed_users)
    except Exception:
        logger.exception("document_ingest_failed")
        raise HTTPException(status_code=503, detail="Ingestion dependency unavailable")
    logger.info("document_ingested event_id=%s tenant=%s doc=%s", uuid.uuid4(), principal.tenant_id, body.document_id)
    return {"status": "ingested", "document_id": body.document_id}


@app.post("/chat")
def chat(body: ChatRequest, principal: Principal = Depends(get_demo_principal)):
    try:
        docs = retrieve(body.message, principal)
        answer = generate_answer(body.message, docs)
    except Exception:
        logger.exception("chat_dependency_failed")
        raise HTTPException(status_code=503, detail="AI service dependency unavailable")
    logger.info("chat_completed event_id=%s tenant=%s retrieved=%d", uuid.uuid4(), principal.tenant_id, len(docs))
    return {"answer": answer, "retrieved_document_ids": [d["document_id"] for d in docs]}


@app.post("/tool-proposal")
def tool_proposal(body: ToolRequest, principal: Principal = Depends(get_demo_principal)):
    decision = authorize_tool(
        principal, body.tool, body.action, body.resource_id, body.arguments, body.approval_ref
    )
    event_id = str(uuid.uuid4())
    logger.info("tool_policy_decision event_id=%s tenant=%s tool=%s decision=%s",
                event_id, principal.tenant_id, body.tool, decision.decision.value)
    if decision.decision == Decision.ALLOW:
        # Synthetic response only. No real ticketing integration or mutation.
        return {"decision": decision.decision.value, "reason": decision.reason,
                "simulated_result": {"ticket_id": body.resource_id, "status": "read_only_demo"}}
    return {"decision": decision.decision.value, "reason": decision.reason}
