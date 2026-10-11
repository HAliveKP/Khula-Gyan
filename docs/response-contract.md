# Response contract

Every `ask()` response follows `ask-response.schema.json`. Keep this contract stable while the team builds the first end-to-end version.

- `status` is `answered` only when retrieved evidence supports the answer. Otherwise use `not_found`.
- `language` describes the answer language: `ne`, `en`, or `mixed`.
- `checklist` always has documents, fees, steps, and where fields. Use empty arrays or an empty string when the sources do not say.
- Every citation names a source, a one-based page number, and a short supporting quote.
- `confidence` communicates evidence strength; it does not replace citations.
- `disclaimer` reminds people to verify current requirements with the relevant official office.

For `not_found`, keep citations empty unless a source quote directly explains why the requested information is unavailable. Do not fill unknown checklist items from model memory.
