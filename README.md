# Khula Gyan

A Nepali civic-document assistant prototype that retrieves document passages and aims to answer with page-linked citations. It must refuse when evidence is insufficient and is not legal advice.

**Product name:** Palika Guide — municipal citizen charter Q&A.

## 1. Project status and badges

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)]

**Pivot (2026-10-13):** Project pivoted from central-government procedures (driving license / citizenship / passport — 0 approved sources, 0 civic chunks, 0 verified questions) to **Palika Guide**: questions about municipal services answered from each municipality's citizen charter (नागरिक बडापत्र).

**Day 1 = Oct 14 ... Day 8 = Oct 21** (code freeze). Team of 3: Member 1 (Data & Documents), Member 2 (Retrieval & Generation), Leader (Integration, UI, Evaluation, Repo, Deployment). Presenter/backup: to be confirmed by a human.

## 2. What it does and who it is for

Khula Gyan (Palika Guide) is intended for people who need help finding information in Nepali municipal citizen charters (नागरिक बडापत्र), and for the student team building and reviewing that assistant. It is a retrieval-augmented generation (RAG) prototype: it searches source passages from a specific municipality's citizen charter, asks a language model to answer from those passages, and returns citations that identify a source, page, municipality, and section. It must say it cannot answer when the available evidence does not support a response, and must never answer from another municipality's charter.

## 3. Demo

**Local demo available.** Run `make run` to start the Streamlit app. The app has a municipality selector (required for Palika Guide questions). No municipality charters are indexed yet — Day 1 feasibility sheet and Day 2 processing will populate the index.

## 4. Features

### Working in the repository (Day 0 legacy)

- **PDF/HTML document processing** preserves page and source metadata. Flags corrupted Nepali PDF text as unusable and attempts OCR (Tesseract + nep/eng). Synthetic regression test covers missing-OCR case.
- **Tesseract OCR** v5.4.0 with eng+nep language data installed. MOHA Kathmandu PDF (5 pages) now extracts readable Nepali text (was 5/5 unusable, now 5/5 good).
- **Dense Chroma retrieval** supports service filtering and reports 0–1 similarity score. Synthetic Chroma test checks result limits, score range, and filtering. Scores are similarities, not probabilities.
- **Answer schema, citation guard, and provider adapter** implemented. Provider calls protected by per-process spend cap ($1.00, NVIDIA free tier).
- **Streamlit Q&A screen** exists and launches. Now includes municipality selector for Palika Guide.
- **Evaluation runner** supports draft-question skipping, fake LLM for plumbing checks, real LLM for quality evaluation.
- **Day 3 baseline** (legacy citizenship): hit@5=100%, citation_acc=67%, correct=0% (fake LLM), false_refusal=0%.

### Palika Guide (Day 1-8, Oct 14-21)

- **Municipality filter** in `search()` and municipality selector in UI.
- **Wrong-municipality guard**: if question names municipality with no indexed charter, or names none, returns `not_found`; never answers from another municipality's charter.
- **Chunk schema** gains optional `municipality`, `district`, `ward`, `section` fields (carried through chunker, indexer, Chroma metadata).
- **Checklist fields** reused for fee, time, officer (unknown stays empty).
- **40 questions** in `eval/questions.jsonl` (26 `palika_guide` + 3 `other` out-of-scope + 10 legacy drafts moved; 39 verified with `municipality` + `must_cite`, 1 draft `pq009` with `expected=["TODO"]`).
- **Legacy sources** tagged `legacy: true, answer_evidence: false` in `data/sources.yaml`; new municipality charter register template added.

### Not yet verified / Day 1-8

- No municipality charters indexed yet (Day 1 feasibility, Day 2 processing).
- Municipality filter in `search()` implemented; needs Day 2 index test.
- Wrong-municipality guard in `ask()` implemented; needs Day 3 test.
- `eval/questions.jsonl`: 40 records; 39 `verified=true` with `municipality` + `must_cite`; 1 `verified=false` draft (`pq009`).
- Real LLM (NVIDIA Nemotron) returns empty for prompts with passages — may need provider change.
- No municipality charters approved yet; written permission required.

