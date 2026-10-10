"""Split extracted document text into chunks that retain source and page data.

The default splitter uses whitespace-delimited pieces as a small, dependency-free
approximation of tokens. Pass a model tokenizer's encode/decode functions when
exact model-token limits are needed. Do not combine text from separate pages.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


def chunk_text(
    text: str,
    *,
    doc_id: str,
    source: str,
    page: int,
    service: str,
    lang: str,
    source_url: str | None = None,
    chunk_size: int = 400,
    overlap: int = 50,
    encode: Callable[[str], list[Any]] | None = None,
    decode: Callable[[list[Any]], str] | None = None,
) -> list[dict[str, Any]]:
    """Return chunks following the blueprint's six-field Chunk contract.

    ``chunk_size`` defaults to 400 and must remain between 300 and 500.
    ``overlap`` defaults to 50. Without tokenizer functions, whitespace words
    are used as an approximation; for exact model tokens, supply both ``encode``
    and ``decode`` from the embedding model's tokenizer.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not doc_id.strip() or not source.strip():
        raise ValueError("doc_id and source are required")
    if not service.strip():
        raise ValueError("service is required")
    if lang not in {"ne", "en"}:
        raise ValueError("lang must be 'ne' or 'en' per the Chunk contract")
    if isinstance(page, bool) or not isinstance(page, int) or page < 1:
        raise ValueError("page must be a positive integer")
    if isinstance(chunk_size, bool) or not isinstance(chunk_size, int) or not 300 <= chunk_size <= 500:
        raise ValueError("chunk_size must be between 300 and 500")
    if isinstance(overlap, bool) or not isinstance(overlap, int) or overlap < 0:
        raise ValueError("overlap must be a non-negative integer")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    if (encode is None) != (decode is None):
        raise ValueError("provide both encode and decode, or neither")

    if encode and decode:
        units = encode(text)
        render = decode
    else:
        units = text.split()
        render = lambda part: " ".join(part)

    if not units:
        return []

    chunks: list[dict[str, Any]] = []
    step = chunk_size - overlap
    for number, start in enumerate(range(0, len(units), step), start=1):
        piece = render(units[start : start + chunk_size]).strip()
        if piece:
            chunks.append(
                {
                    "id": f"{doc_id}_p{page}_c{number}",
                    "text": piece,
                    "source": source,
                    "page": page,
                    "service": service,
                    "lang": lang,
                }
            )
        if start + chunk_size >= len(units):
            break

    return chunks
