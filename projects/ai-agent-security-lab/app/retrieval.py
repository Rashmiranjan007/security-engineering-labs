import uuid
import requests
from qdrant_client import QdrantClient, models
from .config import OLLAMA_URL, OLLAMA_EMBED_MODEL, QDRANT_URL, QDRANT_COLLECTION, VECTOR_SIZE

client = QdrantClient(url=QDRANT_URL)


def ensure_collection():
    names = {c.name for c in client.get_collections().collections}
    if QDRANT_COLLECTION not in names:
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
        )


def embed(text: str) -> list[float]:
    response = requests.post(
        f"{OLLAMA_URL}/api/embed",
        json={"model": OLLAMA_EMBED_MODEL, "input": text},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["embeddings"][0]


def ingest_document(document_id: str, text: str, principal, allowed_users: list[str]):
    ensure_collection()
    vector = embed(text)
    stable_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"ai-agent-lab:{principal.tenant_id}:{document_id}"))
    client.upsert(
        collection_name=QDRANT_COLLECTION,
        points=[models.PointStruct(
            id=stable_id,
            vector=vector,
            payload={
                "document_id": document_id,
                "text": text,
                "tenant_id": principal.tenant_id,
                "allowed_users": allowed_users,
                "source_owner": principal.subject,
            },
        )],
    )


def retrieve(query: str, principal, limit: int = 4) -> list[dict]:
    ensure_collection()
    vector = embed(query)
    acl_filter = models.Filter(must=[
        models.FieldCondition(key="tenant_id", match=models.MatchValue(value=principal.tenant_id)),
        models.FieldCondition(key="allowed_users", match=models.MatchValue(value=principal.subject)),
    ])
    hits = client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=vector,
        query_filter=acl_filter,
        limit=limit,
        with_payload=True,
    ).points
    return [{"document_id": h.payload["document_id"], "text": h.payload["text"]} for h in hits]