## 5. How it works

The intended data path for Palika Guide:

~~~mermaid
flowchart LR
  S["Municipality citizen charter (text PDF/HTML)"] --> P["Extract text with page, municipality, section"]
  P --> C["Chunk while retaining municipality, district, ward, section"]
  C --> E["BAAI/bge-m3 embeddings"]
  E --> V["Chroma index"]
  Q["User question + municipality"] --> R["Dense retrieval + municipality filter"]
  V --> R
  R --> G["Answer generation (LLM)"]
  G --> A["Schema and citation-grounding checks"]
  A --> O["Answer with source, page, municipality, section, quote"]
  A --> N["not_found when evidence insufficient or wrong municipality"]
~~~

Search score is a normalized cosine similarity from 0 to 1; it is not a calibrated confidence or probability.

## 6. Tech stack and pinned versions

| Package | Version |
|---|---:|
| Python target | 3.12 |
| PyTorch | 2.14.1 |
| sentence-transformers | 6.1.0 |
| ChromaDB | 1.5.9 |
| Streamlit | 1.65.0 |
| rank-bm25 | 0.2.2 |
| PyMuPDF | 1.28.2 |
| pdfplumber | 0.11.7 |
| FastAPI | 0.140.1 |
| Uvicorn | 0.38.0 |
| PyYAML | 6.0.3 |
| python-dotenv | 1.2.1 |
| pytesseract | 0.3.13 |
| Pillow | 12.0.0 |
| OpenAI Python client | 3.27.0 |
| jsonschema | 4.26.0 |
| matplotlib | 3.10.8 |
| pytest | 9.1.1 |
| requests | 2.32.5 |

## 7. Prerequisites

- Python 3.12 and Git.
- GNU Make for the Makefile commands (optional; direct Python commands work).
- Network access and enough free disk space for dependency installation and the BAAI/bge-m3 embedding model download.
- **Tesseract OCR** plus the Nepali (`nep`) and English (`eng`) language packs for scanned document OCR.
  - Windows: install to `D:\tx` (or add to PATH). Verify with `tesseract --list-langs` showing `eng`, `nep`, `osd`.
- A paid LLM provider is optional. To use one, select a provider/model, configure its current rates, and keep its key in a local `.env` file. No API key is needed for the fake provider or synthetic tests.

## 8. Quick start and command verification

Run commands from the repository root.

### Option A: Using Make (requires GNU Make)

```sh
make setup      # create .venv, install pinned deps (CPU Torch first)
make fetch      # download only confirmed-open sources (currently only Open Data Nepal env dataset)
make index      # process eligible local sources, build Chroma index
make test       # run pytest suite
make eval       # run evaluation (fake LLM by default; real LLM needs .env)
make run        # start Streamlit app
```

### Option B: Direct Python commands (Windows, no Make needed)

```powershell
# Setup
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Fetch sources (only confirmed-open; currently only Open Data Nepal env dataset)
.\.venv\Scripts\python.exe scripts/fetch_sources.py

# Process local sources and build index (requires Tesseract in PATH for OCR)
$env:PATH = "D:\tx;" + $env:PATH
.\.venv\Scripts\python.exe scripts/build_index.py

# Run tests
.\.venv\Scripts\python.exe -m pytest -q --basetemp=.pytest_tmp

# Run evaluation (fake LLM for plumbing; real LLM needs .env configured)
.\.venv\Scripts\python.exe eval/run_eval.py --fake-llm --use-service-filter --use-municipality-filter --include-unverified --note "test run"

# Start Streamlit
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py
```

### Observed status (2026-10-13, post-pivot)

