"""answer(query, chunks) -> AskResponse  (blueprint section 9.3).

answer() returns only the AskResponse, exactly as the contract says.
answer_with_trace() also returns WHY it answered or refused; the eval and the
UI's "why was this refused?" view use the trace. The schema stays unchanged.
"""

import json
import time

from .guard import citations_grounded, evidence_ok, support_check
from .language import detect_language
from .llm import complete
from .prompt import PROMPT_VERSION, build_messages, build_retry_messages
from .schema import disclaimer, not_found, validate_response
from .settings import setting

CONFIDENCE = {"high", "medium", "low"}


def _parse(raw: str) -> tuple[dict | None, str]:
    """Return (dict, '') or (None, problem). Tolerates ```json fences."""
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("{"):]
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        return None, "no JSON object found"
    try:
        data = json.loads(text[start:end + 1])
    except json.JSONDecodeError as err:
        return None, f"invalid JSON ({err.msg})"
    if not isinstance(data, dict) or data.get("status") not in {"answered", "not_found"}:
        return None, 'missing "status" ("answered" or "not_found")'
    return data, ""


def _as_list(value) -> list[str]:
    if isinstance(value, str):
        return [value] if value.strip() else []
    return [str(v) for v in (value or []) if str(v).strip()]


def _to_response(draft: dict, chunks: list[dict], language: str) -> dict:
    """Turn the model's draft (citations by passage number) into an AskResponse."""
    checklist = draft.get("checklist") or {}
    citations = []
    for cit in draft.get("citations") or []:
        try:
            chunk = chunks[int(cit["passage"]) - 1]
        except (KeyError, ValueError, TypeError, IndexError):
            continue  # citation points at a passage that does not exist
        citations.append({"source": chunk["source"], "page": int(chunk["page"]),
                          "quote": str(cit.get("quote", "")).strip()})
    conf = draft.get("confidence")
    return {
        "status": "answered",
        "language": language,
        "answer": str(draft.get("answer", "")).strip(),
        "checklist": {
            "documents": _as_list(checklist.get("documents")),
            "fees": _as_list(checklist.get("fees")),
            "steps": _as_list(checklist.get("steps")),
            "where": str(checklist.get("where") or ""),
        },
        "citations": citations,
        "confidence": conf if conf in CONFIDENCE else "medium",
        "disclaimer": disclaimer(language),
    }


def answer_with_trace(query: str, chunks: list[dict], check_support: bool | None = None) -> tuple[dict, dict]:
    t0 = time.perf_counter()
    language = detect_language(query)
    passages = chunks[: setting("final_k", 5)]
    min_score = setting("guard_min_score", 0.0)
    if check_support is None:
        check_support = setting("support_check", False)
    trace = {"prompt_version": PROMPT_VERSION, "language": language, "reason": "",
             "top_score": max((float(c.get("score", 0)) for c in passages), default=None),
             "raw": "", "unsupported_claims": []}

    def refuse(reason: str) -> tuple[dict, dict]:
        trace["reason"] = reason
        trace["seconds"] = round(time.perf_counter() - t0, 2)
        return not_found(language), trace

    if not evidence_ok(passages, min_score):
        return refuse(f"guard_score: best score {trace['top_score']} < {min_score}")

    messages = build_messages(query, passages, language)
    raw = complete(messages)
    draft, problem = _parse(raw)
    if draft is None:  # one retry only
        raw = complete(build_retry_messages(messages, raw, problem))
        draft, problem = _parse(raw)
    trace["raw"] = raw
    if draft is None:
        return refuse(f"invalid_output: {problem}")
    if draft["status"] == "not_found":
        return refuse("model_not_found")

    resp = _to_response(draft, passages, language)
    errors = validate_response(resp)
    if errors:
        return refuse("schema: " + "; ".join(errors[:3]))
    if not resp["answer"] or not resp["citations"]:
        return refuse("no_citations")
    if not citations_grounded(resp, passages):
        return refuse("ungrounded_citation")
    if check_support:
        ok, claims = support_check(resp, passages)
        trace["unsupported_claims"] = claims
        if not ok:
            return refuse("support_check_failed")

    trace["reason"] = "answered"
    trace["seconds"] = round(time.perf_counter() - t0, 2)
    return resp, trace


def answer(query: str, chunks: list[dict]) -> dict:
    """Return an AskResponse (9.4). Refuses if evidence is weak."""
    return answer_with_trace(query, chunks)[0]
