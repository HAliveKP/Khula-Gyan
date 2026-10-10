# Next steps

This list maps the current blockers to `docs/user-story-board.md`. The board is a Markdown file; no storyboard Excel file was present in the reviewed branch. Priorities reflect dependencies: source permission and human decisions come before civic indexing or quality claims.

## Priority 0 — Resolve human decisions

- **Leader / whole team — Day 0, setup and provider choice:** confirm the provisional Leader presenter, backup candidate, and USD $1.00 per-process API cap in `docs/decisions.md`. Configure provider input/output rates only after selecting a provider. Until then, paid requests remain blocked.
- **Member 1 / project owner — Day 0 source usage notes; Day 1 first official document:** send the draft in `docs/permission_request.md` to the relevant publishers and record any written permission. Until an appropriate civic source is approved for the intended processing and demo use, keep official pages local-only and do not index them as civic evidence.

## Priority 1 — Establish one approved source-backed flow

- **Member 1 — Day 1 document gathering; Day 2 page extraction:** once a suitable source and permitted use are confirmed, download it locally, record its version/date and terms, process it, and visually check page links and Nepali text. Current evidence records no government source fetched and no civic document extraction.
- **Member 2 — Day 2 chunking and search:** build the index from the approved page-linked output and check that results retain source URL, page, and service. The latest recorded branch check found zero eligible civic chunks, so sample searches were empty and hit@5 remains `-`.
- **Member 3 with Member 1 — Day 1 verified questions; Day 3 baseline:** verify expected facts and source chunks against the approved document before running a civic evaluation. The current set has 25 drafts and zero verified questions; keep expected values as `TODO` until checked.
- **Leader — Day 2 pipeline integration:** after an approved civic index and the source-backed `search()`/`answer()` flow are available, run the app with one supported question and one unsupported question, checking citations and refusal behavior. The recorded headless check started the app, but the sample query returned `not_found` with no citations because no civic index was available.

## Priority 2 — Improve only against measured failures

- **Whole team — Day 3 baseline:** run the real evaluation only after verified questions and an approved index exist; record measured values through the evaluation runner. Do not turn synthetic fixture scores into civic results.
- **Member 3 / Member 2 — Days 4–7:** use the Day 3 error analysis to prioritize language/prompt changes, retrieval comparisons, and refusal-threshold tuning. Record before/after results; do not claim improvement without measurement.
- **Leader — Day 6 clean setup; Days 11–16 demo and submission:** keep setup, architecture, deployment, demo, and final submission work behind the source-backed end-to-end checks in the board. The board’s dates are planning targets, not evidence that a milestone is complete.

## Current blockers

- Written reuse permission or a suitable explicitly licensed procedural civic source is not confirmed.
- No verified civic question/source set or populated civic index is available; civic evaluation metrics remain `-`.
- Presenter/backup assignments and the provisional API cap still need human confirmation.
