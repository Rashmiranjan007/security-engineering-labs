from .rag_data import DOCUMENTS

def retrieve(tenant_id: str, query: str, limit: int = 3) -> list[dict]:
    """Toy keyword retrieval with tenant filtering in trusted application code."""
    terms = [term.casefold() for term in query.split() if len(term) > 2]
    if not terms:
        return []
    owned = [doc for doc in DOCUMENTS if doc["tenant_id"] == tenant_id]
    matches = [doc for doc in owned if any(term in doc["text"].casefold() for term in terms)]
    return matches[:limit]
