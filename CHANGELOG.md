# Changelog

## Unreleased: first public release preparation

### Repository restructure (branch `aash-release`, not yet committed)

- Removed the root-level `test_*.py` experiment scripts, the unused `src/api/` package, and the hackathon agent tooling folders `.hermes/`, `handoff/` and `skills/`.
- Moved hackathon process notes to `docs/history/`: `decisions.md`, `pivot-addendum.md`, `pivot-verification.md`, `user-story-board.md`, `next-steps.md`, `submission_text.md`, `permission_request.md`, `retrieval-score.md`, `extraction-report.md`, `IDEA.md`, `legacy_questions.jsonl` and `question-drafts.md`.
- Rewrote `README.md` and `AGENTS.md` for newcomers. Added `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1), `SECURITY.md`, and GitHub issue and pull request templates.

## 2026-10-13 to 2026-10-25: Palika Guide

### Pivot (2026-10-13, `2124c06`, PR #19)

- Changed the project from central-government procedures (driving license, citizenship, passport) to **Palika Guide**: municipal-service questions answered from each municipality's citizen charter. The old sources are kept as `legacy: true, answer_evidence: false`.
- Added a `municipality` filter to `search()`, a municipality selector in the UI, a wrong-municipality guard in `ask()`, and municipality/district/ward/section fields carried through chunking and indexing.

### Fixes and features (2026-10-15 to 2026-10-17, PRs #20 and #21)

- `pytest.ini` limits collection to `tests/` (`e4f765e`).
- Municipality names in Devanagari (with Nepali case suffixes) are recognised by the guard (`73316f0`). The five charter municipalities are offered and detected (`700afb1`).
- `LLM_REASONING=off` sends OpenRouter's `reasoning: {enabled: false}`, which stops empty Nemotron replies caused by hidden reasoning using the whole output limit (`952f058`). Empty replies are never cached (`4567b75`).
- Registered 12 charter files for 5 municipalities (Pokhara, Bharatpur, Dhulikhel, Ghorahi, Hetauda) in `data/sources.yaml`, local only (`94341a8`).
- Charter extraction: repaired Ghorahi-style Devanagari glyph maps (`47d3851`), converted Preeti-font text to Unicode (`627eaa1`), kept only charter content from municipal HTML pages (`d9b1fbf`), kept number-only fee and serial cells when removing page numbers (`4d6e8e9`), and read Kalimati ASCII digit glyphs as the Devanagari digits they draw (`880998c`).
- Added 40 Palika Guide eval questions (`1213b95`). 39 were verified by a human against the charter pages (`ef07ac0`).

### Pipeline and evaluation (2026-10-23 to 2026-10-25, PR #22 and later)

- `search()` returns `[]` for an unknown service instead of raising, and `ask()` accepts `service="other"` (`1b9b4f1`, `51e2089`).
- Pinned working versions: sentence-transformers 6.2.0, streamlit 1.66.1, Pillow 12.3.0 (`72942db`).
- Added `scripts/demo_script.py` (`2a6b9ef`) and `docs/error-analysis.md` (`367b26f`).
- Local-only approval recorded for 11 charters (`palika_pokhara_2075` excluded). `ask()` returns `not_found` when the LLM call fails, and `eval/run_eval.py` keeps going after provider errors (`284e172`).
- First official Palika Guide baseline by `eval/run_eval.py` (2026-10-25, 39 verified questions, `nvidia/nemotron-3.5-super-vl:free` with `LLM_REASONING=off`): hit@5 81%, citation accuracy 93%, correct 19%, correct refusal 100%, false refusal 48%, p95 503.8 s. Recorded in the Eval runs table of `docs/results.md`. The charters and index stay local-only.

## 2026-10-10 — Decisions and API spend guard close-out

### Changes

- Recorded source reuse, presenter, and API spending decisions in `docs/decisions.md`. Publisher permission, presenter assignment, and the USD $1.00 per-process cap remain provisional or require human confirmation.
- Kept official MOHA and Department of Passports materials local-only in `data/sources.yaml`; the environmental dataset is licensed but excluded from civic answer evidence, and the NCD dataset remains unclear/local-only.
- Added a permission-request email draft in `docs/permission_request.md`; no publisher was contacted.
- Documented the provisional presenter and spend cap in `README.md`, and the stop-before-over-cap rule in `AGENTS.md`.
- Added preflight API cost reservation and evaluation spend reporting. The cap test blocks a provider request whose reservation would exceed the cap.

### Evidence

- `docs/results.md` records the final offline suite as 6 passed, including the provider-mock spend-cap stop check.
- `docs/results.md` records a synthetic fake-LLM evaluation harness run with estimated spend `$0.000000`. This is a plumbing check, not a civic quality result; the civic evaluation metrics remain `-` because no source-backed questions are verified.
- `data/sources.yaml` records the current license status and local-only status for each reviewed source. The NCD dataset is excluded because its metadata says “License Not specified.”
- No publisher permission email was sent, no payment was made, and no numeric evaluation metric was added.

### Human follow-up

- Send permission requests and record written responses; select a permitted procedural civic source.
- Confirm the presenter and backup candidate.
- Confirm or change the provisional USD $1.00 cap and set the selected provider's current input/output rates before any paid run.
