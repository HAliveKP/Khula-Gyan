"""Connect search and answer functions while enforcing the AskResponse shape."""

from __future__ import annotations

from importlib import import_module
from typing import Any


DISCLAIMER = "Verify procedures with the relevant official office. This tool does not provide legal advice."
RESPONSE_FIELDS = {"status", "language", "answer", "checklist", "citations", "confidence", "disclaimer"}
CHECKLIST_FIELDS = {"documents", "fees", "steps", "where"}
CITATION_FIELDS = {"source", "page", "quote"}


def _not_found(message: str) -> dict[str, Any]:
    return {
        "status": "not_found",
        "language": "en",
        "answer": message,
        "checklist": {"documents": [], "fees": [], "steps": [], "where": ""},
        "citations": [],
        "confidence": "low",
        "disclaimer": DISCLAIMER,
    }


def _valid_response(response: Any) -> bool:
    if not isinstance(response, dict) or set(response) != RESPONSE_FIELDS:
        return False
    if response["status"] not in {"answered", "not_found"}:
        return False
    if response["language"] not in {"ne", "en", "mixed"}:
        return False
    if not isinstance(response["answer"], str) or not isinstance(response["disclaimer"], str):
        return False
    if response["confidence"] not in {"high", "medium", "low"}:
        return False
    checklist = response["checklist"]
    if not isinstance(checklist, dict) or set(checklist) != CHECKLIST_FIELDS:
        return False
    if not all(isinstance(checklist[key], list) and all(isinstance(value, str) for value in checklist[key]) for key in ("documents", "fees", "steps")):
        return False
    if not isinstance(checklist["where"], str) or not isinstance(response["citations"], list):
        return False
    for citation in response["citations"]:
        if not isinstance(citation, dict) or set(citation) != CITATION_FIELDS:
            return False
        if not isinstance(citation["source"], str) or not isinstance(citation["quote"], str):
            return False
        if isinstance(citation["page"], bool) or not isinstance(citation["page"], int) or citation["page"] < 1:
            return False
    return True


def ask(query: str, service: str | None = None) -> dict[str, Any]:
    """Run ``search(query, k=5, service)`` then ``answer(query, chunks)``.

    Member 2's ``src.retrieval.search`` and Member 3's
    ``src.generation.answer`` are loaded when present. Until both arrive, this
    function returns an honest ``not_found`` response without demo citations.
    """
    if not isinstance(query, str):
        raise TypeError("query must be a string")
    if service is not None and service not in {"driving_license", "citizenship", "passport"}:
        raise ValueError("service must be driving_license, citizenship, passport, or None")
    if not query.strip():
        return _not_found("Enter a question to search the available official sources.")

    try:
        search_fn = import_module("src.retrieval.search").search
        answer_fn = import_module("src.generation.answer").answer
    except ModuleNotFoundError as exc:
        if exc.name in {"src.retrieval.search", "src.generation.answer"}:
            return _not_found("Search and answer components are not connected yet. No official answer was generated.")
        raise RuntimeError("A required search or answer dependency could not be loaded.") from exc
    except AttributeError as exc:
        raise RuntimeError("Search and answer modules must expose search() and answer().") from exc

    chunks = search_fn(query, k=5, service=service)
    if not isinstance(chunks, list):
        raise RuntimeError("search() must return a list of cited chunks.")
    if not chunks:
        return _not_found("The available official sources do not contain a matching passage.")

    response = answer_fn(query, chunks)
    if not _valid_response(response):
        return _not_found("The answer component returned an invalid response. Please try again later.")
    return response
