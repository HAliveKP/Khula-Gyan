# Khula Gyan

Cited answers from official Nepali documents, in Nepali and English.

Khula Gyan is an open-source project to help people understand government procedures from official documents. It should show the document and page behind each answer, and say when the available sources do not support an answer. It is not a source of legal advice.

## Project status

We are starting with one service: driving-license renewal. The first milestone is a local app that can show a cited answer from one official source. Citizenship and passport support come after that flow works.

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

## Safety and source policy

- Answer from retrieved passages only. Keep each passage connected to its document and page.
- Show citations beside supported answers. Return `not_found` when evidence is absent or weak.
- Do not commit API keys, `.env`, generated indexes, or source documents with unclear redistribution terms.
- Confirm a document is current and check its usage terms before relying on it or redistributing it.

## Team workflow

Use small branches and pull requests. The user-selected working branch is `Hkp`. Agree as a team before creating shared `dev` or `main` branches. Keep the response contract in `docs/ask-response.schema.json` stable so work can proceed in parallel.

## Current project notes

- First service: driving-license renewal.
- Initial sources are candidates listed in `docs/data-sources.md`; verify their currentness before answering procedural questions.
- LLM provider and model are not selected yet. The application must not treat placeholder values in `.env.example` as credentials.
- The Day 0 task board is in `docs/user-story-board.md`.

