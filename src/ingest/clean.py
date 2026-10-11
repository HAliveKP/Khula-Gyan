"""Normalize extracted page text while preserving its source and page fields."""

from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter
from collections.abc import Iterable, Mapping
from typing import Any


_PAGE_NUMBER = re.compile(r"(?i)^(?:page\s+)?\d+(?:\s+of\s+\d+)?$")


def normalize_text(text: str) -> str:
    """Apply safe Unicode and whitespace cleanup, including Devanagari NFC."""
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\ufeff", "").replace("\u00ad", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    cleaned: list[str] = []
    for line in text.split("\n"):
        line = "".join(char for char in line if char == "\t" or unicodedata.category(char) != "Cc")
        line = re.sub(r"[\t ]+", " ", line).strip()
        if line and not _PAGE_NUMBER.fullmatch(line):
            cleaned.append(line)
        elif not line and cleaned and cleaned[-1] != "":
            cleaned.append("")
    return "\n".join(cleaned).strip()


def clean_pages(pages: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Normalize pages and remove lines repeated at page tops or bottoms.

    Only lines repeated near the top/bottom of at least 60% of pages are
    treated as headers/footers. Body text and all page numbers are retained in
    the returned records, except printed page-number-only lines.
    """
    items = [dict(page) for page in pages]
    if not items:
        return []
    if any("page" not in item or "text" not in item for item in items):
        raise ValueError("every page record needs 'page' and 'text'")

    lines_by_page: list[list[str]] = []
    edge_frequency: Counter[str] = Counter()
    for item in items:
        if not isinstance(item["text"], str):
            raise TypeError("page text must be a string")
        normalized = normalize_text(item["text"])
        lines = normalized.splitlines()
        lines_by_page.append(lines)
        nonempty = [line for line in lines if line]
        for line in set(nonempty[:3] + nonempty[-3:]):
            edge_frequency[line.casefold()] += 1

    required_pages = max(2, math.ceil(len(items) * 0.6))
    repeated_edges = {line for line, count in edge_frequency.items() if count >= required_pages}

    cleaned: list[dict[str, Any]] = []
    for item, lines in zip(items, lines_by_page, strict=True):
        kept = [line for line in lines if line.casefold() not in repeated_edges]
        text = "\n".join(kept).strip()
        cleaned.append({**item, "text": text})
    return cleaned


def extraction_rating(text: str) -> str:
    """Give a conservative page-level text-quality signal for review."""
    if not text.strip():
        return "bad"
    if "\ufffd" in text:
        return "bad"
    readable = sum(char.isalnum() or char.isspace() or unicodedata.category(char).startswith("M") for char in text)
    if readable / max(len(text), 1) < 0.75 or len(text.strip()) < 30:
        return "ok"
    return "good"
