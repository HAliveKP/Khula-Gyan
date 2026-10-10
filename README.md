# Khula Gyan

A Nepali civic-document assistant prototype that retrieves document passages and aims to answer with page-linked citations. It must refuse when evidence is insufficient and is not legal advice.

## 1. Project status and badges

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)]

No build or test status badge is configured. A LICENSE file exists (MIT), and the repository targets Python 3.12.

The code and synthetic plumbing checks are present. No verified civic source-backed answer has been demonstrated yet.

## 2. What it does and who it is for

Khula Gyan is intended for people who need help finding information in Nepali public-service documents, and for the student team building and reviewing that assistant. It is a retrieval-augmented generation (RAG) prototype: it searches source passages, asks a language model to answer from those passages, and returns citations that identify a source and page. It should say it cannot answer when the available evidence does not support a response.

## 3. Demo

**Demo coming.** There is no real project screenshot or GIF in the repository. A recorded headless Streamlit launch returned HTTP 200, but the test query returned `not_found` with no citations because no civic answer index was available. That is not a working civic-answer demo.

## 4. Features

### Working in the repository

- PDF/HTML document processing code preserves page and source metadata; the HTML processor has a synthetic fixture test.
- Dense Chroma retrieval code supports service filtering and reports a 0–1 similarity score. A small synthetic Chroma test checks result limits, score range, and filtering. Scores are similarities, not probabilities.
- The answer schema, citation guard, and provider adapter are implemented. Provider calls are protected by a per-process spend cap and fail closed if paid-provider rates are not configured.
- The Streamlit question-and-answer screen exists. Its recorded headless launch returned HTTP 200; a source-backed answer remains unverified.
- The evaluation runner supports draft-question skipping. The offline fixture is a pipeline check only, not a civic quality evaluation.

### Planned or not yet verified

- A permitted civic source set, processed civic pages, and an index containing civic answer evidence.
- A complete real-source question → retrieval → answer → citation flow.
- Human-verified civic evaluation questions and a real quality baseline.
- BM25/hybrid retrieval, reranking, and a public deployment.

## 5. How it works

The intended data path is:

~~~mermaid
flowchart LR
  S["Reviewed local PDF or HTML"] --> P["Extract text with page and URL"]
  P --> C["Chunk while retaining metadata"]
  C --> E["BAAI/bge-m3 embeddings"]
  E --> V["Chroma index"]
  Q["User question"] --> R["Dense retrieval"]
  V --> R
  R --> G["Answer generation"]
  G --> A["Schema and citation-grounding checks"]
  A --> O["Answer with source, page, and quote"]
  A --> N["not_found when evidence is insufficient"]
~~~

The repository has these components, but an indexed, permitted civic source and a cited answer have not been verified. The current search score is a normalized cosine similarity from 0 to 1; it is not a calibrated confidence or probability.

## 6. Tech stack and pinned versions

Versions below are copied from requirements.txt:

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
- GNU Make for the Makefile commands.
- Network access and enough free disk space for dependency installation and the BAAI/bge-m3 embedding model download.
- Tesseract plus the Nepali (nep) and English (eng) language packs only when OCR of scanned documents is needed.
- A paid LLM provider is optional. To use one, select a provider/model, configure its current rates, and keep its key in a local .env file. No API key is needed for the fake provider or synthetic tests.

## 8. Quick start and command verification

Run the commands from the repository root. The Makefile defines these commands:

~~~sh
make setup
make fetch
make index
make test
make eval
make run
~~~

Observed status in this setup environment:

| Make command | Observed status |
|---|---|
| make setup | Attempted and failed before setup: GNU Make is unavailable. PowerShell reported: “The term 'make' is not recognized as a name of a cmdlet, function, script file, or executable program.” |
| make fetch | Make target not run. It downloads only sources currently marked confirmed open. |
| make index | Make target not run. A separately recorded builder run processed one page, found 0 eligible civic chunks, and indexed 0 records. |
| make test | Make target not run because GNU Make is unavailable. The equivalent local pytest command below ran and passed. |
| make eval | Make target not run. The offline fixture runner was exercised by the passing test suite; this is not a civic evaluation. |
| make run | Make target not run. A separate headless Streamlit launch returned HTTP 200, but its query returned not_found without citations. |

