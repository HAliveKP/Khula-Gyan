---
name: readme-audit
description: 'Every README claim must map to command output. No unverified claims allowed.'
---
# readme-audit Skill

Use before submission to verify `README.md` accuracy.

## Audit checklist (verified 2026-10-23)

### Claims verified against actual output

- Line 1 (`A Nepali civic-document assistant prototype...`): Verified (`frontend/app.py` title/caption matches; `AGENTS.md` line 3 confirms).
- Line 10 (`Day 8 = Oct 21`): Verified (`docs/user-story-board.md` line 3; `docs/next-steps.md` line 4).
- Line 13 (`Presenter/backup: to be confirmed by a human`): Verified (`docs/decisions.md` §5; `docs/user-story-board.md` line 12).
- Line 21 (`Local demo available. Run make run... No municipality charters indexed yet`): Verified (`frontend/app.py` launches; `build_index.py` reports 0 civic chunks; `chroma_db/` exists but empty; `README.md` line 280 updated to reflect reality).
- Line 28-32 (`Features — Working in repository`): Verified (`pytest` passes; `search()` works; `answer()` loads; `pipeline.py` connects; `streamlit` launches).
- Line 34 (`Tesseract OCR...`): Partial — `pytesseract` installed; binary + `nep`/`eng` not installed (`docs/results.md` records block).
- Line 42 (`30 draft questions`): Updated to 40 questions (`README.md` line 41 updated); `eval/questions.jsonl` has 39 verified + 1 draft.
- Line 44 (`Not yet verified / Day 1-8`): Updated (`README.md` line 44-51 reflects current verified state: 95 passed; index blocked; questions verified; real LLM blocked; no permissions).
- Line 97 (`Quick start`): Commands verified (`python -m pytest`, `.venv` setup, `fetch_sources.py`, `build_index.py`, `streamlit run`). Note: `make` unavailable in this Windows environment; direct Python commands work.
- Line 145-156 (`Observed status`): Updated (`README.md` line 149-157 reflects 95 passed, streamlit launches, index blocked, real LLM blocked, no verified civic metrics).
- Line 213-218 (`Legacy sources...`): Verified (`data/sources.yaml` has 11 legacy sources tagged `legacy: true` + 12 palika sources + 1 reference).
- Line 219 (`All legacy sources tagged...`): Verified (`data/sources.yaml` line 1-226).
- Line 223-224 (`Day 4 baseline...`): Verified (`docs/results.md` evaluation table shows `-` for civic metrics; real baseline blocked).
- Line 242 (`Project structure`): Verified (`ls -R` matches; `chroma_db/` exists; `data/raw/` has 1 reference file; `data/processed/` missing; `skills/` new).
- Line 260-264 (`Testing`): Verified (`pytest -q --basetemp=.pytest_tmp` → 95 passed, 7 skipped; `tests/test_build_index.py` passes; `tests/test_ingest_text_fixes.py` passes).
- Lines 277-286 (`Known limitations and caveats`): Updated (`README.md` line 277-287 reflects 95 passed, 39 verified questions, index blocked, real LLM blocked, wrong-municipality guard working, OCR blocked).
- Line 300 (`Stretch only...`): Unchanged.

### Mismatches fixed (commit `5e07f76`)

- Test count (`54 passed` → `95 passed`).
- Question count (`30 drafts` → `40 questions` with verification status described).
- `README.md` limitations updated (real LLM blocked; index blocked; verified set count accurate).
- `README.md` evaluation section updated (metrics remain `-` until index exists).

### No mismatches found in claims about

- Pipeline design (`search()` → `answer()`; `municipality` filter; citation guard; refusal on empty chunks).
- Source registry (`data/sources.yaml` entries match descriptions).
- Safety rules (`wrong-municipality guard`; `service` filter; `local_only` restrictions; no redistribution of unclear sources).
- Data hygiene (raw/processed/index excluded from Git; `.env` excluded).
- Branch rules (`Hkp` only; PRs into `Hkp`; no direct `main` pushes without task; `dev` merge disallowed going forward).

## Evidence commands

```bash
.\.venv\Scripts\python.exe -m pytest -q --basetemp=.pytest_tmp
# Expected: 95 passed, 7 skipped.

.\.venv\Scripts\python.exe scripts\demo_script.py
# Expected: 6 demo sections; refusal + wrong-municipality; no fabricated answers.

cat docs/submission_text.md | head -10
# Expected: problem/idea/powers-it sections present; only verified claims.

ls skills/
# Expected: 6 skills (.md files).

grep -n "95 passed" README.md; grep -n "40 questions" README.md; grep -n "not_found" README.md
# Expected: all present; no unverified claims (e.g., no "hit@5=100%" for palika).
```
