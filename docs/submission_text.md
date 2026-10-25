# Submission text — Khula Gyan (Palika Guide)

**Date:** 2026-10-23 | **Code freeze:** Oct 21 | **Submission:** Oct 25

## Problem

Nepali citizens seeking information about municipal services (नागरिक बडापत्र) must navigate scattered, often scanned PDFs from individual municipalities. There is no unified, cited Q&A assistant that links answers to specific charter pages and refuses when evidence is missing.

## Idea

Khula Gyan (Palika Guide) is a retrieval-augmented generation assistant that reads from a municipality's citizen charter (text or HTML), retrieves relevant passages using dense embeddings (`BAAI/bge-m3`), filters by municipality and service, and returns page-linked citations. It must say `not_found` when the indexed charter does not support the answer and must never answer from another municipality's charter.

## How AI powers it

- **Dense retrieval** (`ChromaDB` + `BAAI/bge-m3`) searches indexed charter chunks with optional `municipality` and `service` filters.
- **Language model** (`NVIDIA Nemotron 3 Super 120B` via `https://integrate.api.nvidia.com/v1`) generates answers from retrieved passages. Configured in `.env` (`LLM_PROVIDER=openrouter`, `LLM_MODEL=nvidia/nemotron-3-super-120b-a12b`).
- **Citation guard** (`src/generation/guard.py`) verifies every citation is a verbatim quote from a retrieved chunk and that `source` + `page` matches the evidence (`eval/check_questions.py` enforces `verified=true`, `expected`, `must_cite`).
- **Wrong-municipality guard** (`src/pipeline.py` `ask()`) ensures `service="palika_guide"` requires a municipality; if none given or none indexed, returns `not_found` rather than cross-contaminating with another municipality's chunks.
- **Spend cap** (`MAX_API_SPEND_USD=1.00`) stops paid requests before they exceed the cap; rates configured (`LLM_INPUT_COST_PER_1M_USD=0.00`, `LLM_OUTPUT_COST_PER_1M_USD=0.00` — NVIDIA free tier).

## Current verified state (2026-10-23, Day 8 freeze)