| Command | Status |
|---|---|
| Setup | ✅ `.venv` created, deps installed, embedding smoke check passed |
| Fetch | ✅ Works; only confirmed-open sources downloaded |
| Index (legacy) | ✅ MOHA Kathmandu PDF indexed (5 pages, 5 chunks) |
| Index (Palika) | ⏳ No municipality charters indexed yet (Day 2) |
| Test | ✅ **54 passed, 1 skipped** (all legacy tests pass) |
| Eval (fake LLM) | ✅ Runs; legacy Day 3 baseline recorded |
| Eval (real LLM) | ⚠️ **Blocked** — NVIDIA Nemotron returns empty for prompts with passages |
| Streamlit run | ✅ Launches; municipality selector present |

### Embedding smoke check

```powershell
.\.venv\Scripts\python.exe scripts/smoke_test_embedding.py
```
Passed for 10 examples (5 Nepali + 5 English), vector size 1024.

## 9. Configuration

Copy `.env.example` to `.env` and set local values. **Never commit `.env`** or include real keys in source, documentation, or issue comments.

| Variable | Example / default | Use |
|---|---|---|
| `LLM_PROVIDER` | `openrouter` (or `fake`) | Select provider; `fake` avoids API calls, returns non-realistic answers. |
| `LLM_BASE_URL` | `https://integrate.api.nvidia.com/v1` | OpenAI-compatible provider endpoint. |
| `LLM_MODEL` | `nvidia/nemotron-3-super-120b-a12b` | Model identifier. |
| `LLM_API_KEYS` | *your key here* | Provider secret; supply locally only. |
| `LLM_KEY_STRATEGY` | optional | Optional key-pool behavior. |
| `MAX_API_SPEND_USD` | `1.00` | Per-process cap (confirmed). |
| `LLM_INPUT_COST_PER_1M_USD` | `0.00` | NVIDIA free tier input cost. |
| `LLM_OUTPUT_COST_PER_1M_USD` | `0.00` | NVIDIA free tier output cost. |
| `MAX_API_OUTPUT_TOKENS` | `1024` | Maximum output reservation/request size. |

Paid calls are stopped before sending when rates are missing or a request's estimated reservation would exceed the cap. Estimates are not invoices.

### Current `.env` (example — replace key)

```bash
LLM_PROVIDER=openrouter
LLM_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_MODEL=nvidia/nemotron-3-super-120b-a12b
LLM_API_KEYS=nvapi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
MAX_API_SPEND_USD=1.00
LLM_INPUT_COST_PER_1M_USD=0.00
LLM_OUTPUT_COST_PER_1M_USD=0.00
MAX_API_OUTPUT_TOKENS=1024
```

## 10. Data and licensing

The current source registry is `data/sources.yaml`.

### Legacy sources (central-government, not used for Palika Guide)

| Source group | Registry status | Current use |
|---|---|---|
| DoTM driving-license pages/manual | unclear; local_only: true; **legacy: true** | Not approved as answer evidence. Request permission before broader reuse; do not commit copies. |
| Rules 2054 (Vehicle and Transport Management Rules) | unclear; local_only: true; **legacy: true** | Readable text via ToUnicode repair. Questions not yet verified. No deployment until written permission. |
| MOHA Kathmandu citizenship PDF | unclear; local_only: true; **legacy: true** | **OCR working** — 5 pages indexed, 15 questions verified. No redistribution; permission request pending. |
| Department of Passports pages | all rights reserved; local_only: true; **legacy: true** | Not approved for redistribution or answer evidence; do not commit copies. |
| Open Data Nepal Environment Statistics 2019 | confirmed open; CC BY-SA; local_only: false | Reference-only environmental data, not civic procedure. |

### Palika Guide municipality charter register (to be populated Day 1-2)

| Municipality | District | Province | URL | Format | Date seen | Reuse status | Local only | Answer evidence |
|---|---|---|---|---|---|---|---|---|
| *(to be filled Day 1)* | | | | | | | | |

