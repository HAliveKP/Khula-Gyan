# Khula Gyan

A Nepali civic-document assistant prototype that retrieves document passages and aims to answer with page-linked citations. It must refuse when evidence is insufficient and is not legal advice.

## 1. Project status and badges

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)]

**Day 3 complete (2026-10-11).** Tests: **54 passed, 1 skipped**. Civic index built from MOHA Kathmandu citizenship PDF (5 pages, OCR). 15 verified citizenship questions. Day 3 baseline recorded: hit@5=100%, citation_acc=67%, correct=0% (fake LLM), false_refusal=0%.

## 2. What it does and who it is for

Khula Gyan is intended for people who need help finding information in Nepali public-service documents, and for the student team building and reviewing that assistant. It is a retrieval-augmented generation (RAG) prototype: it searches source passages, asks a language model to answer from those passages, and returns citations that identify a source and page. It should say it cannot answer when the available evidence does not support a response.

## 3. Demo

**Local demo available.** Run `make run` to start the Streamlit app. The civic index currently contains the MOHA Kathmandu citizenship checklist (5 pages, OCR'd). Driving-license questions use the Rules 2054 source (local-only, readable text, not yet verified).

## 4. Features

### Working in the repository (Day 3)

- **PDF/HTML document processing** preserves page and source metadata. Flags corrupted Nepali PDF text as unusable and attempts OCR (Tesseract + nep/eng). Synthetic regression test covers missing-OCR case.
- **Tesseract OCR** v5.4.0 with eng+nep language data installed. MOHA Kathmandu PDF (5 pages) now extracts readable Nepali text (was 5/5 unusable, now 5/5 good).
- **Dense Chroma retrieval** supports service filtering and reports 0–1 similarity score. Synthetic Chroma test checks result limits, score range, and filtering. Scores are similarities, not probabilities.
- **Civic index built** from MOHA Kathmandu citizenship PDF: 5 page records → 5 chunks indexed in `chroma_db/khula_gyan`. Search returns relevant results (scores 0.56–0.68).
- **15 verified citizenship questions** (q001–q015) against MOHA PDF pages 1–5, with `must_cite` page references.
- **Answer schema, citation guard, and provider adapter** implemented. Provider calls protected by per-process spend cap ($1.00, NVIDIA free tier).
- **Streamlit Q&A screen** exists and launches. Returns cited answers for citizenship questions.
- **Evaluation runner** supports draft-question skipping, fake LLM for plumbing checks, real LLM for quality evaluation.
- **Day 3 baseline** recorded: hit@5=100%, citation_acc=67%, correct=0% (fake LLM), false_refusal=0%.

### Not yet verified / Day 4+

- Real LLM (NVIDIA Nemotron) returns empty for prompts with passage content — needs fix (Day 4).
- Rules 2054 (driving-license) text readable but questions not yet verified against it.
- BM25/hybrid retrieval, reranking not yet implemented.
- No public deployment; no written publisher permissions for public demo.

## 5. How it works

The intended data path is:

~~~mermaid
flowchart LR
  S["Reviewed local PDF or HTML"] --> P["Extract text with page and URL (OCR if needed)"]
  P --> C["Chunk while retaining metadata"]
  C --> E["BAAI/bge-m3 embeddings"]
  E --> V["Chroma index"]
  Q["User question"] --> R["Dense retrieval"]
  V --> R
  R --> G["Answer generation (LLM)"]
  G --> A["Schema and citation-grounding checks"]
  A --> O["Answer with source, page, and quote"]
  A --> N["not_found when evidence is insufficient"]
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
.\.venv\Scripts\python.exe eval/run_eval.py --fake-llm --use-service-filter --include-unverified --note "test run"

# Start Streamlit
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py
```

### Observed status (2026-10-11)

| Command | Status |
|---|---|
| Setup | ✅ `.venv` created, deps installed, embedding smoke check passed |
| Fetch | ✅ Works; only confirmed-open sources downloaded |
| Index | ✅ **Civic index built** from MOHA Kathmandu PDF (5 pages, 5 chunks) |
| Test | ✅ **54 passed, 1 skipped** |
| Eval (fake LLM) | ✅ Runs; Day 3 baseline recorded |
| Eval (real LLM) | ⚠️ **Blocked** — NVIDIA Nemotron returns empty for prompts with passages |
| Streamlit run | ✅ Launches; citizenship questions work with real LLM (simple) |

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

| Source group | Registry status | Current use |
|---|---|---|
| DoTM driving-license pages/manual | unclear; local_only: true | Not approved as answer evidence. Request permission before broader reuse; do not commit copies. |
| Rules 2054 (Vehicle and Transport Management Rules) | unclear; local_only: true; **answer_evidence: true** (Leader-approved LOCAL-ONLY baseline 2026-10-11) | Readable text via ToUnicode repair. Questions not yet verified. No deployment until written permission. |
| MOHA Kathmandu citizenship PDF | unclear; local_only: true; **answer_evidence: true** (Leader-approved LOCAL-ONLY baseline 2026-10-11) | **OCR working** — 5 pages indexed, 15 questions verified. No redistribution; permission request pending. |
| Department of Passports pages | all rights reserved; local_only: true | Not approved for redistribution or answer evidence; do not commit copies. |
| Open Data Nepal Environment Statistics 2019 | confirmed open; CC BY-SA; local_only: false | Reference-only environmental data, not civic procedure. |

`make fetch` downloads only registry entries marked `confirmed open` to ignored `data/raw/`. `make index` processes eligible locally available sources to ignored `data/processed/` and `chroma_db/` and excludes sources not marked confirmed open and approved as answer evidence. See `data/sources.yaml` for URLs, terms notes, and attribution.

## 11. Evaluation

Day 3 baseline (2026-10-11) recorded in `docs/results.md`:

| Civic metric | Recorded value | Notes |
|---|---:|---|
| Questions in measured baseline | 15 | Verified citizenship questions from MOHA PDF |
| hit@5 | 100% | Dense search finds correct source for all 15 |
| Citation accuracy | 67% | 10/15 cited exact must_cite page |
| Answer correctness | 0% | Fake LLM returns raw OCR fragments |
| False refusal rate | 0% | No answerable questions refused |

The question file has 25 records: 15 verified (citizenship), 10 draft (7 driving-license, 3 out-of-scope). Synthetic fixture check is a pipeline check only, not a civic quality evaluation.

## 12. Project structure

~~~text
.
├── data/                 source registry; ignored raw/ and processed/ data
├── docs/                 decisions, source notes, story board, and results
├── eval/                 question drafts, runner, judge, and result helpers
├── frontend/             Streamlit interface
├── scripts/              source fetch, document processing, index, smoke check
├── src/api/              optional API package; not part of the verified app flow
├── src/generation/       prompts, answer schema/guard, provider, spend control
├── src/ingest/           extraction, cleanup, chunking, embedding storage
├── src/retrieval/        dense Chroma search
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

Latest run: **54 passed, 1 skipped**.

## 14. Known limitations and caveats

- **Real LLM integration blocked**: NVIDIA Nemotron 3 Super returns empty response for prompts containing passage content (even with 1 passage). Fake LLM works for plumbing; real quality evaluation needs fix (Day 4).
- **Only citizenship service indexed**: MOHA Kathmandu PDF (5 pages). Driving-license (Rules 2054) and passport sources not yet indexed/verified.
- **15 verified questions only**: All citizenship. Driving-license questions (10) remain draft.
- **No publisher permissions**: Local-only use approved by Leader; written permission required for public demo/deployment.
- **Search similarities are not probabilities**; refusal threshold (0.35) uncalibrated.
- **Answers may be wrong**. Verify any procedure with the responsible official office. This project is not legal advice.
- **OCR needs Tesseract** + `nep`/`eng` language packs. MOHA Kathmandu PDF now works; other scanned sources may need it.

## 15. Roadmap

From `docs/user-story-board.md` (Day 4+):

1. **Day 4 (Oct 13)**: BM25/hybrid search, prompt improvements, language handling.
2. **Day 5 (Oct 14)**: Reranker, evidence threshold tuning, guard threshold calibration.
3. **Day 6–7**: Glossary-based query expansion, error analysis.
4. **Day 8+**: Citizenship/passport sources, 80-question evaluation, adversarial testing.
5. **Day 11+**: Public demo, final evaluation, submission.

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
| Member 2 — Retrieval | (assigned) |
| Member 3 — Generation & Evaluation | (assigned) |
| Leader — Integration, UI, Repository, Deployment | **Harikrishna Pokhrel (HAliveKP)** |
| Presenter | **Harikrishna Pokhrel (HAliveKP)** — **CONFIRMED 2026-10-11** |
| Backup presenter | **aash-crest01** — **CONFIRMED 2026-10-11** |

## 18. Licence

The repository contains a `LICENSE` file with the MIT License for the project code. This code licence does not grant rights to redistribute the external source documents listed in `data/sources.yaml`.

## 19. Acknowledgements and data attribution

Open Data Nepal's Environment Statistics of Nepal 2019 record is attributed in `data/sources.yaml` to Open Knowledge Nepal / Open Data Nepal and credits source data to Nepal's Central Bureau of Statistics. Its dataset record lists Creative Commons Attribution Share-Alike and the Data Policy states: "Users are free to use, modify, and share datasets, provided they give appropriate attribution." It is retained as reference only and is not used as civic answer evidence.

Official MOHA and Department of Passports source URLs are listed in `data/sources.yaml` for tracking. Their content is local-only or all-rights-reserved as recorded there; no copies are included or redistributed. No publisher permission email has been sent by this work.

---

**Project notes:** `docs/results.md` records observed checks and measured metrics; `docs/decisions.md` records confirmed decisions (presenter, API cap, local-only approvals); `docs/user-story-board.md` tracks daily task status.