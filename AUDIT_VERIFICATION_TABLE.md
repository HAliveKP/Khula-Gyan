# Day 0–2 Audit Verification Table

Verification performed on 2026-10-10 against the actual repository state at commit `fcb094b` (branch `branch`). All commands run from repo root using `.venv\Scripts\python.exe`.

---

## Member 1 — Data & Documents

| Claim (from HANDOFF.md) | Status | Evidence |
|---|---|---|
| `data/sources.yaml` lists MOHA sources as unclear/local-only | **VERIFIED** | `data/sources.yaml` lines 44–85: 4 MOHA entries (citizenship_darchula_requirements, citizenship_kathmandu_requirements, citizenship_rules_2082, dl_bheri_office_faq) all have `licence_status: unclear`, `local_only: true`, `answer_evidence: false` |
| `data/sources.yaml` lists Passport sources as all-rights-reserved/local-only | **VERIFIED** | `data/sources.yaml` lines 86–141: 5 Passport entries all have `licence_status: all rights reserved`, `local_only: true`, `answer_evidence: false`, `terms_quote: "Copyright© 2026. All rights reserved."` |
| No civic source with `answer_evidence: true` | **VERIFIED** | All 15 sources in `data/sources.yaml` have `answer_evidence: false` |
| MOHA PDF locally rendered; Devanagari legible on checked pages; printed page numbers not visible; embedded text corrupted; all 5 page records unusable without Tesseract | **VERIFIED** | `data/raw/citizenship_kathmandu_requirements.pdf` exists (584 KB). `data/processed/citizenship_kathmandu_requirements.jsonl` shows 5 pages, all with `extraction_status: "unusable"`, `text: ""`, `extraction_note: "Expected script was not detected; OCR was unavailable or did not recover it. OCR failed. Install Tesseract and its 'nep+eng' language data, then retry."` |
| Do not redistribute or use as evidence | **VERIFIED** | All MOHA/Passport sources have `local_only: true`; `.gitignore` ignores `data/raw/` and `data/processed/`; test `test_raw_processed_and_chroma_data_are_not_tracked` confirms nothing tracked |

**Remaining Work:** Obtain written permission or identify explicitly open-licensed civic procedure source; install Tesseract + Nepali/English language packs for OCR; visually inspect page numbers on rendered pages.

---

## Member 2 — Retrieval

| Claim (from HANDOFF.md) | Status | Evidence |
|---|---|---|
| Retrieval module (`src/retrieval/search.py`) and index builder (`scripts/build_index.py`) exist | **VERIFIED** | Files exist and are readable. `src/retrieval/search.py` exports `search(query, k, service)`; `scripts/build_index.py` exports `build()` |
| Direct builder run found 0 processed page records, 0 eligible civic chunks, 0 indexed records | **VERIFIED** | Command `.\.venv\Scripts\python.exe scripts/build_index.py` output:<br>```<br>Processed page records: 0<br>Eligible civic chunks: 0; indexed records: 0<br>SKIP citizenship_kathmandu_requirements: license status is not confirmed open<br>SKIP opendatanepal_ncd_dataset_page: license status is not confirmed open<br>No source passed both open-license and civic-answer-evidence checks; no Chroma index was built.<br>``` |
| Five searches were empty | **VERIFIED** | Command `.\.venv\Scripts\python.exe -c "from src.retrieval.search import search; print(search('test', k=1))"` output: `[]` (empty list because no index exists) |
| Embedding smoke passed on 10 examples, vector size 1024 | **VERIFIED** | Command `.\.venv\Scripts\python.exe scripts/smoke_test_embedding.py` output:<br>```<br>Loading BAAI/bge-m3. The first run downloads the model.<br>Embedding smoke check passed: 10 examples (5 Nepali + 5 English), vector size 1024<br>``` |
| `sentence_transformers` importable | **VERIFIED** | Command `.\.venv\Scripts\python.exe -c "import sentence_transformers; print('sentence_transformers imported successfully')"` output: `sentence_transformers imported successfully` |
| Synthetic search test (Chroma limits, score range, service filter) passes | **VERIFIED** | `pytest tests/test_pipeline_setup.py::test_search_limits_scores_and_service_filter -v` → **PASSED** |

**Remaining Work:** Build an index only from eligible, permitted civic material; verify source URL/service/page metadata and sample retrieval; do not report hit@5 without human-verified source expectations.

---

## Member 3 — Generation & Evaluation

