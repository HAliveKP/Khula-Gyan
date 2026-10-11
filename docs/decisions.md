# Decision record

Checked 2026-10-11 against the project documents, source register, and recorded GitHub history. "Confirmed" is used only where the cited text directly supports the claim.

## 1. Source permission and open-licensed sources

**Decision:** No written permission from MOHA, the Department of Passports, or DoTM is on file in the reviewed repository. Keep their official pages local-only for a demo; keep synthetic fixtures in Git; request written permission before wider reuse. No explicitly open-licensed procedural civic source was verified. The Open Data Nepal environment-statistics dataset is explicitly share-alike licensed and may be retained as a reference source record, but it is unrelated to civic procedures and must not be answer evidence. The NCD dataset is not approved as open because its own metadata says "License Not specified."

**Status:** NOT IN DOCS for publisher permission; PROVISIONAL for the demo source policy.

**Evidence:** `docs/data-sources.md:5`: "Government hosting does not by itself grant redistribution permission." `data/sources.yaml:54` records the MOHA Darchula page as `licence_status: unclear`; line 57 sets `local_only: true`. Lines 95-98 record the Department of Passports process page as `all rights reserved` and `local_only: true`. Open Data Nepal's Data Policy says: "Users are free to use, modify, and share datasets, provided they give appropriate attribution." `data/sources.yaml:174-175` records that exact quote and its [Data Policy URL](https://opendatanepal.com/privacy-policy). Lines 168 and 173 mark the environment-statistics dataset as `Creative Commons Attribution Share-Alike` and `confirmed open` [on its dataset page](https://opendatanepal.com/dataset/environment-statistics-of-nepal-2019); this is environmental data, not civic procedure. Lines 156-160 record the NCD dataset as `unclear` and local-only because its metadata says "License Not specified" [on its dataset page](https://opendatanepal.com/dataset/non-communicable-disease-risk-factors-and-prevalence-nepal-2013-to-2019).

**Who must confirm:** A human project owner must confirm which publishers have given written permission, select suitable open-licensed procedural sources if available, and send permission requests. No publisher has been contacted by this work.

## 2. Branch policy

**Decision:** All work must happen on `Hkp` or a feature branch created from `Hkp`. Pull requests go into `Hkp`. Never push to `main`, merge `dev` unless specifically tasked, or force-push. The `dev` branch was previously merged into `main` (PR #5) but this is now disallowed going forward. The `hkp-opencode` branch contained opencode-specific configuration and must not be merged; a clean `hkp-opencode-v2` (renamed `hkp-feat-*`) was created from `origin/main` with only `.opencode/`, `AUDIT_VERIFICATION_TABLE.md`, and `docx/`.

**Status:** CONFIRMED (matches AGENTS.md).

**Evidence:** `AGENTS.md:33-35` branch rules. `origin/Hkp` is the integration branch. `origin/dev` merged into `origin/main` via PR #5 (historical). `hkp-opencode-v2` created at commit `fbd14f5` from `origin/main` with restricted file set.

**Who must confirm:** Team must follow this policy for all future work.

## 3. Rules 2054 / MOHA local-only approval (2026-10-11)

**Decision:** The MOHA Kathmandu citizenship PDF (`citizenship_kathmandu_requirements`) is approved as LOCAL-ONLY baseline evidence for development and internal testing only. It has `licence_status: unclear`, `local_only: true`, `answer_evidence: true`, and an `approval_note` documenting the Leader's approval. This source and any index built from it MUST NOT be:
- Committed to Git (chroma_db/, data/processed/ remain gitignored)
- Deployed to Hugging Face or any public endpoint
- Used as production answer evidence
- Redistributed in any form

Written permission from MOHA is still required before any broader reuse. The approval is recorded in `data/sources.yaml` with `approved_on: 2026-10-11`, `approved_by: Harikrishna Pokhrel`.

**Status:** APPROVED for local internal baseline only.

**Evidence:** `data/sources.yaml` lines 90-104 (updated 2026-10-11). `scripts/build_index.py` eligibility logic accepts `(confirmed open AND answer_evidence) OR (answer_evidence AND approval_note AND local_only)`.

**Who must confirm:** Leader (Harikrishna Pokhrel) approved 2026-10-11. Publisher permission still pending.

## 4. Presenter

**Decision:** Presenter: **Harikrishna Pokhrel (HAliveKP)**, Leader role. Backup: **aash-crest01** (GitHub handle, Member 3 generation/evaluation work). Both confirmed by Leader on 2026-10-11.

**Status:** CONFIRMED.

**Evidence:** `docs/user-story-board.md:12`: "Leader = Integration, UI, Repository, and Deployment." `docs/results.md:25` shows aash-crest01's Member 3 commit history.

**Who must confirm:** Leader (Harikrishna Pokhrel) confirmed 2026-10-11.

## 5. API spending limit

**Decision:** Cap: **USD $1.00 per process run** (`MAX_API_SPEND_USD=1.00`). Provider: NVIDIA NIM (Nemotron 3 Super 120B) via `https://integrate.api.nvidia.com/v1` — **free tier**, so input/output costs are $0.00/1M tokens. Local embeddings (BAAI/bge-m3) run on user's machine and are free. Spend cap is configured but will not block on free tier.

**Status:** CONFIRMED (2026-10-11).

**Evidence:** `.env` configured with `LLM_INPUT_COST_PER_1M_USD=0.00`, `LLM_OUTPUT_COST_PER_1M_USD=0.00`, `MAX_API_SPEND_USD=1.00`. LLM call tested and working.

**Who must confirm:** Leader (Harikrishna Pokhrel) confirmed 2026-10-11.

## Needs human confirmation

- Send permission requests and record any written responses; identify approved sources (optional for local-only; required for public demo).
- **Presenter/backup: CONFIRMED** (Harikrishna Pokhrel presenter, aash-crest01 backup).
- **API spend cap: CONFIRMED** ($1.00, NVIDIA free tier).
- Confirm branch policy adherence (no direct pushes to main, no dev merges without tasking).