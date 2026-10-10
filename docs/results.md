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
| 2026-10-10 | `0645f41` | (opencode handoff) | chore: add opencode agents and commands | OpenCode subagent setup | 12 agent/command files added; verified against OpenCode v1 schema. |
| 2026-10-10 | `c60eccf` | (opencode handoff) | docs: reverify handoff state with audit evidence | Handoff re-verification | HANDOFF.md updated with VERIFIED/FAILED labels from actual command runs. |
| 2026-10-10 | `bc454ad` | (opencode handoff) | chore: add boss and 4 member subagents for Day 2 execution | Day 2 agent team | 5 subagents added (boss, member1-data, member2-retrieval, member3-generation, member4-integration). |
| 2026-10-10 | `94276b4` | (opencode handoff) | docs: reconcile README with verified state | Day 2 docs reconciliation | README updated: question count 12 (not 25), OCR working, index built (5 chunks), pipeline tested. |

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
| Day 2 | Member 1 — Data & Documents | **Done (dev override)** | Tesseract + nep/eng installed at `D:\tx`. MOHA PDF `citizenship_kathmandu_requirements.pdf` processed: 5 pages OCR extracted, all `good=5` ratings. Source remains `local_only: true` (no written permission); marked dev override in `sources.yaml`. |
| Day 2 | Member 2 — Retrieval | **Done (dev override)** | Index built from MOHA PDF: 5 pages → 5 chunks → 5 records indexed using `all-MiniLM-L6-v2` (384-dim, bge-m3 OOM). Search returns relevant chunks with 0–1 similarity scores. Source is local-only dev override; not production-eligible. |
| Day 2 | Member 3 — Generation & Evaluation | **Partial** | Pipeline works end-to-end with `LLM_PROVIDER=fake`: search → answer with citations (source + page). Question inventory: 10 drafts in `eval/question-drafts.md` + 2 fixtures (1 verified, 1 draft) = 12 total (not 25). No real LLM eval run (requires API key + spend cap). |
| Day 2 | Leader — Integration, UI & Repository | **Partial** | Pipeline connected: `search()` → `answer()` → citations. Streamlit UI code exists. Headless test with fake LLM returns cited answer. Docs reconciliation needed (`results.md`, README, decisions). |

## Evaluation results

Only real output from `eval/run_eval.py` against human-verified civic questions and source chunks belongs in this table. The runner is present, but there is no verified civic evaluation set or permitted civic-source index available for a baseline. The offline synthetic fixture harness is a plumbing check; its mock percentages are not project quality metrics. Unmeasured values remain `-`.

| Run / build | Date | Questions | hit@5 | Citation accuracy | Answer correctness | Refusal rate | Notes |
|---|---|---:|---:|---:|---:|---:|---|
| Day 0–2 baseline | - | - | - | - | - | - | No human-verified civic question set and permitted civic-source index are available for a real baseline. |
| Dev override (local-only MOHA) | 2026-10-10 | 0 | - | - | - | - | Index built from local-only MOHA PDF (5 chunks). No verified questions. Pipeline tested with `LLM_PROVIDER=fake`; answers generated with citations but not evaluated. |

## Setup verification (2026-10-10)

| Check | Result | Evidence / limits |
|---|---|---|
| Offline pytest suite | Pass | `7 passed`; includes synthetic processor metadata, Chroma score/filter behavior, draft-question skipping, and Git tracking guard. Ran with a repo-local pytest temp directory. |
| Synthetic evaluation harness | Pass | The offline fixture runner wrote one ignored run record and skipped the draft item. Its mock percentages are not civic evaluation results and were not copied into the evaluation table. |
| Pinned dependency consistency | Pass | `pip check`: `No broken requirements found.` |
| Embedding smoke check | Pass | Script printed `Embedding smoke check passed: 10 examples (5 Nepali + 5 English), vector size 1024`. Hugging Face warned that free cache space was slightly below the model's advertised download size. |
| GNU Make setup target | Not run | `make setup` failed because `make` is not installed in this Windows environment. The existing `.venv` was already available. |
| Source downloads / index build | **Dev override run** | MOHA PDF downloaded locally (ignored). OCR processed (Tesseract `nep+eng`). Index built (5 chunks, all-MiniLM-L6-v2). Source marked local-only dev override. |

## Day 2 task recheck (2026-10-10)

| Owner | Task | Status | Evidence / remaining work |
|---|---|---|---|
| Member 1 — Data | Find, fetch, process, and visually inspect a usable source | **Done (dev override)** | Tesseract + nep/eng installed at `D:\tx`. MOHA PDF processed: 5 pages OCR extracted, all `good=5`. Source remains `local_only: true` (no written permission); marked dev override in `sources.yaml`. Visual QA pending: page numbers not visible on rendered pages. |
| Member 1 — Processor safeguard | Prevent corrupted Nepali text from being treated as valid | Done | `src/ingest/extract.py` detects replacement characters or very low Devanagari proportion on Nepali PDF pages, attempts OCR, and marks the page unusable if OCR is missing or does not recover Nepali. Regression test covers the missing-OCR case. |
| Member 2 — Retrieval | Build and query an approved civic index | **Done (dev override)** | Index built: 5 pages → 5 chunks → 5 records (all-MiniLM-L6-v2). Search returns relevant chunks with 0–1 similarity scores. Five sample searches (Nepali queries) returned ranked results. Source is local-only dev override; not production-eligible. hit@5 remains `-` (no human-verified expected sources). |
| Member 3 — Generation & Evaluation | Verify questions and run evaluation | **Partial** | Pipeline works end-to-end with `LLM_PROVIDER=fake`: search → answer with citations (source + page). Question inventory reconciled: 10 drafts + 2 fixtures = 12 total (README updated). No real LLM eval run (requires API key + spend cap confirmation). |
| Leader — End-to-end app check | Run the app and try a query | **Partial** | Pipeline tested headless with fake LLM: search returns relevant chunks, answer generated with citations (source + page). Streamlit UI code exists but not launched in this session. Docs reconciliation needed. |

Verification after the processor change: `pytest -q --basetemp=.pytest_tmp\leader` → **7 passed in 4.54s**. Day 2 completion check remains unmet for production until the team has permitted, readable procedural source text, an index built from it, a correct page-linked retrieval result, and a supported cited answer.
