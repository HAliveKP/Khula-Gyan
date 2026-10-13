# Pivot Addendum: Khula Gyan Project Blueprint

**Date:** 2026-10-13  
**From:** Central-government procedures (driving license / citizenship / passport)  
**To:** Palika Guide — municipal citizen charter Q&A

---

## What changed vs. Khula_Gyan_Project_Blueprint.docx

| Aspect | Original Blueprint | Palika Guide Pivot |
|---|---|---|
| **Topic** | Central-government procedures (driving license, citizenship, passport) | Municipal services from citizen charters (नागरिक बडापत्र) |
| **Data sources** | Central govt PDFs/pages (DoTM, MoHA, MoFA) — 0 approved, 0 chunks, 0 verified | Up to 5 municipality citizen charters (text PDF/HTML), 6-8 services each |
| **Retrieval** | Service filter only (`driving_license`, `citizenship`, `passport`) | Service filter + **municipality filter** (mandatory for `palika_guide`) |
| **Safety rule** | None specified | **Wrong-municipality guard**: if question names municipality with no indexed charter, or no municipality given → `not_found`; never answer from another municipality's chunks |
| **Team** | 4 members (Data, Retrieval, Generation, Leader) | **3 members**: Member 1 (Data & Documents), Member 2 (Retrieval & Generation), Leader (Integration, UI, Evaluation, Repo, Deployment) |
| **Timeline** | Oct 8-25 (16 days) | **8 days**: Day 1=Oct 14 ... Day 8=Oct 21 (code freeze); Oct 22-25 buffer |
| **Evaluation** | 100 questions across 3 services | Up to 40 questions across 5 municipalities × 6-8 services |
| **Services** | driving_license, citizenship, passport | `palika_guide` (municipal services: birth registration, marriage, migration, recommendation letters, business registration, etc.) |
| **Legacy sources** | All central-govt sources were primary | All central-govt sources tagged `legacy: true, answer_evidence: false` in `data/sources.yaml`; kept for history only |

---

## Schema changes (minimal, additive)

### Chunk schema (blueprint 9.1) — additive fields
```json
{
  "municipality": "string | null",   // e.g., "Lalitpur"
  "district": "string | null",       // e.g., "Lalitpur"
  "ward": "string | null",           // e.g., "5"
  "section": "string | null"         // e.g., "Birth Registration"
}
```
- Optional, only for `service: palika_guide`
- Existing chunks without these fields continue to work
- Carried through: `process_document.py` → `chunk_text()` → Chroma metadata

### Search signature — additive parameter
```python
search(query: str, k: int = 5, service: str | None = None, municipality: str | None = None) -> list[dict]
```
- Backward compatible: existing calls without `municipality` still work
- When `municipality` provided, only chunks from that municipality are returned
- Chroma `where` clause uses `$and` to combine `service` + `municipality`

### Pipeline guard — new wrong-municipality check
```python
# In src/pipeline.py ask()
if service == "palika_guide" and not municipality:
    # Try to extract from query as fallback
    extracted = _extract_municipality_from_query(query)
    if extracted:
        municipality = extracted
    else:
        return not_found("Please specify which municipality (पालिका) you are asking about.")
```
- Never answers from another municipality's chunks
- If municipality named but no indexed charter → `not_found` with message

### Checklist fields — reuse existing
- `fees` array: document fees mentioned in charter
- `steps` array: procedural steps + time estimates (e.g., "within 3 days")
- `where` string: responsible officer/office + location
- Unknown fields stay empty (`[]` or `""`) — **do not invent**

---

## Data model changes

### data/sources.yaml
- All 20 legacy entries tagged `legacy: true, answer_evidence: false`
- New municipality charter entries use:
  ```yaml
  - id: palika_<municipality_slug>
    title: "<Municipality Name> Citizen Charter (नागरिक बडापत्र)"
    publisher: "<Municipality Name> Municipality (पालिका)"
    service: palika_guide
    lang: ne  # or en, mixed
    answer_evidence: false  # true only after written permission
    legacy: false
    municipality: "<Municipality Name>"
    district: "<District Name>"
    province: "<Province Name/Number>"
    format: text_pdf  # or html, scan, image
    date_seen: 'YYYY-MM-DD'
    reuse_status: unclear / all rights reserved / quoted terms
    reuse_quote: <exact quote if any>
    local_only: true
    answer_evidence: false
  ```

### eval/questions.jsonl — new field
```json
{
  "municipality": "Lalitpur"  // required for palika_guide; null for others
}
```
- Old 25 drafts moved to `eval/legacy_questions.jsonl`
- New 30 drafts in `eval/questions.jsonl` with `municipality` field
- Checker (`eval/check_questions.py`) enforces `municipality` for `palika_guide`

---

## Evaluation changes

### run_eval.py
- New flag: `--use-municipality-filter` passes `municipality` from question to `search()`
- Mock search respects municipality filter

### check_questions.py
- Enforces `municipality` field for `palika_guide` questions
- `SERVICES` now includes `palika_guide`

---

## Pipeline safety (new)

1. **Municipality filter in search**: Only chunks from the specified municipality are retrieved.
2. **Wrong-municipality guard in pipeline**: If `service == "palika_guide"` and no municipality specified → `not_found` with clarification message.
3. **UI selector**: Municipality dropdown (required for `palika_guide` service).
4. **Never cross-contaminate**: Chunks from Municipality A are never used to answer questions about Municipality B.

---

## What stays the same

- All existing honesty rules (no invented text, citations, metrics)
- All branch/data rules (Hkp only, no raw data/.env/keys committed)
- All spend cap rules ($1.00/process, NVIDIA free tier)
- All existing tests pass (54 passed, 1 skipped)
- Existing chunking, embedding, guard, schema validation, citation guard unchanged
- Fake LLM for plumbing checks still works

---

## What was removed / not carried forward

- Member 3 role (merged into Member 2 and Leader)
- Central-government source focus (all legacy)
- 16-day timeline (now 8 days)
- 4th service, FastAPI, feedback storage, glossary, reranker (stretch only)
- `driving_license`, `citizenship`, `passport` as primary services (now legacy)
- Member 3-specific files/tasks (merged into Member 2/Leader)

---

## Human decisions still needed

1. **Permission emails** to municipalities (draft in `docs/permission_request.md`)
2. **Which municipalities** to include (from Day 1 feasibility sheet)
3. **Presenter / backup** (to be confirmed by a human)
4. **API cap** confirmed ($1.00, NVIDIA free tier)