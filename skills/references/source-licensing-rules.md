# Source licensing rules (Khula Gyan)

Reference for `skills/source-rights-check.md`. Use when reading `data/sources.yaml` or deciding whether a source may be fetched, indexed, or used as civic evidence.

## Eligibility matrix

| Condition | Action |
|---|---|
| `legacy: true` | Skip; never index; never redistribute. |
| `licence_status: "confirmed open"` + quoted `terms_quote` | May fetch; may index if `service` in allowed set. |
| `licence_status: "unclear"` or `null` | Never infer reuse from `.gov.np`; keep local-only; do not index. |
| `licence_status: "all rights reserved"` + quoted `terms_quote` | Never index; never redistribute; keep local only for tracking. |
| `service: palika_guide` + `local_only: true` + `answer_evidence: false` | Not civic evidence; may process locally for extraction QA only. |
| `service: palika_guide` + `local_only: true` + `answer_evidence: true` + `approval_note` present + `approved_on` + `approved_by` | Only approved local path (e.g., `citizenship_kathmandu_requirements` approved 2026-10-11 by Harikrishna Pokhrel). Index stays in `chroma_db/` (ignored); no HF deploy; no commit of raw/index data. |
| Any source without `approval_note` / `approved_on` / `approved_by` when `answer_evidence: true` | NOT approved. Do not index. Record in `docs/permission_request.md` draft only. |

## Quoted terms (must be exact text from `data/sources.yaml`)

- `opendatanepal_environment_statistics_2019`: `"Users are free to use, modify, and share datasets, provided they give appropriate attribution. https://opendatanepal.com/privacy-policy"` (`licence_status: confirmed open`).
- `passport_process`: `"Copyright© 2026. All rights reserved."` (`all rights reserved`).
- `palika_pokhara_rates_2074_75`: `"© 2026  पोखरा महानगरपालिका (footer of https://pokharamun.gov.np/citizen-charter; no licence or reuse terms found on the page or in the PDF)"` (`unclear`).

## Pitfall

Government hosting (`.gov.np`) does NOT grant reuse permission. Always read `licence_status`, `terms_quote`, and `reuse_status` in `data/sources.yaml`. If `terms_quote` is `null` and `reuse_status` is `unclear`, assume local-only. Never index without `approval_note` + `approved_on` + `approved_by`.
