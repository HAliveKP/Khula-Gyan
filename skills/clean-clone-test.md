---
name: clean-clone-test
description: 'Fresh clone, follow README exactly, run setup/fetch/index/test/eval/run. Reports missing steps honestly.'
---
# clean-clone-test Skill

Use before submission (or as `release-check` verification step).

## Procedure (run on this workspace; full fresh clone optional)

```bash
# 1. Verify tests
.\.venv\Scripts\python.exe -m pytest -q --basetemp=.pytest_tmp
# Expected: 95 passed, 7 skipped.

# 2. Check tracked secrets/data
git ls-files | grep -E "\.env$|data/raw/.*\.pdf|data/processed/|chroma_db/"
# Expected: empty.

# 3. Source registry
.\.venv\Scripts\python.exe -c "import yaml; s=yaml.safe_load(open('data/sources.yaml'))['sources']; print('Total:', len(s), 'Legacy:', sum(1 for x in s if x.get('legacy')), 'Palika:', sum(1 for x in s if x.get('service')=='palika_guide'), 'Open:', sum(1 for x in s if x.get('licence_status')=='confirmed open'))"
# Expected: 26 total (current count after updates); 14 legacy; 12 palika; 1 open.

# 4. Index status
ls chroma_db/ 2>/dev/null || echo "No chroma_db/"
# Expected: exists (previous attempt) but empty of civic data (`build_index.py` reports 0 indexed civic chunks).

# 5. Demo script
.\.venv\Scripts\python.exe scripts\demo_script.py
# Expected: refusal + wrong-municipality + 4 demo cases; no fabricated answers; pipeline imports OK.
```

## Report format

For each step: `Pass` / `Blocked` / `Partial` with one-line evidence (`pytest` count; `git ls-files` empty; `build_index.py` output; `demo_script.py` final lines). No invented claims.
