"""Extract page text from official HTML or PDF files without losing page IDs."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import unicodedata
from typing import Any


class _VisibleTextParser(HTMLParser):
    """Small standard-library HTML reader that skips script/style contents and site chrome
    (navigation menus, header, footer, sidebars), so a charter page keeps only its content."""

    _BLOCK_TAGS = {"address", "article", "br", "div", "h1", "h2", "h3", "li", "p", "section", "table", "tr"}
    _IGNORED_TAGS = {"script", "style", "noscript", "svg", "nav", "header", "footer", "aside", "form"}
    # Class names of the news ticker, sidebars and tabs in the Drupal template most
    # municipal (palika) websites share.
    _IGNORED_CLASSES = {"header-notice", "region-newsticker", "sidebar", "tabs", "breadcrumb"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip_tag: str | None = None  # tag of the element being skipped
        self._skip_depth = 0  # nesting of that same tag inside it

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self._skip_tag is not None:
            if tag == self._skip_tag:
                self._skip_depth += 1
            return
        classes = set((dict(attrs).get("class") or "").split())
        if tag in self._IGNORED_TAGS or classes & self._IGNORED_CLASSES:
            self._skip_tag, self._skip_depth = tag, 1
        elif tag in self._BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if self._skip_tag is not None:
            if tag == self._skip_tag:
                self._skip_depth -= 1
                if self._skip_depth == 0:
                    self._skip_tag = None
            return
        if tag in self._BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_tag is None:
            self.parts.append(data)


def _extract_html(path: Path) -> list[dict[str, Any]]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    # Keep only the page's main content when it is marked up; menus built from plain
    # <div>s (as on municipal sites) are outside it.
    lowered = raw.lower()
    start, end = lowered.find("<main"), lowered.rfind("</main>")
    if start != -1 and end > start:
        raw = raw[start:end + len("</main>")]
    parser = _VisibleTextParser()
    parser.feed(raw)
    parser.close()
    return [{"page": 1, "text": "".join(parser.parts)}]


def _ocr_page(page: Any, *, languages: str) -> str:
    try:
        import fitz
        import pytesseract
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError(
            "Scanned PDF pages need PyMuPDF, pytesseract, and Pillow. Install the project requirements first."
        ) from exc

    pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
    try:
        return pytesseract.image_to_string(image, lang=languages)
    except Exception as exc:
        raise RuntimeError(
            f"OCR failed. Install Tesseract and its {languages!r} language data, then retry."
        ) from exc


def _has_expected_script(text: str, expected_language: str | None) -> bool:
    """Detect high-confidence mismatches between declared language and text."""
    if "\ufffd" in text:
        return False
    if expected_language != "ne":
        return True
    letters = [char for char in text if unicodedata.category(char).startswith("L")]
    if len(letters) < 40:
        return True
    devanagari_letters = sum("\u0900" <= char <= "\u097f" for char in letters)
    return devanagari_letters / len(letters) >= 0.05


# ---------------------------------------------------------------------------
# Repair for Word-made PDFs whose Devanagari ToUnicode map is wrong.
#
# Some PDFs exported by Microsoft Word (for example the Nepal Law Commission
# copy of the Vehicle and Transport Management Rules 2054, font Kalimati)
# store glyphs in *visual* order and ship a ToUnicode map that gives many
# glyphs the wrong letter: the glyph for "न" maps to "ि", the "ि" sign maps
# to "न"/"द"/"ह"/"श", the reph maps to "थ", and so on. The embedded font
# itself is correct, so we rebuild the glyph -> text map from the font's own
# cmap and GSUB (ligature/substitution) tables, then put the two signs that
# are drawn out of logical order back where Unicode expects them:
#   * "ि" is drawn before its consonant cluster -> moved after it;
#   * reph ("र्" drawn above) is drawn after its syllable -> moved before it.
# The repair runs only for fonts whose ToUnicode map disagrees with the
# font's own cmap, and only in memory: the source file is never changed.
# ---------------------------------------------------------------------------

_REPH_MARK = ""  # private-use marker: reph seen after its syllable
_I_SIGN_MARK = ""  # private-use marker: "ि" seen before its cluster
_CONSONANT = "[क-हक़-य़]़?"  # consonant + optional nukta
_CLUSTER = f"(?:{_CONSONANT}्)*{_CONSONANT}"  # e.g. क, स्थ, न्त्र
_I_SIGN_PATTERN = re.compile(f"{_I_SIGN_MARK}({_CLUSTER})")
_REPH_PATTERN = re.compile(f"({_CLUSTER}[ा-ौॢॣँं]*){_REPH_MARK}")


def restore_logical_order(text: str) -> str:
    """Turn marked visual-order Devanagari back into Unicode logical order.

    Only text carrying the private markers from the font repair is changed.
    A marker that cannot be placed safely becomes its plain character.
    """
    text = _I_SIGN_PATTERN.sub(lambda match: match.group(1) + "ि", text)
    text = _REPH_PATTERN.sub(lambda match: "र्" + match.group(1), text)
    return text.replace(_I_SIGN_MARK, "ि").replace(_REPH_MARK, "र्")


def _join_components(parts: list[str]) -> str:
    """Join ligature parts; a half form plus below-base "्र" becomes "C्र्"."""
    text = ""
    for part in parts:
        if text.endswith("्") and part.startswith("्"):
            text = text[:-1] + part + "्"
        else:
            text += part
    return text


def font_glyph_texts(font_bytes: bytes) -> tuple[dict[int, str], dict[int, str]] | None:
    """Derive glyph id -> text from an embedded TrueType font's own tables.

    Returns ``(derived, direct)``: ``derived`` covers every glyph reachable
    from the cmap through GSUB lookups; ``direct`` holds only glyphs listed in
    the cmap (their identity is certain). Glyphs with two different possible
    readings are left out. Returns None when the font cannot be read.
    """
    try:
        import io
        from fontTools.ttLib import TTFont
    except ImportError:
        return None
    try:
        font = TTFont(io.BytesIO(font_bytes), lazy=True)
        order = font.getGlyphOrder()
        cmap = font.getBestCmap() or {}
    except Exception:
        return None
    names: dict[str, str] = {}
    for code_point, glyph in sorted(cmap.items()):
        names.setdefault(glyph, chr(code_point))
    direct = {order.index(glyph): text for glyph, text in names.items()}
    for glyph, text in names.items():
        if text == "ि":
            names[glyph] = _I_SIGN_MARK

    # Collect simple rules: (input glyphs, output glyph, feature tag).
    rules: list[tuple[list[str], str, str]] = []
    if "GSUB" in font:
        table = font["GSUB"].table
        tags: dict[int, str] = {}
        for record in table.FeatureList.FeatureRecord:
            for index in record.Feature.LookupListIndex:
                tags.setdefault(index, record.FeatureTag)
        for index, lookup in enumerate(table.LookupList.Lookup):
            for subtable in lookup.SubTable:
                kind = lookup.LookupType
                if kind == 7:  # extension wrapper
                    subtable, kind = subtable.ExtSubTable, subtable.ExtSubTable.LookupType
                if kind == 1:
                    rules += [([source], target, tags.get(index, "")) for source, target in subtable.mapping.items()]
                elif kind == 4:
                    for first, ligatures in subtable.ligatures.items():
                        rules += [([first, *lig.Component], lig.LigGlyph, tags.get(index, "")) for lig in ligatures]
    # The reph and below-base ra forms are written in visual position.
    for inputs, output, tag in rules:
        # Some Nepali fonts (e.g. Kalimati) draw the ASCII digit glyphs as
        # Devanagari numerals and list them as substitutes for "०".."९".
        # Read such a glyph as the Devanagari digit it is drawn as.
        source_text = names.get(inputs[0], "")
        if len(inputs) == 1 and len(source_text) == 1 and "०" <= source_text <= "९":
            if names.get(output) == str(ord(source_text) - 0x966):
                names[output] = source_text
        if [names.get(glyph) for glyph in inputs] == ["र", "्"]:
            if tag == "rphf":
                names[output] = _REPH_MARK
            elif tag == "blwf":
                names[output] = "्र"

    # Follow the rules until no new glyph gets a reading.
    changed = True
    while changed:
        changed = False
        for inputs, output, _tag in rules:
            if output not in names and all(glyph in names for glyph in inputs):
                names[output] = _join_components([names[glyph] for glyph in inputs])
                changed = True
    # Drop glyphs that two rules would read differently.
    for inputs, output, _tag in rules:
        if names.get(output) in {_REPH_MARK, "्र"}:
            continue  # set on purpose above
        if output in names and all(glyph in names for glyph in inputs) and len(inputs) > 1:
            if _join_components([names[glyph] for glyph in inputs]) != names[output]:
                names.pop(output)
    derived = {order.index(glyph): text for glyph, text in names.items() if glyph in order}
    return derived, direct


def _parse_tounicode(cmap_text: str) -> dict[int, str]:
    """Read bfchar/bfrange entries of a ToUnicode CMap into code -> text."""

    def decode(hex_text: str) -> str:
        return bytes.fromhex(hex_text).decode("utf-16-be", errors="replace")

    mapping: dict[int, str] = {}
    for block in re.findall(r"beginbfchar(.*?)endbfchar", cmap_text, re.S):
        for source, target in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]*)>", block):
            mapping[int(source, 16)] = decode(target)
    for block in re.findall(r"beginbfrange(.*?)endbfrange", cmap_text, re.S):
        for start, end, target in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*(<[0-9A-Fa-f]*>|\[[^\]]*\])", block):
            first, last = int(start, 16), int(end, 16)
            if target.startswith("["):
                for offset, item in enumerate(re.findall(r"<([0-9A-Fa-f]*)>", target)):
                    mapping[first + offset] = decode(item)
            else:
                base = decode(target[1:-1])
                for offset in range(last - first + 1):
                    mapping[first + offset] = base[:-1] + chr(ord(base[-1]) + offset)
    return mapping


def _write_tounicode(mapping: dict[int, str]) -> bytes:
    """Write a ToUnicode CMap (bfchar entries, 100 per block)."""
    lines = [
        "/CIDInit /ProcSet findresource begin", "12 dict begin", "begincmap",
        "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def",
        "/CMapName /Adobe-Identity-UCS def", "/CMapType 2 def",
        "1 begincodespacerange", "<0000> <FFFF>", "endcodespacerange",
    ]
    items = sorted(mapping.items())
    for start in range(0, len(items), 100):
        chunk = items[start:start + 100]
        lines.append(f"{len(chunk)} beginbfchar")
        lines += [f"<{code:04X}> <{text.encode('utf-16-be').hex().upper()}>" for code, text in chunk]
        lines.append("endbfchar")
    lines += ["endcmap", "CMapName currentdict /CMap defineresource pop", "end", "end"]
    return "\n".join(lines).encode("ascii")


# Some subsets (e.g. the Kalimati in the Ghorahi charter) are embedded
# without a GSUB table, so only the ~80 glyphs in the subset's cmap can be
# read from the font; the many other glyphs Word picked (the "ि" width
# variants, reph, reph + vowel sign, conjuncts) keep their wrong ToUnicode
# text. Their glyph ids are the same in every copy of the same font version,
# so a reference reading built from subsets that do carry GSUB fills the gap
# (see scripts/build_font_reference.py). It is used only when the subset is
# the same font: family name and glyph count match, and every Devanagari
# glyph in the subset's own cmap agrees with the reference.
_FONT_REFERENCE_FILE = Path(__file__).with_name("font_reference.json")
_MIN_REFERENCE_CHECKS = 20


def _font_references() -> dict[str, Any]:
    import json

    try:
        return json.loads(_FONT_REFERENCE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def reference_glyph_texts(font_bytes: bytes, direct: dict[int, str]) -> dict[int, str]:
    """Return reference glyph readings for a known font, or {} if unsure.

    ``direct`` is the subset's own cmap reading (from ``font_glyph_texts``).
    """
    try:
        import io
        from fontTools.ttLib import TTFont

        font = TTFont(io.BytesIO(font_bytes), lazy=True)
        family = font["name"].getDebugName(1) or ""
        glyph_count = len(font.getGlyphOrder())
    except Exception:
        return {}
    entry = _font_references().get(family)
    if not entry or entry.get("glyph_count") != glyph_count:
        return {}
    reference = {int(gid): text for gid, text in entry["glyphs"].items()}
    checks = [gid for gid, text in direct.items() if any("ऀ" <= char <= "ॿ" for char in text)]
    if len(checks) < _MIN_REFERENCE_CHECKS:
        return {}

    def plain(text: str) -> str:
        text = text.replace(_I_SIGN_MARK, "ि").replace(_REPH_MARK, "र्")
        return unicodedata.normalize("NFC", text)

    if any(plain(reference.get(gid, "")) != plain(direct[gid]) for gid in checks):
        return {}
    return reference


def repair_devanagari_tounicode(document: Any) -> list[str]:
    """Fix wrong ToUnicode maps in an open PyMuPDF document, in memory only.

    A Type0/Identity-H font is repaired only when at least one glyph listed in
    its own cmap is mapped to a different letter by the PDF's ToUnicode map.
    Glyphs the font itself cannot explain are read from a matching reference
    font (``reference_glyph_texts``) when one is known.
    Returns the names of the repaired fonts.
    """
    repaired: list[str] = []
    checked: set[int] = set()
    for page in document:
        for xref, _ext, kind, name, _ref, encoding, *_rest in page.get_fonts(full=True):
            if xref in checked or kind != "Type0" or encoding != "Identity-H":
                continue
            checked.add(xref)
            tounicode = document.xref_get_key(xref, "ToUnicode")
            descendants = document.xref_get_key(xref, "DescendantFonts")
            if tounicode[0] != "xref" or descendants[0] not in {"array", "xref"}:
                continue
            if descendants[0] == "xref":  # the array itself is a separate object
                descendants = ("array", document.xref_object(int(descendants[1].split()[0])))
            references = re.findall(r"(\d+) 0 R", descendants[1])
            if not references or document.xref_get_key(int(references[0]), "CIDToGIDMap") != ("name", "/Identity"):
                continue  # glyph ids equal character codes only with an identity map
            font_bytes = document.extract_font(xref)[3]
            readings = font_glyph_texts(font_bytes)
            if not readings:
                continue
            derived, direct = readings
            stream_xref = int(tounicode[1].split()[0])
            current = _parse_tounicode(document.xref_stream(stream_xref).decode("latin-1"))
            wrong = [gid for gid, text in direct.items() if gid in current and current[gid] != text]
            if not wrong:
                continue
            reference = reference_glyph_texts(font_bytes, direct)
            filled = {gid: reference[gid] for gid in current if gid not in derived and gid in reference}
            document.update_stream(stream_xref, _write_tounicode({**current, **filled, **derived}))
            repaired.append(name)
    return repaired


# ---------------------------------------------------------------------------
# Legacy Nepali fonts (Preeti and its look-alikes Kantipur and PCS Nepali).
#
# These fonts draw Devanagari shapes on Latin code points, so the PDF text
# layer holds Latin letters ("l;kmfl/;" for "सिफारिस"). The text is typed in
# visual order: "ि" (key "l") comes before its consonant cluster and the reph
# (key "{") after its syllable. Only spans in such a font are converted.
# The mapping below was checked against rendered pages of the Hetauda
# charter and the DoTM directive (docs/extraction-notes.md).
# ---------------------------------------------------------------------------

_PREETI_FONT = re.compile(r"preeti|kantipur|pcs[\s_-]*nepali", re.I)
_HIMALI_FONT = re.compile(r"himali", re.I)  # Fontasy Himali: digits only seen

_PREETI_MAP = {
    "a": "ब", "b": "द", "c": "अ", "d": "म", "e": "भ", "f": "ा", "g": "न", "h": "ज", "i": "ष्",
    "j": "व", "k": "प", "l": _I_SIGN_MARK, "n": "ल", "o": "य", "p": "उ", "q": "त्र", "r": "च",
    "s": "क", "t": "त", "u": "ग", "v": "ख", "w": "ध", "x": "ह", "y": "थ", "z": "श",
    "A": "ब्", "B": "द्य", "C": "ऋ", "D": "म्", "E": "भ्", "F": "ँ", "G": "न्", "H": "ज्",
    "I": "क्ष्", "J": "व्", "K": "प्", "L": "ी", "M": "ः", "N": "ल्", "O": "इ", "P": "ए",
    "Q": "त्त", "R": "च्", "S": "क्", "T": "त्", "U": "ग्", "V": "ख्", "W": "ध्", "X": "ह्",
    "Y": "थ्", "Z": "श्",
    "0": "ण्", "1": "ज्ञ", "2": "द्द", "3": "घ", "4": "द्ध", "5": "छ", "6": "ट", "7": "ठ",
    "8": "ड", "9": "ढ",
    "!": "१", "@": "२", "#": "३", "$": "४", "%": "५", "^": "६", "&": "७", "*": "८", "(": "९",
    ")": "०", "-": "(", "_": ")", "+": "ं", "=": ".", "[": "ृ", "{": _REPH_MARK, "]": "े",
    "}": "ै", "\\": "्", "|": "्र", ";": "स", ":": "स्", "'": "ु", '"': "ू", ".": "।",
    ">": "श्र", "/": "र", "?": "रु", "~": "ञ्",
    "¿": "रू", "÷": "/", "ª": "ङ", "ˆ": "फ्", "«": "्र", "§": "ट्ट", "¶": "ठ्ठ", "Ë": "ङ्ग",
    "Í": "ङ्क", "å": "द्व", "Ü": "%", "Ø": "्य", "Ù": ";", "¥": "र्‍", "‰": "झ्",
    "›": "द्र", "•": "ड्ड", "Œ": "त्त्", "…": "‘", "Ú": "’", "æ": "“", "Æ": "”",
}
# "m" adds the hook that turns one base glyph into another (k+m = फ, e+m = झ,
# q+m = क्र). Vowel signs or a halant may be typed between base and hook.
_PREETI_HOOK = re.compile(r"([kedqQp])([\\'\"\]}{|]*)m")
_PREETI_HOOKED = {"k": "फ", "e": "झ", "d": "झ", "q": "क्र", "Q": "क्त", "p": "ऊ"}
_PREETI_AFTER = [
    ("्ा", ""),  # half form + "ा" is drawn as the full letter
    ("अाे", "ओ"), ("अाै", "औ"), ("अा", "आ"), ("ाे", "ो"), ("ाै", "ौ"), ("एे", "ऐ"),
    (f"इ{_REPH_MARK}", "ई"),  # "इ" with the reph-shaped hook is "ई"
]


def preeti_to_unicode(text: str) -> str:
    """Convert text typed in the Preeti keyboard layout to Unicode Devanagari."""
    text = re.sub(r"(\]\{)+", "]{", text)  # "]{" typed twice draws once
    text = _PREETI_HOOK.sub(lambda match: _PREETI_HOOKED[match.group(1)] + match.group(2), text)
    text = "".join(_PREETI_MAP.get(char, char) for char in text)
    for old, new in _PREETI_AFTER:
        text = text.replace(old, new)
    text = restore_logical_order(text)
    text = re.sub("([ँं])([ा-ौ])", r"\2\1", text)  # "ँ" typed before its vowel sign
    text = re.sub("([ा-ौ])\\1+", r"\1", text)  # a vowel sign typed twice draws once
    return unicodedata.normalize("NFC", text)


def _himali_to_unicode(text: str) -> str:
    return text.translate({ord("0") + digit: 0x966 + digit for digit in range(10)})


def legacy_font_converters(document: Any) -> dict[str, Any]:
    """Map span font names to a converter for legacy-encoded Nepali fonts.

    The span name is the PDF base font without its subset prefix; when it is
    not descriptive (e.g. "CIDFont+F2") the embedded font's family is used.
    """
    converters: dict[str, Any] = {}
    seen: set[int] = set()
    for page in document:
        for xref, _ext, _kind, name, *_rest in page.get_fonts(full=True):
            if xref in seen:
                continue
            seen.add(xref)
            names = [name, re.sub(r"^[A-Z]{6}\+", "", name)]
            try:
                import io
                from fontTools.ttLib import TTFont

                font = TTFont(io.BytesIO(document.extract_font(xref)[3]), lazy=True)
                names.append(font["name"].getDebugName(1) or "")
            except Exception:
                pass
            label = " ".join(names)
            converter = preeti_to_unicode if _PREETI_FONT.search(label) else _himali_to_unicode if _HIMALI_FONT.search(label) else None
            if converter:
                converters[names[0]] = converters[names[1]] = converter
    return converters


def _page_text(page: Any, converters: dict[str, Any]) -> str:
    """Plain page text; runs of legacy-font spans in a line are converted."""
    if not converters or not any(font[3] in converters for font in page.get_fonts(full=True)):
        return page.get_text("text")
    lines: list[str] = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            parts: list[str] = []
            run: list[str] = []
            run_converter = None
            for span in line["spans"]:
                converter = converters.get(span["font"])
                if run and converter is not run_converter:
                    parts.append(run_converter("".join(run)))
                    run = []
                if converter:
                    run.append(span["text"])
                    run_converter = converter
                else:
                    parts.append(span["text"])
            if run:
                parts.append(run_converter("".join(run)))
            lines.append("".join(parts) + "\n")
    return "".join(lines)


def _extract_pdf(
    path: Path,
    *,
    ocr: bool,
    ocr_languages: str,
    expected_language: str | None,
) -> list[dict[str, Any]]:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PDF extraction needs PyMuPDF. Install the project requirements first.") from exc

    pages: list[dict[str, Any]] = []
    with fitz.open(path) as document:
        # In-memory fix for fonts whose ToUnicode map disagrees with the font.
        repaired_fonts = repair_devanagari_tounicode(document)
        converters = legacy_font_converters(document)
        for page_number, page in enumerate(document, start=1):
            text = _page_text(page, converters)
            if repaired_fonts:
                text = restore_logical_order(text)
            used_ocr = False
            script_mismatch = not _has_expected_script(text, expected_language)
            ocr_error: str | None = None
            if ocr and (len(text.strip()) < 40 or script_mismatch):
                try:
                    text = _ocr_page(page, languages=ocr_languages)
                    used_ocr = True
                    script_mismatch = not _has_expected_script(text, expected_language)
                except RuntimeError as exc:
                    text = ""
                    script_mismatch = True
                    ocr_error = str(exc)
            page_record = {"page": page_number, "text": text, "ocr": used_ocr}
            if script_mismatch:
                page_record.update(
                    text="",
                    extraction_status="unusable",
                    extraction_note=(
                        "Expected script was not detected; OCR was unavailable or did not recover it."
                        + (f" {ocr_error}" if ocr_error else "")
                    ),
                )
            pages.append(page_record)
    return pages


def extract_pages(
    path: str | Path,
    *,
    ocr: bool = True,
    ocr_languages: str = "nep+eng",
    expected_language: str | None = None,
) -> list[dict[str, Any]]:
    """Extract one record per PDF page, or one record for an HTML page.

    OCR runs when a PDF page has fewer than 40 extracted characters or its
    text clearly misses the expected script. Likely corrupted text is marked
    unusable if OCR is disabled or cannot recover it. The original source
    should remain in ignored ``data/raw/``; this function does not download,
    modify, or redistribute source files.
    """
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"Source file does not exist: {source}")
    suffix = source.suffix.lower()
    if suffix in {".html", ".htm"}:
        return _extract_html(source)
    if suffix == ".pdf":
        return _extract_pdf(
            source,
            ocr=ocr,
            ocr_languages=ocr_languages,
            expected_language=expected_language,
        )
    raise ValueError("Supported source formats are PDF (.pdf) and HTML (.html/.htm)")
