# Next steps

This list maps the current blockers to `docs/user-story-board.md`. The board is a Markdown file; no storyboard Excel file was present in the reviewed branch. Priorities reflect dependencies: source permission and human decisions come before civic indexing or quality claims.

## Priority 0 — Resolve human decisions

- **Leader / whole team — Day 0, setup and provider choice:** confirm the provisional Leader presenter, backup candidate, and USD $1.00 per-process API cap in `docs/decisions.md`. Configure provider input/output rates only after selecting a provider. Until then, paid requests remain blocked.
- **Member 1 / project owner — Day 0 source usage notes; Day 1 first official document:** send the draft in `docs/permission_request.md` to the relevant publishers and record any written permission. Until an appropriate civic source is approved for the intended processing and demo use, keep official pages local-only and do not index them as civic evidence.

## Priority 1 — Establish one approved source-backed flow

- **Member 1 — Day 1 document gathering; Day 2 page extraction:** locate an explicitly reusable procedural source or obtain publisher permission. A MOHA Kathmandu citizenship PDF was downloaded only to ignored local storage and visually checked on pages 1, 3, and 5; the rendered Devanagari is legible, but no printed page numbers are visible. Its embedded text is garbled, and OCR could not run because Tesseract with Nepali/English data is unavailable. The improved processor marks all five pages unusable instead of returning the garbled text. Keep this PDF out of civic indexing until permission and usable OCR/text are available.
- **Member 2 — Day 2 chunking and search:** retrieval plumbing and service-filter tests pass, but no source currently qualifies as both confirmed-open and civic answer evidence. The builder reported 0 eligible civic chunks and 0 indexed records; five English/Nepali sample searches returned empty lists. These are empty-index checks; hit@5 remains `-`.
- **Member 3 with Member 1 — Day 1 verified questions; Day 3 baseline:** verify expected facts and source chunks against the approved document before running a civic evaluation. The current set has 25 drafts and zero verified questions; keep expected values as `TODO` until checked.
- **Leader — Day 2 pipeline integration:** the headless Streamlit app served successfully. The sample driving-license renewal question returned `not_found` with no citations because there is no eligible civic index. The refusal path is verified; a supported cited answer is still blocked on an approved usable source and populated index.

## Priority 2 — Improve only against measured failures

- **Whole team — Day 3 baseline:** run the real evaluation only after verified questions and an approved index exist; record measured values through the evaluation runner. Do not turn synthetic fixture scores into civic results.
- **Member 3 / Member 2 — Days 4–7:** use the Day 3 error analysis to prioritize language/prompt changes, retrieval comparisons, and refusal-threshold tuning. Record before/after results; do not claim improvement without measurement.
- **Leader — Day 6 clean setup; Days 11–16 demo and submission:** keep setup, architecture, deployment, demo, and final submission work behind the source-backed end-to-end checks in the board. The board’s dates are planning targets, not evidence that a milestone is complete.

## Current blockers

- Written reuse permission or a suitable explicitly licensed procedural civic source is not confirmed.
- No verified civic question/source set or populated civic index is available; civic evaluation metrics remain `-`.
- Presenter/backup assignments and the provisional API cap still need human confirmation.
