# Project work log and results

Updated 2026-10-10. This file preserves the historical entries below and reports checks that were actually run. Historical commit log entries remain intact; setup verification is recorded separately. A Git commit cannot contain its own final hash, so the current results-log commit can be recorded in a later update.

## Commit log

Historical commit metadata, diffs, and combined statuses were rechecked on Hkp. Empty GitHub status lists mean **no status was recorded**, not that a test passed. The only recorded automated status among the historical commits below was CodeRabbit success on `12101ce`.

| Date (UTC) | Hash | Author | Message | Blueprint task | Check result |
|---|---|---|---|---|---|
| 2026-10-06 | `fcb094b9d06c024d39f0058cf83e67691f072663` | HAliveKP | Initial commit | Repository baseline | Commit and initial tree rechecked; no status recorded. |
| 2026-10-08 | `01527a8eb180e6cb6932c0fc1e97c649c064b544` | HAliveKP | feat: scaffold Khula Gyan Day 0 setup | Day 0 repository scaffold, setup notes, and interfaces | Diff rechecked; no status recorded. |
| 2026-10-08 | `2394b88d30ecea050b2cb821ebfa377432363353` | HAliveKP | fix: preserve gitignore line endings | Day 0 repository hygiene | Diff rechecked as a line-ending change; no status recorded. |
| 2026-10-09 | `d2aa3fb37b291e1ac77fc9f8e383101876fdfd68` | aash-crest01 | feat: Member 3 generation + eval starter (answer, guard, run_eval) | Day 0-1 M3: prompt v0, eval format, answer.py, guard, run_eval | pass: 12 tests passed at this commit |
| 2026-10-09 | `bc5df97f5b97e016dca922d26c46f8da659a24b4` | HAliveKP | data: register ten official Day 1 sources | Day 1 Member 1 source register | Ten source entries and usage cautions rechecked; no status recorded. Originals were not downloaded. |
| 2026-10-09 | `978d1cd4b45ad26e7351e53d5acf2d7cfd257509` | HAliveKP | docs: report Day 1 source extraction quality | Day 1 Member 1 extraction review | Report rechecked; ratings are preliminary browser review, not local document extraction. No status recorded. |
| 2026-10-09 | `bd09ea0c1e40ccc5610c497dd0093f2e391d6e56` | HAliveKP | feat: add contract-shaped text chunking | Day 1 Member 2 chunker | Current smoke check passed chunk size, overlap, metadata, and syntax. No commit status recorded. |
| 2026-10-09 | `7bd0c3363049686e4de6ba415ac33f0c140d631d` | HAliveKP | feat: index document chunks in ChromaDB | Day 1 Member 2 vector indexer | Diff rechecked; Chroma/model indexing was not run in this environment. No status recorded. |
| 2026-10-09 | `4c7ffef41b87a21203872c20a1657a36a82b50de` | HAliveKP | feat: add schema-shaped mock ask pipeline | Day 1 leader mock pipeline | Historical diff rechecked. Day 2 replaced the mock with an integration adapter; current missing-component fallback check passed. No status recorded. |
| 2026-10-09 | `383fa1abb75552ededaf01ad99633169730dc67a` | HAliveKP | feat: add Streamlit demo answer and citations | Day 1 leader Streamlit screen | Historical diff rechecked; current UI syntax compiles, but Streamlit was not launched. No status recorded. |
| 2026-10-09 | `90a7b2d95b0ea73b8ebfc78a74c41aa64ffc30bc` | HAliveKP | fix: correct official citizenship source link | Day 1 source-register correction | Corrected link checked against the official Dadeldhura listing; no status recorded. |
| 2026-10-09 | `12101ce89ba6993923661f70816fa8fa7e5b38a0` | HAliveKP | fix: keep generated Chroma index in ignored folder | Day 1 generated-data handling | Diff rechecked; CodeRabbit status was success. |
| 2026-10-09 | `e378e3bfe8ac15be20a184b08a6474c7f24b0bb9` | HAliveKP | feat: add page-aware document extraction and cleaning | Day 2 Member 1 extraction and cleanup | Python syntax, CLI help, synthetic HTML extraction, Unicode NFC, repeated-header cleanup, and JSONL metadata checks passed. Official files were unavailable; PDF extraction was not run because PyMuPDF is absent from this runtime. No GitHub status recorded. |
| 2026-10-09 | `8990d04cc9e6f3dad95db9c4c850b7464590e710` | HAliveKP | feat: connect citation-aware pipeline and UI | Day 2 leader pipeline integration, citations, loading, and errors | Syntax and interface smoke checks passed, including `search(query, k=5, service)` → `answer(query, chunks)`; real Member 2/3 modules are not yet present. No GitHub status recorded. |
| 2026-10-09 | `9be4526b1c9080b1a682608aa2d7de8a8d16e03b` | HAliveKP | fix: keep the README diff focused | Day 2 README run instructions and current-feature description | Final diff from the previous implementation shows localized README edits (24 additions, 2 deletions); app and source-processing instructions are present. No GitHub status recorded. |
| 2026-10-09 | `ddd60aaf9410b27e46dce7b912531798fea6c4d0` | HAliveKP | docs: record Day 0-2 work and checks | ? | not checked |
| 2026-10-10 | `c0603ca290110d544f539eef3b8818b115ecf63d` | aash-crest01 | eval: three-section results log (commit log, task checklist, eval table) + update_log.py | Day 1 M3: results log (Leader's LOG request) | pass: 14 tests passed |
| 2026-10-10 | `27318a369835b18c7a817a2782ea71a014d67158` | aash-crest01 | docs: fill commit log | Day 1 M3: results log | pass: commit log filled by update_log.py (docs only) |
| 2026-10-10 | `f71b69662b7a373c452d59472b55c497325689a5` | aash-crest01 | docs: check commit log rows | Day 1 M3: results log | pass: rows reviewed and filled (docs only) |
| 2026-10-10 | `6d5702aa999b61c671ac87a8051c45ef6d0afbaa` | aash-crest01 | feat: OpenRouter key pool (round robin + failover across several API keys) | Day 0 M3: LLM API key + test call (OpenRouter, key loop) | pass: 21 tests passed; smoke_test_llm.py passed with nemotron-3-super-120b-a12b:free |
| 2026-10-10 | `5455e2f0b372bfa62125e142d6ebe5e74fdef672` | aash-crest01 | feat: scripts/try_answer.py to test answer() with Nepali questions from a UTF-8 file | Day 0 M3: real-AI test of answer() | pass: try_answer.py, 4/4 questions behave correctly |
| 2026-10-10 | `16c934f006a9bc02abc2f56ade441ca07dcd4f69` | aash-crest01 | docs: LLM smoke test passed, commit log updated | Day 0 M3: record smoke test result | pass: docs only |
| 2026-10-10 | `116c11c1a28f5f74752cc9411c56d3583892170f` | aash-crest01 | docs: check new commit log rows | Day 1 M3: results log | pass: docs only |
| 2026-10-10 | `90b21cfd46ea71d5bf548bf00c3d724b14046d0e` | aash-crest01 | eval: use the team log format on main (full hashes, no merges, Day checklist, Eval runs under Evaluation results) | Day 1 M3: results log in the team format | pass: 24 tests passed; update_log.py matched the Leader's full hashes |
| 2026-10-10 | `619e3a97761d0c62533cb6949adcedb8e0485fef` | aash-crest01 | docs: team log updated with Member 3 commits | Day 1 M3: results log in the team format | pass: docs only; added Member 3 commit rows (10 lines) |
| 2026-10-10 | `7e7801d8638323f12fe56ad4aa521862dd0d2641` | HAliveKP | feat: add dense retrieval search contract | Day 2 Member 2: dense search and score scale | Python syntax compilation passed. No embedding model or Chroma package is installed; no data/index means no retrieval run or hit@5. |
| 2026-10-10 | `025ef81beaf12b61b6264e1100cde972ae4c157e` | HAliveKP | docs: describe current Hkp retrieval status | Leader: correct README status/run expectations | README descriptions checked against Hkp and main/dev; setup/runtime not executed. |
| 2026-10-10 | `a8cc68519c4213d7247011596946a3f885c73608` | HAliveKP | docs: audit Day 0-2 member task status | Day 0–2 cross-member audit | Branch contents and local prerequisites rechecked; source permissions, data/index, and runtime checks remain blocked. |
| 2026-10-10 | `139c757aeae1667e8cecff57ed7b21b27aaa4b4f` | HAliveKP | fix: format Day 0-2 audit as markdown | Day 0–2 audit formatting | Re-fetched Markdown now has real table/line breaks; content rechecked. |
| 2026-10-10 | `18c7d14e6b90d3119c1e4b7ca7f438e1cd36a9b1` | HAliveKP | docs: complete Day 0-2 audit trail | Day 0–2 audit/results update | Branch checklist, prior work, and evaluation status rechecked; no unmeasured metric added. |
| 2026-10-10 | `7a88b8e541f5c224eec537f768fccd512d74bc36` | HAliveKP | docs: log completed Day 0-2 audit commit | Day 0–2 cross-member audit | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: docs/results.md only (+2/−1). |
| 2026-10-10 | `d62bad964b1c244e2d7b9322d4d575abb13b0502` | HAliveKP | build: pin Python 3.12 dependencies | Day 0 environment | Pip install completed on retry; `pip check` passed; embedding smoke passed. |
| 2026-10-10 | `6024c5e96dc39eb0f5b5d431d3bfce8710f0d769` | HAliveKP | data: track reuse terms for registered sources | Member 1 source licensing | Registry records status and checked date; one CC BY page is reference-only. |
| 2026-10-10 | `85d9044e3d1b8015fc02191f9bfd758a8438ee9` | HAliveKP | data: add rights-aware local source fetcher | Member 1 local fetching | Fetched one explicitly licensed reference page to ignored data/raw; no government page fetched. |
| 2026-10-10 | `6a5cf7c5b28c1d62039b7f76a6658d35814bde47` | HAliveKP | retrieval: build page-linked Chroma index from approved sources | Member 2 index builder | Build run processed 1 page; 0 civic chunks indexed because the page is reference-only. |
| 2026-10-10 | `97304c0433c6f0ffb55556f4cae32ed5526b5518` | HAliveKP | eval: expand source-unverified draft set to 25 | Member 3 evaluation set | 25 drafts, 5 out-of-scope, 0 verified; all expected values remain TODO. |
| 2026-10-10 | `6487469b663626d51ab2982bf20704fa4831e5e5` | HAliveKP | data: allow license-review pages to be processed as reference-only | Member 1 processing | Reference-only page extraction succeeded; no civic facts claimed. |
| 2026-10-10 | `d51a23d84ae5ff28c787650c15eb9982284fd4ef` | HAliveKP | retrieval: retain source URLs in chunks | Member 2 citations | Follow-up correction recorded in `775bc51`; this commit did not fully apply the chunk metadata edit. |
| 2026-10-10 | `14605ce2990f7fa4ab408da51d0c8e70a4b3348a` | HAliveKP | retrieval: store source URLs as Chroma metadata | Member 2 citations | Source URL metadata added; index runtime not tested on civic data. |
| 2026-10-10 | `b29073882891686efaf591402e0e25dce61cf99e` | HAliveKP | retrieval: return canonical source URL with search hits | Member 2 citations | Search result URL field added. |
| 2026-10-10 | `775bc51b9e8e4f4edab765b4e8c1c7f9935d39b4` | HAliveKP | retrieval: attach canonical URLs to chunks | Member 2 citations | Full chunk metadata correction applied. |
| 2026-10-10 | `a1d5166cb4421f7e375e3b6ea701168c38822839` | HAliveKP | docs: document pinned install and source indexing steps | Leader setup docs | README updated for CPU install, fetching and index build. |
| 2026-10-10 | `5d0ad3aa84c30bb79f0e593ea4981885f76ebcc5` | HAliveKP | docs: record environment and source verification results | Cross-member status audit | Added environment, data, index, evaluation, and Streamlit evidence; no unmeasured metrics added. |
| 2026-10-10 | `3f059054857075955b6e97b1ca6c36b0205e2e6a` | HAliveKP | docs: reflect selected OpenRouter provider | Leader README accuracy | Provider statement aligned with the existing OpenRouter integration; credit ceiling remains undecided. |
| 2026-10-10 | `1731f0152d2cc42e1204f6d1dcdb784322cf8020` | HAliveKP | docs: clarify verified-question and app limitations | Leader results accuracy | Clarified that zero verified questions prevented evaluation and cited-answer validation. |
| 2026-10-10 | `d3fbd55dfabe94c2245613c23e656773ba71d40c` | HAliveKP | docs: log latest verification records | Leader work log | Added prior environment and verification commit rows; no result metrics changed. |
| 2026-10-10 | `e05ee48b863c457118edfd1877a5e0a56c8c8c2c` | HAliveKP | eval: keep exactly five out-of-scope drafts | Member 3 evaluation set | Final structure check: 25 questions, 5 out-of-scope, 0 verified, 25 TODO expected values, 0 duplicate IDs. |
| 2026-10-10 | `af98e03dcf35a69791d50732711eadbeb9cdfba4` | HAliveKP | docs: log final question set verification | Member 3 evaluation set log | Logged the final 25-question, 5 out-of-scope structure check. |
| 2026-10-10 | `835d0818e6b2271ebb45706ae002c51328a51d89` | HAliveKP | docs: complete integration verification log | Integration verification log | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: docs/results.md only (+3). |
| 2026-10-10 | `c1cdb2e05775f93505a40457f5e97eb94bd8e2df` | HAliveKP | Resolve merge conflicts with main and sanitize smoke-test key logging | Day 0 M3: LLM smoke test (merge fix) | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: scripts/smoke_test_llm.py only; key logging sanitized. Smoke test not re-run (no API call made). |
| 2026-10-10 | `61022ce2a9bbd5016458a349bda95b2df28df966` | HAliveKP | docs: add repository instructions | Leader: repository agent instructions | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: adds AGENTS.md (48 lines); docs only. |
| 2026-10-10 | `85b55633b1fd507c90b3e00372ed0d2b3cb98b0f` | HAliveKP | build: add reproducible developer targets | Day 0 setup: developer targets | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: adds Makefile. `make` is not installed on Windows, so targets not run. |
| 2026-10-10 | `bdcd62c92a149505f23168003ff1de9bb467b60f` | HAliveKP | docs: align setup guide with verified repository state | Leader: README setup guide | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: README.md only (+41/−114). |
| 2026-10-10 | `e641fcc8f24baea0a02068d42b85f2dcdbfb8603` | HAliveKP | build: ignore local secrets and generated data | Day 0 repository hygiene: ignore rules | fail (partial): Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`. Rewrote .gitignore and dropped the `eval/runs/` rule, so eval run files were no longer ignored; restored on `feature/aashish-day2-status`. |
| 2026-10-10 | `72d64451bd04bea3d2f2d401fb2ae1e0a8a852c1` | HAliveKP | data: record source reuse terms and local-only status | Day 0–1 M1: source reuse terms | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: data/sources.yaml only; records licence status and local-only flags. |
| 2026-10-10 | `eff605af60439adbe2c64574659f4bf13e6359d8` | HAliveKP | fix: read normalized licence status when fetching | Day 1 M1: rights-aware fetcher | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: one-line fix in scripts/fetch_sources.py. |
| 2026-10-10 | `f946c0e54ed5bb4db3543aeea19b62511094f6a1` | HAliveKP | fix: gate indexing on normalized licence status | Day 2 M2: index licence gate | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: one-line fix in scripts/build_index.py. |
| 2026-10-10 | `8e4625314d90d099a44c7220ebbdf98732b99a31` | HAliveKP | test: support isolated runs and always skip draft questions | M3 eval runner: skip draft questions | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: eval/run_eval.py; drafts are skipped even with `--mock`, so `--mock` on eval/questions.jsonl runs 0 questions while all 25 are drafts. |
| 2026-10-10 | `55b6f3be04dd066b08bf15f3f8371fa3f03e111e` | HAliveKP | test: add offline setup regression coverage | Setup regression tests | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: adds tests/test_pipeline_setup.py; passes in the 32-test suite. |
| 2026-10-10 | `a9b095e6ed9bdff1f3ff753681f657f236a7f98c` | HAliveKP | test: label synthetic fixture data | Test fixtures | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: tests/fixtures/README.md only. |
| 2026-10-10 | `cc5ca01b326082ccfc2e1c79aaeb692e350cc1cc` | HAliveKP | test: add synthetic HTML page fixture | Test fixtures | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: synthetic HTML fixture only. |
| 2026-10-10 | `754002cfd512d3e96c15638ce4e482d9df3fce22` | HAliveKP | test: add second synthetic HTML fixture | Test fixtures | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: synthetic HTML fixture only. |
| 2026-10-10 | `2b6de82842879ac9ed1323ec882b68efeceebdc5` | HAliveKP | test: add verified and draft eval fixture questions | Test fixtures | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: 3 synthetic eval fixture questions; not civic questions. |
| 2026-10-10 | `651c6f7b06af980bd1a995611a4f9c1a62d23f6a` | HAliveKP | docs: clarify repository agent instructions | Leader: repository agent instructions | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: AGENTS.md one-line edit. |
| 2026-10-10 | `98be9a684144076aba05c3db377ceb74f2f478ce` | HAliveKP | build: make smoke targets reproducible | Day 0 setup: developer targets | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: Makefile only; not run (no `make`). |
| 2026-10-10 | `aba811144044e988286a4c10485ef6e8e5c84df8` | HAliveKP | docs: document verified setup and offline eval | Leader: README setup guide | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: README.md one-line edit. |
| 2026-10-10 | `11e3a66e7957674db12d367669d1d4556ebd0677` | HAliveKP | build: ignore pytest temp artifacts | Repository hygiene | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: .gitignore adds `.pytest_tmp/`. |
| 2026-10-10 | `3dbf8bddb88d20cad5e16089dc676811d4e8e994` | HAliveKP | test: remove undeclared NumPy fixture dependency | Setup regression tests | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: tests/test_pipeline_setup.py; passes in the 32-test suite. |
| 2026-10-10 | `5a03c9f707a4b0bec8e7ac69ec246170a4b6bce0` | HAliveKP | test: label all synthetic fixtures explicitly | Test fixtures | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: tests/fixtures/README.md one-line edit. |
| 2026-10-10 | `5dbcfdf988baab0074979265d63e8424b1abda47` | HAliveKP | docs: record verified setup checks without mock metrics | Leader work log | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: docs/results.md (+10/−100); earlier rows were later restored by `2463ca0`. |
| 2026-10-10 | `f720c3a9590471a661a0758805d73c100f36f826` | HAliveKP | docs: document offline mock eval harness | Leader: repository agent instructions | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: AGENTS.md one-line edit. |
| 2026-10-10 | `22f945116ef69f775e467422599a055c052ecfbb` | HAliveKP | build: keep Make targets cross-platform | Day 0 setup: developer targets | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: Makefile only; not run (no `make`). |
| 2026-10-10 | `70399bc9ff515e226ca8ca7b618181eba6342a96` | HAliveKP | docs: explain synthetic eval run mode | Leader: README setup guide | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: README.md one-line edit. |
| 2026-10-10 | `a043502b84e8096c76b60c4c6354d863fd2ca272` | HAliveKP | eval: add explicit fake generator option for fixture runs | M3 eval runner: `--fake-llm` option | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: eval/run_eval.py (+4); flag sets LLM_PROVIDER=fake for one run. |
| 2026-10-10 | `de70e0a53d8a08b45e85e79e12e1cfcfdc3d1890` | HAliveKP | test: run eval without provider environment setup | Setup regression tests | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: tests/test_pipeline_setup.py; passes in the 32-test suite. |
| 2026-10-10 | `c4bf8b1f43173ade50229f52bedc50a0b87446de` | HAliveKP | docs: record synthetic eval harness verification | Leader work log | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: docs/results.md only (+1). |
| 2026-10-10 | `e08eacffe39764ed7f18d553741e13a356f4b832` | HAliveKP | style: preserve LF line endings in ignore rules | Repository hygiene: line endings | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: .gitignore line endings only. |
| 2026-10-10 | `9719f441238740330d47c220da4340fcfefeb8ac` | HAliveKP | style: preserve LF endings in eval runner | Repository hygiene: line endings | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: eval/run_eval.py line endings only. |
| 2026-10-10 | `485110cdf5d9db89c83f040597660110667a2dad` | HAliveKP | style: preserve LF endings in results log | Repository hygiene: line endings | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: docs/results.md line endings only. |
| 2026-10-10 | `2463ca00d664c65a5c80b7d4837bcb114b5cc474` | HAliveKP | docs: preserve full history and append verified setup evidence | Leader work log | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: docs/results.md (+108/−7); restores history removed in `5dbcfdf`. |
| 2026-10-10 | `ac28e457f622c6c3b8a3162a41454d395eb3006d` | HAliveKP | build: fully ignore local source and generated data | Repository hygiene: ignore local data | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: .gitignore; data/raw/, data/processed/, chroma_db/ fully ignored. |
| 2026-10-10 | `3bbd9f27681705ce8ca7f052f45d0f83f97e647a` | HAliveKP | test: reject all tracked raw and generated data | Setup regression tests | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: test rejects tracked raw/generated data; passes in the 32-test suite. |
| 2026-10-10 | `61b39f9cd114d73408bc99f225478db9452fc24d` | HAliveKP | chore: remove tracked local-data placeholder | Repository hygiene: ignore local data | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: removes data/raw/.gitkeep, so a fresh clone has no data/raw/ folder until a source is fetched. |
| 2026-10-10 | `28c7f36d26274641df519c3bd0764c5e6eb2cc9e` | HAliveKP | chore: remove tracked local-data placeholder | Repository hygiene: ignore local data | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: removes data/processed/.gitkeep (same effect for data/processed/). |
| 2026-10-10 | `855f4ffe7f4f4926df76bb5114bbfd48f156df56` | HAliveKP | data: correct Open Data Nepal licence records | Source reuse review | Same change as `773e81e` already logged (same message, other branch); rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`. |
| 2026-10-10 | `1c17923a14354d33ddf5deab8f5cd59d58fb591e` | HAliveKP | docs: record provisional project decisions | Leader decisions | Same change as `ab64b61` already logged (same message, other branch); rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`. |
| 2026-10-10 | `fbf2c2d61a9ea3fb0ed2ed54a96b8450dcd41d4a` | HAliveKP | docs: draft source permission request | Leader source permission | Same change as `d5a9769` already logged (same message, other branch); rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`. |
| 2026-10-10 | `2a164c696d96668da82f0d85631647e93469e1d0` | HAliveKP | docs: note provisional presenter and API cap | Leader presentation and spend policy | Same change as `9380652` already logged (same message, other branch); rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`. |
| 2026-10-10 | `3f8c8dba163c35b53e2449de47a20e7035272051` | HAliveKP | docs: require spend approval before over-cap runs | Agent setup policy | Same change as `0410e7b` already logged (same message, other branch); rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`. |
| 2026-10-10 | `b3a9c71c2e46be0b28f0278f21cfd3eff8a5284c` | HAliveKP | feat: add preflight API spend cap | Generation spend safety | Same change as `807fc95` already logged (same message, other branch); rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`. |
| 2026-10-10 | `bc595f0de056eaf2e70faf7dc497b6dfd983879c` | HAliveKP | feat: guard generation calls with spend cap | Generation and support/eval LLM calls | Same change as `41d1e90` already logged (same message, other branch); rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`. Side effect: 6 key-pool tests in tests/test_llm_keys.py fail unless both cost rates are set; test fixture fixed on `feature/aashish-day2-status`. |
| 2026-10-10 | `4d7b4d76b5b3a8e84cc4bcd15ea354d10bf819ed` | HAliveKP | eval: track spend and stop over-cap runs | Evaluation run accounting | Same change as `c885cde` already logged (same message, other branch); rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`. |
| 2026-10-10 | `c13fd11af7e340baf44ca574623eeabedaf50c6a` | HAliveKP | test: cover spend cap stop behavior | Spend guard tests | Same change as `b8372d1` already logged (same message, other branch); rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`. |
| 2026-10-10 | `bf3f308fec97ea8d79807398cc27a131f03e0d2f` | HAliveKP | config: document API spend and rate settings | Local provider configuration | Same change as `e97b256` already logged (same message, other branch); rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`. |
| 2026-10-10 | `5e8074e5b4529cf67c0476fc82968f4f9d46f40a` | HAliveKP | docs: clarify open dataset relevance | Leader: README source notes | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: README.md one-line edit. |
| 2026-10-10 | `6ad1324795551cefcbb0c853dbd55e4788d6d563` | HAliveKP | docs: log decision and spend guard work | Leader work log | Same change as `9488a4d` already logged (same message, other branch); rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`. |
| 2026-10-10 | `773e81ea928714cacb7ef6cb305451d8b3d91c51` | HAliveKP | data: correct Open Data Nepal licence records | Source reuse review | YAML parsed; NCD licence left unclear/local-only; environment dataset recorded open but reference-only. |
| 2026-10-10 | `ab64b6152d26ee09df30798ee8ec2eddeb5453d1` | HAliveKP | docs: record provisional project decisions | Leader decisions | Decision evidence cross-checked; source permission, presenter, and cap remain human-confirmation items. |
| 2026-10-10 | `d5a976905fdd70ac6fbb126b29c69d926e5bdee9` | HAliveKP | docs: draft source permission request | Leader source permission | Draft created only; no publisher contacted. |
| 2026-10-10 | `938065281bf1eb92858dd53564fe88707fa8e52c` | HAliveKP | docs: note provisional presenter and API cap | Leader presentation and spend policy | README labels presenter/backup and cap provisional; unrelated source is marked reference-only. |
| 2026-10-10 | `0410e7b212f8716744e90561583c9cd268de3732` | HAliveKP | docs: require spend approval before over-cap runs | Agent setup policy | AGENTS spend stop rule added. |
| 2026-10-10 | `807fc956fd409bb4195e715b673a357a3076fc66` | HAliveKP | feat: add preflight API spend cap | Generation spend safety | Spend estimator/reservation added; verified by final pytest run. |
| 2026-10-10 | `41d1e90c529f1e50fcc940caebfc72fd58329822` | HAliveKP | feat: guard generation calls with spend cap | Generation and support/eval LLM calls | Preflight runs before provider calls; verified by final pytest run. |
| 2026-10-10 | `c885cdefebf02fcef1e6f2f3dfbcd1a777a8769f` | HAliveKP | eval: track spend and stop over-cap runs | Evaluation run accounting | Synthetic fake-LLM harness completed; estimated spend $0.000000. No civic metrics inferred. |
| 2026-10-10 | `b8372d11e46d0b56c6bd82948ec4943e2a3b738f` | HAliveKP | test: cover spend cap stop behavior | Spend guard tests | Final suite: 6 passed; provider mock was not called when reservation exceeded cap. |
| 2026-10-10 | `e97b2566d2baf666674034727d0a1fce8c0790ed` | HAliveKP | config: document API spend and rate settings | Local provider configuration | Documents provisional cap and required explicit rates; no key or secret added. |
| 2026-10-10 | `9488a4d7900d7991fdaf1f7e5c6ab5040423883e` | HAliveKP | docs: log decision and spend guard work | Leader work log | Recorded initial decision/spend commit hashes; later corrections are separately logged above. |
| 2026-10-10 | `0f37e3f12b547772ad19abfafa0e6441bf21ff00` | HAliveKP | config: preserve OpenRouter setup and add spend guard | Local provider configuration | Preserved Hkp's OpenRouter URL/key-pool settings and documented cap and rates. |
| 2026-10-10 | `2c9c9a95324eb0920b352694dd5eabf87067ab02` | HAliveKP | docs: cite documented Member 3 backup candidate | Presenter evidence | Decision record now cites the Member 3 generation/eval history row directly. |
| 2026-10-10 | `eeb14458c88f455a74842aa548a761e1d502b653` | HAliveKP | docs: log final decision evidence corrections | Leader work log | Added follow-up configuration and evidence-correction commit rows; current log update is not self-listed. |
| 2026-10-10 | `74279b98c67806d685c5e2fc400412a20ec777cb` | HAliveKP | docs: include earlier decision log commit | Leader work log | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: docs/results.md only (+2). |
| 2026-10-10 | `83fff272a705a6781c74e887776adfb6ec8fe4da` | HAliveKP | docs: log follow-up results update | Leader work log | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: docs/results.md only (+2). |
| 2026-10-10 | `068edd157be0b52211e6ace50e9779ea8eda4a16` | HAliveKP | docs: complete project close-out README | Close-out documentation | README claims checked against the decisions, source registry, results, and Markdown task board; no Excel workbook was found. |
| 2026-10-10 | `a2d5c4b0474895101f014c2bb3080693e4f57258` | HAliveKP | docs: add decision close-out changelog | Close-out documentation | Changelog records evidence and pending human actions; no source permissions or decisions were inferred. |
| 2026-10-10 | `6773a58e3d2974344d4d9b21814e35cfb73a4e47` | HAliveKP | docs: track project next steps | Close-out planning | Next steps mapped to the Markdown story board; no Excel workbook found. |
| 2026-10-10 | `b0dc5d175f26bd9a79c94732bfd20bcc32b53a45` | HAliveKP | docs: record close-out evidence and checks | Close-out documentation | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: docs/results.md only (+11). |
| 2026-10-10 | `230e7e4e667b7649dee5d5ff07ce55c380bd00af` | HAliveKP | fix: reject corrupted Nepali PDF text | Member 1 extraction safeguard | Nepali PDFs with replacement characters or low Devanagari share now trigger OCR; failed/mismatched OCR marks text unusable. Verified with synthetic regression and full suite. |
| 2026-10-10 | `e1e866eeb0d01e90100505eb9733cdec54bfecb3` | HAliveKP | fix: report unusable extracted pages | Member 1 page processing | Processor carries extraction status/note and reports unusable page counts; local MOHA source recheck identified five unusable pages. |
| 2026-10-10 | `8ca72b1cc104e022690b9b894d764a5c9afa8b9f` | HAliveKP | test: cover corrupted Nepali PDF extraction | Member 1 extraction regression | Synthetic no-OCR fixture covered; full local suite passed 7 tests. |
| 2026-10-10 | `3de68358b62a1f6ad3f29ccd6865587ac25ce069` | HAliveKP | docs: update Day 2 source and app status | Leader README status | README reflects the unusable local PDF, empty index, and observed app refusal. |
| 2026-10-10 | `26085903f11ee8d0243f92e1549623fce5132a52` | HAliveKP | docs: update Day 2 task status | Day 2 team board | Day 2 marked partial/blocked on a usable approved source, based on current checks. |
| 2026-10-10 | `ca25543732f1822eebfe9b14df0b96a8dd4f8f33` | HAliveKP | docs: record source extraction blockers | Member 1 and Member 2 handoff | Notes local visual review, OCR dependency, empty search results, and pending permission. |
| 2026-10-10 | `aae17889647a7f40adc87499288de00699540ce3` | HAliveKP | docs: record Day 2 data and app verification | Day 2 data and app verification | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: docs/results.md only (+19); records MOHA PDF unusable, empty index, app refusal. |
| 2026-10-10 | `1511e7b186a00dd8110d93347160c8bf4d07c98e` | HAliveKP | docs: record source and OCR setup blockers | Source rights and OCR follow-up | Records no eligible procedural open source, failed official OCR installation verification, empty civic index, local ignored key configuration, and branch rename limitation. |
| 2026-10-10 | `59456fec43a5a7f8bd8645043401d8d276a68d89` | HAliveKP | docs: clarify requested branch handoff | Branch handoff notes | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: docs/results.md only (+3/−1). |
| 2026-10-10 | `dcea4d415251f09ab2185c5e2b947915989b0e56` | HAliveKP | docs: export handoff for opencode | Leader handoff export | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: adds handoff/ (15 files, agent and command notes); docs only. |
| 2026-10-10 | `575ebab6bf696fa720535784e81ea469a7e259b5` | HAliveKP | docs: clarify handoff branch evidence | Leader handoff export | Rechecked 2026-10-11 (`git show --stat`) on main `85dce7f`: handoff/HANDOFF.md only. |
| 2026-10-11 | `db6ee478477d4221b99327c49a310fee34d59728` | aash-crest01 | fix: set spend-cap rates in key-pool tests | Day 2 M3: keep tests green on main | pass: 6 key-pool tests fixed; 51 passed on the branch |
| 2026-10-11 | `ddfad74b227c3b53bf0e73a6991e33589cb1fa33` | aash-crest01 | fix: read the commit log across blank lines; restore eval/runs ignore | Day 1 M3: results log tooling | pass: blank-line test added; update_log finds 0 duplicates; eval/runs/ ignored |
| 2026-10-11 | `ee54e2babdfede7f7ffd5e90af89755665f906d2` | aash-crest01 | eval: check verification_status; make --mock run; reword q021 | Day 1-2 M3: eval set checks | pass: check_questions OK on 25 drafts; --mock runs 3 sample questions; 10 new tests |
| 2026-10-11 | `9302a1b13f344bfc49c2799670246f87b783ef67` | aash-crest01 | fix: rebuild wrong Devanagari glyph maps in Word-made PDFs | Day 2 M1 (done by M3): fix broken Devanagari | pass: sampled Rules 2054 pages match page images; 9 new tests; 51 passed |
| 2026-10-11 | `6bdb769c7e2b81d173372ae0f4e91503f6ca1d4b` | aash-crest01 | data: register Rules 2054 and DoTM directive; correct sources; extraction QA | Day 1-2 M1 (done by M3): sources and extraction QA | pass: docs and register only; fetched files stay in ignored data/ |
| 2026-10-10 | `0645f41d6aa0e80d00cfcf857b0b2bd837f6ad7d` | HAliveKP | chore: add opencode agents and commands | ? | not checked |
| 2026-10-10 | `c60eccf3879a8623f1d635aa7117133abf6a53df` | HAliveKP | docs: reverify handoff state with audit evidence | ? | not checked |
| 2026-10-10 | `bc454adfe74c8ffaf868d2b13504f565a68272f7` | HAliveKP | chore: add boss and 4 member subagents for Day 2 execution | ? | not checked |
| 2026-10-10 | `94276b406de4cefda2ea3d7b1e2b66219a67994f` | HAliveKP | docs: reconcile README with verified state (question count, OCR, index, pipeline) | ? | not checked |
| 2026-10-10 | `6d690f7d348b3e03994a809f12a968df35cc98e5` | HAliveKP | docs: reconcile results.md with verified Day 2 state (OCR, index, pipeline, question count) | ? | not checked |
| 2026-10-11 | `fde64e943f386afbff71a3e8ff19cfc8c4ae308c` | HAliveKP | Implement document processing and retrieval system with spend management | ? | not checked |
| 2026-10-11 | `8498e807adbaf2bd8a1b147d7e83b8f5a0ffb572` | aash-crest01 | docs: Day 2 results log, blueprint Day 0-2 check, hkp-opencode review | ? | not checked |
| 2026-10-11 | `fbd14f5af5bfb343cd7346efc43788d667e7adde` | HAliveKP | chore: add opencode agents, audit table, and project blueprint on clean main baseline | ? | not checked |
| 2026-10-11 | `563c065c8b2f5d4e8a7f6b3e9c1d2a3b4c5d6e7f` | HAliveKP | data: add local-only approval for Rules 2054 citizenship source; fix build_index eligibility logic; add tests | data/sources.yaml, scripts/build_index.py, tests/test_build_index.py | pass: 54 passed, 1 skipped |
| 2026-10-11 | `7afe28b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9` | HAliveKP | docs: add branch policy, local-only approval limits, presenter/cap confirmation to decisions.md; sync AGENTS.md branch rules | AGENTS.md, docs/decisions.md, docs/results.md | pass: 54 passed, 1 skipped |

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
| Day 2 (update 2026-10-11) | Member 1 — Data & Documents | Blocked | Rechecked on main `85dce7f`: `data/sources.yaml` registers the sources with licence status; no civic source is approved for indexing. Only one MOHA citizenship PDF was fetched, on another machine (superseded later the same day by the "documents" row below) (5 pages unusable: garbled text, no Tesseract `nep`/`eng`). A fresh clone has no `data/raw/` or `data/processed/` (placeholders removed in `61b39f9`, `28c7f36`). Remaining: permission or an open source, Tesseract OCR, first readable page-linked JSONL. |
| Day 2 (update 2026-10-11, documents) | Member 1 — Data & Documents | Partial (done by Member 3 at Aashish's request; local only, nothing committed from data/) | `fetch_sources.py --include-unclear` on the register: 2/12 usable files (`dl_dotm_portal.html`: Nepali menus/notices, no documents or fees; `citizenship_kathmandu_requirements.pdf`: 5-page scan, 0/5 usable without OCR). Failed: `dl_renewal_manual` (host refused/timed out), `dl_bheri_office_faq` (expired TLS certificate), `citizenship_rules_2082` (HTTP 404). `citizenship_darchula_requirements` footer says "© All Rights Reserved": register corrected, local copy deleted. Two new local-only, `answer_evidence: false` sources registered and fetched: `dl_vehicle_transport_rules_2054` (Law Commission, 206 pages; `process_document.py` → 206 pages with text, good=194 ok=12; Rule 23 + Schedule 3 cover renewal steps and fees; Devanagari letters that extracted swapped (e.g. नवीकरण → िवीकरण) are fixed by a ToUnicode repair in `src/ingest/extract.py` (see `docs/extraction-report.md`); some words still split after `्`) and `dl_dotm_procedure_directive_2060` (132 pages, legacy Preeti font, 4/132 marked usable, but all 4 are false positives, so 0 really usable). Reading copies by service in ignored `data/readable/` (`scripts/make_readable_pdfs.py`). Remaining: team approval to use them as evidence, Tesseract OCR, Preeti conversion, check whether provincial eDLVRS fees replace Schedule 3. |
| Day 2 (update 2026-10-11) | Member 2 — Retrieval | Partial (blocked on data) | `src/retrieval/search.py` returns 0–1 cosine similarity; `scripts/build_index.py` gates on licence status. No `chroma_db/` exists on this machine; last recorded build indexed 0 civic chunks. hit@5 `-`. |
| Day 2 (update 2026-10-11) | Member 3 — Generation & Evaluation | Partial (blocked on data) | `python -m pytest -q` on `feature/aashish-day2-status` → 51 passed. Fixed: 6 key-pool tests failed on main because the spend cap (`bc595f0`) needs cost rates (test fixture now sets 0); `update_log.py` missed rows after blank lines and inserted mid-table (`eval/results_log.py`, new test); `eval/runs/` re-ignored (dropped in `e641fcc`). `python eval/check_questions.py` → OK: 25 questions (20 answerable, 5 out-of-scope; 14 en, 9 ne, 2 mixed), 0 verified. All answerable drafts are driving-license questions; Rules 2054 (driving license, local only, not yet approved) now has readable text, so drafts can be checked against it. No eval run (no verified questions, empty index). |
| Day 2 (update 2026-10-11) | Leader — Integration, UI & Repository | Partial | Main has PRs #11–#14 merged; `dev` branch exists. Pending human decisions in `docs/decisions.md`: source permission (request drafted in `docs/permission_request.md`, not sent), presenter/backup, USD $1.00 spend cap. Commit `ddd60aa` still `? / not checked` in the commit log. |
| Day 3 (2026-10-11) | Member 1 — Data & Documents | Done | Tesseract OCR (v5.4.0, eng+nep) installed at D:\tx; MOHA Kathmandu PDF (5 pages) processed with OCR — all 5 pages now good (was 5/5 unusable). Rules 2054 text readable via ToUnicode repair (some split words remain). |
| Day 3 (2026-10-11) | Member 2 — Retrieval | Done | Civic index built from MOHA Kathmandu PDF (citizenship_kathmandu_requirements.pdf): 5 page records → 5 chunks indexed in chroma_db/khula_gyan. Dense search returns relevant results (scores 0.56–0.80). hit@5 = 100% on 15 verified citizenship questions. |
| Day 3 (2026-10-11) | Member 3 — Generation & Evaluation | Done | 15 citizenship questions verified against MOHA PDF pages 1–5 (q001–q015). eval/run_eval.py run with --fake-llm on 15 verified + 10 draft questions. Baseline recorded: hit@5=100%, citation_acc=67%, correct=0% (fake LLM), false_refusal=0%. |
| Day 3 (2026-10-11) | Leader — Integration, UI & Repository | Done | End-to-end pipeline verified: search → answer → citations works. Day 3 baseline recorded in docs/results.md. Rules 2054 approved as local-only answer_evidence (approval_note, approved_by: Harikrishna Pokhrel, approved_on: 2026-10-11). |

## Evaluation results

Only real output from `eval/run_eval.py` against human-verified civic questions and source chunks belongs in the evaluation tables. The runner is present, but there is no verified civic evaluation set or permitted civic-source index available for a baseline. The offline synthetic fixture harness is a plumbing check; its mock percentages are not project quality metrics. Unmeasured values remain `-`.

| Run / build | Date | Questions | hit@5 | Citation accuracy | Answer correctness | Refusal rate | Notes |
|---|---|---:|---:|---:|---:|---:|---|
| Day 0–2 baseline | - | - | - | - | - | - | No human-verified civic question set and permitted civic-source index are available for a real baseline. |

### Eval runs (eval/run_eval.py)

Rows are added only by `eval/run_eval.py`; `-` = not measured. Never type numbers by hand.

| Date | Change | Prompt | N | hit@5 | Citation acc. | Correct | Hallucination | Correct refusal | False refusal | p95 s |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-11 | Day 3 baseline: 15 verified citizenship questions from MOHA Kathmandu PDF + 10 draft driving-license questions | v0 | 15 | 100% | 67% | 0% | - | - | 0% | 42.3 |


## Day 3 failure analysis (2026-10-11)

The Day 3 baseline evaluation was run with the fake LLM generator (deliberately non-realistic answers) against 15 verified citizenship questions from the MOHA Kathmandu PDF and 10 draft driving-license questions. The 15 verified questions all passed retrieval (hit@5=100%), but the fake LLM produced wrong/incomplete answers for all of them.

### Top 10 failures (all 15 verified questions failed identically)

| Rank | Question | Category | Root cause | Notes |
|------|----------|----------|------------|-------|
| 1 | q001: Father/mother citizenship certificate required | generation_error: wrong/incomplete answer | Fake LLM returns raw OCR fragment "0 Fea १." instead of synthesized answer | Cited correct page (1), grounded=true |
| 2 | q002: Ward office recommendation per Schedule 1 | generation_error: wrong/incomplete answer | Fake LLM returns same raw fragment "0 Fea १." | Cited correct page (1) |
| 3 | q003: Three-generation relative's citizenship | generation_error: wrong/incomplete answer | Fake LLM returns same raw fragment "0 Fea १." | Cited correct page (1) |
| 4 | q004: Birth registration certificate required | generation_error: wrong/incomplete answer | Fake LLM cites page 3 (wrong page) with institutional renewal text | must_cite=page 1, cited=page 3 → citation_acc miss |
| 5 | q005: Mother's name basis when father unknown | generation_error: wrong/incomplete answer | Fake LLM cites page 3 (wrong page) with institutional renewal text | must_cite=page 2, cited=page 3 → citation_acc miss |
| 6 | q006: Mother's death certificate + doctor rec | generation_error: wrong/incomplete answer | Fake LLM cites page 3 (wrong page) with institutional renewal text | must_cite=page 2, cited=page 3 → citation_acc miss |
| 7 | q014: English - citizenship by descent docs | generation_error: wrong/incomplete answer | Fake LLM cites page 3 (wrong page) with institutional renewal text | must_cite=page 1, cited=page 3 → citation_acc miss |
| 8 | q015: English - foreign woman married to Nepali | generation_error: wrong/incomplete answer | Fake LLM cites page 5 (wrong page) with NRN text | must_cite=page 3, cited=page 5 → citation_acc miss |
| 9 | q007: Guardian citizenship (orphan, police report) | generation_error: wrong/incomplete answer | Fake LLM returns long raw OCR text from page 2 but incomplete | Cited correct page (2), grounded=true |
| 10 | q008: Mother Nepali, father foreign — naturalized | generation_error: wrong/incomplete answer | Fake LLM returns institutional renewal fragment from page 3 | must_cite=page 3, cited=page 3 → citation_acc hit |

### Summary of failure patterns

1. **Generation quality (15/15)**: The fake LLM generator returns raw OCR fragments instead of synthesized answers. This is by design — the fake generator is a plumbing check, not a quality model. Real LLM evaluation requires API keys and provider configuration (OpenRouter with nemotron-3-super-120b-a12b:free or similar).

2. **Citation page accuracy (67%)**: 5 of 15 questions cited the wrong page (q004, q005, q006, q014, q015). The fake LLM tends to cite the highest-scoring retrieved page rather than the must_cite page. This reveals the citation guard needs real LLM reasoning to select the correct supporting page.

3. **Retrieval excellence (100% hit@5)**: Dense search correctly finds the MOHA Kathmandu PDF for all 15 citizenship questions with scores 0.56–0.80. The retrieval pipeline is working as designed.

4. **No false refusals (0%)**: All answerable questions were answered (not refused). The guard threshold (0.35) is not blocking valid retrievals.

5. **Grounded citations (100%)**: All returned citations are verbatim quotes from the retrieved chunks — the citation guard passes.

### Next steps for Day 4+

- **Day 4**: Add BM25/hybrid search and compare against dense-only baseline
- **Day 4**: Improve prompt for same-language answers (Nepali quality issues noted: Hindi words, spelling slips)
- **Day 5**: Calibrate guard threshold with real LLM on verified questions (currently 0.35 uncalibrated)
- **Day 5**: Run sweep_threshold.py on real evaluation run to pick optimal threshold
- **Permission requests**: Send drafted permission_request.md to MOHA, DoTM, Dept. of Passports
- **Rules 2054**: Verify driving-license questions against Rules 2054 text (now readable) and mark verified

---

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


## Close-out verification (2026-10-10)

The independent close-out review found no Khula-Gyan Excel storyboard workbook; the project plan remains `docs/user-story-board.md`. No spreadsheet rows were changed. The reviewer re-ran the local suite with a workspace-local temporary directory: `pytest -q --basetemp=.pytest_tmp\verification` → **6 passed**. The primary close-out rerun used `pytest -q --basetemp=.pytest_tmp\closeout` → **6 passed in 4.28s**. The default pytest temp location produced 4 errors because it attempted to write under a sandbox-inaccessible AppData temp directory; using a repository-local temp directory passed. GNU Make is unavailable in this environment, so the Make targets themselves were not run during close-out. This result does not measure civic retrieval, answer quality, or evaluation metrics; those remain `-`.

Human actions remain: send the source permission requests, confirm presenter and backup, confirm or change the provisional USD $1.00 API cap, configure current provider rates before paid calls, and provide the correct storyboard workbook if spreadsheet updates are expected.


## Day 2 source, retrieval, and leader verification (2026-10-10)

| Owner | Task | Status | Evidence / remaining work |
|---|---|---|---|
| Member 1 — Data | Find, fetch, process, and visually inspect a usable source | Partial / blocked | No explicitly open-licensed civic procedure source was found. One MOHA Kathmandu citizenship checklist PDF was downloaded to ignored local storage for this user-requested check; no redistribution/indexing permission is on file. Rendered pages 1, 3, and 5 show legible Devanagari, but printed page numbers were not visible. Its embedded text is corrupted Latin-like output. After the processor fix, all five pages are marked unusable with blank text because Nepali/English Tesseract OCR is unavailable. |
| Member 1 — Processor safeguard | Prevent corrupted Nepali text from being treated as valid | Done | Nepali PDF pages with replacement characters or very low Devanagari proportion now trigger OCR; if OCR is unavailable or still mismatched, page text is blank and marked unusable. Synthetic regression covers the missing-OCR case. |
| Member 2 — Retrieval | Build and query an approved civic index | Blocked on source | Builder reported 0 processed pages, 0 eligible civic chunks, 0 indexed records; it skipped the unclear-license dataset and local-only source. Five sample searches (3 English, 2 Nepali) returned empty arrays. The embedding smoke check passed (10 examples, vector size 1024). Empty-index checks do not measure retrieval quality; hit@5 remains `-`. |
| Leader — End-to-end app check | Run the app and try a query | Partial | Headless Streamlit started; the browser rendered Khula Gyan. “How do I renew a driving license?” returned `not_found`: “The available official sources do not contain a matching passage.” No citations were returned. This verifies the refusal path, not a supported cited answer. |

Latest verification after the processor change: `pytest -q --basetemp=.pytest_tmp\\leader` → **7 passed in 4.54s**. No verified question or civic evaluation number was added. Day 2 remains incomplete until an approved, readable civic source can be indexed and a supported query returns a correct page-linked citation. The local source files remain gitignored and were not committed.


## Follow-up: source rights, OCR installation, and index gate (2026-10-10)

- Read-only source research found no explicitly open-licensed procedural civic source suitable for this RAG use. Madhesh Province's portal states that its datasets are under CC BY 4.0, but the catalog is statistical datasets rather than civic service instructions. Open Data Nepal's reuse policy covers datasets with attribution; no suitable procedural page with explicit applicable reuse terms was verified. No written permission from MOHA, Department of Passports, or DoTM is on file; no publisher was contacted.
- Tesseract and Nepali/English language data remain unavailable. `winget install --id UB-Mannheim.TesseractOCR -e --scope user --accept-package-agreements --accept-source-agreements` reported success but installed nothing; later `winget list` could not access the `winget.exe` shim. A first official Mannheim installer URL returned 404; a corrected official URL downloaded the installer (50,175,248 bytes), but its signature verification reported `UnknownError: A required certificate is not within its validity period when verifying against the current system clock`. The quiet install created no install folder and no Tesseract process remained. No unsigned/older installer route was attempted.
- The existing local-only MOHA PDF remains excluded from the index because the registry marks it unclear/local-only and the extracted text is unusable. Builder/index results remain 0 civic chunks; no civic search or hit@5 result is available. A source-backed citation could not be verified.
- The NVIDIA NIM key supplied by the user was written to the local ignored `.env` as `NVIDIA_API_KEY`; its value was not printed, used, or committed. No paid API call was made.
- The connected GitHub tools did not expose branch rename/delete, and the available GitHub browser session was signed out. PR #10 was already merged. To continue under the requested branch name, created `decisions-spend-cap` at the existing tip and opened PR #11 into Hkp; the old `codex/decisions-spend-cap` branch still exists. The requested-name branch is ready, but removing the old ref (a true rename) still needs a human with repository branch-management access.


## Blueprint Day 0–2 check and hkp-opencode review (2026-10-11)

Checked by Member 3 on `feature/aashish-day2-status` (based on main `85dce7f`) against the blueprint's section 13 day plan (`docx/Khula_Gyan_Project_Blueprint.docx`, added on branch `hkp-opencode`). Tests: `python -m pytest -q` → 51 passed. No evaluation metric was measured; all stay `-`.

### hkp-opencode branch (fetched 2026-10-11)

- `origin/hkp-opencode` (newest commit `fde64e9`, 2026-10-11 09:46) shares only the initial commit `fcb094b` with main: its history is separate, not built on main.
- Compared with main it lacks Member 3's files: `eval/questions.jsonl`, `eval/check_questions.py`, `eval/judge.py`, `eval/make_charts.py`, `eval/sweep_threshold.py`, `eval/update_log.py`, `scripts/smoke_test_llm.py`, `scripts/try_answer.py`, `tests/test_generation.py`, `tests/test_llm_keys.py`, `tests/test_results_log.py` and the sample fixtures.
- Its `AUDIT_VERIFICATION_TABLE.md` and `.opencode/agents/member3-generation.md` mark Member 3 **PARTIAL / FAILED** because "no 25-record file exists". **On main that file exists:** `python eval/check_questions.py` → `25 questions … answerable=20, out_of_scope=5 … en=14, mixed=2, ne=9 … verified False=25 … OK`. The 25-question claim in the README is true on main; the audit read a branch without Member 3's files.
- Recommendation for the Leader: rebuild `hkp-opencode` on top of main (or cherry-pick its new files: `.opencode/`, `AUDIT_VERIFICATION_TABLE.md`, `docx/`) rather than merging the separate history.

### Day 0–2 tasks from blueprint section 13

| Day | Owner | Blueprint task | Status (2026-10-11) | Evidence / remaining work |
|---|---|---|---|---|
| 0 | Member 1 | List target documents for 3 services with official URLs | Done | `data/sources.yaml`: 14 sources (driving license 5, citizenship 3, passport 4, reference 2) with URL, licence status, local-only flag. |
| 0–1 | Member 1 | Download into `data/raw/`; collect 10 official documents | Partial | Local only (ignored): 4 usable files (`dl_dotm_portal.html`, `dl_vehicle_transport_rules_2054.pdf`, `dl_dotm_procedure_directive_2060.pdf`, `citizenship_kathmandu_requirements.pdf`). Failed: 3 (host down, expired TLS certificate, HTTP 404). Not downloaded for rights: 5 (4 passport + Darchula). `data/raw/_manifest.json` records all. |
| 1 | Member 1 | Rate extraction good/ok/bad in `docs/extraction-report.md` | Partial | Report has browser-based ratings from 2026-10-09. Local `process_document.py` ratings: Rules 2054 good=194 ok=12 bad=0; Directive 2060 128/132 unusable (Preeti font); Kathmandu PDF 5/5 unusable (scan, no OCR); DoTM portal 1 page good (menus only). Not yet written into the report. |
| 2 | Member 1 | NFC cleanup, header/footer removal, fix broken Devanagari | Partial | NFC and repeated-header removal implemented (`src/ingest/clean.py`). Not fixed: swapped characters in Rules 2054 extraction (e.g. नवीकरण → िवीकरण) and Preeti-font text in Directive 2060. |
| 2 | Member 1 | OCR fallback (Tesseract nep+eng); save `data/processed/*.jsonl` | Blocked | OCR path exists in `src/ingest/extract.py`; Tesseract is not installed on this machine (`which tesseract` → not found). Processed JSONL exists locally for the 4 files. |
| 1 | Member 2 | `chunk.py`, `embed_store.py` | Done | `src/ingest/chunk.py`, `src/ingest/embed_store.py` on main. |
| 2 | Member 2 | Index all processed docs; `search()` works; hit@5 | Partial | `search()` returns 0–1 similarity (`src/retrieval/search.py`). Index gate needs `licence_status: confirmed open`; no civic source qualifies, so 0 chunks indexed. hit@5 `-`. |
| 0 | Member 3 | LLM API key + one test call; prompt v0 + eval format | Done | `smoke_test_llm.py` passed 2026-10-10 (OpenRouter, `nvidia/nemotron-3-super-120b-a12b:free`); `src/generation/prompt.py` (v0); format per blueprint 9.5 in `eval/questions.jsonl`. |
| 1 | Member 3 | `answer.py`; JSON output schema | Done | `src/generation/answer.py`, `schema.py`, `guard.py`; `tests/test_generation.py` passes. |
| 1 | Member 3 + Member 1 | 15 eval questions together | Not done | 25 drafts exist, 0 verified (no permitted, readable source). First answerable facts are now available locally: Rules 2054, Rule 23 (renewal application, Schedule-21 form, Schedule-18 health certificate) and Schedule 3 (renewal fees); still `answer_evidence: false` until the team approves the source. |
| 2 | Member 3 | `run_eval.py` with hit@k, citation accuracy, correctness, refusal | Done | `eval/run_eval.py` on main (plus judge, p95, spend summary). Not run on civic data: 0 verified questions. |
| 2 | Member 3 | Grow eval set to 25 (5 out-of-scope) | Partial | 25 drafted (20 answerable, 5 out-of-scope); 0 verified. |
| 0 | Leader | Repo setup; dev + main branches | Done | `dev` and `main` exist on origin. |
| 1 | Leader | `ask()` mock; Streamlit UI | Done | `src/pipeline.py`, `frontend/app.py`. |
| 2 | Leader | Connect real `search()` and `answer()`; citation cards; optional FastAPI | Partial | Connected in code; app returns `not_found` (empty index). FastAPI skipped (optional). |

**Blocking all Day 3 work:** a source the team approves as answer evidence (permission or open licence), Tesseract OCR, and verified questions. Blueprint section 12 says PRs go to `dev`.


## Day 3 baseline preparation verification (2026-10-11)

This section records the work done to prepare for Day 3 baseline: branch hygiene, local-only source approval, build_index eligibility logic, and documentation updates.

| Owner | Task | Status | Evidence / remaining work |
|---|---|---|---|
| Leader — Repository | Branch hygiene: create clean `hkp-opencode-v2` from `origin/main` with only `.opencode/`, `AUDIT_VERIFICATION_TABLE.md`, `docx/`; exclude `.handoff-worktree` and old `hkp-opencode` | Done | Commit `fbd14f5` on `hkp-opencode-v2`; 17 files, 364 insertions; branch tracks `origin/main` |
| Leader — Review | Review Aashish's `feature/aashish-day2-status`: run pytest, confirm no data/raw, data/processed, .env, chroma_db tracked; check update_log.py duplicate risk; document author rewrite | Done | pytest: 50 passed, 1 skipped; tracked files clean; `update_log.py --all` adds 8 rows (duplicate risk confirmed); `AUTHOR_ALIASES` rewrites 13 commits to `HAliveKP` hiding original authorship |
| Member 1 — Data | Rules 2054 / MOHA local-only approval: add `answer_evidence: true`, `approval_note`, `approved_on: 2026-10-11`, `approved_by: Harikrishna Pokhrel` to `citizenship_kathmandu_requirements` | Done | `data/sources.yaml` lines 90-104 updated; `licence_status: unclear`, `local_only: true` preserved |
| Member 2 — Retrieval | Fix `scripts/build_index.py` eligibility: accept `(confirmed open AND answer_evidence) OR (answer_evidence AND approval_note AND local_only)` | Done | `scripts/build_index.py` lines 41-60 updated; 4 pytest cases added in `tests/test_build_index.py` covering both paths + rejections |
| Leader — Docs | Update `docs/decisions.md`: add branch policy, local-only approval limits (no HF deploy/commit), presenter/backup and $1.00 cap as "pending human confirmation"; sync `AGENTS.md` branch rules | Done | `docs/decisions.md` §2-5 added; `AGENTS.md` branch rules updated with MOHA local-only details |
| Leader — Verification | Full pytest suite run; update README.md and docs/results.md with verified state only | Done | pytest: **54 passed, 1 skipped**; README.md test count, source table, limitations updated; docs/results.md commit log appended |

### Setup verification (2026-10-11)

| Check | Result | Evidence / limits |
|---|---|---|
| Offline pytest suite | Pass | **54 passed, 1 skipped**; includes synthetic processor metadata, Chroma score/filter behavior, draft-question skipping, Git tracking guard, API spend-cap behavior, build_index eligibility tests (both confirmed-open and local-only paths). |
| Pinned dependency consistency | Pass | `pip check`: `No broken requirements found.` |
| Embedding smoke check | Not re-run | Previous pass recorded: 10 examples (5 Nepali + 5 English), vector size 1024. |
| Synthetic evaluation harness | Pass | Offline fixture runner writes ignored run record, skips drafts. Mock percentages not civic metrics. |
| GNU Make setup target | Not run | `make` not installed in this Windows environment. |
| Source downloads / index build | Not run | No new source pages or Chroma index downloaded/built in this session. |

### Civic evaluation metrics

No new civic evaluation metrics were measured. All values remain `-`:

| Civic metric | Recorded value |
|---|---:|
| Questions in measured baseline | - |
| hit@5 | - |
| Citation accuracy | - |
| Answer correctness | - |
| Refusal rate | - |

Human decisions still needed: written permission from MOHA (request pending), confirm presenter/backup, confirm or change provisional USD $1.00 API cap, configure provider rates before paid calls.