All legacy sources tagged `legacy: true, answer_evidence: false` in `data/sources.yaml`. New municipality charter entries will have `service: palika_guide`, `answer_evidence: false` until written permission is recorded.

`make fetch` downloads only registry entries marked `confirmed open` to ignored `data/raw/`. `make index` processes eligible locally available sources to ignored `data/processed/` and `chroma_db/` and excludes sources not marked confirmed open and approved as answer evidence. See `data/sources.yaml` for URLs, terms notes, and attribution.

## 11. Evaluation

**Legacy Day 3 baseline (2026-10-11)** recorded in `docs/results.md`:

| Civic metric | Recorded value | Notes |
|---|---:|---|
| Questions in measured baseline | 15 | Verified citizenship questions from MOHA PDF |
| hit@5 | 100% | Dense search finds correct source for all 15 |
| Citation accuracy | 67% | 10/15 cited exact must_cite page |
| Answer correctness | 0% | Fake LLM returns raw OCR fragments |
| False refusal rate | 0% | No answerable questions refused |

The legacy question file has 25 records: 15 verified (citizenship), 10 draft (7 driving-license, 3 out-of-scope). Moved to `eval/legacy_questions.jsonl`.

### Palika Guide evaluation (Day 4+)

New municipal question set: 40 records in `eval/questions.jsonl` (26 `palika_guide` verified + 3 `other` out-of-scope verified + 10 legacy drafts moved + 1 draft `pq009`). 39 verified (`verified=true`, `expected` filled, `must_cite` filled, `municipality` present); 1 draft (`pq009`) with `expected=["TODO"]`. Target remains up to 40 verified questions across 5 municipalities × 6-8 services.

Day 4 baseline will be recorded in `docs/results.md` via `eval/run_eval.py --use-service-filter --use-municipality-filter`.

## 12. Project structure

~~~text
.
├── data/                 source registry; ignored raw/ and processed/ data
├── docs/                 decisions, source notes, story board, results, pivot addendum
├── eval/                 question sets (legacy + municipal), runner, judge, chart helpers
├── frontend/             Streamlit interface with municipality selector
├── scripts/              source fetch, document processing, index, smoke check
├── src/api/              optional API package; not part of the verified app flow
├── src/generation/       prompts, answer schema/guard, provider, spend control
├── src/ingest/           extraction, cleanup, chunking (municipality fields), embedding storage
├── src/retrieval/        dense Chroma search with municipality filter
├── tests/fixtures/       synthetic pages, chunks, and eval fixture
├── chroma_db/            generated local index; ignored by Git
└── docx/                 project blueprint
~~~

## 13. Testing

