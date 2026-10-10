# Khula Gyan

Khula Gyan is a Nepali civic-document assistant that retrieves passages from public service documents and answers with page-linked citations. It should refuse when the available evidence does not support an answer and is not a source of legal advice.

## Current status

The repository contains the Streamlit app, document processing, Chroma indexing, dense search, citation-aware generation, and an evaluation runner. The source register currently has no confirmed-open civic answer source; MOHA sources are unclear and Department of Passports pages state all rights reserved. Those sources are fetched locally only when permitted and are not included in the index. The explicitly share-alike licensed Open Data Nepal environmental dataset is unrelated to civic procedures and excluded from answer evidence; a separate health dataset has no specified license and is also excluded. No performance metric is claimed until measured on verified questions.

## Presentation assignment

The presenter is **provisionally the Leader role** because that role owns integration, UI, repository, and deployment. **Backup candidate: `aash-crest01` (provisional, unconfirmed)** based on recorded Member 3 work; the team must confirm both people before the presentation.

## API spend safety

The provisional API spend cap is **USD $1.00 per process run** (`MAX_API_SPEND_USD`). Confirm or change it with the project owner. Before paid API requests, set `LLM_INPUT_COST_PER_1M_USD` and `LLM_OUTPUT_COST_PER_1M_USD` to the selected provider's current prices; requests are blocked if prices are unset or the estimated reservation would exceed the cap. `MAX_API_OUTPUT_TOKENS` bounds each request. Estimates use provider-reported token counts when available and are not invoices.

## Requirements and setup

Use Python 3.12, Git, and GNU Make. The first setup installs pinned Python packages and the CPU-only PyTorch wheel. It needs network access and enough disk space for the embedding model.

Run these from the repository root:

```sh
make setup
make test
make run
```

The first embedding run downloads `BAAI/bge-m3`:

```sh
.venv/bin/python scripts/smoke_test_embedding.py
```

On Windows, use `.venv/Scripts/python.exe scripts/smoke_test_embedding.py` instead. OCR of scanned documents additionally requires the Tesseract application and Nepali (`nep`) and English (`eng`) language packs.

## Local source workflow

`data/sources.yaml` records source URLs and reuse status. `make fetch` downloads only entries marked `confirmed open` into ignored `data/raw/`. `make index` processes locally present, eligible sources into ignored `data/processed/` and `chroma_db/`. Never commit raw data, processed copies, generated indexes, `.env` files, or API keys. Do not use a source as answer evidence unless its reuse terms and content have been reviewed.

## Run commands

- `make fetch` downloads sources whose terms are confirmed open.
- `make index` processes eligible local sources and builds the ignored Chroma index.
- `make test` runs offline tests using synthetic fixtures.
- `make eval` runs the offline mock evaluator and fake generator on a synthetic fixture and writes an ignored run record. This is a harness check, not a civic quality metric.
- `make run` starts the Streamlit interface.

See `AGENTS.md` for branch rules, source handling requirements, and the repository map. Keep `docs/results.md` limited to checks and evaluation results that were actually observed.

