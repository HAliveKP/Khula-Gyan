---
name: stack-audit
description: 'Lists every dependency, whether used, whether needed, lighter alternative if exists.'
---
# stack-audit Skill

Use before submission to verify dependencies.

## Dependency audit (verified in `.venv`)

| Dependency | Used? | Needed? | Lighter alternative / note |
| `torch==2.14.1` | Yes (`BAAI/bge-m3` embeddings) | Yes | CPU-only; must install first. |
| `sentence-transformers==6.2.0` | Yes (`SentenceTransformer` load) | Yes | Required for `search()`. Installed 6.2.0 (updated from 6.1.0). |
| `chromadb==1.5.9` | Yes (`PersistentClient`, collection query) | Yes | Index storage; no lighter alternative. |
| `streamlit==1.66.1` | Yes (`frontend/app.py`) | Yes | UI framework. Installed 1.66.1 (updated from 1.65.0). |
| `rank-bm25==0.2.2` | Not actively used (dense search only) | Optional (future BM25/hybrid) | Can be removed until hybrid search needed. |
| `PyMuPDF==1.28.2` | Yes (`process_document.py` PDF text layer) | Yes | PDF processing. |
| `pdfplumber==0.11.7` | Yes (PDF text layer, tables) | Yes | Often used alongside `PyMuPDF`. |
| `fonttools==4.66.1` | Yes (`src/ingest/font_reference.json`, Preeti font repair) | Yes | Devanagari font repair for legacy PDFs. |
| `fastapi==0.140.1` | Not actively used (optional API in blueprint) | Optional | Can be removed; `uvicorn` also optional. Installed 0.140.1 matches. |
| `uvicorn==0.38.0` | Not actively used | Optional | Only needed with `fastapi`. Installed 0.38.0 matches. |
| `PyYAML==6.0.3` | Yes (`data/sources.yaml` read) | Yes | Source registry parsing. |
| `python-dotenv==1.2.1` | Yes (`.env` load) | Yes | Config/env loading. Installed 1.2.2; updated. |
| `pytesseract==0.3.13` | Yes (`_ocr_page` in `extract.py`) | Yes | Required when `ocr=True`. Binary (`tesseract`) + `nep`/`eng` packs must also be installed separately; not covered by this package. |
| `Pillow==12.3.0` | Yes (`PIL` import for image/OCR) | Yes | Image processing. Installed 12.3.0 (updated from 12.0.0). |
| `openai==3.27.0` | Yes (`LLM` provider adapter) | Yes | OpenAI-compatible API client. Installed 3.27.0 matches. |
| `jsonschema==4.26.0` | Yes (`src/generation/schema.py` validation) | Yes | Response schema validation. |
| `matplotlib==3.10.8` | Not actively used (no charts in current flow) | Optional (future `eval/make_charts.py`) | Can be removed until evaluation charts needed. |
| `pytest==9.1.1` | Yes (`tests/`) | Yes | Testing. Installed 9.1.1 matches. |
| `requests==2.32.5` | Yes (`scripts/fetch_sources.py`) | Yes | Source fetching. Installed 2.33.0; close match. |

## Unused / optional packages to consider removing

- `rank-bm25`: Not used in current dense-only retrieval. Can be removed until BM25/hybrid implemented (`docs/retrieval-score.md` mentions as future improvement).
- `fastapi` + `uvicorn`: Not used in verified app flow (only `frontend/app.py` Streamlit). Can be removed unless FastAPI deployment planned.
- `matplotlib`: Only needed for `eval/make_charts.py` (future). Can be removed until chart generation needed.

## Version conflicts / updates applied

- `sentence-transformers`: 6.1.0 → 6.2.0 (`requirements.txt` updated; installed in `.venv`).
- `streamlit`: 1.65.0 → 1.66.1 (`requirements.txt` updated; installed in `.venv`).
- `Pillow`: 12.0.0 → 12.3.0 (`requirements.txt` updated; installed in `.venv`).
- `python-dotenv`: installed 1.2.2 (close to 1.2.1). No conflict.
- `requests`: installed 2.33.0 (close to 2.32.5). No conflict.