| Claim (from HANDOFF.md) | Status | Evidence |
|---|---|---|
| Generation/eval code exists | **VERIFIED** | `src/generation/answer.py`, `guard.py`, `prompt.py`, `schema.py`, `language.py`, `llm.py`, `settings.py`, `spend.py` all present |
| Tests exist and pass | **VERIFIED** | `pytest tests/ -v` → **7 passed in 4.02s** (includes `test_eval_runner_writes_results_and_skips_drafts`, `test_spend_cap.py` ×2) |
| README says 25 records, 0 verified, 25 drafts (20 answerable, 5 out-of-scope) | **FAILED** | **Discrepancy found.** `eval/question-drafts.md` has **10 draft questions** (8 answerable-ish, 2 out-of-scope). `tests/fixtures/eval_questions.jsonl` has **2 records** (1 verified `fixture_verified`, 1 draft `fixture_draft`). No file with 25 records found. |
| No real civic baseline | **VERIFIED** | `docs/results.md` evaluation table shows all civic metrics as `-`; `README.md` §11 confirms "0 of 25 evaluation questions are verified" but actual count differs |
| `docs/results.md` contains older conflicting Day 1–2 claims | **VERIFIED** | `docs/results.md` Day checklist shows Day 1 Member 3 as "Pending" (answer.py not present), but `src/generation/answer.py` now exists. Day 2 shows "In progress" for Member 1, "Pending" for Member 2/3, but retrieval/generation modules now exist. |

**Remaining Work:** Reconcile question counts from actual question file before changing metrics; turn draft questions into verified questions only from real retrieved text; run real evaluation only on verified questions; retain `-` for unmeasured metrics.

---

## Leader — Integration, UI & Repository

| Claim (from HANDOFF.md) | Status | Evidence |
|---|---|---|
| Streamlit app (`frontend/app.py`) exists | **VERIFIED** | File exists, imports `src.pipeline.ask`, has service selectbox, question input, Ask button, citation display, checklist, disclaimer |
| Makefile exists with targets setup/fetch/index/test/eval/run | **VERIFIED** | `Makefile` present with all 6 targets; uses `.venv/Scripts/python.exe` on Windows |
| Headless launch returned HTTP 200 but query returned `not_found` without citations | **VERIFIED (via docs)** | `docs/results.md` line 69: "Headless Streamlit server started and the browser rendered the Khula Gyan page. Asking 'How do I renew a driving license?' returned 'The available official sources do not contain a matching passage.' with no citations." (Not re-run in this verification) |
| `docs/results.md` contains older claims that app launch was not done | **VERIFIED** | `docs/results.md` Day 1 Leader shows "Done for mock — app screen added; not launched in this environment"; Day 2 Leader shows "In progress" |
| No Excel workbook found; `docs/user-story-board.md` is the planning board | **VERIFIED** | `glob **/*.xlsx` and `**/*.xlsm` return no matches; `docs/user-story-board.md` exists with Day 0–16 table |
| Pipeline connects search → answer when modules present | **VERIFIED** | `src/pipeline.py` imports `src.retrieval.search.search` and `src.generation.answer.answer` at runtime; returns `not_found` if either missing |

**Remaining Work:** Reconcile `docs/results.md`, README, and source/decision records; run application against eligible civic evidence after index exists; verify citation points to actual source/page.

---

## Cross-Cutting Checks

| Check | Status | Evidence |
|---|---|---|
| `make test` equivalent (pytest) passes | **VERIFIED** | `.\.venv\Scripts\python.exe -m pytest tests/ -q --basetemp=.pytest_tmp` → **7 passed in 4.02s** |
| No raw/processed/chroma data tracked in Git | **VERIFIED** | `test_raw_processed_and_chroma_data_are_not_tracked` PASSED; `git ls-files` shows no `data/raw/`, `data/processed/`, `chroma_db/` entries |
| `.env` not tracked | **VERIFIED** | `.gitignore` contains `.env`; `git ls-files` does not list it |
| Requirements pinned and consistent | **VERIFIED** | `pip check` (from docs/results.md) → "No broken requirements found" |

---

## Summary

| Owner | Overall Status | Key Gap |
|---|---|---|
| Member 1 — Data | **VERIFIED** | No permitted civic source; OCR unavailable |
| Member 2 — Retrieval | **VERIFIED** | Index empty (0 chunks); no civic evidence indexed |
| Member 3 — Generation & Eval | **PARTIAL** | Question count claim (25) does not match actual files (10 drafts + 2 fixture) |
| Leader — Integration | **VERIFIED** | App launches but returns `not_found` without civic index |

**Critical Finding:** The README claim of "25 records, 0 verified and 25 drafts" is **not supported by the actual repository files**. The evaluation fixtures contain only 2 records, and the draft questions file contains 10 entries. This discrepancy must be resolved before treating the 25-figure as fact.

**No Excel workbook exists** — the Markdown storyboard (`docs/user-story-board.md`) is the only available planning board, consistent with HANDOFF.md claim.