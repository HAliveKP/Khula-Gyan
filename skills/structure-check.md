---
name: structure-check
description: 'Checks file tree matches README docs, .gitignore covers data/index/.env, no stray files, no untracked secrets.'
---
# structure-check Skill

Use before submission to verify repository hygiene.

## Checks (verified 2026-10-23)

- `.gitignore` includes: `data/raw/`, `data/processed/`, `chroma_db/`, `.env`, `.env.*`, `eval/runs/`.
- `.gitignore` excludes: `.pytest_tmp/`.
- No tracked files in ignored folders: `git ls-files | grep -E "data/raw/.*\.pdf|data/processed/|chroma_db/|\.env$"` → empty (verified by `git status` clean of tracked data/index/secrets).
- `README.md` tree (`docs/user-story-board.md` section 12) matches real tree: `data/`, `docs/`, `eval/`, `frontend/`, `scripts/`, `src/`, `tests/`, `skills/`, `chroma_db/` (ignored), `.hermes/plans/` (new).
- `skills/` directory exists with 6 `.md` files (`env-setup.md`, `source-rights-check.md`, `doc-processing-qa.md`, `eval-runner.md`, `docs-sync.md`, `release-check.md`). Additional skills (`ocr-and-nepali-qa.md`, `guard-calibration.md`, `prompt-injection-tester.md`, `latency-profiler.md`, `ui-review.md`, `stack-audit.md`, `readme-audit.md`) added; `structure-check.md` is this file.
- `.env` exists locally (`.env` in workspace root, not tracked by Git — `git status` shows `.env` as untracked, not committed; `.env.example` tracked).
- `docs/submission_text.md` exists and references only verified behavior.
- `scripts/demo_script.py` exists; runs; clearly labels synthetic/non-realistic results; no fabricated citations.
- `docs/user-story-board.md` updated; `docs/results.md` updated; `README.md` updated; `docs/error-analysis.md` exists; `docs/submission_text.md` exists.

## Verification command

```bash
git status --short
# Expected: no untracked raw/index data committed; `.env` untracked (not committed); `.gitignore` effective.

cat .gitignore | grep -v "^#" | grep -v "^$"
# Expected: exclusions present.
```
