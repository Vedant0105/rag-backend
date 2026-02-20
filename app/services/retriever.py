from typing import List
from app.services.embeddings import embed_query
from app.services.vector_store import vector_store
from app.core.config import settings


def retrieve_relevant_chunks(question: str) -> List[str]:
    """
    Embed question and retrieve top-k similar chunks.
    """
    query_vector = embed_query(question)

    results = vector_store.search(
        query_vector=query_vector,
        top_k=settings.TOP_K,
    )

    return results