Run the full test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp=.pytest_tmp
```

The suite covers:
- Synthetic HTML processing and source/service metadata
- Top-k and score-range checks plus service filtering with temporary Chroma index
- Evaluation output and draft skipping
- Git tracking guard for raw/processed/index data
- Pre-send API spend-cap behavior
- Build_index source eligibility logic (confirmed-open path and local-only approval path)
- **NEW**: Municipality filter tests (service + municipality combined filter)

Latest run: **95 passed, 7 skipped** (verified 2026-10-23 with `--basetemp=.pytest_tmp`). All tests pass; 7 skipped (embedding model download/time-sensitive tests).

## 14. Known limitations and caveats

- **Real LLM integration blocked**: NVIDIA Nemotron 3 Super returns empty response for prompts containing passage content (even with 1 passage). Fake LLM works for plumbing; real quality evaluation needs fix or provider change.
- **No municipality charters indexed yet**: Day 1 feasibility, Day 2 processing, Day 3 indexing.
- **39 verified Palika Guide questions** (26 `palika_guide` + 3 `other` out-of-scope; 1 `verified=false` draft `pq009` with `expected=["TODO"]`). No civic evaluation baseline recorded (`hit@5=-`, `citation_acc=-`, `correct=-`) because no municipality charter is indexed.
- **No municipality permissions**: Written permission required from each municipality before public demo/deployment.
- **Search similarities are not probabilities**; refusal threshold (0.35) uncalibrated.
- **Answers may be wrong**. Verify any procedure with the responsible official office. This project is not legal advice.
- **Wrong-municipality guard**: If question names municipality with no indexed charter, or names none, returns `not_found`; never answers from another municipality's charter.
- **OCR needs Tesseract** + `nep`/`eng` language packs. MOHA Kathmandu PDF works; other scanned sources may need it.

## 15. Roadmap

From `docs/user-story-board.md` (Palika Guide, Day 1 = Oct 14):

1. **Day 1 (Oct 14)**: Feasibility sheet (~20 municipalities); pick ≤5 text/HTML charters; schema/filter changes; permission draft.
2. **Day 2 (Oct 15)**: Fetch/process chosen charters; page/section-linked JSONL with municipality; visual inspection; charter-row chunking.
3. **Day 3 (Oct 16)**: Index + municipality filter + guard; first real cited answer; 20-25 draft questions.
4. **Day 4 (Oct 17)**: Verify questions against pages; first real eval; BASELINE in `docs/results.md`.
5. **Day 5 (Oct 18)**: Fix top failures; calibrate `guard_min_score`; checklist fields; UI selector.
6. **Day 6 (Oct 19)**: Error analysis; adversarial/wrong-municipality/out-of-scope tests; test deploy.
7. **Day 7 (Oct 20)**: Grow verified set honestly (target 40; report real count); final eval; clean-machine README test.
8. **Day 8 (Oct 21)**: Code freeze; final README/results; demo script (2 Nepali, 2 English, 1 refusal, 1 wrong-municipality); submission text; tag `v0.1-palika`.

Stretch only if time remains: BM25/hybrid, reranker, glossary, FastAPI, feedback storage. They must not delay the cited-answer flow.

## 16. Contributing

- Work on `Hkp` or on a feature branch created from `Hkp`.
- Open pull requests into `Hkp`. Do not push changes to `main` or force-push.
- Make small commits with clear messages such as `feat:`, `fix:`, `test:`, or `docs:`.
- Before opening a PR, run tests and review `README.md` and `docs/results.md` for claims that need evidence.
- Track tasks in `docs/user-story-board.md`; update statuses only when the documented completion checks pass.
- Follow `AGENTS.md` for source, secret, generated-data, and API-spend rules.

## 17. Team and roles

| Role | Person |
|---|---|
| Member 1 — Data & Documents | (assigned) |
| Member 2 — Retrieval & Generation | (assigned) |
| Leader — Integration, UI, Evaluation, Repo, Deployment | (assigned) |
| Presenter | **to be confirmed by a human** |
| Backup presenter | **to be confirmed by a human** |

(Previous Member 3 role merged into Member 2 and Leader per pivot.)

## 18. Licence

The repository contains a `LICENSE` file with the MIT License for the project code. This code licence does not grant rights to redistribute the external source documents listed in `data/sources.yaml`.

## 19. Acknowledgements and data attribution

Open Data Nepal's Environment Statistics of Nepal 2019 record is attributed in `data/sources.yaml` to Open Knowledge Nepal / Open Data Nepal and credits source data to Nepal's Central Bureau of Statistics. Its dataset record lists Creative Commons Attribution Share-Alike and the Data Policy states: "Users are free to use, modify, and share datasets, provided they give appropriate attribution." It is retained as reference only and is not used as civic answer evidence.

Official MOHA and Department of Passports source URLs are listed in `data/sources.yaml` for tracking. Their content is local-only or all-rights-reserved as recorded there; no copies are included or redistributed. No publisher permission email has been sent by this work.

---

**Project notes:** `docs/results.md` records observed checks and measured metrics; `docs/decisions.md` records confirmed decisions (pivot, presenter, API cap, local-only approvals); `docs/user-story-board.md` tracks daily task status; `docs/pivot-addendum.md` summarizes changes vs. blueprint.