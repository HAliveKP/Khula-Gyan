# Error analysis — Palika Guide (2026-10-23)

No civic index exists (`chroma_db/` contains only previous attempt; 0 eligible civic chunks). No verified evaluation against indexed charter pages has been run. The categories below are defined per `eval/run_eval.py` `categorize()` and `docs/retrieval-score.md`.

## Failure categories (defined; not measured against real index)

| Category | Definition | Current state |
|---|---|---|
| `retrieval_miss` | Chunk with expected `must_cite` (`source` + `page`) not found in `search()` top-5 results. | Theoretical: without index, `search()` always returns `[]`; any verified question would show `hit=0`. |
| `guard_error: guard_score` | `guard_min_score` (configured 0.35, uncalibrated) blocks a valid retrieval. | Theoretical: threshold not calibrated; `eval/sweep_threshold.py` requires real evaluation data. |
| `guard_error: wrong_municipality` | `service="palika_guide"` but question names municipality with no indexed charter, or names none (`ask()` returns `not_found`). | Verified working: `pipeline.py` lines 159-165; `demo_script.py` shows refusal (`palika_guide` + no municipality) and wrong-municipality (`Lalitpur` — no charter fetched/indexed). |
| `generation_error: wrong/incomplete answer` | LLM produces answer not supported by chunks (`keyword_correct()` checks at least 50% of expected facts present). | Theoretical for real LLM; with `fake-llm`, `keyword_correct()` returns `False` (by design — fake generator returns non-realistic answers). |
| `generation_error: hallucination` | LLM introduces facts not in retrieved chunks (`judge()` checks). | Theoretical; `judge()` requires `judge.py` module (not fully verified). |

## Evidence (verified commands, 2026-10-23)

- `pytest -q --basetemp=.pytest_tmp` → 95 passed, 7 skipped.
- `.\.venv\Scripts\python.exe eval\run_eval.py --fake-llm --use-service-filter --use-municipality-filter --include-unverified --note "plumbing" --no-write` → 40 records; all verified palika questions `not_found`; metrics `-`; no synthetic metrics added to `docs/results.md`.
- `scripts/fetch_sources.py --include-unclear` → 1 fetched; 12 palika sources blocked (`WinError 10060`/`10061`).
- `scripts/build_index.py` → `No source passed both open-license and civic-answer-evidence checks; no Chroma index was built.`
- `chroma_db/` exists (previous index file, 188416 bytes) but `collection.count()` = 0 (no civic chunks indexed in this run). Confirmed by `ls chroma_db/` and `python -c` import of `src.retrieval.search`.

## Next steps for error analysis (requires indexed charter + verified evaluation)

Once index exists (`build_index.py` produces `collection.count() > 0`) and verified questions (`eval/questions.jsonl` with `verified=true`, `must_cite` filled) are evaluated with a working real LLM:

1. Run `eval/run_eval.py --judge --use-service-filter --use-municipality-filter --note "Day 4 baseline"`.
2. Record metrics (`hit@5`, `citation_acc`, `correct`, `hallucination`, `correct_refusal`, `false_refusal`, `p95_s`) in `docs/results.md` (only real numbers).
3. List top 10 failures with categories (this file) based on `rec["category"]` from `run_eval.py`.
4. Fix top failures: improve prompt (`src/generation/prompt.py`); calibrate `guard_min_score` (`eval/sweep_threshold.py`); fix extraction (`docs/next-steps.md` Day 5); add adversarial tests.
