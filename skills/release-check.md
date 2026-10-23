---
name: release-check
description: 'Clean-clone test following README exactly. Reports every missing step. Never reports synthetic results as civic quality.'
---
# release-check Skill

Use before submission. Follows README exactly. Reports missing steps honestly.

## Procedure

```bash
# 1. Fresh clone (optional; current workspace is sufficient for this session)
# 2. Setup
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt --no-cache-dir

# 3. Tests
.\.venv\Scripts\python.exe -m pytest -q --basetemp=.pytest_tmp
# Expected: 95 passed, 7 skipped (2026-10-23).

# 4. Fetch
.\.venv\Scripts\python.exe scripts\fetch_sources.py --include-unclear
# Expected: 1 fetched (opendatanepal_environment_statistics_2019); others skipped or fail (network).

# 5. Index
.\.venv\Scripts\python.exe scripts\build_index.py
# Expected: 0 eligible civic chunks (no approved palika sources); 0 indexed records.

# 6. Eval
.\.venv\Scripts\python.exe eval\run_eval.py --fake-llm --use-service-filter --use-municipality-filter --note "plumbing" --no-write --mock
# Expected: synthetic only; no civic metrics in docs/results.md.

# 7. Run
.\.venv\Scripts\python.exe -m streamlit run frontend\app.py --server.headless true --server.port 8501
# Expected: serves HTML; refusal path works (empty index → not_found).

# 8. Check docs accuracy
# Compare README.md line 276 (test count) with pytest output.
# Compare docs/results.md evaluation table with actual eval outputs.
# Report any discrepancy.
```

## Verification checklist

- [ ] `pytest` count matches `README.md`
- [ ] `fetch_sources.py` output matches reality (1 reference fetched; palika sources blocked)
- [ ] `build_index.py` reports 0 civic chunks (current state — no approved palika sources)
- [ ] `eval/run_eval.py` does NOT write mock metrics to `docs/results.md`
- [ ] `frontend/app.py` serves; refusal message appears
- [ ] No `.env`, raw data, or `chroma_db/` committed (`git status` clean of tracked secrets/data)
