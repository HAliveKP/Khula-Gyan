"""Day 0 check: every API key works, and the model answers JSON in Nepali and English.

Usage:  python scripts/smoke_test_llm.py
"""

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.generation.llm import _make_client, api_keys, complete  # noqa: E402

MESSAGES = [{"role": "system", "content": 'Reply with JSON only: {"answer": "..."}'}]
QUESTIONS = [
    "सवारी चालक अनुमतिपत्र नवीकरण गर्न के गर्नुपर्छ? Answer in Nepali.",
    "In one sentence, what is a driving license renewal? Answer in English.",
]

# 1. Each key on its own, so a bad key is named instead of hidden by the others.
model, base_url = os.getenv("LLM_MODEL", ""), os.getenv("LLM_BASE_URL") or None
keys = api_keys()
print(f"Model: {model}   Keys found: {len(keys)}")
bad = 0
for idx, key in enumerate(keys, start=1):
    try:
        _make_client(key, base_url).chat.completions.create(
            model=model, messages=MESSAGES + [{"role": "user", "content": "Say ok"}], max_tokens=20)
        print(f"  key #{idx}: OK")
    except Exception as err:
        bad += 1
        print(f"  key #{idx}: FAILED ({type(err).__name__}, status {getattr(err, 'status_code', None)})")

# 2. Real questions through the normal client (uses the key pool).
for q in QUESTIONS:
    t0 = time.perf_counter()
    raw = complete(MESSAGES + [{"role": "user", "content": q}], use_cache=False)
    print(f"{time.perf_counter() - t0:.1f}s  {raw}")
    json.loads(raw)  # fails loudly if the provider ignored JSON mode

if bad:
    print(f"LLM smoke check passed, but {bad} key(s) failed. Fix or remove them from LLM_API_KEYS.")
else:
    print("LLM smoke check passed. Judge the Nepali by eye: spelling, script, natural wording.")
