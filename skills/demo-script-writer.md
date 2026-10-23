---
name: demo-script-writer
description: 'Writes demo script with 2 Nepali, 2 English, 1 refusal, 1 wrong-municipality. Clearly labels synthetic/non-realistic.'
---
# demo-script-writer Skill

Use to create or verify `scripts/demo_script.py`.

## Requirements (from user's request / docs/submission_text.md)

- 2 Nepali questions (`service="palika_guide"` + `municipality` filled, `verified` status documented).
- 2 English questions (same structure).
- 1 refusal (`service="palika_guide"`, `municipality` empty or unknown; `not_found` message).
- 1 wrong-municipality (`service="palika_guide"`, municipality named with no indexed charter; `not_found` message).
- Every result clearly states `not_found` or `Result (no index)`; no synthetic answers claimed as real.
- Pipeline verification (`search`, `answer`, `ask` imports) included.
- Index status (`chroma_db/`, `data/raw/` palika files) printed honestly.
- Final status banner confirms: NO municipality charters indexed; NO civic metrics measured; real LLM blocked.

## Verification

Run: `.\.venv\Scripts\python.exe scripts\demo_script.py`
Check output lines contain `not_found`, `Result (no index):`, and final banner (`DEMO COMPLETE — No synthetic answers claimed as real.`).
