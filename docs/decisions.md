# Decision record

Checked 2026-10-10 against the project documents, source register, and recorded GitHub history. “Confirmed” is used only where the cited text directly supports the claim.

## 1. Source permission and open-licensed sources

**Decision:** No written permission from MOHA, the Department of Passports, or DoTM is on file in the reviewed repository. Keep their official pages local-only for a demo; keep synthetic fixtures in Git; request written permission before wider reuse. No explicitly open-licensed procedural civic source was verified. The Open Data Nepal environment-statistics dataset is explicitly share-alike licensed and may be retained as a reference source record, but it is unrelated to civic procedures and must not be answer evidence. The NCD dataset is not approved as open because its own metadata says “License Not specified.”

**Status:** NOT IN DOCS for publisher permission; PROVISIONAL for the demo source policy.

**Evidence:** `docs/data-sources.md:5`: “Government hosting does not by itself grant redistribution permission.” `data/sources.yaml:54` records the MOHA Darchula page as `licence_status: unclear`; line 57 sets `local_only: true`. Lines 95–98 record the Department of Passports process page as `all rights reserved` and `local_only: true`. Open Data Nepal's Data Policy says: “Users are free to use, modify, and share datasets, provided they give appropriate attribution.” `data/sources.yaml:174–175` records that exact quote and its [Data Policy URL](https://opendatanepal.com/privacy-policy). Lines 168 and 173 mark the environment-statistics dataset as `Creative Commons Attribution Share-Alike` and `confirmed open` [on its dataset page](https://opendatanepal.com/dataset/environment-statistics-of-nepal-2019); this is environmental data, not civic procedure. Lines 156–160 record the NCD dataset as `unclear` and local-only because its metadata says “License Not specified” [on its dataset page](https://opendatanepal.com/dataset/non-communicable-disease-risk-factors-and-prevalence-nepal-2013-to-2019).

**Who must confirm:** A human project owner must confirm which publishers have given written permission, select suitable open-licensed procedural sources if available, and send permission requests. No publisher has been contacted by this work.

## 2. Presenter

**Decision:** No presenter is assigned by name in the reviewed documents. PROVISIONAL presenter: the Leader role, because the board assigns integration, UI, repository, and deployment to that role. PROVISIONAL backup candidate: GitHub handle `aash-crest01`, whose history includes Member 3 generation/evaluation work; this is a candidate only, not a documented presentation assignment or consent.

**Status:** PROVISIONAL (named presenter and backup are NOT IN DOCS).

**Evidence:** `docs/user-story-board.md:12`: “Member 1 = Data & Documents; Member 2 = Retrieval; Member 3 = Generation & Evaluation; Leader = Integration, UI, Repository, and Deployment.” `docs/results.md:25`: “| 2026-10-09 | `d2aa3fb37b291e1ac77fc9f8e383101876fdfd68` | aash-crest01 | feat: Member 3 generation + eval starter (answer, guard, run_eval) | Day 0-1 M3: prompt v0, eval format, answer.py, guard, run_eval | pass: 12 tests passed at this commit |”.

**Who must confirm:** The team must confirm the Leader as presenter and whether `aash-crest01` accepts the backup role, or name different people.

## 3. API spending limit

**Decision:** PROVISIONAL cap: USD $1.00 per process run, configurable as `MAX_API_SPEND_USD`. Local embeddings run on the user's machine and are free, so API spend is limited to generation and evaluation. A $1.00-per-run cap is deliberately small and must be confirmed by a human before any run that could exceed it. Paid calls are blocked unless provider input and output rates are configured; estimated usage is reserved before each call.

**Status:** PROVISIONAL (the blueprint gives no numeric cap).

**Evidence:** `docx/Khula_Gyan_Project_Blueprint.docx`, §10: “Models and tools are chosen to be free or low-cost, multilingual, and replaceable.” The reviewed blueprint and `docs/results.md` do not specify a credit amount; `docs/results.md:54` says “credit ceiling remains undecided.”

**Who must confirm:** A human project owner must confirm or change the $1.00 cap and provide the selected provider’s input/output prices before any paid run.

## Needs human confirmation

- Send permission requests and record any written responses; identify approved sources.
- Confirm the presenter and backup.
- Confirm or change the USD $1.00 spend cap and configure provider rates.

