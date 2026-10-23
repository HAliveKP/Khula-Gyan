---
name: docs-sync
description: 'After verified change, updates README.md, docs/results.md, docs/next-steps.md, docs/user-story-board.md to match reality.'
---
# docs-sync Skill

Use after any verified code or data change to keep documentation accurate.

## Checklist

1. `README.md`: update setup/test/eval/run status table with exact test counts (`pytest` output).
2. `docs/results.md`: append commit log row (date, full hash, author, message, task, check result). Add evaluation table rows ONLY from real `eval/run_eval.py` runs on verified questions.
3. `docs/next-steps.md`: move tasks Backlog → In Progress → Done only when their completion check passes.
4. `docs/user-story-board.md`: sync day status and evidence lines.
5. `AGENTS.md`: sync branch rules, source rules, spend rules if changed.

## Verification

Compare claims in `README.md` and `docs/results.md` against actual command outputs (`pytest`, `git log`, `ls chroma_db/`, `cat data/raw/_manifest.json` if exists). If discrepancy exists, fix docs before marking task done.
