---
name: ocr-and-nepali-qa
description: 'Checks Tesseract nep+eng installation, Devanagari share, page numbers, marks pages usable/unusable.'
---
# ocr-and-nepali-qa Skill

Use when processing scanned Nepali PDFs that need OCR (`pytesseract` with `nep`/`eng`).

## Procedure

1. Verify Tesseract installed: `which tesseract` or `tesseract --list-langs` should show `nep`, `eng`, `osd`.
2. If Tesseract missing: install via official UB-Mannheim installer (`D:\tx` recommended for Windows); verify language packs downloaded.
3. For each PDF page flagged `low_devanagari_share` or `replacement_characters`: run `extract_pages(source, ocr=True, expected_language='ne')`.
4. After OCR, run `clean_pages(raw_pages)`; check `extraction_rating()` per page (`good`/`ok`/`bad`/`unusable`).
5. If `extraction_status == "unusable"`: text blanked; must NOT index (`build_index.py` skips it).
6. Visual QA: compare `data/processed/*.jsonl` `text` field against original PDF page images for Devanagari accuracy, page numbers, header/footer removal.

## Evidence (current session)

`docs/results.md` line 414: `Tesseract is not installed on this machine (which tesseract → not found)`. `docs/data-sources.md` line 16: `citizenship_kathmandu_requirements.pdf` requires OCR check. `tests/test_ingest_text_fixes.py` covers synthetic no-OCR case.
