# Khula Gyan handoff

## Project and architecture

- **VERIFIED (repo files):** README describes Khula Gyan as a Nepali civic-document assistant intended to retrieve passages and answer with page-linked citations, refusing when evidence is insufficient and disclaiming legal advice. Existing components include document extraction/chunking/embedding (`src/ingest/`), dense Chroma retrieval (`src/retrieval/search.py`), answer generation and citation guard (`src/generation/`), pipeline (`src/pipeline.py`), Streamlit (`frontend/app.py`), fetch/process/index/smoke scripts, and evaluation tools.
- **VERIFIED (README/docs):** the described architecture is local PDF/HTML → page/URL extraction → chunking → embeddings → Chroma → retrieval → generation → schema/citation checks → cited answer or refusal. README says a permitted civic source-backed answer has not been demonstrated.
- **TOLD (prior task reports in this session):** the app started headlessly and returned `not_found` without citations for a driving-license query; no eligible civic index was present at that time.

## Branch state

- **VERIFIED (local Git metadata):** local HEAD is `fcb094b` on branch `branch` (`origin/branch`); local working tree already has broad modifications/untracked project files. The direct local branch switch to `hkp-handoff` failed with `Permission denied` creating `.git/refs/heads/hkp-handoff.lock`; a clean worktree from `origin/Hkp` was then created for the export.
- **VERIFIED (remote-tracking refs in local Git):** `origin/Hkp` = `c284207` (“Merge pull request #8 from HAliveKP/hkp-setup”); `origin/main` = `f7f0291` (“Merge pull request #9 from HAliveKP/Hkp”); `origin/dev` = `870211c` (“Merge pull request #5 from HAliveKP/feature/aashish-generation”). `origin/Hkp` is the merge base of `origin/main`; the merge base of `origin/Hkp` and `origin/dev` is `870211c`.
- **VERIFIED (local Git counts):** `origin/Hkp...origin/main` is `0 2` (Hkp has 0 commits unique to it; main has 2). `origin/Hkp...origin/dev` is `64 0` (Hkp has 64 commits unique to it; dev has 0). These refs show Hkp behind main, but not behind dev.
- **ASSUMED:** current checkout files are a later snapshot layered over an old local initial commit; their exact relationship to remote commits is not established. The export was instead committed from a clean Hkp-based worktree.
- **VERIFIED:** export commit `dcea4d4` is on `hkp-handoff` from `origin/Hkp`, and Git reported the branch tracks `origin/hkp-handoff`. The follow-up `ls-remote` check failed with `getaddrinfo() thread failed to start`, so remote visibility could not be independently confirmed.

## Day 0–2 audit by owner

These are current documentation claims unless explicitly labeled as prior task reports; several docs disagree. Reconcile before treating as a final audit.

| Owner | Status and evidence |
|---|---|
| Member 1 — Data | **VERIFIED (docs):** `data/sources.yaml` lists MOHA sources as unclear/local-only, Passport sources as all-rights-reserved/local-only, and no civic source with `answer_evidence: true`. **TOLD (prior task reports):** a MOHA PDF was locally rendered; Devanagari appeared legible on checked pages, printed page numbers were not visible, embedded text was corrupted, and all five page records were unusable without Tesseract. Do not redistribute or use as evidence. |
| Member 2 — Retrieval | **VERIFIED (docs):** retrieval module and index builder exist; README reports the direct builder found 0 processed page records, 0 eligible civic chunks, and 0 indexed records; five searches were empty. README reports embedding smoke passed on 10 examples, vector size 1024. These are repository documentation claims; not rerun for this export. |
| Member 3 — Generation & Evaluation | **VERIFIED (docs):** generation/eval code and tests exist. README says there are 25 records, 0 verified and 25 drafts (20 answerable drafts, 5 out-of-scope), with no real civic baseline. `docs/results.md` contains older conflicting Day 1–2 claims; resolve via fresh verification. |
| Leader — Integration/UI/Repository | **VERIFIED (docs):** Streamlit app and Makefile exist. README reports a headless launch returned HTTP 200 but the query returned `not_found` without citations. `docs/results.md` contains older claims that app launch was not done. No Excel workbook was found in the repo file listing; `docs/user-story-board.md` is the planning board. |

## Blockers and open decisions

- **VERIFIED (repo):** dependency files and `.venv` usage are referenced by README; the exact current environment state was not checked in this export. Do not assert “dependencies not installed” as current fact.
- **VERIFIED (docs):** no approved civic source-backed answer or populated civic index is documented; index build reported zero eligible civic chunks.
- **VERIFIED (source registry):** MOHA records are unclear/local-only; Department of Passports records are all rights reserved/local-only. No permission is recorded. Open Data Nepal's explicitly licensed environment dataset is unrelated reference data, not civic procedure evidence.
- **VERIFIED (README):** 0 of 25 questions are verified; no measured civic baseline. `docs/results.md` has older contradictory counts; reconcile from actual question file before changing metrics.
- **VERIFIED (Git refs):** Hkp is an ancestor of main; Hkp and dev have a different merge base (`870211c`). A merge into an integration branch remains work, but this export task forbids doing it.
- **VERIFIED (docs/decisions.md and README):** publisher permission is absent; presenter and API cap are provisional, not confirmed. README lists `MAX_API_SPEND_USD=1.00` as provisional and a named provisional presenter; inspect the decision record before treating either as fact.

## Storyboard

- **VERIFIED:** no `.xlsx` or `.xlsm` file was found by the repository file search. The available storyboard is `docs/user-story-board.md` (Day 0–16 table with owner columns for Member 1, Member 2, Member 3, Leader; completion check; status). There is no Excel header row to report.
- **VERIFIED:** the Markdown board says Member 1 should select/record a source and process/inspect eligible pages; Member 2 should run embedding, build index and search; Member 3 should verify questions/evaluate; Leader should set up integration and run the app. Day 0 execution record is present; its status may be stale against later code/docs.

## Prioritized next steps mapped to the available board

1. **Day 0/Day 1 — Member 1:** confirm written permission or identify a literal reuse-licensed civic procedure source; keep MOHA/Passport local-only. Resolve OCR installation/language packs before further PDF extraction. Record page-level visual QA.
2. **Day 1/Day 2 — Member 2:** build an index only from eligible, permitted civic material; verify source URL/service/page metadata and sample retrieval. Do not report hit@5 without human-verified source expectations.
3. **Day 1/Day 2 — Member 3:** turn draft questions into verified questions only from real retrieved text; run real evaluation only on verified questions and retain `-` for unmeasured metrics.
4. **Day 2 — Leader:** reconcile `docs/results.md`, README, and source/decision records; run the application against eligible civic evidence after index exists and verify the citation points to the actual source/page.
5. **Decision task:** have a human send permission requests, confirm the presenter, and confirm/change the provisional spend cap. Do not send communications or make paid calls without authorization/cap compliance.
6. **Integration task (separate authorization):** reconcile Hkp/dev in the requested integration branch, record all conflict resolutions, and open a PR into Hkp; never merge main or force-push.

## Current export work and unfinished items

- **VERIFIED:** wrote the OpenCode agent and command files under `handoff/opencode/` and this handoff. No app, test, install, or web search was run, per instruction.
- **VERIFIED:** the original checkout branch creation failed with `fatal: cannot lock ref 'refs/heads/hkp-handoff': Unable to create 'D:/Khula-Gyan/.git/refs/heads/hkp-handoff.lock': Permission denied`; a separate Hkp-based worktree was used for the export. No files outside `handoff/` were intentionally changed by this export.
- **TOLD:** earlier task reports said the `.env` contains a local NVIDIA key; it was not opened or copied. Never stage `.env` or secrets.
