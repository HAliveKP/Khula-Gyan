"""Create embeddings and store contract-shaped chunks in persistent ChromaDB."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {"id", "text", "source", "page", "service", "lang"}
ALLOWED_SERVICES = {"driving_license", "citizenship", "passport"}
ALLOWED_LANGUAGES = {"ne", "en"}


def _validated_chunks(chunks: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    prepared: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for position, chunk in enumerate(chunks, start=1):
        missing = REQUIRED_FIELDS - chunk.keys()
        if missing:
            raise ValueError(f"chunk {position} is missing: {', '.join(sorted(missing))}")

        item = dict(chunk)
        for field in ("id", "text", "source", "service", "lang"):
            if not isinstance(item[field], str) or not item[field].strip():
                raise ValueError(f"chunk {position} needs a non-empty string '{field}'")
        if item["service"] not in ALLOWED_SERVICES:
            raise ValueError(f"chunk {position} has an unknown service")
        if item["lang"] not in ALLOWED_LANGUAGES:
            raise ValueError(f"chunk {position} lang must be 'ne' or 'en'")
        if isinstance(item["page"], bool) or not isinstance(item["page"], int) or item["page"] < 1:
            raise ValueError(f"chunk {position} page must be a positive integer")
        if item["id"] in seen_ids:
            raise ValueError(f"duplicate chunk id: {item['id']}")
        seen_ids.add(item["id"])
        prepared.append(item)
    return prepared


def index_chunks(
    chunks: Iterable[Mapping[str, Any]],
    *,
    persist_directory: str | Path = "data/index/chroma",
    collection_name: str = "khula_gyan",
    model_name: str = "BAAI/bge-m3",
    batch_size: int = 32,
) -> Any:
    """Embed and upsert chunks, returning the Chroma collection.

    Heavy optional libraries are imported only when this function runs, so the
    source package remains importable on a beginner's setup before installation.
    Index files are local generated data and should not be committed.
    """
    if not collection_name.strip():
        raise ValueError("collection_name cannot be empty")
    if isinstance(batch_size, bool) or not isinstance(batch_size, int) or batch_size < 1:
        raise ValueError("batch_size must be a positive integer")

    items = _validated_chunks(chunks)

    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            "Install the project requirements before indexing: chromadb and sentence-transformers are required."
        ) from exc

    client = chromadb.PersistentClient(path=str(persist_directory))
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine", "embedding_model": model_name},
    )
    if not items:
        return collection

    model = SentenceTransformer(model_name)
    for start in range(0, len(items), batch_size):
        batch = items[start : start + batch_size]
        vectors = model.encode(
            [item["text"] for item in batch],
            normalize_embeddings=True,
            show_progress_bar=False,
        ).tolist()
        collection.upsert(
            ids=[item["id"] for item in batch],
            documents=[item["text"] for item in batch],
            metadatas=[
                {
                    "source": item["source"],
                    "page": item["page"],
                    "service": item["service"],
                    "lang": item["lang"],
                }
                for item in batch
            ],
            embeddings=vectors,
        )
    return collection
