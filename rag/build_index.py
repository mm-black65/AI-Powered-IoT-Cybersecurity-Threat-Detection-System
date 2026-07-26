
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

KB_FOLDER = "knowledge_base"          # folder of .txt files, one doc per file
INDEX_PATH = "kb_index.faiss"
DOCS_PATH = "kb_docs.json"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # small, fast, good enough for this use case


def load_knowledge_base(folder: str = KB_FOLDER) -> list[dict]:
    """Load all .txt files from the knowledge base folder into memory."""
    if not os.path.exists(folder):
        raise FileNotFoundError(
            f"Knowledge base folder '{folder}' not found. "
            f"Create it and add .txt files (e.g., MITRE ATT&CK summaries, "
            f"mitigation playbooks) before running this script."
        )

    docs = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            path = os.path.join(folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    docs.append({"source": filename, "text": content})

    print(f"Loaded {len(docs)} knowledge base documents.")
    return docs


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    """Split long documents into overlapping chunks for better retrieval granularity."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def build_index(folder: str = KB_FOLDER):
    docs = load_knowledge_base(folder)

    all_chunks = []
    chunk_metadata = []

    for doc in docs:
        chunks = chunk_text(doc["text"])
        for chunk in chunks:
            all_chunks.append(chunk)
            chunk_metadata.append({"source": doc["source"], "text": chunk})

    print(f"Total chunks to embed: {len(all_chunks)}")

    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = model.encode(all_chunks, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    with open(DOCS_PATH, "w", encoding="utf-8") as f:
        json.dump(chunk_metadata, f, indent=2)

    print(f"Index saved to {INDEX_PATH}")
    print(f"Chunk metadata saved to {DOCS_PATH}")


if __name__ == "__main__":
    build_index()