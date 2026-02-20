from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

# Lazy-loaded global model
_model = None


def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_texts(texts: List[str]) -> np.ndarray:
    """
    Embed list of texts into vectors.
    """
    model = get_embedding_model()
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings


def embed_query(text: str) -> np.ndarray:
    """
    Embed single query.
    """
    model = get_embedding_model()
    embedding = model.encode([text], show_progress_bar=False)
    return embedding[0]
