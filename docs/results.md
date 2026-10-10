# Project work log and results

Updated 2026-10-10. This file preserves the historical entries below and reports checks that were actually run. Historical commit log entries remain intact; setup verification is recorded separately. A Git commit cannot contain its own final hash, so the current results-log commit can be recorded in a later update.

## Commit log

Historical commit metadata, diffs, and combined statuses were rechecked on Hkp. Empty GitHub status lists mean **no status was recorded**, not that a test passed. The only recorded automated status among the historical commits below was CodeRabbit success on `12101ce`.

| Date (UTC) | Hash | Author | Message | Blueprint task | Check result |
|---|---|---|---|---|---|
| 2026-10-06 | `fcb094b9d06c024d39f0058cf83e67691f072663` | Harikrishna Pokhrel | Initial commit | Repository baseline | Commit and initial tree rechecked; no status recorded. |
| 2026-10-08 | `01527a8eb180e6cb6932c0fc1e97c649c064b544` | Harikrishna Pokhrel | feat: scaffold Khula Gyan Day 0 setup | Day 0 repository scaffold, setup notes, and interfaces | Diff rechecked; no status recorded. |
| 2026-10-08 | `2394b88d30ecea050b2cb821ebfa377432363353` | Harikrishna Pokhrel | fix: preserve gitignore line endings | Day 0 repository hygiene | Diff rechecked as a line-ending change; no status recorded. |
| 2026-10-09 | `bc5df97f5b97e016dca922d26c46f8da659a24b4` | Harikrishna Pokhrel | data: register ten official Day 1 sources | Day 1 Member 1 source register | Ten source entries and usage cautions rechecked; no status recorded. Originals were not downloaded. |
| 2026-10-09 | `978d1cd4b45ad26e7351e53d5acf2d7cfd257509` | Harikrishna Pokhrel | docs: report Day 1 source extraction quality | Day 1 Member 1 extraction review | Report rechecked; ratings are preliminary browser review, not local document extraction. No status recorded. |
| 2026-10-09 | `bd09ea0c1e40ccc5610c497dd0093f2e391d6e56` | Harikrishna Pokhrel | feat: add contract-shaped text chunking | Day 1 Member 2 chunker | Current smoke check passed chunk size, overlap, metadata, and syntax. No commit status recorded. |
| 2026-10-09 | `7bd0c3363049686e4de6ba415ac33f0c140d631d` | Harikrishna Pokhrel | feat: index document chunks in ChromaDB | Day 1 Member 2 vector indexer | Diff rechecked; Chroma/model indexing was not run in this environment. No status recorded. |
| 2026-10-09 | `4c7ffef41b87a21203872c20a1657a36a82b50de` | Harikrishna Pokhrel | feat: add schema-shaped mock ask pipeline | Day 1 leader mock pipeline | Historical diff rechecked. Day 2 replaced the mock with an integration adapter; current missing-component fallback check passed. No status recorded. |
| 2026-10-09 | `383fa1abb75552ededaf01ad99633169730dc67a` | Harikrishna Pokhrel | feat: add Streamlit demo answer and citations | Day 1 leader Streamlit screen | Historical diff rechecked; current UI syntax compiles, but Streamlit was not launched. No status recorded. |
| 2026-10-09 | `90a7b2d95b0ea73b8ebfc78a74c41aa64ffc30bc` | Harikrishna Pokhrel | fix: correct official citizenship source link | Day 1 source-register correction | Corrected link checked against the official Dadeldhura listing; no status recorded. |
| 2026-10-09 | `12101ce89ba6993923661f70816fa8fa7e5b38a0` | Harikrishna Pokhrel | fix: keep generated Chroma index in ignored folder | Day 1 generated-data handling | Diff rechecked; CodeRabbit status was success. |
| 2026-10-09 | `e378e3bfe8ac15be20a184b08a6474c7f24b0bb9` | Harikrishna Pokhrel | feat: add page-aware document extraction and cleaning | Day 2 Member 1 extraction and cleanup | Python syntax, CLI help, synthetic HTML extraction, Unicode NFC, repeated-header cleanup, and JSONL metadata checks passed. Official files were unavailable; PDF extraction was not run because PyMuPDF is absent from this runtime. No GitHub status recorded. |
| 2026-10-09 | `8990d04cc9e6f3dad95db9c4c850b7464590e710` | Harikrishna Pokhrel | feat: connect citation-aware pipeline and UI | Day 2 leader pipeline integration, citations, loading, and errors | Syntax and interface smoke checks passed, including `search(query, k=5, service)` → `answer(query, chunks)`; real Member 2/3 modules are not yet present. No GitHub status recorded. |
| 2026-10-09 | `9be4526b1c9080b1a682608aa2d7de8a8d16e03b` | Harikrishna Pokhrel | fix: keep the README diff focused | Day 2 README run instructions and current-feature description | Final diff from the previous implementation shows localized README edits (24 additions, 2 deletions); app and source-processing instructions are present. No GitHub status recorded. |
| 2026-10-09 | `d2aa3fb37b291e1ac77fc9f8e383101876fdfd68` | aash-crest01 | feat: Member 3 generation + eval starter (answer, guard, run_eval) | Day 0-1 M3: prompt v0, eval format, answer.py, guard, run_eval | pass: 12 tests passed at this commit |
| 2026-10-09 | `ddd60aaf9410b27e46dce7b912531798fea6c4d0` | Harikrishna Pokhrel | docs: record Day 0-2 work and checks | ? | not checked |
| 2026-10-10 | `c0603ca290110d544f539eef3b8818b115ecf63d` | aash-crest01 | eval: three-section results log (commit log, task checklist, eval table) + update_log.py | Day 1 M3: results log (Leader's LOG request) | pass: 14 tests passed |
| 2026-10-10 | `27318a369835b18c7a817a2782ea71a014d67158` | aash-crest01 | docs: fill commit log | Day 1 M3: results log | pass: commit log filled by update_log.py (docs only) |
| 2026-10-10 | `f71b69662b7a373c452d59472b55c497325689a5` | aash-crest01 | docs: check commit log rows | Day 1 M3: results log | pass: rows reviewed and filled (docs only) |
| 2026-10-10 | `6d5702aa999b61c671ac87a8051c45ef6d0afbaa` | aash-crest01 | feat: OpenRouter key pool (round robin + failover across several API keys) | Day 0 M3: LLM API key + test call (OpenRouter, key loop) | pass: 21 tests passed; smoke_test_llm.py passed with nemotron-3-super-120b-a12b:free |
| 2026-10-10 | `5455e2f0b372bfa62125e142d6ebe5e74fdef672` | aash-crest01 | feat: scripts/try_answer.py to test answer() with Nepali questions from a UTF-8 file | Day 0 M3: real-AI test of answer() | pass: try_answer.py, 4/4 questions behave correctly |
| 2026-10-10 | `16c934f006a9bc02abc2f56ade441ca07dcd4f69` | aash-crest01 | docs: LLM smoke test passed, commit log updated | Day 0 M3: record smoke test result | pass: docs only |
| 2026-10-10 | `116c11c1a28f5f74752cc9411c56d3583892170f` | aash-crest01 | docs: check new commit log rows | Day 1 M3: results log | pass: docs only |
| 2026-10-10 | `90b21cfd46ea71d5bf548bf00c3d724b14046d0e` | aash-crest01 | eval: use the team log format on main (full hashes, no merges, Day checklist, Eval runs under Evaluation results) | Day 1 M3: results log in the team format | pass: 24 tests passed; update_log.py matched the Leader's full hashes |

| 2026-10-10 | `7e7801d8638323f12fe56ad4aa521862dd0d2641` | Harikrishna Pokhrel | feat: add dense retrieval search contract | Day 2 Member 2: dense search and score scale | Python syntax compilation passed. No embedding model or Chroma package is installed; no data/index means no retrieval run or hit@5. |
| 2026-10-10 | `025ef81beaf12b61b6264e1100cde972ae4c157e` | Harikrishna Pokhrel | docs: describe current Hkp retrieval status | Leader: correct README status/run expectations | README descriptions checked against Hkp and main/dev; setup/runtime not executed. |
| 2026-10-10 | `a8cc68519c4213d7247011596946a3f885c73608` | Harikrishna Pokhrel | docs: audit Day 0-2 member task status | Day 0–2 cross-member audit | Branch contents and local prerequisites rechecked; source permissions, data/index, and runtime checks remain blocked. |
| 2026-10-10 | `139c757aeae1667e8cecff57ed7b21b27aaa4b4f` | Harikrishna Pokhrel | fix: format Day 0-2 audit as markdown | Day 0–2 audit formatting | Re-fetched Markdown now has real table/line breaks; content rechecked. |
| 2026-10-10 | `18c7d14e6b90d3119c1e4b7ca7f438e1cd36a9b1` | Harikrishna Pokhrel | docs: complete Day 0-2 audit trail | Day 0–2 audit/results update | Branch checklist, prior work, and evaluation status rechecked; no unmeasured metric added. |

| 2026-10-10 | `d62bad964b1c244e2d7b9322d4d575abb13b0502` | Codex | build: pin Python 3.12 dependencies | Day 0 environment | Pip install completed on retry; `pip check` passed; embedding smoke passed. |
| 2026-10-10 | `6024c5e96dc39eb0f5b5d431d3bfce8710f0d769` | Codex | data: track reuse terms for registered sources | Member 1 source licensing | Registry records status and checked date; one CC BY page is reference-only. |
| 2026-10-10 | `85d9044e3d1b8015fc02191f9bfd758a8438ee9` | Codex | data: add rights-aware local source fetcher | Member 1 local fetching | Fetched one explicitly licensed reference page to ignored data/raw; no government page fetched. |
| 2026-10-10 | `6a5cf7c5b28c1d62039b7f76a6658d35814bde47` | Codex | retrieval: build page-linked Chroma index from approved sources | Member 2 index builder | Build run processed 1 page; 0 civic chunks indexed because the page is reference-only. |
| 2026-10-10 | `97304c0433c6f0ffb55556f4cae32ed5526b5518` | Codex | eval: expand source-unverified draft set to 25 | Member 3 evaluation set | 25 drafts, 5 out-of-scope, 0 verified; all expected values remain TODO. |
| 2026-10-10 | `6487469b663626d51ab2982bf20704fa4831e5e5` | Codex | data: allow license-review pages to be processed as reference-only | Member 1 processing | Reference-only page extraction succeeded; no civic facts claimed. |
| 2026-10-10 | `d51a23d84ae5ff28c787650c15eb9982284fd4ef` | Codex | retrieval: retain source URLs in chunks | Member 2 citations | Follow-up correction recorded in `775bc51`; this commit did not fully apply the chunk metadata edit. |
| 2026-10-10 | `14605ce2990f7fa4ab408da51d0c8e70a4b3348a` | Codex | retrieval: store source URLs as Chroma metadata | Member 2 citations | Source URL metadata added; index runtime not tested on civic data. |
| 2026-10-10 | `b29073882891686efaf591402e0e25dce61cf99e` | Codex | retrieval: return canonical source URL with search hits | Member 2 citations | Search result URL field added. |
| 2026-10-10 | `775bc51b9e8e4f4edab765b4e8c1c7f9935d39b4` | Codex | retrieval: attach canonical URLs to chunks | Member 2 citations | Full chunk metadata correction applied. |
| 2026-10-10 | `a1d5166cb4421f7e375e3b6ea701168c38822839` | Codex | docs: document pinned install and source indexing steps | Leader setup docs | README updated for CPU install, fetching and index build. |

| 2026-10-10 | `3f059054857075955b6e97b1ca6c36b0205e2e6a` | Codex | docs: reflect selected OpenRouter provider | Leader README accuracy | Provider statement aligned with the existing OpenRouter integration; credit ceiling remains undecided. |
| 2026-10-10 | `1731f0152d2cc42e1204f6d1dcdb784322cf8020` | Codex | docs: clarify verified-question and app limitations | Leader results accuracy | Clarified that zero verified questions prevented evaluation and cited-answer validation. |
| 2026-10-10 | `5d0ad3aa84c30bb79f0e593ea4981885f76ebcc5` | Codex | docs: record environment and source verification results | Cross-member status audit | Added environment, data, index, evaluation, and Streamlit evidence; no unmeasured metrics added. |

| 2026-10-10 | `e05ee48b863c457118edfd1877a5e0a56c8c8c2c` | Codex | eval: keep exactly five out-of-scope drafts | Member 3 evaluation set | Final structure check: 25 questions, 5 out-of-scope, 0 verified, 25 TODO expected values, 0 duplicate IDs. |

| 2026-10-10 | `d3fbd55dfabe94c2245613c23e656773ba71d40c` | Codex | docs: log latest verification records | Leader work log | Added prior environment and verification commit rows; no result metrics changed. |
| 2026-10-10 | `af98e03dcf35a69791d50732711eadbeb9cdfba4` | Codex | docs: log final question set verification | Member 3 evaluation set log | Logged the final 25-question, 5 out-of-scope structure check. |

| 2026-10-10 | `773e81ea928714cacb7ef6cb305451d8b3d91c51` | Codex | data: correct Open Data Nepal licence records | Source reuse review | YAML parsed; NCD licence left unclear/local-only; environment dataset recorded open but reference-only. |
| 2026-10-10 | `ab64b6152d26ee09df30798ee8ec2eddeb5453d1` | Codex | docs: record provisional project decisions | Leader decisions | Decision evidence cross-checked; source permission, presenter, and cap remain human-confirmation items. |
| 2026-10-10 | `d5a976905fdd70ac6fbb126b29c69d926e5bdee9` | Codex | docs: draft source permission request | Leader source permission | Draft created only; no publisher contacted. |
| 2026-10-10 | `938065281bf1eb92858dd53564fe88707fa8e52c` | Codex | docs: note provisional presenter and API cap | Leader presentation and spend policy | README labels presenter/backup and cap provisional; unrelated source is marked reference-only. |
| 2026-10-10 | `0410e7b212f8716744e90561583c9cd268de3732` | Codex | docs: require spend approval before over-cap runs | Agent setup policy | AGENTS spend stop rule added. |
| 2026-10-10 | `807fc956fd409bb4195e715b673a357a3076fc66` | Codex | feat: add preflight API spend cap | Generation spend safety | Spend estimator/reservation added; verified by final pytest run. |
| 2026-10-10 | `41d1e90c529f1e50fcc940caebfc72fd58329822` | Codex | feat: guard generation calls with spend cap | Generation and support/eval LLM calls | Preflight runs before provider calls; verified by final pytest run. |
| 2026-10-10 | `c885cdefebf02fcef1e6f2f3dfbcd1a777a8769f` | Codex | eval: track spend and stop over-cap runs | Evaluation run accounting | Synthetic fake-LLM harness completed; estimated spend $0.000000. No civic metrics inferred. |
| 2026-10-10 | `b8372d11e46d0b56c6bd82948ec4943e2a3b738f` | Codex | test: cover spend cap stop behavior | Spend guard tests | Final suite: 6 passed; provider mock was not called when reservation exceeded cap. |
| 2026-10-10 | `e97b2566d2baf666674034727d0a1fce8c0790ed` | Codex | config: document API spend and rate settings | Local provider configuration | Documents provisional cap and required explicit rates; no key or secret added. |

## Day checklist and evidence

| Day | Owner | Status | Evidence / remaining work |
|---|---|---|---|
| Day 0 | Member 1 — Data & Documents | Partial | Source register exists. No originals are in `data/raw/`; usage terms and a first local extraction remain to be confirmed. |
| Day 0 | Member 2 — Retrieval | Partial | Dependency list and embedding smoke script exist. A successful local model smoke run is not recorded. |
| Day 0 | Member 3 — Generation & Evaluation | Partial | Response contract and starter question drafts exist. Provider choice and a successful LLM call remain pending. |
| Day 0 | Leader — Integration, UI & Repository | Partial | Setup files and README exist; Hkp is the selected branch. Shared `dev` and `main` branches were not created. |
| Day 1 | Member 1 — Data & Documents | Partial | Ten sources are registered and a preliminary extraction report exists. No files were downloaded or locally extracted. |
| Day 1 | Member 2 — Retrieval | Partial | Chunking and Chroma index code exist. A sample dataset and populated index have not been produced. |
| Day 1 | Member 3 — Generation & Evaluation | Pending | `src/generation/answer.py` and the 15-question Day 1 set are not present. |
| Day 1 | Leader — Integration, UI & Repository | Done for mock | `ask()` and the initial Streamlit screen were added; the screen was not launched in this environment. |
| Day 2 | Member 1 — Data & Documents | In progress | PDF/HTML extraction, NFC cleanup, repeated header/footer removal, and page-linked JSONL output are implemented. Synthetic HTML checks passed. Process a permitted official source and inspect each page when the download and PyMuPDF prerequisites are available. |
| Day 2 | Member 2 — Retrieval | Pending (not part of this request) | The real `src/retrieval/search.py` module is not present, so index search cannot yet run end to end. |
| Day 2 | Member 3 — Generation & Evaluation | Pending (not part of this request) | The real `src/generation/answer.py` module is not present, so no answer generation or evaluation can run. |
| Day 2 | Leader — Integration, UI & Repository | In progress | `ask()` now connects to the documented `search()` and `answer()` interfaces when available; the UI has citation display, loading, and friendly error states. It safely returns `not_found` until those modules and reviewed source text exist. Optional FastAPI was skipped. |
| Day 0 (update 2026-10-10) | Member 3 — Generation & Evaluation | Done | Provider: OpenRouter (Leader's choice). `python scripts/smoke_test_llm.py` passed with `nvidia/nemotron-3-super-120b-a12b:free` (Nepali 5.0 s, English 0.9 s); `google/gemma-4-31b-it:free` was rate-limited upstream. Prompt v0 in `src/generation/prompt.py`; question format in `eval/questions.jsonl` (10 drafts, unverified); `python eval/check_questions.py` → OK. Code in PR #5. |
| Day 1 (update 2026-10-10) | Member 3 — Generation & Evaluation | Partial | `src/generation/answer.py` exists (`answer()` per contract 9.3, guard, schema validation); `python -m pytest -q` → 24 passed. Real-AI check: `python scripts/try_answer.py` answered English, Nepali and Romanized questions with grounded citations on the sample passages and refused an off-topic question. Nepali has Hindi words and spelling slips (prompt v1, Day 4). Remaining: 15 verified questions with Member 1 (10 drafts, 0 verified). |
| Day 2 (update 2026-10-10) | Member 3 — Generation & Evaluation | Partial (code ready) | `eval/run_eval.py` exists and ran end to end on sample passages with the fake LLM (`--mock`). Not yet run on real `search()` (Member 2's module not present). Remaining: 25 questions (5 out-of-scope). |

## Evaluation results

Only real output from `eval/run_eval.py` against human-verified civic questions and source chunks belongs in the evaluation tables. The runner is present, but there is no verified civic evaluation set or permitted civic-source index available for a baseline. The offline synthetic fixture harness is a plumbing check; its mock percentages are not project quality metrics. Unmeasured values remain `-`.

| Run / build | Date | Questions | hit@5 | Citation accuracy | Answer correctness | Refusal rate | Notes |
|---|---|---:|---:|---:|---:|---:|---|
| Day 0–2 baseline | - | - | - | - | - | - | No human-verified civic question set and permitted civic-source index are available for a real baseline. |

### Eval runs (eval/run_eval.py)

Rows are added only by `eval/run_eval.py`; `-` = not measured. Never type numbers by hand.

| Date | Change | Prompt | N | hit@5 | Citation acc. | Correct | Hallucination | Correct refusal | False refusal | p95 s |
|---|---|---|---|---|---|---|---|---|---|---|


## Day 0–2 task audit (2026-10-10)

This audit is the 2026-10-10 snapshot of Hkp before integration. Current integration status is recorded in the section below.

| Owner | Day 0–2 task | Status | Evidence / next step |
|---|---|---|---|
| Member 1 — Data | Download official PDFs/pages, verify reuse permission | Blocked | `data/raw/` contains only `.gitkeep`. The registered sources do not provide a confirmed reuse/redistribution grant; the blueprint directs us to keep URLs and skip files when rights are unclear. Ask each publisher before redistributing; keep source copies local only if the team confirms lawful internal use. |
| Member 1 — Data | Process, visually inspect Nepali/page numbers, deliver processed JSONL | Partial | Processor supports PDF/HTML, NFC cleanup, page fields, OCR fallback, and synthetic HTML checks passed earlier. No official files/PyMuPDF/Tesseract data available here; `data/processed/` contains only `.gitkeep`, so no visual page QA or deliverable exists. |
| Member 1 + Member 3 | Write and verify 15 Day 1 questions together | Pending | `eval/question-drafts.md` has 10 unverified drafts; `main/dev` has 10 JSONL records, 0 verified. Requires source pages before filling expected facts and citations. |
| Member 2 — Retrieval | Run embedding smoke test | Blocked | Attempted `python scripts/smoke_test_embedding.py`; failed with `ModuleNotFoundError: sentence_transformers`. Install project requirements/model before rerunning. |
| Member 2 — Retrieval | Build Chroma index from Member 1's processed files | Blocked | No processed chunks exist and Chroma is not installed. No index built. |
| Member 2 — Retrieval | Implement `search(query, k=5, service=None)`, explain score | Partial | Hkp commit `7e7801d` implements dense Chroma search with source/page metadata and cosine-derived 0–1 similarity (not probability). Runtime retrieval is unverified; BM25/RRF/reranker remain future work. |
| Member 2 — Retrieval | Report hit@5 | Pending | Requires permitted processed sources, populated index, and verified questions. No metric is recorded. |
| Member 3 — Generation | Provide `answer()` and prompt/schema | Done on main/dev; absent on Hkp | Existing merged PR #5 added generation, schema/guard, tests, and a provider smoke check on main; Hkp has not incorporated those commits. |
| Member 3 — Evaluation | Grow set to 25 including 5 off-topic | Pending | Main/dev has 10 unverified question entries only. Do not invent expected facts or mark questions verified without page evidence. |
| Member 3 — Evaluation | First real evaluation after `search()`; Day 3 baseline | Pending | Main/dev runner supports evaluation, but no Hkp index or real search run exists. The results table correctly keeps unmeasured metrics as `-`. |
| Leader | Answer provider/credits/threshold/intermediate stage/results owner/submission/presenter questions | Partial | Main/dev records OpenRouter as provider, but the other decisions are not answered in the checked project notes. Threshold remains uncalibrated; default 0 is only a starting configuration, not approval to disable the guard. |
| Leader | Create shared `dev` branch | Done | Created `dev` from current `main` (2026-10-10). |
| Leader | Run Streamlit end-to-end after search exists | Blocked | Streamlit, Chroma, embedding package, index, and Hkp generation module are missing in this runtime/branch. |

No real evaluation numbers were added: the required source-backed question set and populated retrieval index are still missing.


## Integration branch status (2026-10-10)

The branch includes both the Hkp retrieval score implementation and the generation/evaluation changes merged to dev. It is not a live civic demo yet: no permitted civic sources or source-verified questions are available, and the embedding dependencies were not installed in the current environment at this point. All quality metrics remain `-`.

### Merge resolutions

- `.gitignore`: retained Hkp's local raw/processed/index exclusions and dev's `eval/runs/` exclusion.
- `.env.example`: retained dev's OpenRouter variable names and key-pool configuration; no real secrets are included.
- `config.yaml`: retained Hkp's 0.35 starting guard threshold and dev's `support_check: false`; replaced dev's instruction to set threshold 0 with a note to keep the guard on until calibration.
- `README.md`: combined dev's generation/run guidance with Hkp's 0–1 dense-score explanation and current source/index limitations.
- `docs/results.md`: retained dev's Member 3 log and eval-run table; appended Hkp audit/commit rows. No historical rows removed.
- `requirements.txt`: retained dev's dependency categories; it will be pinned in the environment commit.
- `src/retrieval/search.py` and `docs/retrieval-score.md`: kept Hkp's dense search and score documentation.


## Follow-up verification (2026-10-10)

| Area | Status | Evidence |
|---|---|---|
| Environment | Done | CPU-only torch 2.14.1+cpu installed first; pinned requirements installed after two WinError 32 file-lock attempts; final `pip check` reported “No broken requirements found.” Embedding smoke check passed: 10 examples (5 Nepali + 5 English), vector size 1024. |
| Sources and rights | Partial | Registry marks official DoTM/MOHA terms unclear and passport pages all-rights-reserved; no such page was fetched. One Open Data Nepal page carries the literal CC BY 4.0 footer text and was fetched locally for extraction only. Human approval is still required before selecting civic sources. |
| Processing | Partial | One HTML page produced one page-linked JSONL row. Visual/content spot check found navigation/footer and license text only; not useful dataset substance and not civic evidence. |
| Retrieval | Partial | Builder ran: one processed page, 0 eligible civic chunks, 0 indexed records. Five sample searches returned empty lists; no score values exist. hit@5 remains “-” because no human-verified expected sources exist. |
| Evaluation set | Partial | 25 records now exist: 20 answerable drafts and 5 out-of-scope drafts; all have expected=TODO, verified=false, and empty source chunk/URL. The normal runner has zero eligible verified questions and must not produce quality metrics. |
| Streamlit | Partial | Headless Streamlit announced localhost:8501 and localhost HTTP probe returned 200. The local checkout lacks the merged generation module, and no civic index exists, so the sample real query returned `not_found` with an empty citations list; a supported cited answer cannot yet be verified. |

No measured evaluation row was added. The eval runner’s default selector has zero verified questions; its code exits with “No questions to run. Add verified questions or pass --include-unverified.” before computing metrics. It was not invoked on this branch because no source-backed verified questions exist. The test fixture values are synthetic and are not used as evaluation results.

Human decisions still needed: written permission/open licensed civic sources, presenter name, and API-credit spending limit. Also confirm whether any unclear-terms sources may be downloaded for private extraction, which is distinct from redistribution permission.


## Agent setup verification (2026-10-10)

| Check | Result | Evidence / limits |
|---|---|---|
| Offline pytest suite | Pass | `4 passed`; synthetic processor metadata, Chroma score/filter behavior, draft-question skipping, and Git tracking guard. Used a repository-local pytest temp directory because the sandbox temp directory was not writable. |
| Pinned dependency consistency | Pass | `pip check`: `No broken requirements found.` |
| Embedding smoke check | Pass | Script printed `Embedding smoke check passed: 10 examples (5 Nepali + 5 English), vector size 1024`. Hugging Face warned that free cache space was slightly below the model's advertised download size. |
| Synthetic evaluation harness | Pass | The offline fixture runner wrote one ignored run record and skipped the draft item. Mock percentages are not civic evaluation results and were not added to the evaluation tables. |
| GNU Make setup target | Not run | `make setup` failed because `make` is not installed in this Windows environment. The existing `.venv` was already available. |
| Source downloads / index build | Not run | Setup-only session; no source pages or Chroma index were downloaded or built. |
