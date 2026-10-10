"""Run with:  python -m pytest -q"""

import json
from pathlib import Path

import pytest

from src.generation import answer as answer_mod
from src.generation import guard as guard_mod
from src.generation.answer import answer, answer_with_trace
from src.generation.language import detect_language
from src.generation.schema import not_found, validate_response

FIX = Path(__file__).parent / "fixtures"
CHUNKS = json.loads((FIX / "sample_chunks.json").read_text(encoding="utf-8"))


def fake_llm(reply: dict | str):
    text = reply if isinstance(reply, str) else json.dumps(reply, ensure_ascii=False)
    return lambda messages, **kw: text


GOOD = {"status": "answered",
        "answer": "Submit a copy of the citizenship certificate, the old license and a medical certificate.",
        "checklist": {"documents": ["citizenship certificate copy", "old driving license", "medical certificate"],
                      "fees": [], "steps": [], "where": ""},
        "citations": [{"passage": 1, "quote": "the applicant must submit a copy of the citizenship certificate"}],
        "confidence": "high"}


@pytest.fixture(autouse=True)
def no_threshold(monkeypatch):
    monkeypatch.setattr(answer_mod, "setting",
                        lambda name, default=None: {"final_k": 5, "guard_min_score": 0.35,
                                                    "support_check": False}.get(name, default))


def test_fixtures_match_schema():
    for name in ("sample_answered.json", "sample_not_found.json"):
        assert validate_response(json.loads((FIX / name).read_text(encoding="utf-8"))) == []


def test_not_found_is_valid_in_every_language():
    for lang in ("ne", "en", "mixed"):
        assert validate_response(not_found(lang)) == []


def test_good_answer_passes(monkeypatch):
    monkeypatch.setattr(answer_mod, "complete", fake_llm(GOOD))
    resp, trace = answer_with_trace("Which documents do I need to renew my license?", CHUNKS)
    assert trace["reason"] == "answered"
    assert resp["citations"][0] == {"source": "mock_dl_renewal.pdf", "page": 2,
                                    "quote": GOOD["citations"][0]["quote"]}
    assert validate_response(resp) == []


def test_made_up_quote_is_refused(monkeypatch):
    bad = dict(GOOD, citations=[{"passage": 1, "quote": "the fee is 500 rupees"}])
    monkeypatch.setattr(answer_mod, "complete", fake_llm(bad))
    resp, trace = answer_with_trace("What is the fee?", CHUNKS)
    assert resp["status"] == "not_found" and trace["reason"] == "ungrounded_citation"


def test_citation_to_missing_passage_is_refused(monkeypatch):
    bad = dict(GOOD, citations=[{"passage": 9, "quote": "anything"}])
    monkeypatch.setattr(answer_mod, "complete", fake_llm(bad))
    assert answer("Which documents?", CHUNKS)["status"] == "not_found"


def test_weak_evidence_skips_llm(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("LLM must not be called when evidence is weak")
    monkeypatch.setattr(answer_mod, "complete", boom)
    weak = [dict(c, score=0.1) for c in CHUNKS]
    resp, trace = answer_with_trace("Which documents?", weak)
    assert resp["status"] == "not_found" and trace["reason"].startswith("guard_score")


def test_invalid_json_retries_once_then_refuses(monkeypatch):
    calls = []
    monkeypatch.setattr(answer_mod, "complete", lambda m, **k: calls.append(1) or "sorry, here you go")
    resp, trace = answer_with_trace("Which documents?", CHUNKS)
    assert len(calls) == 2 and resp["status"] == "not_found" and trace["reason"].startswith("invalid_output")


def test_retry_can_recover(monkeypatch):
    replies = iter(["not json", json.dumps(GOOD)])
    monkeypatch.setattr(answer_mod, "complete", lambda m, **k: next(replies))
    assert answer("Which documents?", CHUNKS)["status"] == "answered"


def test_model_not_found_is_respected(monkeypatch):
    monkeypatch.setattr(answer_mod, "complete", fake_llm({"status": "not_found"}))
    assert answer("Who won the football match?", CHUNKS)["status"] == "not_found"


def test_support_check_blocks(monkeypatch):
    monkeypatch.setattr(answer_mod, "complete", fake_llm(GOOD))
    monkeypatch.setattr(guard_mod, "complete", fake_llm({"supported": False, "unsupported_claims": ["x"]}))
    resp, trace = answer_with_trace("Which documents?", CHUNKS, check_support=True)
    assert resp["status"] == "not_found" and trace["reason"] == "support_check_failed"


def test_nepali_quote_with_ellipsis(monkeypatch):
    nep = dict(GOOD, citations=[{"passage": 2, "quote": "नागरिकता प्रमाणपत्रको प्रतिलिपि ... पेस गर्नुपर्छ"}])
    monkeypatch.setattr(answer_mod, "complete", fake_llm(nep))
    resp = answer("लाइसेन्स नवीकरणका लागि कुन कागजात चाहिन्छ?", CHUNKS)
    assert resp["status"] == "answered" and resp["language"] == "ne"


def test_language_detection():
    assert detect_language("लाइसेन्स नवीकरणका लागि कुन कागजात चाहिन्छ?") == "ne"
    assert detect_language("How do I renew my driving license?") == "en"
    assert detect_language("License renew garna k k kagaj chahincha?") == "mixed"
    assert detect_language("Driving license नवीकरण कसरी गर्ने?") == "mixed"
