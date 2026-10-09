"""Validate AskResponse dicts and build the standard refusal."""

import json
from functools import lru_cache

from jsonschema import Draft202012Validator

from .settings import REPO_ROOT

SCHEMA_PATH = REPO_ROOT / "docs" / "ask-response.schema.json"

DISCLAIMER = {
    "en": "This explains official procedures only, not legal advice. Verify with the official office before submitting.",
    # Ask Member 1 to check this Nepali wording.
    "ne": "यो आधिकारिक प्रक्रियाको जानकारी मात्र हो, कानुनी सल्लाह होइन। आवेदन दिनुअघि सम्बन्धित कार्यालयमा पुष्टि गर्नुहोस्।",
}

NOT_FOUND_TEXT = {
    "en": "Not found in official sources. Please check with the relevant government office or its official website.",
    "ne": "आधिकारिक स्रोतहरूमा भेटिएन। कृपया सम्बन्धित सरकारी कार्यालय वा आधिकारिक वेबसाइटमा सोध्नुहोस्।",
}


def _pick(texts: dict, language: str) -> str:
    if language == "mixed":
        return texts["ne"] + "\n" + texts["en"]
    return texts.get(language, texts["en"])


@lru_cache(maxsize=1)
def _validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def validate_response(resp: dict) -> list[str]:
    """Return a list of problems; an empty list means the response is valid."""
    errors = []
    for e in _validator().iter_errors(resp):
        where = "/".join(str(p) for p in e.path) or "(top level)"
        errors.append(f"{where}: {e.message}")
    return errors


def disclaimer(language: str) -> str:
    return _pick(DISCLAIMER, language)


def not_found(language: str = "en") -> dict:
    """The one refusal shape every part of the app uses."""
    return {
        "status": "not_found",
        "language": language,
        "answer": _pick(NOT_FOUND_TEXT, language),
        "checklist": {"documents": [], "fees": [], "steps": [], "where": ""},
        "citations": [],
        "confidence": "low",
        "disclaimer": disclaimer(language),
    }
