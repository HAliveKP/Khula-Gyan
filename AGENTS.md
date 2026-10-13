# Khula Gyan agent guide

Khula Gyan is a Nepali civic-document assistant that retrieves passages from approved documents and answers with page-linked citations. It must refuse when it cannot find reliable evidence and must not present itself as legal advice.

## Repository map

- `data/sources.yaml`: source URLs, publishers, reuse status, and local filenames. Legacy central-government sources tagged `legacy: true, answer_evidence: false`. New municipality charter entries with `service: palika_guide`, `municipality`, `district`, `province`, `format`, `reuse_status`, `local_only`, `answer_evidence`.
- `data/raw/`: local source downloads; ignored by Git.
- `data/processed/`: extracted page-linked JSONL; ignored by Git.
- `docs/`: response contract, source notes, task board, extraction notes, results log, pivot addendum.
- `eval/`: question sets (legacy + municipal), runner, result logging, judge, and chart helpers.
- `frontend/app.py`: Streamlit interface with municipality selector.
- `scripts/fetch_sources.py`: fetches locally allowed sources into `data/raw/`.
- `scripts/process_document.py`: extracts PDF/HTML into page-linked records (carries municipality fields).
- `scripts/build_index.py`: processes eligible local sources and builds Chroma.
- `scripts/smoke_test_embedding.py`: embedding model smoke check.
- `src/ingest/`: extraction, cleaning, chunking (with municipality fields), and embedding storage.
- `src/retrieval/search.py`: dense Chroma search with optional `municipality` filter; scores are 0–1 similarities, not probabilities.
- `src/generation/`: answer generation, citation guard, prompts, schema, and LLM provider adapter.
- `src/pipeline.py`: connects search and answer functions; wrong-municipality guard for Palika Guide.
- `tests/`: small synthetic fixtures and offline regression tests (including municipality filter tests).
- `chroma_db/`: generated local search index; ignored by Git.

## Setup and commands

Run from the repository root. Install GNU Make and Python 3.12 first.

- `make setup` creates `.venv` and installs pinned dependencies (CPU Torch first).
- `make fetch` downloads only sources marked `confirmed open` in the local registry.
- `make index` processes eligible local sources and builds the ignored Chroma index.
- `make test` runs the pytest suite.
- `make eval` runs the mock evaluator and fake generator on the synthetic fixture question and writes an ignored run record; it is not a civic quality metric.
- `make run` starts the Streamlit app.

## Branch and data rules

- Work on `Hkp` or a feature branch created from `Hkp`; open pull requests into `Hkp`.
- Never push to `main`, merge `dev` unless specifically tasked, or force-push. The `dev` branch was merged into `main` historically (PR #5) but this is now disallowed.
- The `hkp-opencode` branch contained opencode-specific config and must not be merged. A clean baseline `hkp-opencode-v2` (renamed to `hkp-feat-*` style) was created from `origin/main` with only `.opencode/`, `AUDIT_VERIFICATION_TABLE.md`, and `docx/`.
- MOHA pages are not cleared for redistribution. Department of Passports pages state all rights reserved. Fetch them locally only when appropriate, and keep them ignored; do not commit them.
- The MOHA Kathmandu citizenship PDF (`citizenship_kathmandu_requirements`) has Leader-approved LOCAL-ONLY baseline status (2026-10-11). It has `answer_evidence: true`, `approval_note`, `local_only: true`, `licence_status: unclear`. Any index built from it stays in gitignored `chroma_db/`; no Hugging Face deployment or commit until written permission is on file.
- **Legacy central-government sources** in `data/sources.yaml` are tagged `legacy: true, answer_evidence: false`. **New municipality charter entries** have `service: palika_guide`, `answer_evidence: false` until written permission is recorded with `approval_note`, `approved_on`, `approved_by`.
- Never commit raw source data, `.env` files, API keys, or the Chroma database. Only source data explicitly marked `confirmed open` with a quoted license may be considered for version control; generated/private copies stay local.
- Use only the license status and quote recorded in `data/sources.yaml`; do not infer permission from government hosting.

## Honesty and done criteria

- Do not invent source text, expected answers, citations, or evaluation numbers.
- Mark unverified questions as `draft`; use `-` for metrics that were not measured.
- A task is done only when the relevant tests pass and `README.md` and `docs/results.md` describe verified behavior and results accurately.
- Stop and ask before any run that could exceed the configured API spend cap. Paid calls require explicit provider rates and are blocked before sending if a request reservation would exceed `MAX_API_SPEND_USD`.

## Multi-subagent workflow

### Roles

- **Orchestrator** (main agent): makes decisions, delegates, resolves conflicts, only agent that commits. Appends one row per commit to `docs/results.md`.
- **Subagents** (spawned only for independent work; never repeat a search you delegated):
  1. **data-fetcher/processor**: fetches/processes municipality charters; owns `scripts/fetch_sources.py`, `scripts/process_document.py`, `data/raw/`, `data/processed/`, `src/ingest/extract.py`, `src/ingest/clean.py`.
  2. **retrieval**: implements `search()`, municipality filter, wrong-municipality guard; owns `src/retrieval/search.py`, `src/ingest/chunk.py`, `src/ingest/embed_store.py`, `scripts/build_index.py`.
  3. **generation**: answer generation, citation guard, prompts, schema, LLM adapter; owns `src/generation/`.
  4. **eval/verification**: `eval/run_eval.py`, `eval/check_questions.py`, `eval/questions.jsonl`, `eval/sweep_threshold.py`, tests in `tests/`.
  5. **docs**: `docs/*.md`, `README.md`, `docs/results.md`, `docs/user-story-board.md`, `docs/next-steps.md`, `docs/decisions.md`, `AGENTS.md`.
  6. **reviewer**: verifies claims in README/results against evidence before a task is marked done; did not write the code being reviewed.

### Parallelism

- Independent tasks run in parallel in one batch (e.g., data-fetcher + retrieval schema changes).
- Dependent tasks run in sequence: process → index → eval.

### File ownership

- Each subagent owns a disjoint set of files/directories listed in its brief.
- Two subagents never edit the same file in the same round.
- Shared files (`README.md`, `docs/results.md`, `docs/user-story-board.md`, `AGENTS.md`) are edited **only by the orchestrator or the docs subagent after others finish**.

### Isolation

- Code-editing subagents work in separate git worktrees/branches created from `Hkp` (e.g., `feature/data-fetcher-day2`, `feature/retrieval-municipality-filter`).
- The orchestrator merges, resolves conflicts, and runs the full test suite before any PR into `Hkp`.

### Briefs

Every subagent brief states:
- Goal
- Input files
- Owned files
- Forbidden actions
- Interface contract it must meet
- Exact output to return

### Return format

Each subagent returns a short report:
- What changed
- Commands run with real outputs
- What was not verified
- Open questions

The orchestrator **must not trust a report without re-running the key check** (tests, a quick file inspection).

### Verification

A separate **reviewer subagent** that did not write the code checks claims in `README.md` and `docs/results.md` against evidence before a task is marked done.

### Hard stops for all subagents

- No contacting publishers or sending email.
- No fetching sources not permitted by `data/sources.yaml`.
- No committing raw data, keys, or Chroma.
- Paid calls only with configured rates, and subagents share the single `MAX_API_SPEND_USD` cap, which the orchestrator allocates.
- Stop and ask the human on cap overruns, source-permission questions, or any listed human decision.

### Escalation

- If two subagents' outputs conflict, or a task needs a decision listed under "human decisions", stop and report to the human.

### Logging

The orchestrator appends one row per commit to `docs/results.md` (commit log format: date, full hash, author, message, task, check result).