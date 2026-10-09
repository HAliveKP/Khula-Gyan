"""Small mock pipeline that keeps the AskResponse shape stable on Day 1."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


DISCLAIMER = "Demo only. Check the current requirements with the relevant official office before applying."


def ask(query: str, service: str | None = None) -> dict[str, Any]:
    """Return a schema-shaped demo response until retrieval and answer logic exist.

    The citation is deliberately labeled as a demo placeholder; it is not
    evidence and must never be presented as an official answer.
    """
    if not isinstance(query, str):
        raise TypeError("query must be a string")
    if service is not None and service not in {"driving_license", "citizenship", "passport"}:
        raise ValueError("service must be driving_license, citizenship, passport, or None")

    if not query.strip():
        return {
            "status": "not_found",
            "language": "en",
            "answer": "Enter a question to see the sample screen.",
            "checklist": {"documents": [], "fees": [], "steps": [], "where": ""},
            "citations": [],
            "confidence": "low",
            "disclaimer": DISCLAIMER,
        }

    return deepcopy(
        {
            "status": "answered",
            "language": "en",
            "answer": "This is a layout demo. Official documents are not connected yet, so this is not guidance for an application.",
            "checklist": {"documents": [], "fees": [], "steps": [], "where": ""},
            "citations": [
                {
                    "source": "DEMO ONLY — not an official document",
                    "page": 1,
                    "quote": "Placeholder citation used only to demonstrate the citation card.",
                }
            ],
            "confidence": "low",
            "disclaimer": DISCLAIMER,
        }
    )
