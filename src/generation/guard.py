"""Evidence guard (blueprint section 10.3): three independent reasons to refuse."""

import json
import re
import unicodedata

from .llm import complete
from .prompt import build_support_messages


def evidence_ok(chunks: list[dict], min_score: float) -> bool:
    """Guard v1: refuse when the best retrieved passage scores below the threshold."""
    if not chunks:
        return False
    best = max(float(c.get("score", 0.0)) for c in chunks)
    return best >= min_score


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = text.replace("‌", "").replace("‍", "")  # zero-width joiners
    text = re.sub(r"[\"'“”‘’]", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def quote_in_text(quote: str, text: str) -> bool:
    """True if the quote (or every piece of it around '...') appears in the text."""
    pieces = [p for p in re.split(r"\.\.\.|…", quote) if _norm(p)]
    body = _norm(text)
    return bool(pieces) and all(_norm(p) in body for p in pieces)


def citations_grounded(resp: dict, chunks: list[dict]) -> bool:
    """Every citation must point at a retrieved (source, page) and quote it verbatim."""
    if not resp.get("citations"):
        return False
    for cit in resp["citations"]:
        same_page = [c for c in chunks if c["source"] == cit["source"] and int(c["page"]) == int(cit["page"])]
        if not any(quote_in_text(cit["quote"], c["text"]) for c in same_page):
            return False
    return True


def support_check(draft: dict, chunks: list[dict]) -> tuple[bool, list[str]]:
    """Guard v2: a second LLM call asks 'is every claim supported?'"""
    raw = complete(build_support_messages(draft, chunks), json_mode=True)
    try:
        verdict = json.loads(raw)
        return bool(verdict.get("supported")), list(verdict.get("unsupported_claims", []))
    except (json.JSONDecodeError, AttributeError):
        return False, ["support check returned invalid JSON"]
