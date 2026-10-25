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

## Day 2 processing implementation

Added `src/ingest/extract.py`, `src/ingest/clean.py`, and `scripts/process_document.py`. The processor supports local HTML and PDF, keeps one page-linked record per PDF page, normalizes text to Unicode NFC, removes repeated page-edge headers/footers, and writes JSONL into ignored `data/processed/`. Scanned pages use Tesseract with Nepali and English when OCR is installed. A synthetic HTML smoke check passed for extraction, normalization, repeated-header cleanup, JSONL metadata, and rating output. No official source file was available to process; PDF extraction was not run in this environment because PyMuPDF is not installed here. The ten official-source ratings above remain preliminary browser review only.

## Local extraction check (2026-10-11)

Per-file results from `data/processed/*.jsonl` after this check. "Unusable" pages had their text blanked by the extractor. Ratings come from `extraction_rating()`, which looks only at readable-character ratios and cannot detect wrong letters.

| File | Pages | Pages with text | Unusable | Ratings (good / ok / bad) | Notes |
|---|---|---|---|---|---|
| `dl_vehicle_transport_rules_2054.jsonl` | 206 | 206 | 0 | 194 / 12 / 0 | Regenerated with the ToUnicode repair described below (`--no-ocr`). Seven sampled pages were checked against rendered images. |
| `dl_dotm_procedure_directive_2060.jsonl` | 132 | 4 | 128 | 2 / 2 / 128 | Legacy Preeti font. The 4 pages kept as "usable" are false positives: PDF pages 107, 117 and 121 are Preeti Latin text (for example `kl/R5]b – ^`), and page 3 uses another broken encoding (`ÓयवÖथा`). Treat the whole file as unusable. |
| `citizenship_kathmandu_requirements.jsonl` | 5 | 0 | 5 | 0 / 0 / 5 | Scanned pages. The embedded text layer is bad OCR from the scanner. Tesseract is not installed, so OCR did not run. |
| `dl_dotm_portal.jsonl` | 1 | 1 | 0 | 1 / 0 / 0 | HTML. Regenerated with `--lang ne` to match the corrected register. |

### Vehicle and Transport Management Rules 2054: diagnosis

- The PDF was made by Microsoft Word 2013. Body text uses an embedded Kalimati subset (Type0, Identity-H, CIDToGIDMap Identity); a few lines use Mangal in the same way.
- The PDF stores glyphs in **visual order**, and its ToUnicode map gives many glyphs the wrong letter. The embedded font is correct: its own `cmap` and GSUB tables disagree with the ToUnicode map. PyMuPDF (`get_text()`, `sort=True`, `rawdict`) and pdfplumber all read the same ToUnicode map, so they show the same errors. pdfplumber also splits vowel signs (for example `अिमु नतपत्रको`).
- Whole-document counts of wrong mappings for the Kalimati font (glyph uses):
  - Glyphs listed in the font's own cmap but given another letter: `न` read as `ि` (5,404), `ह` read as `ि` (1,148), `ि` read as `श` (1,046), `भ` read as `ि` (940), `ँ` read as `ाँ` (752), `श` read as `ि` (319), `घ` read as `र्` (164).
  - Alternate glyphs: `ि` variants read as `न` (2,847), `ह` (904), `द` (389) and `र` (331); reph (`र्` above the line) read as `थ` (1,324); `म्` half form read as a space (535); `ल्` read as `ल` (158); `ख्` read as `त` (110); `क्ष` read as `ि` (196).
  - Below-base `्र` ligatures (`त्र`, `प्र`, ...) were correct. Ligatures that combine a vowel sign with a reph (`ेर्`, `ीर्`, `ोर्`, `र्ं`) lost the reph.
  - Some fee digits use Kalimati's ASCII-digit glyphs, which the font draws as Devanagari numerals (checked by rendering the embedded font). Those extracted as `8००/-` while the page shows `८००/-`.
  - In total, 24,736 of 138,399 Kalimati glyph uses (17.9%) had a reading different from the one the font defines.
- Example image vs extracted text (PDF page 17, Rule 23): image `चालक अनुमतिपत्रको नवीकरणः`, extracted `चालक अिुमनतपत्रको िवीकरणः`; image `दिने कार्यालयमा`, extracted `ददिे कायाथलयमा`. Schedule 3 (PDF page 43): image `सार्वजनिक ... ८००/-`, extracted `सावथजनिक ... 8००/-`.

### Fix and before/after

- `src/ingest/extract.py` now has `repair_devanagari_tounicode()`. It runs only for a Type0/Identity-H font with an identity CID-to-glyph map whose ToUnicode map gives a different letter from the font's own cmap for at least one glyph. For this file that is Kalimati and Mangal. For such fonts it rebuilds the glyph-to-text map from the embedded font's cmap and GSUB tables, using fontTools (already installed as a matplotlib dependency). Glyphs that two GSUB rules would read differently keep their original mapping. The new map is written into the open document in memory; the source file is not changed. `restore_logical_order()` then moves `ि` after its consonant cluster and the reph before its syllable. The other two PDFs do not trigger the repair.
- Sampled pages (PDF pages 1, 17, 43, 44, 93, 151 and 186; 1,011 Devanagari words after the fix): before the fix, 589 words (58.3%) matched the page image. After the fix, all words match except 11 places where the PDF itself contains a space after a half consonant (for example `प्राप् त`, `राख् नु`, `अञ् चल`), which the image shows joined. These spaces are real characters in the PDF and were left unchanged (611 occurrences in the whole document).
- Whole document: `नवीकरण` 0 → 107 occurrences, `अनुसूची` 0 → 172, `कार्यालय` 0 → 288; words starting with a dependent vowel sign (impossible in correct text) 2,159 → 0; `िवीकरण` 107 → 0.
- Tests: `tests/test_ingest_text_fixes.py` covers the reordering, CMap parsing and writing, GSUB reading with a small generated font, and (when the local PDF exists) the Rule 23 and Schedule 3 text.
- Remaining limits: only seven pages were checked by eye. Tables are extracted cell by cell. The Rules remain `answer_evidence: false` until the licence status is cleared.
