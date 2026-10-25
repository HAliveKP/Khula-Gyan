# Contributing to Palika Guide (Khula Gyan)

Thanks for helping. This project answers citizen questions from official municipal documents, so **accuracy and source rights matter more than features**. Please read the rules below before opening a pull request.

By taking part you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md). Report security problems privately, as described in [SECURITY.md](SECURITY.md), not in public issues.

## Development setup

You need Python 3.12 and Git. GNU Make and Tesseract (`nep` + `eng`) are optional. Full details are in the [README](README.md#setup).

```bash
git clone https://github.com/HAliveKP/Khula-Gyan.git
cd Khula-Gyan

# with Make
make setup                     # if `py -3.12` is not found on Windows: make setup PYTHON=python

# or by hand (check `python --version` shows 3.12.x)
python -m venv .venv           # macOS/Linux: python3.12 -m venv .venv   |   uv: uv venv --python 3.12 .venv
source .venv/Scripts/activate  # Windows Git Bash;  macOS/Linux: source .venv/bin/activate
python -m pip install torch==2.14.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt

cp .env.example .env           # set LLM_PROVIDER=fake to work without an API key
```

## Running tests

```bash
make test                      # or: python -m pytest -q
python -m pytest tests/test_generation.py -q          # one file
python -m pytest tests/test_generation.py::test_good_answer_passes -q   # one test
python eval/run_eval.py --mock --fake-llm --note "plumbing" --no-write  # eval harness without index or key
```

The suite is offline. New code needs a test that uses synthetic fixtures (`tests/fixtures/`). Tests must never need real charter files, an index or an API key.

## Branches

- Branch from an up-to-date `main` and open pull requests into `main`.
- Names: `feature/<short-topic>`, `fix/<short-topic>`, `docs/<short-topic>` (for example `fix/preeti-ligatures`).
- Keep one topic per branch. Do not force-push shared branches or rewrite published history. A maintainer merges PRs.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```text
feat: add ward filter to search()
fix: keep number-only fee cells when removing page numbers
docs: explain local-only approval fields
test: cover Devanagari municipality aliases
```

Common types: `feat`, `fix`, `docs`, `test`, `refactor`, `build`, `chore`, `eval`, `data`. Write in the imperative and keep the subject under about 72 characters.

## Pull request checklist

- [ ] `python -m pytest -q` passes locally.
- [ ] No `.env`, API key, token or other secret anywhere in the diff, commit messages or screenshots.
- [ ] No source documents or generated data: nothing under `data/raw/`, `data/processed/`, `data/readable/`, `chroma_db/`, `artifacts/` or `eval/runs/`.
- [ ] `docs/results.md` is **append-only**: existing rows are not edited or deleted. Evaluation numbers come only from `eval/run_eval.py` (`-` when not measured), never typed by hand.
- [ ] Expected answers in `eval/questions.jsonl` come from real document pages that **a human checked personally**, never from an AI model or memory. Unchecked questions stay `verified: false`. `python eval/check_questions.py` reports `OK`.
- [ ] Nepali text is compared after Unicode **NFC** normalization (ingest cleaning, quote grounding, eval matching).
- [ ] Any change to the response shape keeps [docs/ask-response.schema.json](docs/ask-response.schema.json) and [docs/response-contract.md](docs/response-contract.md) in sync.
- [ ] The README and docs describe only behaviour you actually checked.

## Adding a municipality or document

1. **Check the rights first.** Record the publisher's reuse terms (quote them) in `data/sources.yaml`. Do not infer permission from the fact that a government site hosts the file. Without an open licence or written permission, the document may be used only locally (`local_only: true`) and must never be committed.
2. Put the file in `data/raw/` and add an entry to `data/sources.yaml` using the template comment in the Palika Guide section (`id: palika_<slug>`, `filename`, `url`, `service: palika_guide`, `lang: ne|en`, `municipality`, `district`, `province`, `format`, `date_seen`, `reuse_status`, `reuse_quote`, `local_only`, `answer_evidence`, `approval_note`, `approved_on`, `approved_by`).
3. Preview the extraction: `python scripts/process_document.py data/raw/<file> --service palika_guide --lang ne --municipality <Name> --district <District>`. Compare several pages with the original. Glyph and Preeti issues are described in [docs/extraction-notes.md](docs/extraction-notes.md).
4. `scripts/build_index.py` indexes a source only when `answer_evidence: true` and either `licence_status: confirmed open`, or `local_only: true` with an `approval_note`. Run `make index` and read the `SKIP` lines.
5. For a new municipality, add the canonical name to the selector in `frontend/app.py` and its romanized + Devanagari spellings to `MUNICIPALITY_ALIASES` in `src/pipeline.py`, with a test in `tests/`.
6. Add eval questions only after a human has checked the answer on the actual page (`must_cite` = source file + page).

A PR that adds a municipality changes code and the source register only. It never includes the document itself.
