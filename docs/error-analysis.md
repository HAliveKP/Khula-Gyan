# Error analysis — Palika Guide (2026-10-23)

No civic index exists (`chroma_db/` contains only previous attempt; 0 eligible civic chunks). No verified evaluation against indexed charter pages has been run. The categories below are defined per `eval/run_eval.py` `categorize()` and `docs/history/retrieval-score.md`.

## Failure categories (defined; not measured against real index)

| Category | Definition | Current state |
|---|---|---|
| `retrieval_miss` | Chunk with expected `must_cite` (`source` + `page`) not found in `search()` top-5 results. | Theoretical: without index, `search()` always returns `[]`; any verified question would show `hit=0`. |
| `guard_error: guard_score` | `guard_min_score` (configured 0.35, uncalibrated) blocks a valid retrieval. | Theoretical: threshold not calibrated; `eval/sweep_threshold.py` requires real evaluation data. |
| `guard_error: wrong_municipality` | `service="palika_guide"` but question names municipality with no indexed charter, or names none (`ask()` returns `not_found`). | Verified working: `pipeline.py` lines 159-165; `demo_script.py` shows refusal (`palika_guide` + no municipality) and wrong-municipality (`Lalitpur` — no charter fetched/indexed). |
| `generation_error: wrong/incomplete answer` | LLM produces answer not supported by chunks (`keyword_correct()` checks at least 50% of expected facts present). | Theoretical for real LLM; with `fake-llm`, `keyword_correct()` returns `False` (by design — fake generator returns non-realistic answers). |
| `generation_error: hallucination` | LLM introduces facts not in retrieved chunks (`judge()` checks). | Theoretical; `judge()` requires `judge.py` module (not fully verified). |

## Extraction failures found and fixed (added 2026-10-25)

*Update 2026-10-25:* the table above covers only answer-time categories. Processing the 12 charter files on aash-crest01's machine on 2026-10-15 found these `source/extraction` failures. Each was fixed with a regression test in `tests/test_ingest_text_fixes.py`, merged via PR #20 (`f879fa5`). Page-by-page checks against rendered page images are in `docs/extraction-notes.md`. These are counts from document processing, not evaluation metrics.

| Failure | Where seen | Effect before the fix | Fix (commit) |
|---|---|---|---|
| Wrong ToUnicode glyph map in an embedded Kalimati subset with no GSUB table | `palika_ghorahi.pdf`; some Bharatpur files | Words with "ि" or reph came out wrong, e.g. image `गर्ने व्यक्तिको नागरिकता` read `गने व्र्णिको नागररकता` (Ghorahi page 2) | Glyphs read from a Kalimati 1.20 reference (`src/ingest/font_reference.json`, built by `scripts/build_font_reference.py`), used only when font family, glyph count and every Devanagari cmap glyph agree (`47d3851`; its message says other Bharatpur charters gain `दर्ता`, `सम्बन्धित`, `कार्यालय` and Pokhara output is unchanged) |
| Kalimati ASCII digit glyphs drawn as Devanagari numerals | `palika_ghorahi.pdf` pages 15-16; `palika_hetauda_2083_84.pdf` page 1 | Fees read `1००००` for `१००००`, `200` for `२००`; Hetauda title `२०८3/८4` | Reference also supplies the digit glyphs (`880998c`) |
| Legacy Preeti / Kantipur / PCS Nepali font text | `palika_hetauda_2083_84.pdf` (almost all text); parts of Pokhara FY 2075/76 and Bharatpur revenue | Text extracted as Latin letters; 22 of 24 Hetauda pages were marked unusable | Spans in those fonts converted to Unicode (`627eaa1`) |
| Number-only lines deleted as page numbers | All charters; seen on `palika_ghorahi.pdf` pages 1 and 8 | Fee cells such as `४५०`, `२५०००`, `९००`, `७५०` and table serial numbers were removed by `src/ingest/clean.py` | A number-only line is removed only when its value minus the page index is an offset shared by at least 60% of pages (`4d6e8e9`) |
| Website menus, headers and footers mixed into HTML charter text | `palika_dhulikhel.html` | Menu and news text of the shared Drupal site template went into the extracted page | nav/header/footer/aside/form, news ticker, sidebar, tabs and breadcrumb skipped; Dhulikhel lost 53 menu/news words and kept all service rows (`d9b1fbf`) |

Not re-checked here: the feasibility check saw wrong glyph mapping in `palika_pokhara_2075.pdf` (e.g. `घर` read as `घय`); `47d3851` did not change Pokhara output. Not fixed: `palika_pokhara_2075.pdf` keeps its private-use `U+F031` serial-number boxes; in `palika_bharatpur_revenue.pdf`, text the author typed in Preeti (`IEE`/`EIA`) is reproduced as drawn (`docs/extraction-notes.md`).

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
4. Fix top failures: improve prompt (`src/generation/prompt.py`); calibrate `guard_min_score` (`eval/sweep_threshold.py`); fix extraction (`docs/history/next-steps.md` Day 5); add adversarial tests.
