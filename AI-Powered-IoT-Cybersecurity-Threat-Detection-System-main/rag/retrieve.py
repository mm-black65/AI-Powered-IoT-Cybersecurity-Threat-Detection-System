import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_PATH = "kb_index.faiss"
DOCS_PATH = "kb_docs.json"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

_model = None
_index = None
_docs = None


def _load_resources():
    """Lazy-load the model, index, and docs once, reuse across calls."""
    global _model, _index, _docs

    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)

    if _index is None:
        try:
            _index = faiss.read_index(INDEX_PATH)
        except Exception as e:
            raise RuntimeError(
                f"Could not load FAISS index from '{INDEX_PATH}'. "
                f"Run build_index.py first. Original error: {e}"
            )

    if _docs is None:
        with open(DOCS_PATH, "r", encoding="utf-8") as f:
            _docs = json.load(f)


def retrieve(query: str, top_k: int = 3) -> list[dict]:
    """
    Return the top_k most relevant knowledge base chunks for a given query.

    Example:
        results = retrieve("DDoS TCP flood mitigation", top_k=3)
        for r in results:
            print(r["source"], "-", r["score"])
    """
    _load_resources()

    query_embedding = _model.encode([query]).astype("float32")

    distances, indices = _index.search(query_embedding, top_k)

    results = []
    for rank, idx in enumerate(indices[0]):
        if idx == -1:
            continue
        doc = _docs[idx]
        results.append({
            "source": doc["source"],
            "text": doc["text"],
            "score": float(distances[0][rank]),  # lower = more similar (L2 distance)
        })

    return results


def build_rag_context(prediction: str, confidence: float, threat_level: str, top_k: int = 3) -> str:
    """
    Convenience function: turns an ML prediction into a retrieval query,
    then formats the retrieved chunks into a single context string ready
    to insert into an LLM prompt.
    """
    query = f"{prediction} attack, threat level {threat_level}, mitigation steps"
    results = retrieve(query, top_k=top_k)

    if not results:
        return "No relevant knowledge base information found."

    context_parts = [f"[{r['source']}]: {r['text']}" for r in results]
    return "\n\n".join(context_parts)


if __name__ == "__main__":
    # Quick manual test
    sample_context = build_rag_context("DDoS-TCP_Flood", 99.9, "HIGH")
    print(sample_context)