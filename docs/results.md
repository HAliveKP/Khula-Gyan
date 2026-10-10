# Project work log and results

Updated 2026-10-09. This file keeps previous entries and reports only checks that were actually run. The commit log below includes every Hkp commit through the immediately preceding Day 2 implementation commit. A Git commit cannot contain its own final hash; this log's commit will be included when the log is next updated.

## Commit log

Historical commit metadata, diffs, and combined statuses were rechecked on Hkp. Empty GitHub status lists mean **no status was recorded**, not that a test passed. The only recorded automated status among the historical commits below was CodeRabbit success on `12101ce`.

| Date (UTC) | Hash | Author | Message | Blueprint task | Check result |
|---|---|---|---|---|---|
| 2026-10-06 | `fcb094b9d06c024d39f0058cf83e67691f072663` | Harikrishna Pokhrel | Initial commit | Repository baseline | Commit and initial tree rechecked; no status recorded. |
| 2026-10-08 | `01527a8eb180e6cb6932c0fc1e97c649c064b544` | Harikrishna Pokhrel | feat: scaffold Khula Gyan Day 0 setup | Day 0 repository scaffold, setup notes, and interfaces | Diff rechecked; no status recorded. |
| 2026-10-08 | `2394b88d30ecea050b2cb821ebfa377432363353` | Harikrishna Pokhrel | fix: preserve gitignore line endings | Day 0 repository hygiene | Diff rechecked as a line-ending change; no status recorded. |
| 2026-10-09 | `bc5df97f5b97e016dca922d26c46f8da659a24b4` | Harikrishna Pokhrel | data: register ten official Day 1 sources | Day 1 Member 1 source register | Ten source entries and usage cautions rechecked; no status recorded. Originals were not downloaded. |
| 2026-10-09 | `978d1cd4b45ad26e7351e53d5acf2d7cfd257509` | Harikrishna Pokhrel | docs: report Day 1 source extraction quality | Day 1 Member 1 extraction review | Report rechecked; ratings are preliminary browser review, not local document extraction. No status recorded. |
| 2026-10-09 | `bd09ea0c1e40ccc5610c497dd0093f2e391d6e56` | Harikrishna Pokhrel | feat: add contract-shaped text chunking | Day 1 Member 2 chunker | Current smoke check passed chunk size, overlap, metadata, and syntax. No commit status recorded. |
| 2026-10-09 | `7bd0c3363049686e4de6ba415ac33f0c140d631d` | Harikrishna Pokhrel | feat: index document chunks in ChromaDB | Day 1 Member 2 vector indexer | Diff rechecked; Chroma/model indexing was not run in this environment. No status recorded. |
| 2026-10-09 | `4c7ffef41b87a21203872c20a1657a36a82b50de` | Harikrishna Pokhrel | feat: add schema-shaped mock ask pipeline | Day 1 leader mock pipeline | Historical diff rechecked. Day 2 replaced the mock with an integration adapter; current missing-component fallback check passed. No status recorded. |
| 2026-10-09 | `383fa1abb75552ededaf01ad99633169730dc67a` | Harikrishna Pokhrel | feat: add Streamlit demo answer and citations | Day 1 leader Streamlit screen | Historical diff rechecked; current UI syntax compiles, but Streamlit was not launched. No status recorded. |
| 2026-10-09 | `90a7b2d95b0ea73b8ebfc78a74c41aa64ffc30bc` | Harikrishna Pokhrel | fix: correct official citizenship source link | Day 1 source-register correction | Corrected link checked against the official Dadeldhura listing; no status recorded. |
| 2026-10-09 | `12101ce89ba6993923661f70816fa8fa7e5b38a0` | Harikrishna Pokhrel | fix: keep generated Chroma index in ignored folder | Day 1 generated-data handling | Diff rechecked; CodeRabbit status was success. |
| 2026-10-09 | `e378e3bfe8ac15be20a184b08a6474c7f24b0bb9` | Harikrishna Pokhrel | feat: add page-aware document extraction and cleaning | Day 2 Member 1 extraction and cleanup | Python syntax, CLI help, synthetic HTML extraction, Unicode NFC, repeated-header cleanup, and JSONL metadata checks passed. Official files were unavailable; PDF extraction was not run because PyMuPDF is absent from this runtime. No GitHub status recorded. |
| 2026-10-09 | `8990d04cc9e6f3dad95db9c4c850b7464590e710` | Harikrishna Pokhrel | feat: connect citation-aware pipeline and UI | Day 2 leader pipeline integration, citations, loading, and errors | Syntax and interface smoke checks passed, including `search(query, k=5, service)` → `answer(query, chunks)`; real Member 2/3 modules are not yet present. No GitHub status recorded. |
| 2026-10-09 | `9be4526b1c9080b1a682608aa2d7de8a8d16e03b` | Harikrishna Pokhrel | fix: keep the README diff focused | Day 2 README run instructions and current-feature description | Final diff from the previous implementation shows localized README edits (24 additions, 2 deletions); app and source-processing instructions are present. No GitHub status recorded. |
| 2026-10-09 | `d2aa3fb37b291e1ac77fc9f8e383101876fdfd68` | aash-crest01 | feat: Member 3 generation + eval starter (answer, guard, run_eval) | Day 0-1 M3: prompt v0, eval format, answer.py, guard, run_eval | pass: 12 tests passed at this commit |
| 2026-10-09 | `ddd60aaf9410b27e46dce7b912531798fea6c4d0` | Harikrishna Pokhrel | docs: record Day 0-2 work and checks | ? | not checked |
| 2026-10-10 | `c0603ca290110d544f539eef3b8818b115ecf63d` | aash-crest01 | eval: three-section results log (commit log, task checklist, eval table) + update_log.py | Day 1 M3: results log (Leader's LOG request) | pass: 14 tests passed |
| 2026-10-10 | `27318a369835b18c7a817a2782ea71a014d67158` | aash-crest01 | docs: fill commit log | Day 1 M3: results log | pass: commit log filled by update_log.py (docs only) |
| 2026-10-10 | `f71b69662b7a373c452d59472b55c497325689a5` | aash-crest01 | docs: check commit log rows | Day 1 M3: results log | pass: rows reviewed and filled (docs only) |
| 2026-10-10 | `6d5702aa999b61c671ac87a8051c45ef6d0afbaa` | aash-crest01 | feat: OpenRouter key pool (round robin + failover across several API keys) | Day 0 M3: LLM API key + test call (OpenRouter, key loop) | pass: 21 tests passed; smoke_test_llm.py passed with nemotron-3-super-120b-a12b:free |
| 2026-10-10 | `5455e2f0b372bfa62125e142d6ebe5e74fdef672` | aash-crest01 | feat: scripts/try_answer.py to test answer() with Nepali questions from a UTF-8 file | Day 0 M3: real-AI test of answer() | pass: try_answer.py, 4/4 questions behave correctly |
| 2026-10-10 | `16c934f006a9bc02abc2f56ade441ca07dcd4f69` | aash-crest01 | docs: LLM smoke test passed, commit log updated | Day 0 M3: record smoke test result | pass: docs only |
| 2026-10-10 | `116c11c1a28f5f74752cc9411c56d3583892170f` | aash-crest01 | docs: check new commit log rows | Day 1 M3: results log | pass: docs only |
| 2026-10-10 | `90b21cfd46ea71d5bf548bf00c3d724b14046d0e` | aash-crest01 | eval: use the team log format on main (full hashes, no merges, Day checklist, Eval runs under Evaluation results) | Day 1 M3: results log in the team format | pass: 24 tests passed; update_log.py matched the Leader's full hashes |

## Day checklist and evidence

| Day | Owner | Status | Evidence / remaining work |
|---|---|---|---|
| Day 0 | Member 1 — Data & Documents | Partial | Source register exists. No originals are in `data/raw/`; usage terms and a first local extraction remain to be confirmed. |
| Day 0 | Member 2 — Retrieval | Partial | Dependency list and embedding smoke script exist. A successful local model smoke run is not recorded. |
| Day 0 | Member 3 — Generation & Evaluation | Partial | Response contract and starter question drafts exist. Provider choice and a successful LLM call remain pending. |
| Day 0 | Leader — Integration, UI & Repository | Partial | Setup files and README exist; Hkp is the selected branch. Shared `dev` and `main` branches were not created. |
| Day 1 | Member 1 — Data & Documents | Partial | Ten sources are registered and a preliminary extraction report exists. No files were downloaded or locally extracted. |
| Day 1 | Member 2 — Retrieval | Partial | Chunking and Chroma index code exist. A sample dataset and populated index have not been produced. |
| Day 1 | Member 3 — Generation & Evaluation | Pending | `src/generation/answer.py` and the 15-question Day 1 set are not present. |
| Day 1 | Leader — Integration, UI & Repository | Done for mock | `ask()` and the initial Streamlit screen were added; the screen was not launched in this environment. |
| Day 2 | Member 1 — Data & Documents | In progress | PDF/HTML extraction, NFC cleanup, repeated header/footer removal, and page-linked JSONL output are implemented. Synthetic HTML checks passed. Process a permitted official source and inspect each page when the download and PyMuPDF prerequisites are available. |
| Day 2 | Member 2 — Retrieval | Pending (not part of this request) | The real `src/retrieval/search.py` module is not present, so index search cannot yet run end to end. |
| Day 2 | Member 3 — Generation & Evaluation | Pending (not part of this request) | The real `src/generation/answer.py` module is not present, so no answer generation or evaluation can run. |
| Day 2 | Leader — Integration, UI & Repository | In progress | `ask()` now connects to the documented `search()` and `answer()` interfaces when available; the UI has citation display, loading, and friendly error states. It safely returns `not_found` until those modules and reviewed source text exist. Optional FastAPI was skipped. |
| Day 0 (update 2026-10-10) | Member 3 — Generation & Evaluation | Done | Provider: OpenRouter (Leader's choice). `python scripts/smoke_test_llm.py` passed with `nvidia/nemotron-3-super-120b-a12b:free` (Nepali 5.0 s, English 0.9 s); `google/gemma-4-31b-it:free` was rate-limited upstream. Prompt v0 in `src/generation/prompt.py`; question format in `eval/questions.jsonl` (10 drafts, unverified); `python eval/check_questions.py` → OK. Code in PR #5. |
| Day 1 (update 2026-10-10) | Member 3 — Generation & Evaluation | Partial | `src/generation/answer.py` exists (`answer()` per contract 9.3, guard, schema validation); `python -m pytest -q` → 24 passed. Real-AI check: `python scripts/try_answer.py` answered English, Nepali and Romanized questions with grounded citations on the sample passages and refused an off-topic question. Nepali has Hindi words and spelling slips (prompt v1, Day 4). Remaining: 15 verified questions with Member 1 (10 drafts, 0 verified). |
| Day 2 (update 2026-10-10) | Member 3 — Generation & Evaluation | Partial (code ready) | `eval/run_eval.py` exists and ran end to end on sample passages with the fake LLM (`--mock`). Not yet run on real `search()` (Member 2's module not present). Remaining: 25 questions (5 out-of-scope). |

## Evaluation results

Only `eval/run_eval.py` output belongs in this table. That runner is not present on Hkp, so no quality numbers have been measured. Smoke checks above are implementation checks, not evaluation results.

| Run / build | Date | Questions | hit@5 | Citation accuracy | Answer correctness | Refusal rate | Notes |
|---|---|---:|---:|---:|---:|---:|---|
| Day 0–2 baseline | - | - | - | - | - | - | `eval/run_eval.py` is not available; run the evaluation after the answer and search modules are connected. |

### Eval runs (eval/run_eval.py)

Rows are added only by `eval/run_eval.py`; `-` = not measured. Never type numbers by hand.

| Date | Change | Prompt | N | hit@5 | Citation acc. | Correct | Hallucination | Correct refusal | False refusal | p95 s |
|---|---|---|---|---|---|---|---|---|---|---|
