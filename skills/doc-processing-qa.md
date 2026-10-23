---
name: doc-processing-qa
description: 'Doc processing QA: corruption, pages, Devanagari share.'
---
# doc-processing-qa Skill

Use when processing PDF/HTML sources for Palika Guide or legacy services.

## Procedure

1. Check file exists in `data/raw/`. If missing, fetch first (`fetch_sources.py --include-unclear` only if `licence_status` permits).
2. Run extraction:

```bash
.\.venv\Scripts\python.exe scripts\process_document.py data\raw\<filename> \
    --service palika_guide --lang ne --municipality <name> --district <district>
```

3. Inspect output at `data/processed/<stem>.jsonl`.
4. Check fields: `extraction_status` (`good`/`ok`/`unusable`), `extraction_note`, `page` (must match original).
5. If `extraction_status == "unusable"`: text is blanked; must NOT index.
6. If `low_devanagari_share` or `replacement_characters`: OCR needed (`pytesseract` with `nep`/`eng`); mark for review.
7. Count ratings: if `bad` > 0 or `unusable` > 0, do not index until fixed.

## Verification (when raw file exists)

```bash
.\.venv\Scripts\python.exe scripts\process_document.py data\raw\palika_pokhara_rates_2074_75.pdf \
    --service palika_guide --lang ne --municipality Pokhara --district Kaski
```

Expected: writes to `data/processed/palika_pokhara_rates_2074_75.jsonl`; prints page count and ratings (`good`, `ok`, `bad`).

If file missing: `FileNotFoundError`.
