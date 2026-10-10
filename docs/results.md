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

| 2026-10-10 | `7e7801d8638323f12fe56ad4aa521862dd0d2641` | Harikrishna Pokhrel | feat: add dense retrieval search contract | Day 2 Member 2: dense search and score scale | Python syntax compilation passed. No embedding model or Chroma package is installed; no data/index means no retrieval run or hit@5. |
| 2026-10-10 | `025ef81beaf12b61b6264e1100cde972ae4c157e` | Harikrishna Pokhrel | docs: describe current Hkp retrieval status | Leader: correct README status/run expectations | README descriptions checked against Hkp and main/dev; setup/runtime not executed. |

## Day checklist and evidence

| Day | Owner | Status | Evidence / remaining work |
|---|---|---|---|
| Day 0 | Member 1 — Data & Documents | Partial | Source register exists. No originals are in `data/raw/`; usage terms and a first local extraction remain to be confirmed. |
| Day 0 | Member 2 — Retrieval | Partial | Dependency list and embedding smoke script exist. A successful local model smoke run is not recorded. |
| Day 0 | Member 3 — Generation & Evaluation | Partial | Response contract and starter question drafts exist. Provider choice and a successful LLM call remain pending. |
| Day 0 | Leader — Integration, UI & Repository | Partial | Setup files and README exist; Hkp is the selected branch. `dev` was created from `main` on 2026-10-10; end-to-end app run remains blocked on source/index and Hkp generation module. |
| Day 1 | Member 1 — Data & Documents | Partial | Ten sources are registered and a preliminary extraction report exists. No files were downloaded or locally extracted. |
| Day 1 | Member 2 — Retrieval | Partial | Chunking and Chroma index code exist. A sample dataset and populated index have not been produced. |
| Day 1 | Member 3 — Generation & Evaluation | Pending | `src/generation/answer.py` and the 15-question Day 1 set are not present. |
| Day 1 | Leader — Integration, UI & Repository | Done for mock | `ask()` and the initial Streamlit screen were added; the screen was not launched in this environment. |
| Day 2 | Member 1 — Data & Documents | In progress | PDF/HTML extraction, NFC cleanup, repeated header/footer removal, and page-linked JSONL output are implemented. Synthetic HTML checks passed. Process a permitted official source and inspect each page when the download and PyMuPDF prerequisites are available. |
| Day 2 | Member 2 — Retrieval | Partial | `src/retrieval/search.py` now implements dense search and 0–1 cosine similarity. No source chunks/index exist; embedding smoke test failed because `sentence-transformers` is missing; hit@5 is not measured. |
| Day 2 | Member 3 — Generation & Evaluation | Partial on Hkp; code ready on main/dev | `answer.py` and `run_eval.py` are in `main`/`dev` (merged PR #5); Hkp does not contain them. Ten questions are drafts, zero verified; the required 25-question set and real retrieval eval are incomplete. |
| Day 2 | Leader — Integration, UI & Repository | In progress | `ask()` now connects to the documented `search()` and `answer()` interfaces when available; the UI has citation display, loading, and friendly error states. It safely returns `not_found` until those modules and reviewed source text exist. Optional FastAPI was skipped. |

## Evaluation results

Only `eval/run_eval.py` output belongs in this table. That runner is not present on Hkp, so no quality numbers have been measured. Smoke checks above are implementation checks, not evaluation results.

| Run / build | Date | Questions | hit@5 | Citation accuracy | Answer correctness | Refusal rate | Notes |
|---|---|---:|---:|---:|---:|---:|---|
| Day 0–2 baseline | - | - | - | - | - | - | `eval/run_eval.py` is not available; run the evaluation after the answer and search modules are connected. |


## Day 0–2 task audit (2026-10-10)

This audit checks the working branch `Hkp` and notes when work exists only on shared `main`/`dev`. No task is marked complete based only on a code file existing.

| Owner | Day 0–2 task | Status | Evidence / next step |
|---|---|---|---|
| Member 1 — Data | Download official PDFs/pages, verify reuse permission | Blocked | `data/raw/` contains only `.gitkeep`. The registered sources do not provide a confirmed reuse/redistribution grant; the blueprint directs us to keep URLs and skip files when rights are unclear. Ask each publisher before redistributing; keep source copies local only if the team confirms lawful internal use. |
| Member 1 — Data | Process, visually inspect Nepali/page numbers, deliver processed JSONL | Partial | Processor supports PDF/HTML, NFC cleanup, page fields, OCR fallback, and synthetic HTML checks passed earlier. No official files/PyMuPDF/Tesseract data available here; `data/processed/` contains only `.gitkeep`, so no visual page QA or deliverable exists. |
| Member 1 + Member 3 | Write and verify 15 Day 1 questions together | Pending | `eval/question-drafts.md` has 10 unverified drafts; `main/dev` has 10 JSONL records, 0 verified. Requires source pages before filling expected facts and citations. |
| Member 2 — Retrieval | Run embedding smoke test | Blocked | Attempted `python scripts/smoke_test_embedding.py`; failed with `ModuleNotFoundError: sentence_transformers`. Install project requirements/model before rerunning. |
| Member 2 — Retrieval | Build Chroma index from Member 1's processed files | Blocked | No processed chunks exist and Chroma is not installed. No index built. |
| Member 2 — Retrieval | Implement `search(query, k=5, service=None)`, explain score | Partial | Hkp commit `7e7801d` implements dense Chroma search with source/page metadata and cosine-derived 0–1 similarity (not probability). Runtime retrieval is unverified; BM25/RRF/reranker remain future work. |
| Member 2 — Retrieval | Report hit@5 | Pending | Requires permitted processed sources, populated index, and verified questions. No metric is recorded. |
| Member 3 — Generation | Provide `answer()` and prompt/schema | Done on main/dev; absent on Hkp | Existing merged PR #5 added generation, schema/guard, tests, and a provider smoke check on main; Hkp has not incorporated those commits. |
| Member 3 — Evaluation | Grow set to 25 including 5 off-topic | Pending | Main/dev has 10 unverified question entries only. Do not invent expected facts or mark questions verified without page evidence. |
| Member 3 — Evaluation | First real evaluation after `search()`; Day 3 baseline | Pending | Main/dev runner supports evaluation, but no Hkp index or real search run exists. The results table correctly keeps unmeasured metrics as `-`. |
| Leader | Answer provider/credits/threshold/intermediate stage/results owner/submission/presenter questions | Partial | Main/dev records OpenRouter as provider, but the other decisions are not answered in the checked project notes. Threshold remains uncalibrated; default 0 is only a starting configuration, not approval to disable the guard. |
| Leader | Create shared `dev` branch | Done | Created `dev` from current `main` (2026-10-10). |
| Leader | Run Streamlit end-to-end after search exists | Blocked | Streamlit, Chroma, embedding package, index, and Hkp generation module are missing in this runtime/branch. |

No real evaluation numbers were added: the required source-backed question set and populated retrieval index are still missing.
