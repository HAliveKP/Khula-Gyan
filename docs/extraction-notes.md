# Extraction notes: page-level QA

Checked 2026-10-11 by rendering each page to PNG (100–120 dpi) and comparing it by eye with the extracted text. "PDF page" is the 1-based page index in the file; the JSONL `page` field uses the same number. "Before" is the original PyMuPDF text and "after" is the text after the ToUnicode repair in `src/ingest/extract.py` (see `docs/extraction-report.md`).

## `dl_vehicle_transport_rules_2054.pdf`

| PDF page | Printed page number visible? | Script legible? | Extraction matches image? | Example |
|---|---|---|---|---|
| 1 | Yes, १ (the text layer also has "1" in the header area) | Yes, clear Unicode Devanagari with a light watermark | Before: partly. After: yes, except two split words | Before `संशोधन` came out as `संिोधि`. After: matches, except `संक्षिप् त` and `प्रसङ् गले`, where the PDF contains a space |
| 17 (Rule 23, renewal) | Yes, १७ | Yes | Before: no for most words. After: yes, except three split words | Image `अनुमतिपत्रको नवीकरणको लागि अनुसूची-३`; before `अिुमनतपत्रको िवीकरणको लानग अिुसूची-३`; after identical to the image. Remaining split words: `राख् नु`, `प्राप् त`, `सञ् चालन` |
| 43 (Schedule 3, fee table) | Yes, ४३ | Yes | Before: partly. After: yes | Image `सार्वजनिक ८००/-`; before `सावथजनिक 8००/-`; after identical to the image. Table cells come out one per line |
| 44 (Schedule 3, continued) | Yes, ४४ | Yes | Before: partly. After: yes | Image `दर्ता प्रमाण पत्र नवीकरण दस्तुर`; before `दताथ प्रमाण पत्र िवीकरण दस्तुर`; after identical |
| 93 (Schedule 19, register form) | Yes, ९३ | Yes | Before: partly. After: yes, except three split words | Image `यातायात व्यवस्था कार्यालय`; before `कायाथलय`; after identical. Split: `अञ् चल`, `समाप् त` |
| 151 (form) | Yes, १५१ | Yes | Before: no (26% of words matched). After: yes | Image `नवीकरण, नामसारी, खारेज, पुनः दर्ता`; after identical |
| 186 (traffic signs) | Yes, १८६ | Yes; the sign pictures have no text | Before: partly. After: yes, except one split word | Image `गोलाकार भई सेतो रङ्गको भुँई`; after identical. Split: `अङ् ग्रेजी` |

Extra check: the ASCII digit glyphs of the embedded Kalimati font, rendered on their own, are drawn as Devanagari numerals `०१२३४५६७८९`. This is why `8००/-` is read as `८००/-` after the fix.

## `dl_dotm_procedure_directive_2060.pdf`

| PDF page | Printed page number visible? | Script legible? | Extraction matches image? | Example |
|---|---|---|---|---|
| 107 | Yes, १०७ | Yes in the image (Preeti-font Devanagari) | No | Image `परिच्छेद - ६ अनुसूचीहरू`; extracted `kl/R5]b – ^ cg';"rLx¿`. The page header reads `यातायात व्यवस्थापन कार्यविधि निर्देशिका, २०७४` (Preeti `@)&$` = २०७४) |

## `citizenship_kathmandu_requirements.pdf`

| PDF page | Printed page number visible? | Script legible? | Extraction matches image? | Example |
|---|---|---|---|---|
| 1 | No | Yes: a slightly skewed scan with a stamp and signature | No | Image `१. वंशजको आधारमा नागरिकता प्रमाणपत्र ...`; the scanner's text layer reads `+.) qrg sTrqr ffi Trrrko rTWr:`. Needs OCR (`nep+eng`) |
