# Khula Gyan

Cited answers from official Nepali documents, in Nepali and English.

Khula Gyan is an open-source project to help people understand government procedures from official documents. It should show the document and page behind each answer, and say when the available sources do not support an answer. It is not a source of legal advice.

## Project status

We are starting with one service: driving-license renewal. The dense retrieval adapter and pipeline contract are in place, but there are no approved source files or populated index yet. The generation implementation is available on `main`/`dev` but has not been merged into `Hkp`. Until reviewed source text, an index, and the answer module are available on this branch, the app returns `not_found`; it does not invent an answer or citation.

## Getting started

### Requirements

- Python 3.12
- Git
- Internet access for installing packages and downloading the embedding model on its first run
- An LLM provider and API key, once the team chooses one (do not commit the key)

On Windows, check that `py -3.12 -V` prints a Python 3.12 version. If `py` is not recognized, install Python 3.12 from the official Python downloads page, enable the launcher option if offered, then reopen PowerShell.

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and fill in the provider settings after the team agrees on a provider. Never share the completed `.env` file or commit it.

If PowerShell blocks activation, run the commands in a new Command Prompt instead:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
```

### macOS or Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

### Check the setup

With the virtual environment active, run:

```bash
python scripts/smoke_test_embedding.py
```

The first run downloads the embedding model and may take several minutes. The script checks that it can create vectors for five Nepali and five English examples. OCR also needs the separate Tesseract application and Nepali (`nep`) and English (`eng`) language data; OCR is optional for the first text-based PDF.

### Run the current app

After installing the requirements, start the UI from the repository root:

```bash
streamlit run frontend/app.py
```

The screen currently shows a clear not-found message until approved processed source text is indexed and `src/generation/answer.py` is present on this branch. Dense similarity scores are normalized to 0–1; they are not probabilities, and the guard threshold has not been calibrated. The search interface is `search(query, k=5, service=None)`.

### Prepare a local source document

Keep a source copy in `data/raw/` only after checking its reuse terms. The Day 2 processor supports PDF and HTML and keeps one JSONL row per source page. To see its options from a clean checkout, run:

```bash
python scripts/process_document.py --help
```

Scanned PDFs use Tesseract OCR when the text layer is empty or very short. Install Tesseract with Nepali (`nep`) and English (`eng`) language data before processing a scanned document.

## Project map

```text
data/raw/          Official source files; add only when usage terms allow
data/processed/    Extracted, cleaned text and chunks
docs/              Data sources, contracts, and project notes
eval/              Draft and verified evaluation questions
frontend/          Streamlit user interface
scripts/            Setup and data helper scripts
src/                Application code
```

Document extraction and Unicode cleanup live in `src/ingest/`; `scripts/process_document.py` writes cleaned, page-linked JSONL records into the ignored `data/processed/` folder.

## Safety and source policy

- Answer from retrieved passages only. Keep each passage connected to its document and page.
- Show citations beside supported answers. Return `not_found` when evidence is absent or weak.
- Do not commit API keys, `.env`, generated indexes, or source documents with unclear redistribution terms.
- Confirm a document is current and check its usage terms before relying on it or redistributing it.

## Team workflow

Use small branches and pull requests. The user-selected working branch is `Hkp`; shared `dev` was created from `main` on 2026-10-10. Keep the response contract in `docs/ask-response.schema.json` stable so work can proceed in parallel.

## Current project notes

- First service: driving-license renewal.
- Initial sources are candidates listed in `docs/data-sources.md`; verify their currentness before answering procedural questions.
- On `Hkp`, provider and model settings are still placeholders. `main`/`dev` has an OpenRouter implementation; coordinate before copying provider settings across branches. The application must not treat placeholder values in `.env.example` as credentials.
- The task board is in `docs/user-story-board.md`; checked commit history and measured evaluation results are tracked in `docs/results.md`.

