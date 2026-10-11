# Prompt log

Prompts below are ordered by the available conversation history. Text marked **SUMMARY** was reconstructed from the session context rather than copied verbatim. No API key or secret is reproduced.

1. **SUMMARY — initial planning:** user asked to read `Khula_Gyan_Project_Blueprint.docx`, explain how beginners could start, and provide proper steps/modifications for initial framework setup.
2. **SUMMARY — storyboard:** user asked for a user story board of each member's tasks by day.
3. **SUMMARY — Day 0:** user asked to read `docs/user-story-board.md`, complete Day 0 tasks for all four members, commit per task, and push to Hkp with checks.
4. **SUMMARY — Day 1:** user asked to implement Member 1, Member 2, and Leader Day 1 plan from the blueprint, with two commits per member task.
5. **SUMMARY — Day 2 leader:** user asked to implement leader Day 2, update `docs/results.md` without deleting rows, record commit/check evidence, update README only if needed, and use actual evaluator values only.
6. **SUMMARY — Day 2 audit:** user asked to inspect blueprint section 13, check all members through Day 2, commit one commit per task, and resolve issues/suggestions.
7. **SUMMARY — setup request:** user requested setup-only on Hkp (or `hkp-setup`), including root `AGENTS.md`, pinned requirements, Makefile targets, install fallback attempts, synthetic tests/fixtures, source tracking, optional CI, and a report; explicitly forbade dataset building, merging dev, touching main, or force-push.
8. **SUMMARY — decisions request:** user requested a read-only subagent to resolve publisher/source, presenter, and API spending decisions from docs, with quoted file/line evidence, a decision record, source registry updates, provisional README presenter, spend cap enforcement/test, and draft permission email; no contacting publishers.
9. **SUMMARY — Day 2 status/API key:** user asked whether the project was up to date to Day 2 and whether an API key was needed, offering an OpenRouter key.
10. **SUMMARY — delegation:** user asked to assign one subagent to source processing, another retrieval, then leader work, resolving issues with additional subagents.
11. **SUMMARY — OCR/index:** user asked to divide permission/source selection, Tesseract Nepali+English setup, and civic index/source-backed answer verification across agents. User supplied an NVIDIA NIM key and requested it only in the environment, never commits; also asked to rename a branch from `codex/decisions-spend-cap` to `decisions-spend-cap`.
12. **VERBATIM — current export-only request:**

> My usage limit is nearly exhausted, so this is an export-only task. Spend as few tokens as possible: do NOT install anything, run tests, run the app, or search the web. Only read existing repo files and git history where needed, and write the files below. Another agent (OpenCode) will take over from these files, so they must be complete enough to work without this chat.
>
> Work on branch Hkp (or a new branch hkp-handoff if there are uncommitted changes). Do not touch main. Do not force-push. Never include secrets, .env contents, API keys, or raw source data.
>
> Honesty rules
> - Separate what you VERIFIED (ran and saw) from what you were TOLD (from my prompts in this session) and from what you ASSUME. Label each item with one of: VERIFIED / TOLD / ASSUMED.
> - Do not invent results, numbers, names, or licences. Unknown means "unknown".
> - Where you have the exact text of an instruction I gave you in this session, copy it verbatim rather than paraphrasing.
>
> Priority 1: Sub-agent definitions (most important)
> The sub-agents are the regulating body for this project, so write them first, as ready-to-copy OpenCode files in `handoff/opencode/.opencode/agents/` (one Markdown file per agent). Each file needs frontmatter with description and mode: subagent, then a full system prompt. Make each prompt self-contained, because subagents start with fresh context and know only what is in their file plus the repo.
>
> Create at least these four, using every rule and requirement I gave you in this session for each:
> 1. decisions: answers the open questions (permitted or explicitly open-licensed sources, presenter, API spending cap) strictly from the project docs, quotes evidence with file and line, writes `docs/decisions.md`.
> 2. verifier: read-only; checks every storyboard Excel task against evidence, re-runs relevant checks itself, outputs a table of old status, new status, evidence, remaining work; never marks DONE without proof.
> 3. readme-writer: writes README.md like a well-maintained open-source project, with every section I specified, describing only what is verified.
> 4. docs-updater: updates docs/results.md, docs/decisions.md, AGENTS.md, CHANGELOG.md, docs/next-steps.md after each task without deleting history.
> Also include any other sub-agent or role you created or were asked to create. If you used a differently named agent, keep its name and note the mapping.
>
> Then write `handoff/opencode/commands/` these slash commands:
> - closeout.md: full close-out protocol from earlier prompt (verifier -> Excel update with backup, new rows for discovered work, status/Evidence/Last updated/Notes columns -> readme-writer -> docs-updater -> consistency check -> tests -> report).
> - fix-blockers.md: full fix-everything plan from earlier prompt (environment, data/legal handling, retrieval/index, branch integration via hkp-integration, evaluation set, end-to-end), including never invent facts/numbers.
> - decide.md: invokes decisions agent.
>
> Priority 2: `handoff/HANDOFF.md`
> Include project goal/architecture as actually shown; branch state Hkp/main/dev from git log (brief); Day 0-2 audit per owner labeled VERIFIED/TOLD/ASSUMED; blockers (dependencies not installed, no source/index, unclear licenses, 10 drafts vs target 25, Hkp behind main/dev); decisions and open decisions; storyboard Excel location/header only; next steps mapped to board tasks; unfinished work with exact files/state.
>
> Priority 3: `handoff/AGENTS.md` (<100 lines) draft with repo layout, commands, branch/data/honesty rules, closeout protocol.
>
> Priority 4: `handoff/PROMPT_LOG.md` major prompts in order, verbatim where available otherwise summary marked summary.
>
> Finish: commit messages like `docs: export handoff for opencode`; push if remote configured.
> Final short: list files written, VERIFIED/TOLD/ASSUMED at a glance, missing items due to running out of context.
> If you are running low on tokens, write files in the priority order above and stop; an incomplete Priority 3 or 4 is fine, an incomplete Priority 1 is not.
