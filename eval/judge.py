"""LLM-as-judge for answer correctness and hallucination (blueprint section 11.3).

Always confirm the judge with a human spot-check of 20 answers before trusting it.
"""

import json

from src.generation.llm import complete
from src.generation.prompt import format_passages

JUDGE_SYSTEM = """You grade answers from a government-procedure assistant.
You get: the question, the EXPECTED facts (written by the team from the official page),
the retrieved passages, and the system's answer. The answer may be in Nepali, English or both;
judge meaning, not wording or language.

correct = true if the answer states (in any language) at least the main expected facts and
does not contradict them.
hallucinated = true if the answer or checklist states ANY fact that the passages do not support.
Reply with JSON only: {"correct": true/false, "hallucinated": true/false, "reason": "one sentence"}"""


def judge(question: str, expected: list[str], response: dict, chunks: list[dict]) -> dict:
    shown = {"answer": response["answer"], "checklist": response["checklist"]}
    user = (
        f"QUESTION: {question}\n"
        f"EXPECTED FACTS: {json.dumps(expected, ensure_ascii=False)}\n\n"
        f"{format_passages(chunks)}\n\n"
        f"SYSTEM ANSWER: {json.dumps(shown, ensure_ascii=False)}"
    )
    raw = complete([{"role": "system", "content": JUDGE_SYSTEM}, {"role": "user", "content": user}])
    try:
        out = json.loads(raw)
        return {"correct": bool(out.get("correct")), "hallucinated": bool(out.get("hallucinated")),
                "reason": str(out.get("reason", ""))}
    except json.JSONDecodeError:
        return {"correct": False, "hallucinated": False, "reason": "judge returned invalid JSON"}
