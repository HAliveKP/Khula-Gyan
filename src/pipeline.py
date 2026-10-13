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


def _extract_municipality_from_query(query: str) -> str | None:
    """Best-effort extraction of municipality name from query.
    Returns the municipality name if found, else None.
    This is a simple heuristic; the UI selector is the primary source.
    """
    # Common Nepali municipality names that might appear in queries
    municipalities = [
        "kathmandu", "lalitpur", "bhaktapur", "pokhara", "biratnagar", "birgunj",
        "dharan", "hetauda", "butwal", "dhangadhi", "mahendranagar", "nepalgunj",
        "janakpur", "dhulikhel", "banepa", "panauti", "kirtipur", "madhyapur",
        "thimi", "gokarneshwor", "chandragiri", "tokha", "nagarjun", "dakshinkali",
        "kageshwari", "manohara", "suryabinayak", "godawari", "konjyosome",
        "mahalaxmi", "lalitpur", "kathmandu", "budhanilkantha", "dakshinkali",
        "shankharapur", "kageshwari", "manohara", "tarakeshwor", "dakshinkali",
    ]
    query_lower = query.lower()
    for mun in municipalities:
        if mun in query_lower:
            return mun.title()
    return None


def ask(query: str, service: str | None = None, municipality: str | None = None) -> dict[str, Any]:
    """Run ``search(query, k=5, service, municipality)`` then ``answer(query, chunks)``.

    Member 2's ``src.retrieval.search`` and Member 3's
    ``src.generation.answer`` are loaded when present. Until both arrive, this
    function returns an honest ``not_found`` response without demo citations.

    Safety: If the question names a municipality with no indexed charter,
    or names none and the municipality selector is empty, return not_found
    or a clarification response; never answer from another municipality's chunks.
    """
    if not isinstance(query, str):
        raise TypeError("query must be a string")
    if service is not None and service not in {"driving_license", "citizenship", "passport", "palika_guide"}:
        raise ValueError("service must be driving_license, citizenship, passport, palika_guide, or None")
    if municipality is not None and not isinstance(municipality, str):
        raise TypeError("municipality must be a string or None")
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

    # Wrong/missing municipality guard
    # If palika_guide service but no municipality specified, ask for clarification
    if service == "palika_guide" and not municipality:
        # Try to extract from query as fallback
        extracted = _extract_municipality_from_query(query)
        if extracted:
            municipality = extracted
        else:
            return _not_found("Please specify which municipality (पालिका) you are asking about. Use the municipality selector or include the municipality name in your question.")

    chunks = search_fn(query, k=5, service=service, municipality=municipality)
    if not isinstance(chunks, list):
        raise RuntimeError("search() must return a list of cited chunks.")
    if not chunks:
        msg = "The available official sources do not contain a matching passage."
        if municipality:
            msg += f" No indexed charter found for {municipality}."
        return _not_found(msg)

    response = answer_fn(query, chunks)
    if not _valid_response(response):
        return _not_found("The answer component returned an invalid response. Please try again later.")
    return response