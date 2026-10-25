# Agent guide: Palika Guide (Khula Gyan)

Palika Guide answers questions about Nepali municipal services from each municipality's citizen charter (नागरिक बडापत्र), in Nepali and English. Every answer cites a document and page. It must return `not_found` when the evidence is missing or weak, or when the question's municipality has no indexed charter. It must never answer from another municipality's charter or present itself as legal advice.

## Repository map

- `src/ingest/`: `extract.py` (PDF/HTML, Devanagari glyph-map repair, Preeti→Unicode, Tesseract OCR fallback), `clean.py` (NFC, header/page-number removal), `chunk.py`, `embed_store.py` (bge-m3 → Chroma).
- `src/retrieval/search.py`: `search(query, k=5, service=None, municipality=None)`. Dense Chroma search with filters. `score` is a 0–1 similarity, not a probability. Returns `[]` with no index.
- `src/generation/`: `answer.py` (`answer()` / `answer_with_trace()`), `prompt.py` (`PROMPT_VERSION`), `llm.py` (OpenAI-compatible client, key pool, disk cache, `mask()`), `spend.py` (spend cap), `guard.py` (score guard, quote grounding, support check), `schema.py`, `language.py`, `fake_llm.py`, `settings.py` (reads `config.yaml`).
- `src/pipeline.py`: `ask(query, service=None, municipality=None)`. Wrong-municipality guard (`MUNICIPALITY_ALIASES`) and response validation.
- `frontend/app.py`: Streamlit UI.
- `scripts/`: `fetch_sources.py`, `process_document.py`, `build_index.py`, `build_font_reference.py`, `make_readable_pdfs.py`, `smoke_test_embedding.py`, `smoke_test_llm.py`, `try_answer.py`, `demo_script.py`.
- `eval/`: `questions.jsonl`, `run_eval.py`, `check_questions.py`, `judge.py`, `sweep_threshold.py`, `make_charts.py`, `results_log.py`, `update_log.py`.
- `data/sources.yaml`: source register (URLs, rights, approvals). `data/raw/`, `data/processed/`, `data/readable/` are ignored.
- `docs/`: response contract (`ask-response.schema.json`, `response-contract.md`), `data-sources.md`, `extraction-notes.md`, `error-analysis.md`, `results.md` (work log and eval runs), `history/` (hackathon notes, read-only).
- `tests/`: offline pytest suite with synthetic fixtures.

## Commands

Run from the repository root with the venv active (`source .venv/Scripts/activate` on Windows Git Bash, `source .venv/bin/activate` elsewhere).

- `make setup`: create `.venv` and install CPU torch + `requirements.txt`. Use `make setup PYTHON=python` if `py -3.12` is not available.
- `make test` / `python -m pytest -q`: the offline suite (`pytest.ini` limits it to `tests/`).
- `make index` / `python scripts/build_index.py`: build `chroma_db/` from eligible sources in `data/raw/`.
- `make run` / `python -m streamlit run frontend/app.py`: start the UI.
- `make eval`: fake-LLM plumbing check on fixtures. Not a quality metric.
- `python eval/check_questions.py`: validate the question file.
- `python eval/run_eval.py --use-service-filter --use-municipality-filter --note "..."`: real eval. Appends a row to `docs/results.md`.
- `LLM_PROVIDER=fake` in `.env` runs everything without a key (answers are nonsense on purpose).

## Branches

Branch from `main` as `feature/…`, `fix/…` or `docs/…`, and open PRs into `main`. Never push directly to `main`, force-push, or rewrite shared history. Use Conventional Commits. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Data and secret rules

- Never commit `.env`, API keys, `data/raw/`, `data/processed/`, `data/readable/`, `chroma_db/`, `artifacts/` or `eval/runs/`. Never print a full key; use `mask()`.
- Municipal charters are local-only: none has a reuse grant. `scripts/build_index.py` indexes a source only if `answer_evidence: true` and either `licence_status: confirmed open`, or `local_only: true` with an `approval_note`. Do not set these fields without a human's decision, and do not infer permission from government hosting.
- Do not fetch sources that `data/sources.yaml` does not permit. Do not contact publishers.
- Real LLM calls need both cost rates set and stay under `MAX_API_SPEND_USD`. Stop and ask before any run that could exceed the cap.

## Honesty rules

- Do not invent source text, expected answers, citations or evaluation numbers.
- Expected answers in `eval/questions.jsonl` come only from real pages checked by a human. Unchecked questions stay `verified: false`.
- `docs/results.md` is append-only. Eval numbers come only from `eval/run_eval.py`; use `-` for anything not measured. Do not edit `docs/history/`.
- Use Unicode NFC whenever you compare Nepali text.
- A task is done only when the tests pass and the docs describe behaviour that was actually checked. Report what was not verified.
