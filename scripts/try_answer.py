"""Day 0 Step 7: try answer() on the sample passages with a few questions.

Usage:  python scripts/try_answer.py
The questions live in this file (saved as UTF-8), so Nepali text is not mangled
the way it is when typed into a Windows terminal command.
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from src.generation.answer import answer_with_trace  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")  # print Nepali correctly on Windows

QUESTIONS = [
    "Which documents do I need to renew my driving license?",
    "लाइसेन्स नवीकरणका लागि कुन कागजात चाहिन्छ?",
    "License renew garna k k kagaj chahincha?",
    "Who won the cricket match yesterday?",
]

chunks = json.loads((REPO / "tests" / "fixtures" / "sample_chunks.json").read_text(encoding="utf-8"))
for q in QUESTIONS:
    resp, trace = answer_with_trace(q, chunks)
    print("Q:", q)
    print("reason:", trace["reason"], "| language:", trace["language"])
    print(json.dumps(resp, ensure_ascii=False, indent=2)[:700], "\n")
