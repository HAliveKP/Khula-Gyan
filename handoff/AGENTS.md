# OpenCode handoff instructions

## Project

Khula Gyan is a Nepali civic-document assistant intended to retrieve source passages and answer with page-linked citations. It should refuse unsupported questions and is not legal advice. Treat repository documentation as claims until verified against code or command output.

## Layout

- `data/sources.yaml`: source URLs, publishers, reuse notes, and eligibility.
- `data/raw/`, `data/processed/`: local source downloads and extracted records; keep ignored.
- `docs/`: decisions, story board, response contract, source/extraction notes, results, next steps.
- `eval/`: draft questions and evaluation scripts.
- `frontend/app.py`: Streamlit interface.
- `scripts/`: fetch, process, build index, embedding smoke check.
- `src/ingest/`, `src/retrieval/`, `src/generation/`, `src/pipeline.py`: ingestion, search, answer generation, and flow.
- `tests/`: synthetic/offline checks; `chroma_db/` is a generated local index and must be ignored.
- `handoff/opencode/`: OpenCode agent prompts and slash commands.

## Commands

Run from repo root with Python 3.12 and GNU Make where available:

- `make setup` — create environment/install pinned requirements.
- `make fetch` — fetch only eligible confirmed-open sources.
- `make index` — process eligible local sources and build ignored Chroma index.
- `make test` — run pytest.
- `make eval` — run configured evaluation target; distinguish synthetic checks from civic quality metrics.
- `make run` — start Streamlit.

Do not state a command succeeded unless you ran it and saw success. Check Makefile behavior before relying on these targets.

## Branch and data rules

- Work on Hkp or a feature branch based on Hkp; PR into Hkp.
- Never push to main, merge dev unless specifically tasked, or force-push.
- MOHA and Department of Passports pages are local-only and gitignored; do not commit their copies.
- Only sources marked `confirmed open` in `data/sources.yaml` with a literal quoted reuse license may be considered for committing. Do not infer permission from government hosting.
- Never commit raw/processed data, Chroma, `.env`, or API keys.
- Stop and ask before any run that could exceed `MAX_API_SPEND_USD`; paid calls require explicit provider rates and a preflight reservation.

## Honesty

- Do not invent source text, expected answers, citations, permissions, names, or evaluation numbers.
- Label claims VERIFIED, TOLD, or ASSUMED when evidence provenance matters.
- Mark unverified questions `draft`; unmeasured metrics are `-`.
- README and `docs/results.md` must describe only verified state.

## Close-out protocol

Use `/closeout` after each task: verifier first; safely back up and update the storyboard with Status, Evidence, Last updated, Notes, preserving history and adding new work rows; then readme-writer; then docs-updater; check cross-file consistency and secret/data tracking; run relevant checks and report exact outputs, remaining tasks, and human decisions. Never mark DONE without proof.
