import faiss
import numpy as np
from typing import List


class VectorStore:
    def __init__(self):
        self.index = None
        self.text_chunks: List[str] = []

    def add_embeddings(self, embeddings: np.ndarray, chunks: List[str]):
        """
        Add embeddings and corresponding chunks to FAISS.
        """
        if self.index is None:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings.astype("float32"))
        self.text_chunks.extend(chunks)

    def search(self, query_vector: np.ndarray, top_k: int = 4) -> List[str]:
        """
        Search similar chunks.
        """
        if self.index is None or self.index.ntotal == 0:
            return []

        query_vector = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.text_chunks):
                results.append(self.text_chunks[idx])

        return results


# 🔥 Global singleton (important)
vector_store = VectorStore()