- **Repository:** `main` (commit `2a6b9ef` — demo script; `5e07f76` — docs sync; `b6a61b0` — skills; `097780f` — docs-sync skill; `3ac9148` — eval-runner; `5c929cc` — doc-processing-qa; `6c5faf3` — source-rights-check). Previous: `65f235a` (env-setup); `1b9b4f1` (search fix); `a2dd598` (original merge).
- **Branch rules:** All work on `main` (or feature branches from `Hkp`); PRs into `Hkp` per `AGENTS.md`. No pushes to `main` without review.
- **Tests:** `pytest -q --basetemp=.pytest_tmp` → **95 passed, 7 skipped** (verified 2026-10-23).
- **Streamlit:** Launches (`frontend/app.py` serves HTML at `localhost:8501`; municipality selector present; refusal path works with empty index).
- **Environment:** `.venv/` created; `torch==2.14.1+cpu` installed first; `pip check`: `No broken requirements found.`; `streamlit-1.66.1` installed; `sentence-transformers-6.2.0` installed; `chromadb-1.5.9` installed; `jsonschema-4.26.0` installed.
- **Sources (`data/sources.yaml`):** 20 entries total. 11 legacy (`legacy: true`, `answer_evidence: false`). 1 reference (`opendatanepal_environment_statistics_2019`, `licence_status: confirmed open`, `local_only: false`, `answer_evidence: false`). 12 `palika_guide` municipality entries (`service: palika_guide`, `municipality`: Pokhara/Bharatpur/Dhulikhel/Ghorahi/Hetauda; `district`/`province` filled; `format`: text_pdf/html; `date_seen`: 2026-10-15; `reuse_status`: unclear; `reuse_quote`: exact footer text recorded; `local_only: true`; `answer_evidence: false`; `approval_note`: null; `approved_on`: null; `approved_by`: null).
- **Fetch:** `scripts/fetch_sources.py` downloads 1 source (`opendatanepal_environment_statistics_2019`, 18532 bytes). All 12 palika URLs fail with `WinError 10060` / `WinError 10061` (connection timeout / refused). No `data/raw/` palika PDFs exist locally. *Update 2026-10-25:* this was the Leader's machine. On aash-crest01's machine all 12 charter files were downloaded and processed on 2026-10-15 into ignored `data/raw/` and `data/processed/` (12 JSONL files, 126 page records); none is committed.
- **Index:** `chroma_db/` exists (188416 bytes `chroma.sqlite3`) but contains **0 eligible civic chunks** (no approved sources indexed). `build_index.py` reports: `Processed page records: 0`; `Eligible civic chunks: 0`; `Indexed records: 0`; `No source passed both open-license and civic-answer-evidence checks; no Chroma index was built.` (message printed; file exists from previous index attempt but is empty of civic data).
- **Pipeline (`src/pipeline.py`):** `search()` + `answer()` + `ask()` connected; `municipality` filter works; `service` filter works; wrong-municipality guard returns `not_found` for missing municipality; `service='other'` fixed (`search()` returns `[]` instead of `ValueError`). `RESPONSE_FIELDS`, `CHECKLIST_FIELDS`, `CITATION_FIELDS` enforced by `_valid_response()`.
- **Chunk schema (`src/ingest/chunk.py`):** Carries optional `municipality`, `district`, `ward`, `section` fields; `chunk_text()` passes these through.
- **Questions (`eval/questions.jsonl`):** 40 records. *Update 2026-10-25 (counted in the file):* the split below is off; the file has 37 `palika_guide` (36 verified + draft `pq009`) and 3 `other`, all `pq001`–`pq040`, with no legacy `q016`–`q025` records (those are in `eval/legacy_questions.jsonl`). 39 verified on 2026-10-17 (`ef07ac0`, PR #21).
  - 26 `palika_guide` verified (`verified=true`, `expected` filled, `must_cite` filled, `municipality` present, `verified_by=Aashish (via verify_app)`, `verified_on=2026-10-17`).
  - 3 `other` out-of-scope verified (`pq037`: passport; `pq038`: other; `pq039`: out-of-scope fake request; `verified=true`, `expected=["not_found"]`).
  - 10 legacy drafts moved from old set (`q016`–`q025` in `eval/legacy_questions.jsonl`).
  - 1 draft (`pq009`: Bharatpur personal event registration copy fee; `expected=["TODO"]`, `verified=false`, `verification_status=draft`).
- **Evaluation:** `eval/check_questions.py eval/questions.jsonl` → `40 questions ... OK` (2026-10-23). No format errors. `eval/run_eval.py --fake-llm --use-service-filter --use-municipality-filter --include-unverified --note "plumbing" --no-write` runs plumbing only; all verified palika questions return `not_found` (no index); metrics (`hit@5`, `citation_acc`, `correct`, `false_refusal`) remain `-`; no synthetic numbers written to `docs/results.md`.
- **Real LLM (`NVIDIA Nemotron`):** `.env` configured (`LLM_PROVIDER=openrouter`, `LLM_MODEL=nvidia/nemotron-3-super-120b-a12b`, `LLM_API_KEYS=...` not printed, `LLM_BASE_URL=https://integrate.api.nvidia.com/v1`, `MAX_API_SPEND_USD=1.00`, `LLM_INPUT_COST_PER_1M_USD=0.00`, `LLM_OUTPUT_COST_PER_1M_USD=0.00`, `MAX_API_OUTPUT_TOKENS=1024`). Returns empty for prompts with passage content (same pre-pivot issue). Paid calls blocked by zero rates and $1.00 cap. *Update 2026-10-25:* cause found on 2026-10-15: Nemotron's hidden reasoning used the whole 1024-token output limit (`finish_reason=length`). Fix merged via PR #20: `LLM_REASONING=off` (`952f058`) and no caching of empty replies (`4567b75`). The switch is OpenRouter's `reasoning` parameter; it worked with `LLM_BASE_URL=https://openrouter.ai/api/v1` and `nvidia/nemotron-3-super-120b-a12b:free`, and is untested with the NVIDIA NIM base URL configured above.
- **Demo script (`scripts/demo_script.py`):** Created and runs successfully (`.venv/Scripts/python.exe scripts/demo_script.py`). Demonstrates 2 Nepali (`pokhara` birth fee; `bharatpur` death docs), 2 English (`dhulikhel` birth time; `ghorahi` citizenship fee), 1 refusal (`palika_guide` without municipality), 1 wrong-municipality (`lalitpur` — no indexed charter). All results clearly labeled `not_found` or `Result (no index): ...`. No synthetic answers claimed as real. Pipeline imports verified (`search`, `answer`, `ask` OK). Index status (`chroma_db/` exists but empty of civic data) printed.
- **Skills (`skills/`):** 6 skills saved (`env-setup.md`, `source-rights-check.md`, `doc-processing-qa.md`, `eval-runner.md`, `docs-sync.md`, `release-check.md`). All descriptions <60 chars; full details in `.md` body.
- **Docs updates (`README.md`, `docs/results.md`, `docs/next-steps.md`, `docs/user-story-board.md`, `docs/decisions.md`):** `README.md` updated (test count 95 passed; verified question count 39; limitations updated). `docs/results.md` updated (commit log preserved; evaluation table kept with `-`; new verification section added with evidence). `docs/user-story-board.md` preserved (Day 8 freeze noted). `docs/decisions.md` preserved (pivot confirmed, local-only approval recorded, presenter pending, cap confirmed).
- **Data hygiene:** `data/raw/` only contains fetched allowed files (`opendatanepal_environment_statistics_2019.html`); no raw palika PDFs committed. `data/processed/` does not exist (no processed civic data). `chroma_db/` exists but only from previous index attempt (empty civic data). `.env` not committed. `.gitignore` excludes `data/raw/`, `data/processed/`, `chroma_db/`.
- **Honesty rules (`AGENTS.md` §46–51):** No invented source text. No fabricated citations. No synthetic evaluation numbers in `docs/results.md`. Unverified questions marked `draft` (`pq009`). Metrics unmeasured = `-`. No legal advice claimed (`frontend/app.py` caption; `README.md` line 327; `docs/submission_text.md`).

## What works (verified by actual command output, not described)

1. `pytest` passes (95/7).
2. `search()` + `ask()` + `pipeline.py` work; `municipality` filter works; wrong-municipality guard works; `service='other'` fixed.
3. `build_index.py` runs; reports 0 civic chunks (honest — no approved sources).
4. `eval/check_questions.py` passes (`40 OK`).
5. `eval/run_eval.py` plumbing works (`--fake-llm`, `--no-write`).
6. `frontend/app.py` launches; refusal path verified.
7. `scripts/demo_script.py` runs; clearly shows synthetic/non-realistic results.
8. `skills/*.md` saved.
9. `README.md` and `docs/results.md` updated to match verified state.
10. No `.env`, raw palika PDFs, or `chroma_db/` civic index committed.

## What does NOT work (honest limits — must be stated in submission)

1. **No municipality charter indexed.** `build_index.py` produces 0 civic chunks because no palika source has `approval_note` + `approved_on` + `approved_by` in `data/sources.yaml`, and all 12 URLs fail to fetch in this environment (`WinError 10060`/`10061`). *Update 2026-10-25:* the files are fetched and processed on aash-crest01's machine; the missing approval is the remaining reason. *Update 2026-10-25 (evening):* first official BASELINE run by `eval/run_eval.py` (see the Eval runs table in `docs/results.md`): official index from 11 local-only approved charters (`palika_pokhara_2075` excluded; approved by Aashish with authority delegated by the Leader), `nvidia/nemotron-3.5-super-vl:free` with `LLM_REASONING=off`, 39 verified questions: hit@5 81%, citation_acc 93%, correct 19% (exact keyword match), correct_refusal 100%, false_refusal 48%; 2 questions hit LLM provider errors and count as not correct.
2. **No verified civic evaluation baseline.** `hit@5`, `citation_acc`, `correct`, `false_refusal` remain `-` (`docs/results.md` evaluation table; `docs/submission_text.md`).
3. **Real LLM (NVIDIA Nemotron) blocked.** Returns empty response for prompts containing passage content. No real quality evaluation possible (`README.md` line 279; `docs/submission_text.md`). *Update 2026-10-25:* the empty replies are fixed with `LLM_REASONING=off` on the OpenRouter base URL (see "Real LLM" above); real evaluation is still blocked by the empty charter index (item 1). *Update 2026-10-25 (evening):* first official BASELINE run by `eval/run_eval.py` (see the Eval runs table in `docs/results.md`): official index from 11 local-only approved charters (`palika_pokhara_2075` excluded; approved by Aashish with authority delegated by the Leader), `nvidia/nemotron-3.5-super-vl:free` with `LLM_REASONING=off`, 39 verified questions: hit@5 81%, citation_acc 93%, correct 19% (exact keyword match), correct_refusal 100%, false_refusal 48%; 2 questions hit LLM provider errors and count as not correct.
4. **No written municipality permission.** (*Update 2026-10-25:* emails for all 5 municipalities drafted locally on 2026-10-15; sending pending.) `docs/permission_request.md` exists (draft only); no publisher contacted (`AGENTS.md` §108: no contacting publishers). All 12 palika sources remain `answer_evidence: false` (`docs/submission_text.md`).
5. **Network access to Nepali municipality sites blocked.** All 12 charter URLs (`pokharamun.gov.np`, `bharatpurmun.gov.np`, `dhulikhelmun.gov.np`, `ghorahimun.gov.np`, `hetaudamun.gov.np`) fail. Charters must be fetched locally or from pre-downloaded files before indexing can occur (`docs/submission_text.md` step 1; `docs/next-steps.md` Priority 1). *Update 2026-10-25:* applies to the Leader's machine only; aash-crest01's machine reached the sites and holds the files (they can be shared privately, not through Git).
6. **Embedding smoke not fully verified.** `BAAI/bge-m3` download (~2.6 GB) times out; `scripts/smoke_test_embedding.py` not completed (`docs/submission_text.md`).

## How to reach production (documented plan, not promised timeline)

1. **Confirm presenter/backup** (`docs/decisions.md` §5: pending human confirmation).
2. **Select ≤5 municipalities** (`docs/user-story-board.md` Day 1: currently `Pokhara`, `Bharatpur`, `Dhulikhel`, `Ghorahi`, `Hetauda` registered; confirm final set).
3. **Send permission requests** (`docs/permission_request.md` draft; update `data/sources.yaml` with `approval_note`, `approved_on`, `approved_by` once written permission received; set `answer_evidence: true`).
4. **Fetch/process approved charters** (`scripts/fetch_sources.py` or manual download to `data/raw/`; `scripts/process_document.py` with municipality fields; inspect `data/processed/*.jsonl`; fix `bad`/`unusable` pages).
5. **Build index** (`scripts/build_index.py`); verify `chroma_db/` exists and `collection.count() > 0`; verify `search()` returns results for verified questions (`eval/check_questions.py` + manual page inspection).
6. **Verify questions** (`eval/check_questions.py`); ensure `expected` has real facts (not `"TODO"`) and `must_cite` points to real pages; remove `verified=false` for questions that now have evidence.
7. **Run real evaluation** (`eval/run_eval.py --fake-llm` first for plumbing; then with real LLM once provider fixed). Record BASELINE in `docs/results.md` with only real numbers.
8. **Calibrate `guard_min_score`** (`eval/sweep_threshold.py`); fix checklist fields (`docs/next-steps.md` Day 5); improve prompt for same-language answers; add municipality selector improvements.
9. **Error analysis** (`docs/error-analysis.md`): classify failures (retrieval miss, guard error, generation error, hallucination) against real evaluation.
10. **Adversarial tests** (`tests/`): out-of-scope (`service="other"`), wrong-municipality (`service="palika_guide"` + unknown municipality), refusal (`empty chunks`).
11. **Fix real LLM** (`.env` provider change or NVIDIA Nemotron fix for empty responses with passages); confirm spend cap behavior (`tests/test_llm_keys.py` passes when rates set). *Update 2026-10-25:* fix exists (`LLM_REASONING=off`, PR #20); remaining step is to set `LLM_BASE_URL=https://openrouter.ai/api/v1` on the Leader's machine, or test NIM's own reasoning switch.
12. **Clean-machine README test** (`skills/release-check.md` procedure): fresh clone, follow `README.md`, verify `pytest`, `fetch`, `index`, `eval`, `run` results match docs.
13. **Final demo recording** (`scripts/demo_script.py` updated with real cited answers when index exists); update `docs/submission_text.md` with verified metrics only.
14. **Tag release** (`v0.1-palika`) and submit (`docs/submission_text.md` ready; `README.md` and `docs/results.md` accurate).
