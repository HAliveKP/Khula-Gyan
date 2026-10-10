# Khula Gyan agent guide

Khula Gyan is a Nepali civic-document assistant that retrieves passages from approved documents and answers with page-linked citations. It must refuse when it cannot find reliable evidence and must not present itself as legal advice.

## Repository map

- `data/sources.yaml`: source URLs, publishers, reuse status, and local filenames.
- `data/raw/`: local source downloads; ignored by Git.
- `data/processed/`: extracted page-linked JSONL; ignored by Git.
- `docs/`: response contract, source notes, task board, extraction notes, and results log.
- `eval/`: question sets, runner, result logging, judge, and chart helpers.
- `frontend/app.py`: Streamlit interface.
- `scripts/fetch_sources.py`: fetches locally allowed sources into `data/raw/`.
- `scripts/process_document.py`: extracts PDF/HTML into page-linked records.
- `scripts/build_index.py`: processes eligible local sources and builds Chroma.
- `scripts/smoke_test_embedding.py`: embedding model smoke check.
- `src/ingest/`: extraction, cleaning, chunking, and embedding storage.
- `src/retrieval/search.py`: dense Chroma search; scores are 0–1 similarities, not probabilities.
- `src/generation/`: answer generation, citation guard, prompts, schema, and LLM provider adapter.
- `src/pipeline.py`: connects search and answer functions.
- `tests/`: small synthetic fixtures and offline regression tests.
- `chroma_db/`: generated local search index; ignored by Git.

## Setup and commands

Run from the repository root. Install GNU Make and Python 3.12 first.

- `make setup` creates `.venv` and installs pinned dependencies (CPU Torch first).
- `make fetch` downloads only sources marked `confirmed open` in the local registry.
- `make index` processes eligible local sources and builds the ignored Chroma index.
- `make test` runs the pytest suite.
- `make eval` runs the evaluator on verified questions and writes the run record.
- `make run` starts the Streamlit app.

## Branch and data rules

- Work on `Hkp` or a feature branch created from `Hkp`; open pull requests into `Hkp`.
- Never push to `main`, merge `dev` as part of setup, or force-push.
- MOHA pages are not cleared for redistribution. Department of Passports pages state all rights reserved. Fetch them locally only when appropriate, and keep them ignored; do not commit them.
- Never commit raw source data, `.env` files, API keys, or the Chroma database. Only source data explicitly marked `confirmed open` with a quoted license may be considered for version control; generated/private copies stay local.
- Use only the license status and quote recorded in `data/sources.yaml`; do not infer permission from government hosting.

## Honesty and done criteria

- Do not invent source text, expected answers, citations, or evaluation numbers.
- Mark unverified questions as `draft`; use `-` for metrics that were not measured.
- A task is done only when the relevant tests pass and `README.md` and `docs/results.md` describe verified behavior and results accurately.

