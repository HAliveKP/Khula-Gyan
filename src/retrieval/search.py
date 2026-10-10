"""Dense Chroma retrieval for contract-shaped Khula Gyan chunks."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any


MODEL_NAME = "BAAI/bge-m3"
COLLECTION_NAME = "khula_gyan"
PERSIST_DIRECTORY = Path("chroma_db")
ALLOWED_SERVICES = {"driving_license", "citizenship", "passport"}


@lru_cache(maxsize=1)
def _load_model() -> Any:
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            "Install requirements.txt before searching; sentence-transformers is required."
        ) from exc
    return SentenceTransformer(MODEL_NAME)


def _collection() -> Any | None:
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError(
            "Install requirements.txt before searching; chromadb is required."
        ) from exc
    client = chromadb.PersistentClient(path=str(PERSIST_DIRECTORY))
    try:
        return client.get_collection(COLLECTION_NAME)
    except Exception as exc:
        # Chroma's missing-collection exception class changed between releases.
        if exc.__class__.__name__ in {"InvalidCollectionException", "NotFoundError"}:
            return None
        raise


def _similarity(distance: float) -> float:
    """Convert Chroma cosine distance [0, 2] to bounded similarity [0, 1]."""
    return max(0.0, min(1.0, 1.0 - float(distance)))


def search(query: str, k: int = 5, service: str | None = None) -> list[dict]:
    """Return top-k chunks with source/page metadata and a 0–1 similarity score.

    A score of 1 is an identical vector; 0 means cosine distance is 1 or more.
    This is a normalized similarity, not a calibrated probability. The blueprint's
    guard threshold must be tuned against verified questions before production.
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be a non-empty string")
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    if service is not None and service not in ALLOWED_SERVICES:
        raise ValueError("service must be driving_license, citizenship, passport, or None")

    collection = _collection()
    if collection is None or collection.count() == 0:
        return []

    query_embedding = _load_model().encode(
        [query.strip()], normalize_embeddings=True, show_progress_bar=False
    ).tolist()[0]
    where = {"service": service} if service else None
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(k, collection.count()),
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    found: list[dict] = []
    ids = result.get("ids", [[]])[0]
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]
    for chunk_id, text, metadata, distance in zip(ids, documents, metadatas, distances):
        if not isinstance(metadata, dict) or not isinstance(text, str):
            continue
        page = metadata.get("page")
        try:
            page = int(page)
        except (TypeError, ValueError):
            continue
        if page < 1 or not metadata.get("source"):
            continue
        found.append(
            {
                "id": chunk_id,
                "text": text,
                "source": str(metadata["source"]),
                "page": page,
                "service": metadata.get("service"),
                "lang": metadata.get("lang"),
                "score": _similarity(distance),
            }
        )
    return found
