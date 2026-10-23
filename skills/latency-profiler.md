---
name: latency-profiler
description: 'Measures latency per stage (search, answer, pipeline), memory, model load time, cold start. Reports p95 under 8s target.'
---
# latency-profiler Skill

Use when evaluating performance before deployment.

## Measurement points (from `docs/retrieval-score.md` and `docs/user-story-board.md` Day 6+)

- `search()` latency: encode embedding (`BAAI/bge-m3`) + Chroma query.
- `answer()` latency: LLM call (if real provider used) + guard check.
- `pipeline.py` total latency: `ask()` (search + answer + guard).
- Memory: embedding model load (`SentenceTransformer`) ~2.6 GB (`BAAI/bge-m3`).
- Cold start: first `search()` after `.venv` start (model download/load).

## Command

```bash
.\.venv\Scripts\python.exe -c "
import time
from src.retrieval.search import search
from src.generation.answer import answer
start = time.time()
chunks = search('test', k=5, service='palika_guide', municipality='Pokhara')
search_time = time.time() - start
print('Search latency (empty index):', round(search_time, 2), 's')
"
```

Expected (empty index): ~0.1–1.0 s (embedding load dominates first call; faster after load). Target (`docs/retrieval-score.md`): `max_latency_seconds: 8`.

## Evidence (current session)

`docs/results.md` line 418: `p95_s` unmeasured (`-`). No real evaluation run completed. Embedding smoke check (`scripts/smoke_test_embedding.py`) not completed (model download timeouts). `README.md` line 74 notes `p95_s` not measured.
