# Next steps

This list maps the current blockers to `docs/user-story-board.md` for the Palika Guide pivot (Day 1 = Oct 14 ... Day 8 = Oct 21). Priorities reflect dependencies: human decisions come first, then one approved source-backed flow, then improvements only against measured failures.

## Priority 0 — Resolve human decisions

- **Project owner — Day 1 feasibility sheet; Day 2 fetch/process charters**: send the draft permission request in `docs/permission_request.md` to the relevant municipalities and record any written permission. Until an appropriate civic source is approved for the intended processing and demo use, keep official charters local-only and do not index them as civic evidence.
- **Leader / whole team — Day 1 schema & eval format**: confirm the provisional Leader presenter, backup candidate, and the $1.00 per-process API cap (already configured for NVIDIA free tier). Configure provider input/output rates only after selecting a provider. Until then, paid requests remain blocked.
- **Whole team — Day 1 municipality selection**: pick up to 5 municipalities from the Day 1 feasibility sheet that have usable text/HTML charters. Reduce if feasibility check finds fewer.

## Priority 1 — Establish one approved source-backed flow

- **Member 1 — Day 1 feasibility sheet; Day 2 fetch/process**: locate at least 5 municipalities with explicitly reusable citizen charters (text PDF or HTML). A scanned PDF without OCR is not usable. Keep original files in ignored `data/raw/`; never commit them without permission.
- **Member 1 — Day 2 process**: extract text page by page from the chosen charters; record extraction quality; fix obvious text/Unicode problems. Visually inspect Nepali text and page numbers against the original.
- **Member 2 — Day 2 schema & index**: charter-row chunking that carries `municipality`, `district`, `ward`, `section` through to Chroma metadata. `search()` gains `municipality` filter; `ask()` gains wrong-municipality guard.
- **Member 2 — Day 3 index**: build Chroma index from approved local charters; first real question → cited answer with municipality filter.
- **Leader — Day 3 integration**: `ask()` connects real `search()` and `answer()` with municipality filter; wrong-municipality guard returns `not_found` for missing/unknown municipality; UI has municipality selector.

## Priority 2 — Improve only against measured failures

- **Day 4 baseline**: run `eval/run_eval.py` with real search + fake LLM (or real if LLM fixed) on 20-25 verified questions; record BASELINE in `docs/results.md` (only real numbers from the runner). List the ten most important failures.
- **Day 5+**: fix top failures from baseline; calibrate `guard_min_score` with `eval/sweep_threshold.py`; improve checklist fields (fee, time, officer); improve prompt for same-language answers and valid JSON; add municipality selector to UI.
- **Day 6+**: error analysis in `docs/error-analysis.md`; adversarial/wrong-municipality/out-of-scope tests; test deploy on Hugging Face Spaces (or documented fallback).
- **Day 7+**: grow verified set honestly (target 40; report real count); final eval; clean-machine README test.
- **Day 8**: code freeze; final README/results; demo script (2 Nepali, 2 English, 1 refusal, 1 wrong-municipality); submission text; tag.

## Current blockers (2026-10-13)

1. **No municipality charters approved yet** — need Day 1 feasibility sheet and written permission.
2. **No municipality filter in search** — must be implemented on Day 2.
3. **No wrong-municipality guard** — must be added on Day 2-3.
4. **LLM integration blocked** — NVIDIA Nemotron returns empty for prompts with passages (same as before pivot). Real quality evaluation needs fix or provider change.
5. **No verified questions** — all 30 new drafts are `verified=false`, `expected=TODO`.
6. **Human decisions pending** — permission emails, municipality selection, presenter/backup confirmation.