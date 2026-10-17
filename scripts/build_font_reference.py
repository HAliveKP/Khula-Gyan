"""Rebuild src/ingest/font_reference.json from local PDFs.

The reference gives glyph id -> text for a font version, read from embedded
subsets that still carry their GSUB table. extract.py uses it for subsets of
the same font that were embedded without GSUB (see reference_glyph_texts).

    python scripts/build_font_reference.py --family Kalimati data/raw/a.pdf data/raw/b.pdf

Glyphs that two subsets read differently are left out, except the ASCII
digit glyphs of Kalimati, which the font draws as Devanagari numerals.
"""

from __future__ import annotations

import argparse
import io
import json
from pathlib import Path
import sys
import unicodedata

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ingest.extract import _FONT_REFERENCE_FILE, font_glyph_texts


def build(family: str, pdfs: list[Path]) -> dict:
    import fitz
    from fontTools.ttLib import TTFont

    glyphs: dict[int, str] = {}
    conflicts: set[int] = set()
    glyph_counts: set[int] = set()
    for path in pdfs:
        with fitz.open(path) as document:
            seen: set[int] = set()
            for page in document:
                for xref, _ext, kind, _name, *_rest in page.get_fonts(full=True):
                    if xref in seen or kind != "Type0":
                        continue
                    seen.add(xref)
                    font_bytes = document.extract_font(xref)[3]
                    try:
                        font = TTFont(io.BytesIO(font_bytes), lazy=True)
                    except Exception:
                        continue
                    if font["name"].getDebugName(1) != family or "GSUB" not in font:
                        continue
                    glyph_counts.add(len(font.getGlyphOrder()))
                    readings = font_glyph_texts(font_bytes)
                    for gid, text in (readings[0] if readings else {}).items():
                        text = unicodedata.normalize("NFC", text)
                        if glyphs.setdefault(gid, text) != text:
                            conflicts.add(gid)
    if len(glyph_counts) != 1:
        raise SystemExit(f"Expected one glyph count for {family}, found {sorted(glyph_counts)}")
    if family == "Kalimati":  # ASCII digit glyphs are drawn as Devanagari numerals
        glyphs.update({gid: chr(0x966 + gid - 18) for gid in range(18, 28)})
        conflicts -= set(range(18, 28))
    for gid in conflicts:
        glyphs.pop(gid)
    return {"glyph_count": glyph_counts.pop(), "glyphs": {str(gid): glyphs[gid] for gid in sorted(glyphs)}}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--family", required=True, help="font family name, e.g. Kalimati")
    parser.add_argument("pdfs", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        references = json.loads(_FONT_REFERENCE_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        references = {}
    references[args.family] = build(args.family, args.pdfs)
    text = json.dumps(references, ensure_ascii=False, indent=1, sort_keys=True)
    # Keep the private-use reordering markers visible as escapes.
    text = text.replace("\ue000", "\\ue000").replace("\ue001", "\\ue001")
    _FONT_REFERENCE_FILE.write_text(text + "\n", encoding="utf-8")
    print(f"{args.family}: {len(references[args.family]['glyphs'])} glyphs -> {_FONT_REFERENCE_FILE}")


if __name__ == "__main__":
    main()
