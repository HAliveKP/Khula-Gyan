# Decision record

Checked 2026-10-13 against the project documents, source register, and recorded GitHub history. "Confirmed" is used only where the cited text directly supports the claim.

## 1. Pivot to Palika Guide (2026-10-13)

**Decision:** The project pivots from central-government procedures (driving license / citizenship / passport) to "Palika Guide": answering questions about municipal services from each municipality's citizen charter (नागरिक बडापत्र). The original topic had too little usable, permitted data (0 approved civic sources, 0 civic chunks, 0 verified questions). The new scope targets up to 5 municipalities with text/HTML citizen charters, 6-8 common services per municipality, and a municipality filter in retrieval.

**Status:** CONFIRMED (human decision 2026-10-13).

**Evidence:** 
- Original topic: 0 approved civic sources, 0 civic chunks, 0 verified questions after Oct 8-13 work.
- New scope: up to 5 municipalities, 6-8 services each, municipality filter in retrieval, wrong-municipality guard.
- Team reduced to 3 members: Member 1 (Data & Documents), Member 2 (Retrieval & Generation), Leader (Integration, UI, Evaluation, Repo, Deployment).
- Timeline compressed to 8 days (Day 1 = Oct 14 ... Day 8 = Oct 21 code freeze).

**Who must confirm:** Human project owner confirmed pivot on 2026-10-13.

## 2. Source permission and open-licensed sources

**Decision:** No written permission from any municipality is on file. Keep official charters local-only for demo; keep synthetic fixtures in Git; request written permission before wider reuse. No explicitly open-licensed procedural civic source was verified. The Open Data Nepal environment-statistics dataset is explicitly share-alike licensed and may be retained as a reference source record, but it is unrelated to civic procedures and must not be answer evidence.

**Status:** NOT IN DOCS for publisher permission; PROVISIONAL for the demo source policy.

**Evidence:** `docs/data-sources.md:5`: "Government hosting does not by itself grant redistribution permission." `data/sources.yaml` legacy entries tagged `legacy: true, answer_evidence: false`. New municipality entries will have `answer_evidence: false` until written permission is recorded.

**Who must confirm:** A human project owner must confirm which municipalities have given written permission, select suitable charters if available, and send permission requests. No publisher has been contacted by this work.

## 3. Branch policy

