---
name: ui-review
description: 'Checks frontend/app.py for Nepali/English toggle, checklist, citations, mobile layout, accessibility, loading and error states.'
---
# ui-review Skill

Use when reviewing `frontend/app.py` for mobile, accessibility, bilingual support.

## Checks (verified 2026-10-23)

- `st.selectbox` municipality selector present (`"", "Bharatpur", ...`); `format_func` labels empty as `— Select a municipality —`.
- `service` selectbox with `palika_guide`, `driving_license`, `citizenship`, `passport`.
- `st.info()` banner explains refusal behavior ("If sources don't support response, says it cannot find the answer.").
- `st.spinner()` shows `"Searching official sources…"` during `ask()`.
- Response `status == "not_found"` shows `st.info()`; `status == "answered"` shows answer, checklist (`documents`/`fees`/`steps`/`where`), citations with `source · page`, `confidence`, and `disclaimer` (`"Verify procedures... This tool does not provide legal advice."`).
- `st.subheader()` for Answer and Citations; `st.expander()` for Checklist.
- `st.caption()` shows `Khula Gyan explains official procedures; it does not provide legal advice.`

## Known limits

- No language toggle (Nepali/English) in UI; questions are entered in any language (`lang` field in `eval/questions.jsonl` shows `ne`, `en`, `mixed`).
- No mobile-specific CSS; Streamlit's responsive layout handles it.
- No accessibility audit (screen reader tags on `st.selectbox` not verified).
- Loading state present (`st.spinner`); error state (`st.error`) present for exceptions.

## Verification command

```bash
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py --server.headless true --server.port 8501
# Confirm HTML serves; municipality dropdown renders; refusal message appears with empty index.
```