The latest direct test command run in this checkout was:

~~~powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp=.pytest_tmp
~~~

Observed output: **6 passed in 4.28s** (latest close-out run). To use the documented setup commands on Windows, first install GNU Make and Python 3.12. The embedding smoke command is:

~~~powershell
.\.venv\Scripts\python.exe scripts/smoke_test_embedding.py
~~~

The setup record reports that this smoke check passed for 10 examples (5 Nepali and 5 English), with vector size 1024. It also reports a warning that available cache space was slightly below the model's advertised download size.

## 9. Configuration

Copy .env.example to .env and set local values. Never commit .env or include real keys in source, documentation, or issue comments.

| Variable | Example / default | Use |
|---|---|---|
| LLM_PROVIDER | openrouter (or fake) | Select the provider; fake avoids API calls and returns deliberately non-realistic answers. |
| LLM_BASE_URL | https://openrouter.ai/api/v1 | OpenAI-compatible provider endpoint. |
| LLM_MODEL | choose-with-team | Select a model with the team. |
| LLM_API_KEYS | blank in example | Provider secret; supply locally only. |
| LLM_KEY_STRATEGY | optional; commented example | Optional key-pool behavior. |
| MAX_API_SPEND_USD | 1.00 | Provisional per-process cap; a human must confirm or change it. |
| LLM_INPUT_COST_PER_1M_USD | blank | Set the selected provider's current input price; blank blocks paid calls. |
| LLM_OUTPUT_COST_PER_1M_USD | blank | Set the selected provider's current output price; blank blocks paid calls. |
| MAX_API_OUTPUT_TOKENS | 1024 | Maximum output reservation/request size per provider call. |

Paid calls are stopped before sending when rates are missing or a request's estimated reservation would exceed the cap. Stop and ask before any run that could exceed the cap. Estimates are not invoices.

## 10. Data and licensing

The current source registry is data/sources.yaml. It has no civic source approved as answer evidence; all registered entries currently have answer_evidence: false. No MOHA, Department of Passports, or DoTM content is redistributed.

| Source group | Registry status | Current use |
|---|---|---|
| DoTM driving-license pages/manual | unclear; local_only: true | Not approved as answer evidence. Request permission before broader reuse; do not commit copies. |
| MOHA citizenship pages | unclear; local_only: true | Not approved as answer evidence. Request permission before broader reuse; do not commit copies. |
| Department of Passports pages | all rights reserved; local_only: true | Not approved for redistribution or answer evidence; do not commit copies. |
| Open Data Nepal health/NCD dataset page | unclear; local_only: true; its dataset metadata says “License Not specified” | Unrelated to civic procedures and excluded. |
| Open Data Nepal Environment Statistics of Nepal 2019 datasets | confirmed open; Creative Commons Attribution Share-Alike; local_only: false | Reference-only environmental data, unrelated to civic procedures; not answer evidence and excluded from the civic index. |

No explicitly open-licensed procedural civic source has been verified. The source register quotes the Open Data Nepal policy: “Users are free to use, modify, and share datasets, provided they give appropriate attribution.” The environment dataset is retained only as an openly licensed reference record; the source register says its source data is credited to the Central Bureau of Statistics. Do not treat that dataset as evidence for civic-service answers.

make fetch downloads only registry entries marked confirmed open, to ignored data/raw/. It does not fetch unclear or all-rights-reserved entries. Use official local-only materials only after the team confirms private-use permission; do not redistribute them. make index processes eligible locally available sources to ignored data/processed/ and chroma_db/ and excludes sources not marked confirmed open and approved as answer evidence. See data/sources.yaml for URLs, terms notes, and attribution.

## 11. Evaluation

The evaluation table in docs/results.md contains no measured civic baseline. The recorded Day 0–2 baseline values are:

| Civic metric | Recorded value |
|---|---:|
| Questions in measured baseline | - |
| hit@5 | - |
| Citation accuracy | - |
| Answer correctness | - |
| Refusal rate | - |

The question file has 25 records, 0 verified and 25 drafts (20 answerable drafts and 5 out-of-scope drafts). There are no source-backed expected answers yet. The synthetic fixture check does not count as civic evaluation and its mock percentages are not quality scores. Unmeasured values remain “-”.

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

