# Day 1 source text extraction report

Checked 2026-10-09 against the official web pages and their browser-readable text/PDF indexing. This is a preliminary extraction review, not a successful run of PyMuPDF/pdfplumber on local files: the local download attempt failed because the remote host closed the transport connection, and `data/raw/` contains no source copies. Re-run the local extractor after downloading the sources from a permitted network, then replace these preliminary ratings with page-by-page results.

Rating guide: **good** = readable text and structure in the available web extraction; **ok** = usable text with a limitation that needs manual review; **bad** = extraction is unavailable or too garbled to trust. A good rating does not mean the source is current, reusable, or approved for answers.

| Source ID | Preliminary rating | What was observed | Follow-up |
|---|---|---|---|
| `dl_dotm_portal` | good | The official page text is readable; it says users should select their province portal. | Extract locally and check relevant provincial pages before answering renewal questions. |
| `dl_renewal_manual` | ok | Search indexing exposes readable instructions and page markers for a 22-page manual, but the document is several years old and local PDF extraction did not run. | Compare every procedure against the active provincial portal; extract locally page by page. |
| `dl_bheri_office_faq` | bad | The official FAQ timed out in the web reader and the local download connection closed. No reliable text was reviewed. | Retry later; do not use it until readable text and office scope are confirmed. |
| `citizenship_darchula_requirements` | good | The official page exposes a readable table of document requirements. Its requirements are specific to Darchula and applicant cases. | Extract locally and confirm with the intended district office before use. |
| `citizenship_kathmandu_requirements` | bad | The five-page PDF's available text layer contains garbled romanized output and control characters. | Try OCR with Nepali (`nep`) and English (`eng`); compare pages visually before using. |
| `citizenship_rules_2082` | good | The official Dadeldhura listing is readable and identifies the citizenship rules with the 2082 fourth amendment. The linked PDF itself was not extracted locally. | Download the linked current PDF; check Nepali text and page-level extraction. Confirm legal/current version before use. |
| `passport_process` | good | Official Department of Passports process page is readable in the browser. | Extract locally and retain page/section references; recheck current application rules. |
| `passport_required_documents` | good | Official required-documents page is readable in the browser. | Extract locally and preserve applicant-type context. |
| `passport_fees` | good | Official fee page is readable in the browser. | Extract locally; fees must be rechecked immediately before use. |
| `passport_pre_enrollment` | ok | Search indexing yields readable instructions and a concrete step, but the full PDF was not extracted locally. | Download and inspect all pages before adding to the answer library. |

## Current outcome

- Preliminary browser-level review: 6 good, 2 ok, 2 bad.
- Local source files downloaded: 0 of 10 (the connection was forcibly closed).
- Local PDF/HTML extraction pipeline runs completed: 0 of 10.
- Do not mark Member 1's collection/extraction task complete until the originals are obtained through an approved route and the extractor is run against each one. Keep copies out of Git while reuse terms are unclear.
