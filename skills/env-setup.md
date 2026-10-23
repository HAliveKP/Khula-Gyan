---
name: env-setup
description: 'Use when setting up Khula Gyan dev env. Creates venv, installs CPU Torch first, pinned deps, verifies with pip check, pytest, embedding smoke test.'
category: 'devops'
---
# env-setup Skill

Use when setting up the Khula Gyan development environment.

## Procedure

```bash
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install torch==2.14.1 --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r requirements.txt --no-cache-dir
.\.venv\Scripts\python.exe -m pip check
# Expected: No broken requirements found.
.\.venv\Scripts\python.exe -m pytest -q --basetemp=.pytest_tmp
# Expected: 95 passed, 7 skipped (verified 2026-10-23).
```

After `sentence-transformers` and `streamlit` are installed (if missing from initial install):

```bash
.\.venv\Scripts\python.exe -m pip install sentence-transformers streamlit
.\.venv\Scripts\python.exe scripts\smoke_test_embedding.py
# Expected: Embedding smoke check passed: 10 examples (5 Nepali + 5 English), vector size 1024.
```

## Verification checklist

- [ ] `.venv/` exists
- [ ] `pip check` reports "No broken requirements found."
- [ ] `pytest -q --basetemp=.pytest_tmp` passes with 95 passed, 7 skipped
- [ ] `streamlit` import works
- [ ] `scripts/smoke_test_embedding.py` runs (requires model download; may time out in restricted networks)