Run the full test suite with:

~~~sh
make test
~~~

The suite covers synthetic HTML processing and source/service metadata, top-k and score-range checks plus service filtering with a temporary Chroma index, evaluation output and draft skipping, a Git tracking guard for raw/processed/index data, and pre-send API spend-cap behavior.

The direct pytest command was run in this setup environment and reported **6 passed**. GNU Make is not installed here, so the Makefile test target itself was not run.

## 14. Known limitations and caveats

- There is no approved civic answer source or populated civic index. A real source-backed civic answer has not been demonstrated.
- 0 of 25 evaluation questions are verified. Do not read mock results as quality measurements.
- Nepali and English processing paths exist, but answer quality, spelling, and language consistency have not been evaluated on verified civic material.
- Source freshness and page-specific procedural accuracy have not been checked through an end-to-end indexed answer.
- Search similarities are not calibrated probabilities; the refusal threshold is not calibrated against verified questions.
- Answers may be wrong. Verify any procedure with the responsible official office. This project is not legal advice.
- OCR needs Tesseract and its language packs. No official PDF/page visual QA is recorded.
- The Streamlit process can start, but without an eligible civic index it returns not_found rather than a supported cited answer.

## 15. Roadmap

No Excel storyboard workbook was found in the repository. The open-task summary below is from docs/user-story-board.md, which remains the available planning source.

1. **Source permission and extraction:** obtain written permissions or identify suitable explicitly open-licensed civic procedure sources; process allowed documents and visually inspect page numbers and Nepali text.
2. **First end-to-end service:** build an index from approved source pages and verify retrieval, answer, citation, and refusal behavior.
3. **Day 3 baseline:** verify expected answers and sources, then measure hit@5, citation accuracy, correctness, and refusal metrics.
4. **Search and answer quality:** the board schedules BM25/hybrid search, possible reranking, Nepali/English wording checks, and evidence-threshold tuning after a baseline exists.
5. **Release preparation:** later board items include error analysis, deployment checks, final evaluation, a demo recording, and submission checks. They remain planned.

## 16. Contributing

- Work on Hkp or on a feature branch created from Hkp.
- Open pull requests into Hkp. Do not push changes to main or force-push.
- Make small commits with clear messages such as feat:, fix:, test:, or docs:.
- Before opening a PR, run make test and review README.md and docs/results.md for claims that need evidence.
- Track tasks in docs/user-story-board.md; update statuses only when the documented completion checks pass.
- Follow AGENTS.md for source, secret, generated-data, and API-spend rules.

## 17. Team and roles

The project documents roles rather than assigning personal names:

- Member 1 — Data & Documents.
- Member 2 — Retrieval.
- Member 3 — Generation & Evaluation.
- Leader — Integration, UI, Repository, and Deployment.
- Presenter — **provisionally the Leader role**. Backup candidate: **aash-crest01**, provisional and unconfirmed. These assignments require human confirmation; the username is not a verified personal name.

## 18. Licence

The repository contains a LICENSE file with the MIT License for the project code. This code licence does not grant rights to redistribute the external source documents listed in data/sources.yaml.

## 19. Acknowledgements and data attribution

Open Data Nepal's Environment Statistics of Nepal 2019 record is attributed in data/sources.yaml to Open Knowledge Nepal / Open Data Nepal and credits source data to Nepal's Central Bureau of Statistics. Its dataset record lists Creative Commons Attribution Share-Alike and the Data Policy states: “Users are free to use, modify, and share datasets, provided they give appropriate attribution.” It is retained as reference only and is not used as civic answer evidence. Source details: https://opendatanepal.com/dataset/environment-statistics-of-nepal-2019 and https://opendatanepal.com/privacy-policy.

Official MOHA and Department of Passports source URLs are listed in data/sources.yaml for tracking. Their content is local-only or all-rights-reserved as recorded there; no copies are included or redistributed. No publisher permission email has been sent by this work.

Additional project notes: docs/results.md records observed checks and unmeasured metrics; docs/decisions.md records provisional source, presenter, and spend-cap decisions.
