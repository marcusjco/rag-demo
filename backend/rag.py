"""
RAG pipeline — embed documents into ChromaDB, retrieve relevant chunks for a query.
Uses sentence-transformers locally (no extra API key needed).
"""
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from documents import DOCUMENTS

_collection = None


def _get_collection():
    global _collection
    if _collection is None:
        ef = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        client = chromadb.Client()
        _collection = client.get_or_create_collection(
            name="meridian_kb",
            embedding_function=ef,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def load_knowledge_base():
    col = _get_collection()
    if col.count() > 0:
        return

    col.add(
        ids=[d["id"] for d in DOCUMENTS],
        documents=[d["text"] for d in DOCUMENTS],
        metadatas=[{"doc": d["doc"], "section": d["section"], "category": d["category"]} for d in DOCUMENTS],
    )
    print(f"Loaded {len(DOCUMENTS)} chunks into ChromaDB.")


def retrieve(query: str, n_results: int = 4) -> list[dict]:
    col = _get_collection()
    results = col.query(query_texts=[query], n_results=n_results)

    chunks = []
    for i, doc_text in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][i]
        dist = results["distances"][0][i]
        chunks.append({
            "id":       results["ids"][0][i],
            "text":     doc_text,
            "doc":      meta["doc"],
            "section":  meta["section"],
            "category": meta["category"],
            "score":    round(1 - dist, 3),  # cosine similarity
        })
    return chunks


def list_documents() -> list[dict]:
    seen = {}
    for d in DOCUMENTS:
        key = d["doc"]
        if key not in seen:
            seen[key] = {"doc": d["doc"], "category": d["category"], "sections": []}
        seen[key]["sections"].append(d["section"])
    return list(seen.values())
