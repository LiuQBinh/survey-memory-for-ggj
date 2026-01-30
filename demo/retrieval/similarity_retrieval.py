"""
D1 – Similarity-based retrieval demo.
In-memory vector store: add documents, embed (simple bag-of-words style), query with top-k.
Run: python demo/retrieval/similarity_retrieval.py
"""

from __future__ import annotations

import math
import re
from typing import List, Tuple


def simple_embed(text: str, dim: int = 64) -> List[float]:
    """Simple deterministic 'embedding': normalized bag-of-words style vector (hash-based)."""
    words = re.findall(r"\w+", text.lower())
    vec = [0.0] * dim
    for w in words:
        h = hash(w) % dim
        vec[h] += 1.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Cosine similarity between two vectors (same length)."""
    return sum(x * y for x, y in zip(a, b))


class InMemoryVectorStore:
    """In-memory vector store: add docs, query by text with top-k."""

    def __init__(self, dim: int = 64):
        self.dim = dim
        self.documents: List[str] = []
        self.embeddings: List[List[float]] = []

    def add(self, text: str) -> None:
        self.documents.append(text)
        self.embeddings.append(simple_embed(text, self.dim))

    def query(self, text: str, top_k: int = 3) -> List[Tuple[str, float]]:
        q = simple_embed(text, self.dim)
        scores = [(doc, cosine_similarity(q, emb)) for doc, emb in zip(self.documents, self.embeddings)]
        scores.sort(key=lambda x: -x[1])
        return scores[:top_k]


def main() -> None:
    store = InMemoryVectorStore()
    # Add some memory-like documents
    store.add("User prefers dark mode and compact layout.")
    store.add("The agent decided to use retrieval because the query was about past context.")
    store.add("Meeting scheduled for Tuesday 3pm with the design team.")
    store.add("User asked for a summary of the last three conversations.")
    store.add("Error log: connection timeout after 5s; retry succeeded.")

    print("Similarity-based retrieval (D1)\n")
    queries = [
        "What are the user interface preferences?",
        "When is the design meeting?",
        "What did the agent do for retrieval?",
    ]
    for q in queries:
        print(f"Query: {q}")
        for doc, score in store.query(q, top_k=2):
            print(f"  [{score:.3f}] {doc}")
        print()

    print("Done.")


if __name__ == "__main__":
    main()
