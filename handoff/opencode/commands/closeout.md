# Close out a completed Khula Gyan task

Run this after each task. Do not skip stages or claim unverified work as done.

1. **Verifier first:** invoke the `verifier` subagent read-only. Find the storyboard Excel workbook, if one exists. Compare every task row with artifacts and relevant checks; report old status, new status, evidence, and remaining work. If there is no workbook, use the Markdown board as the available plan and say the workbook is absent. Never mark DONE without proof.
2. **Update the board safely:** make a timestamped backup of the workbook outside tracked source/data directories before editing. Preserve formulas, styles, and unrelated content. Update/add only the task/status/evidence fields requested by the workbook; ensure columns include `Status`, `Evidence`, `Last updated`, and `Notes`. Add rows for newly discovered work rather than hiding it. Reopen/read back the workbook and check row counts, headers, formulas, and formatting. Do not claim validation if not performed.
3. **README:** invoke `readme-writer`; describe only behavior and results verified in this checkout. All documented commands should be appropriate for a clean checkout, and unbuilt features must be labeled planned.
4. **Project docs:** invoke `docs-updater` for `docs/results.md`, `docs/decisions.md`, `AGENTS.md`, `CHANGELOG.md`, and `docs/next-steps.md`. Preserve old rows and append evidence. Use `-` for unmeasured evaluation values; do not invent facts, metrics, citations, permissions, or names.
5. **Consistency check:** compare README, results, decisions, next steps, AGENTS, code, source registry, and storyboard. Resolve contradictions or label unknowns. Ensure no raw source data, Chroma database, `.env`, or key is tracked.
6. **Checks:** run relevant tests and checks after edits, including the project test target when available. Record exact commands and observed outputs. Do not claim checks passed when they were not run; respect API spending cap and ask before any run that could exceed it.
7. **Report:** summarize changed files, commit(s), exact check evidence, remaining tasks, and any human decisions. Preserve prior history and never push to `main` or force-push.
