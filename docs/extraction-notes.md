# Extraction notes: page-level QA

Checked 2026-10-11 by rendering each page to PNG (100–120 dpi) and comparing it by eye with the extracted text. "PDF page" is the 1-based page index in the file; the JSONL `page` field uses the same number. "Before" is the original PyMuPDF text and "after" is the text after the ToUnicode repair in `src/ingest/extract.py` (see `docs/history/extraction-report.md`).

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

Update 2026-10-15: spans in Preeti, Kantipur or PCS Nepali fonts are now converted to Unicode (`preeti_to_unicode` in `src/ingest/extract.py`); Fontasy Himali spans (page numbers) get Devanagari digits. The embedded font names here are `CIDFont+F*`, so the family is read from the embedded font's name table.

| PDF page | Extraction matches image? | Example |
|---|---|---|
| 4 (contents) | Yes (all ~100 sampled words) | `५. बाझिएमा गर्ने ः ... ११`, `निर्देशक (जनशक्ति व्यवस्थापन शाखा) को जिम्मेवारी ... १३` |
| 107 | Yes | `यातायात व्यवस्थापन कार्यविधि निर्देशिका, २०७४`, `परिच्छेद – ६ अनुसूचीहरू` |

## `palika_hetauda_2083_84.pdf` (Hetauda citizen charter, 24 pages)

Checked 2026-10-15 at 144 dpi. Almost all text is Preeti; before the conversion 22 of 24 pages were marked unusable.

| PDF page | Extraction matches image? | Example |
|---|---|---|
| 3 | Yes (all ~150 sampled words) | `१) निवेदन सहित तोकिएको कागजातहरु पेश गर्ने` (source types `ug]{]{`; the doubled sign is drawn once) |
| 15 | Yes except `सस्ंथा` (image `सस्था`, a stray anusvara in the source), ~150 words | `२) सस्ंथा भाडामा बस्ने भए सम्झौता पत्र र बहाल कर` |

Mixed documents: only spans in a legacy font are converted, so `palika_pokhara_2075.pdf` keeps its Unicode text and gains the Preeti column headers of page 1; its private-use `U+F031` serial-number boxes (another font) are left as they are. In `palika_bharatpur_revenue.pdf` the author typed `IEE`/`EIA` and `आ.व.`'s dots in Preeti; the page image shows Devanagari junk (`क्ष्भ्भ्`) and dandas, and the conversion reproduces what is drawn.

## `citizenship_kathmandu_requirements.pdf`

| PDF page | Printed page number visible? | Script legible? | Extraction matches image? | Example |
|---|---|---|---|---|
| 1 | No | Yes: a slightly skewed scan with a stamp and signature | No | Image `१. वंशजको आधारमा नागरिकता प्रमाणपत्र ...`; the scanner's text layer reads `+.) qrg sTrqr ffi Trrrko rTWr:`. Needs OCR (`nep+eng`) |

## `palika_ghorahi.pdf` (Ghorahi citizen charter, 19 pages)

Checked 2026-10-15 at 144 dpi. The Kalimati subset is embedded without a GSUB table, so the font alone explains only its ~80 cmap glyphs; the "ि" width variants (gids 464–468), the reph (gid 91) and the vowel + reph glyphs (566–575) kept Word's wrong ToUnicode text. They are now read from the Kalimati 1.20 reference in `src/ingest/font_reference.json` (built with `scripts/build_font_reference.py` from Kalimati subsets that do carry GSUB), used only when family, glyph count and every Devanagari cmap glyph agree.

| PDF page | Printed page number visible? | Script legible? | Extraction matches image? | Example |
|---|---|---|---|---|
| 2 | Yes, 2 | Yes | Before: no for most words with "ि" or reph. After: yes (all ~80 sampled words) | Image `गर्ने व्यक्तिको नागरिकता प्रमाणपत्र`; before `गने व्र्णिको नागररकता प्रमाणपत्र`; after identical to the image |
| 7 | Yes, 7 | Yes | After: yes (all ~90 sampled words) | Image `सम्बन्धित व्यक्तिको निबेदन, लालपूर्जा, नागरिकता`; after identical |

Update 2026-10-15 (fee digits). Two causes, checked against rendered pages 1, 8, 15 and 16:

- Kalimati's ASCII digit glyphs (gids 18–20 in this subset) are drawn as Devanagari numerals, but without GSUB the subset's cmap only says `0`–`9`, so page 15 read `1००००` for the drawn `१००००` and page 16 `200` for `२००`. The Kalimati reference now supplies these readings too (`reference_digit_glyphs`). The same subset font in `palika_hetauda_2083_84.pdf` now gives `२०८३/८४` on page 1 (was `२०८3/८4`).
- The fee cells `४५०` (page 1) and `२५०००`, `९००`, `९००`, `७५०` (page 8) were extracted but then removed by `src/ingest/clean.py`, which dropped every number-only line as a page number (`\d` also matches Devanagari digits). A number-only line is now removed only when its value minus the page index is an offset shared by at least 60% of the pages, so Ghorahi's printed page numbers `1`–`19` are still removed and fees and table serial numbers in all charters are kept.
