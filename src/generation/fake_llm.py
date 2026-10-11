"""A no-key stand-in for the LLM (set LLM_PROVIDER=fake in .env).

It answers by quoting the first sentence of passage 1, so the whole pipeline,
UI and eval can run before the team has an API key. Never use it for real numbers.
"""

import json
import re


def fake_complete(messages: list[dict]) -> str:
    system = messages[0]["content"]
    user = messages[-1]["content"]
    if "unsupported claims" in system:
        return json.dumps({"supported": True, "unsupported_claims": []})
    if "grade" in system.lower():
        return json.dumps({"correct": True, "hallucinated": False, "reason": "fake judge"})
    match = re.search(r'<passage n="1"[^>]*>\n(.*?)\n</passage>', user, re.S)
    if not match:
        return json.dumps({"status": "not_found"})
    first_sentence = re.split(r"(?<=[.।])\s", match.group(1).strip())[0]
    quote = " ".join(first_sentence.split()[:20])
    return json.dumps({
        "status": "answered",
        "answer": first_sentence,
        "checklist": {"documents": [], "fees": [], "steps": [], "where": ""},
        "citations": [{"passage": 1, "quote": quote}],
        "confidence": "medium",
    }, ensure_ascii=False)
