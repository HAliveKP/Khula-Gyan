# Changelog

## 2026-10-10 — Decisions and API spend guard close-out

### Changes

- Recorded source reuse, presenter, and API spending decisions in `docs/decisions.md`. Publisher permission, presenter assignment, and the USD $1.00 per-process cap remain provisional or require human confirmation.
- Kept official MOHA and Department of Passports materials local-only in `data/sources.yaml`; the environmental dataset is licensed but excluded from civic answer evidence, and the NCD dataset remains unclear/local-only.
- Added a permission-request email draft in `docs/permission_request.md`; no publisher was contacted.
- Documented the provisional presenter and spend cap in `README.md`, and the stop-before-over-cap rule in `AGENTS.md`.
- Added preflight API cost reservation and evaluation spend reporting. The cap test blocks a provider request whose reservation would exceed the cap.

### Evidence

- `docs/results.md` records the final offline suite as 6 passed, including the provider-mock spend-cap stop check.
- `docs/results.md` records a synthetic fake-LLM evaluation harness run with estimated spend `$0.000000`. This is a plumbing check, not a civic quality result; the civic evaluation metrics remain `-` because no source-backed questions are verified.
- `data/sources.yaml` records the current license status and local-only status for each reviewed source. The NCD dataset is excluded because its metadata says “License Not specified.”
- No publisher permission email was sent, no payment was made, and no numeric evaluation metric was added.

### Human follow-up

- Send permission requests and record written responses; select a permitted procedural civic source.
- Confirm the presenter and backup candidate.
- Confirm or change the provisional USD $1.00 cap and set the selected provider's current input/output rates before any paid run.
