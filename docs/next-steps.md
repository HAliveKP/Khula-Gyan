# Next steps

This list maps the current blockers to `docs/user-story-board.md` for the Palika Guide pivot (Day 1 = Oct 14 ... Day 8 = Oct 21). Priorities reflect dependencies: human decisions come first, then one approved source-backed flow, then improvements only against measured failures.

## Priority 0 — Resolve human decisions

- **Project owner — Day 1 feasibility sheet; Day 2 fetch/process charters**: send the draft permission request in `docs/permission_request.md` to the relevant municipalities and record any written permission. Until an appropriate civic source is approved for the intended processing and demo use, keep official charters local-only and do not index them as civic evidence.
- **Leader / whole team — Day 1 schema & eval format**: confirm the provisional Leader presenter, backup candidate, and the $1.00 per-process API cap (already configured for NVIDIA free tier). Configure provider input/output rates only after selecting a provider. Until then, paid requests remain blocked.
- **Whole team — Day 1 municipality selection**: pick up to 5 municipalities from the Day 1 feasibility sheet that have usable text/HTML charters. Reduce if feasibility check finds fewer.
  - *Update 2026-10-25:* 5 municipalities (Pokhara, Bharatpur, Dhulikhel, Ghorahi, Hetauda) were chosen by Aashish on 2026-10-15 from a 20-site feasibility check and registered by `94341a8`, merged by the Leader via PR #20 (`f879fa5`). An explicit Leader confirmation of the set is still open (`docs/decisions.md` §8).

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

## Current blockers (2026-10-25)

*Update 2026-10-25 (evening):* first official BASELINE run by `eval/run_eval.py` (see the Eval runs table in `docs/results.md`): official index from 11 local-only approved charters (`palika_pokhara_2075` excluded; approved by Aashish with authority delegated by the Leader), `nvidia/nemotron-3.5-super-vl:free` with `LLM_REASONING=off`, 39 verified questions: hit@5 81%, citation_acc 93%, correct 19% (exact keyword match), correct_refusal 100%, false_refusal 48%; 2 questions hit LLM provider errors and count as not correct.

Checked on aash-crest01's laptop at `main` `c7fab92` (evidence in `docs/results.md`, Day checklist rows "update 2026-10-25").

1. **Official index has 0 eligible charter chunks (by design).** All 12 `palika_*` entries in `data/sources.yaml` have `answer_evidence: false` and `approval_note: null`, so `scripts/build_index.py` skips them. Unblock: the Leader records a local-only approval (`answer_evidence: true`, `approval_note`, `approved_on`, `approved_by`), as was done for the MOHA PDF on 2026-10-11 (`docs/decisions.md` §4), then `make index` runs on the machine that has the files (aash-crest01's laptop) or on a machine given a privately shared copy. The charter files must stay out of Git.
2. **The charters are only on aash-crest01's laptop.** They were downloaded and processed there on 2026-10-15 (12 files in ignored `data/raw/` and `data/processed/`). The Leader's machine could not reach the .gov.np sites (`WinError 10060`/`10061`, `docs/error-analysis.md`).
3. **No municipality has replied with permission.** Permission emails for all 5 municipalities were drafted locally on 2026-10-15; sending is pending. Until a written reply is on file, charters stay local-only: no public deployment, no committed copies.
4. **LLM base-URL mismatch.** The empty-reply fix (`LLM_REASONING=off`, `952f058`; no caching of empty replies, `4567b75`; both PR #20) sends OpenRouter's `reasoning: {enabled: false}` parameter. It was tested with `LLM_BASE_URL=https://openrouter.ai/api/v1` and `LLM_MODEL=nvidia/nemotron-3-super-120b-a12b:free`. `docs/submission_text.md` records the Leader's `.env` as `LLM_BASE_URL=https://integrate.api.nvidia.com/v1`; with NVIDIA NIM directly the switch is untested. The Leader should either use the OpenRouter base URL or test NIM's own switch.
5. **Day 4 baseline not recorded.** Waits on blocker 1; only `eval/run_eval.py` output may be recorded.
6. **`pq009` still a draft** (`verified: false`, `expected: ["TODO"]`); 39 of 40 questions are verified (`ef07ac0`, PR #21).
7. **Presenter / backup** still to be confirmed by a human (`docs/decisions.md` §5).

## Blockers as of 2026-10-13 (history)

*Update 2026-10-25:* superseded by the list above. Items 1 (feasibility and selection), 2-3 (filter and guard: on `main`), 4 (empty Nemotron replies: root cause and fix in PR #20, see `docs/decisions.md` §8) and 5 (39 of 40 verified) are resolved or changed; permission and presenter/backup remain open.

1. **No municipality charters approved yet** — need Day 1 feasibility sheet and written permission.
2. **No municipality filter in search** — must be implemented on Day 2.
3. **No wrong-municipality guard** — must be added on Day 2-3.
4. **LLM integration blocked** — NVIDIA Nemotron returns empty for prompts with passages (same as before pivot). Real quality evaluation needs fix or provider change.
5. **No verified questions** — all 30 new drafts are `verified=false`, `expected=TODO`.
6. **Human decisions pending** — permission emails, municipality selection, presenter/backup confirmation.