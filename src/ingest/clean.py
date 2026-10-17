"""Normalize extracted page text while preserving its source and page fields."""

from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter
from collections.abc import Iterable, Mapping
from typing import Any


# "Page 3", "3 of 10" and "Page 3 of 10" are always page labels. A line that is
# only a number is ambiguous: in charter tables it is often a fee ("९००") or a
# serial number, so ``clean_pages`` drops it only when it matches the page's
# printed number (see ``_page_number_offsets``). ``\d`` also matches
# Devanagari digits.
_PAGE_LABEL = re.compile(r"(?i)^(?:page\s+\d+(?:\s+of\s+\d+)?|\d+\s+of\s+\d+)$")
_BARE_NUMBER = re.compile(r"^\d{1,4}$")


def normalize_text(text: str) -> str:
    """Apply safe Unicode and whitespace cleanup, including Devanagari NFC.

    Lines like "Page 3" or "3 of 10" are removed; number-only lines are kept
    (``clean_pages`` removes the ones that are page numbers).
    """
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\ufeff", "").replace("\u00ad", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    cleaned: list[str] = []
    for line in text.split("\n"):
        line = "".join(char for char in line if char == "\t" or unicodedata.category(char) != "Cc")
        line = re.sub(r"[\t ]+", " ", line).strip()
        if line and not _PAGE_LABEL.fullmatch(line):
            cleaned.append(line)
        elif not line and cleaned and cleaned[-1] != "":
            cleaned.append("")
    return "\n".join(cleaned).strip()


def _bare_number(line: str) -> int | None:
    return int(line) if _BARE_NUMBER.fullmatch(line) else None


def _page_number_offsets(pages: list[tuple[Any, list[str]]], required_pages: int) -> set[int]:
    """Offsets (printed number - page index) shared by enough pages to be page numbers.

    A document whose pages print their own number has the same offset (often
    0) on most pages; a fee or serial number gives a different offset on each.
    """
    counts: Counter[int] = Counter()
    for page, lines in pages:
        if not isinstance(page, int):
            continue
        counts.update({number - page for line in lines if (number := _bare_number(line)) is not None})
    return {offset for offset, count in counts.items() if count >= required_pages}


def clean_pages(pages: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Normalize pages and remove lines repeated at page tops or bottoms.

    Only lines repeated near the top/bottom of at least 60% of pages are
    treated as headers/footers. Body text and all page numbers are retained in
    the returned records, except printed page-number-only lines: a number-only
    line is dropped when its value minus the page index is an offset shared by
    at least 60% of pages, so fees and serial numbers in tables are kept.
    """
    items = [dict(page) for page in pages]
    if not items:
        return []
    if any("page" not in item or "text" not in item for item in items):
        raise ValueError("every page record needs 'page' and 'text'")

    required_pages = max(2, math.ceil(len(items) * 0.6))
    normalized_pages: list[list[str]] = []
    for item in items:
        if not isinstance(item["text"], str):
            raise TypeError("page text must be a string")
        normalized_pages.append(normalize_text(item["text"]).splitlines())
    offsets = _page_number_offsets([(item["page"], lines) for item, lines in zip(items, normalized_pages)], required_pages)

    lines_by_page: list[list[str]] = []
    edge_frequency: Counter[str] = Counter()
    for item, normalized_lines in zip(items, normalized_pages, strict=True):
        page = item["page"]
        lines: list[str] = []
        for line in normalized_lines:
            number = _bare_number(line)
            if number is not None and isinstance(page, int) and number - page in offsets:
                continue  # printed page number
            if line or (lines and lines[-1]):
                lines.append(line)
        lines_by_page.append(lines)
        nonempty = [line for line in lines if line]
        for line in set(nonempty[:3] + nonempty[-3:]):
            edge_frequency[line.casefold()] += 1

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
