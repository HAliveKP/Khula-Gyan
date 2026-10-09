"""Day 0 check: one LLM call in Nepali and one in English, with JSON output.

Usage:  python scripts/smoke_test_llm.py
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.generation.llm import complete  # noqa: E402

QUESTIONS = [
    "सवारी चालक अनुमतिपत्र नवीकरण गर्न के गर्नुपर्छ? Answer in Nepali.",
    "In one sentence, what is a driving license renewal? Answer in English.",
]

for q in QUESTIONS:
    t0 = time.perf_counter()
    raw = complete(
        [{"role": "system", "content": 'Reply with JSON only: {"answer": "..."}'},
         {"role": "user", "content": q}],
        use_cache=False,
    )
    print(f"{time.perf_counter() - t0:.1f}s  {raw}")
    json.loads(raw)  # fails loudly if the provider ignored JSON mode
print("LLM smoke check passed. Judge the Nepali by eye: spelling, script, natural wording.")