**Decision:** All work must happen on `Hkp` or a feature branch created from `Hkp`. Pull requests go into `Hkp`. Never push to `main`, merge `dev` unless specifically tasked, or force-push. The `dev` branch was previously merged into `main` (PR #5) but this is now disallowed going forward. The `hkp-opencode` branch contained opencode-specific configuration and must not be merged; a clean `hkp-opencode-v2` (renamed `hkp-feat-*`) was created from `origin/main` with only `.opencode/`, `AUDIT_VERIFICATION_TABLE.md`, and `docx/`.

**Status:** CONFIRMED (matches AGENTS.md).

**Evidence:** `AGENTS.md:33-35` branch rules. `origin/Hkp` is the integration branch. `origin/dev` merged into `origin/main` via PR #5 (historical). `hkp-opencode-v2` created at commit `fbd14f5` from `origin/main` with restricted file set.

**Who must confirm:** Team must follow this policy for all future work.

## 4. Rules 2054 / MOHA local-only approval (2026-10-11)

**Decision:** The MOHA Kathmandu citizenship PDF (`citizenship_kathmandu_requirements`) is approved as LOCAL-ONLY baseline evidence for development and internal testing only. It has `licence_status: unclear`, `local_only: true`, `answer_evidence: true`, and an `approval_note` documenting the Leader's approval. This source and any index built from it MUST NOT be:
- Committed to Git (chroma_db/, data/processed/ remain gitignored)
- Deployed to Hugging Face or any public endpoint
- Used as production answer evidence
- Redistributed in any form

Written permission from MOHA is still required before any broader reuse. The approval is recorded in `data/sources.yaml` with `approved_on: 2026-10-11`, `approved_by: Harikrishna Pokhrel`.

**Status:** APPROVED for local internal baseline only.

**Evidence:** `data/sources.yaml` lines 90-104 (updated 2026-10-11). `scripts/build_index.py` eligibility logic accepts `(confirmed open AND answer_evidence) OR (answer_evidence AND approval_note AND local_only)`.

**Who must confirm:** Leader (Harikrishna Pokhrel) approved 2026-10-11. Publisher permission still pending.

## 5. Presenter

**Decision:** Presenter: **to be confirmed by a human**. Backup: **to be confirmed by a human**. The old provisional assignment (Harikrishna Pokhrel / aash-crest01) is superseded by the pivot; new human confirmation required.

**Status:** TO BE CONFIRMED.

**Who must confirm:** Human project owner must confirm presenter and backup.

## 6. API spending limit

**Decision:** Cap: **USD $1.00 per process run** (`MAX_API_SPEND_USD=1.00`). Provider: NVIDIA NIM (Nemotron 3 Super 120B) via `https://integrate.api.nvidia.com/v1` — **free tier**, so input/output costs are $0.00/1M tokens. Local embeddings (BAAI/bge-m3) run on user's machine and are free. Spend cap is configured but will not block on free tier.

**Status:** CONFIRMED (2026-10-11).

**Evidence:** `.env` configured with `LLM_INPUT_COST_PER_1M_USD=0.00`, `LLM_OUTPUT_COST_PER_1M_USD=0.00`, `MAX_API_SPEND_USD=1.00`. LLM call tested and working.

**Who must confirm:** Leader (Harikrishna Pokhrel) confirmed 2026-10-11.

*Update 2026-10-25:* "LLM call tested and working" held for short prompts only; prompts with passages came back empty. Root cause and fix are in §8. The provider configuration in use differs between machines (§8).

## 7. Pivot to Palika Guide (2026-10-13) — additional detail

**Decision:** The project pivots to Palika Guide (municipal citizen charters). All legacy central-government sources in `data/sources.yaml` are tagged `legacy: true, answer_evidence: false`. New municipality charter entries will be added with `service: palika_guide` and `answer_evidence: false` until written permission is recorded. The chunk schema gains optional `municipality`, `district`, `ward`, `section` fields. Retrieval gains a `municipality` filter. Pipeline adds a wrong-municipality guard. Team is now 3 members (Member 1, Member 2, Leader). Timeline: 8 days (Oct 14-21), code freeze Day 8.

**Status:** CONFIRMED.

**Evidence:** This decision record; updated `docs/history/user-story-board.md` with 8-day board; `data/sources.yaml` legacy entries tagged; new municipality charter register template added.

**Who must confirm:** Human project owner confirmed 2026-10-13.

## 8. Municipalities chosen and LLM provider facts (2026-10-25)

### 8.1 Five municipalities

**Decision:** Palika Guide covers Pokhara (Kaski, Gandaki), Bharatpur (Chitwan, Bagmati), Dhulikhel (Kavrepalanchok, Bagmati), Ghorahi (Dang, Lumbini) and Hetauda (Makwanpur, Bagmati): 12 charter files in all.

**Status:** CHOSEN by Aashish (`aash-crest01`) on 2026-10-15; merged by the Leader in PR #20 (`f879fa5`, 2026-10-17). The Leader has not confirmed the set in writing; merging the PR is not counted as an explicit confirmation.

**Evidence:**
- 20 municipality websites checked on 2026-10-15 (charter present, format, date, reuse text). The sheet is a local draft (`.local-backups/drafts/feasibility_sheet.md` on aash-crest01's machine, git-excluded, marked "needs human check"). No site grants reuse. For the 5 chosen, the charter pages show only a "© 2026 <municipality>" footer (quoted in each entry's `reuse_quote`).
- `94341a8` registers the 12 files in `data/sources.yaml`: all `reuse_status: unclear`, `local_only: true`, `answer_evidence: false`, `approval_note: null`.

**Who must confirm:** Leader (Harikrishna Pokhrel).

### 8.2 LLM provider and empty replies

**Facts:**
- §6 names NVIDIA NIM (`https://integrate.api.nvidia.com/v1`). Aashish's working setup is OpenRouter (`https://openrouter.ai/api/v1`) with `nvidia/nemotron-3-super-120b-a12b:free`. `docs/history/submission_text.md` records the Leader's `.env` as `LLM_PROVIDER=openrouter` with `LLM_BASE_URL=https://integrate.api.nvidia.com/v1`, so provider name and base URL disagree there.
- **Empty replies, root cause (found 2026-10-15):** Nemotron is a reasoning model. Its hidden reasoning used the whole `MAX_API_OUTPUT_TOKENS=1024`, so `content` came back empty with `finish_reason=length`. With reasoning turned off, the same Nepali prompt returned valid JSON in 284 tokens (Aashish's local notes, 2026-10-15).
- **Fix (merged via PR #20):** `LLM_REASONING=off` sends OpenRouter's `reasoning: {enabled: false}` (`952f058`); empty replies are never cached (`4567b75`). Documented in `.env.example`.

**Status:** Fix CONFIRMED with the OpenRouter base URL only. With the NVIDIA NIM base URL the switch is untested; NIM may need a different parameter.

**Who must confirm:** Leader: use the OpenRouter base URL with `LLM_REASONING=off`, or test NIM directly; then correct §6.

## Needs human confirmation

- Send permission requests to municipalities and record any written responses; identify approved sources.
- **Presenter/backup: TO BE CONFIRMED BY A HUMAN** (pivot supersedes old assignment).
- **API spend cap: CONFIRMED** ($1.00, NVIDIA free tier).
- Confirm branch policy adherence (no direct pushes to main, no dev merges without tasking).
- Select up to 5 municipalities from Day 1 feasibility sheet for the demo. *Update 2026-10-25:* 5 chosen (§8.1); Leader to confirm explicitly.
- *Added 2026-10-25:* LLM base URL for the Leader's machine (§8.2).
- *Added 2026-10-25:* Local-only approval for the 12 charters (`approval_note`, `approved_on`, `approved_by` in `data/sources.yaml`, as in §4) if the team wants a local charter index before any municipality replies.