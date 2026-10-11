"""Tests for the Devanagari ToUnicode repair in src/ingest/extract.py."""

from __future__ import annotations

import io
from pathlib import Path

import pytest

from src.ingest.extract import (
    _I_SIGN_MARK,
    _REPH_MARK,
    _join_components,
    _parse_tounicode,
    _write_tounicode,
    extract_pages,
    font_glyph_texts,
    restore_logical_order,
)

RULES_PDF = Path(__file__).resolve().parents[1] / "data" / "raw" / "dl_vehicle_transport_rules_2054.pdf"


def test_i_sign_moves_after_its_consonant_cluster() -> None:
    # Visual order "ि न" -> logical "नि"; a conjunct cluster stays together.
    assert restore_logical_order(f"{_I_SIGN_MARK}नयम") == "नियम"
    assert restore_logical_order(f"अनुम{_I_SIGN_MARK}तपत्र") == "अनुमतिपत्र"
    assert restore_logical_order(f"{_I_SIGN_MARK}स्थ") == "स्थि"


def test_reph_moves_before_its_syllable() -> None:
    # Visual "कायार्" (reph after "या") -> logical "कार्या".
    assert restore_logical_order(f"काया{_REPH_MARK}लय") == "कार्यालय"
    assert restore_logical_order(f"दता{_REPH_MARK}") == "दर्ता"
    # "ि" first, then the reph: visual "ि द र्" -> "र्दि".
    assert restore_logical_order(f"नि{_I_SIGN_MARK}द{_REPH_MARK}ष्ट") == "निर्दिष्ट"


def test_unplaceable_marks_become_plain_characters() -> None:
    assert restore_logical_order(f"{_I_SIGN_MARK} ") == "ि "
    assert restore_logical_order(f" {_REPH_MARK}") == " र्"


def test_text_without_marks_is_unchanged() -> None:
    text = "चालक अनुमतिपत्रको नवीकरण 123"
    assert restore_logical_order(text) == text


def test_half_form_plus_below_base_ra() -> None:
    assert _join_components(["क्", "्र"]) == "क्र्"
    assert _join_components(["त", "्र"]) == "त्र"


def test_tounicode_round_trip_including_ranges() -> None:
    cmap = (
        "1 beginbfchar\n<0003> <0020>\nendbfchar\n"
        "2 beginbfrange\n<0010> <0012> <0966>\n<0020> <0021> [<0928> <0930094D>]\nendbfrange\n"
    )
    parsed = _parse_tounicode(cmap)
    assert parsed == {3: " ", 0x10: "०", 0x11: "१", 0x12: "२", 0x20: "न", 0x21: "र्"}
    assert _parse_tounicode(_write_tounicode(parsed).decode("ascii")) == parsed


def _tiny_font() -> bytes:
    """Build a small TrueType font with Devanagari-style GSUB rules."""
    fontbuilder = pytest.importorskip("fontTools.fontBuilder")
    feature_lib = pytest.importorskip("fontTools.feaLib.builder")
    from fontTools.pens.ttGlyphPen import TTGlyphPen

    names = [".notdef", "ka", "ra", "halant", "iSign", "zeroDeva", "zero", "kaHalf", "reph", "iSignAlt"]
    builder = fontbuilder.FontBuilder(1000, isTTF=True)
    builder.setupGlyphOrder(names)
    builder.setupCharacterMap({0x915: "ka", 0x930: "ra", 0x94D: "halant", 0x93F: "iSign", 0x966: "zeroDeva", 0x30: "zero"})
    pen = TTGlyphPen(None)
    pen.moveTo((0, 0))
    pen.lineTo((0, 100))
    pen.lineTo((100, 0))
    pen.closePath()
    builder.setupGlyf({name: pen.glyph() for name in names})
    builder.setupHorizontalMetrics({name: (500, 0) for name in names})
    builder.setupHorizontalHeader(ascent=800, descent=-200)
    builder.setupNameTable({"familyName": "Tiny", "styleName": "Regular"})
    builder.setupOS2()
    builder.setupPost()
    features = (
        "languagesystem DFLT dflt;\n"
        "feature rphf { sub ra halant by reph; } rphf;\n"
        "feature half { sub ka halant by kaHalf; } half;\n"
        "feature pres { sub iSign by iSignAlt; } pres;\n"
        "feature locl { sub zeroDeva by zero; } locl;\n"
    )
    feature_lib.addOpenTypeFeaturesFromString(builder.font, features)
    stream = io.BytesIO()
    builder.save(stream)
    return stream.getvalue()


def test_font_glyph_texts_reads_cmap_and_gsub() -> None:
    readings = font_glyph_texts(_tiny_font())
    assert readings is not None
    derived, direct = readings
    # Glyph ids follow the order given in _tiny_font().
    assert direct[1] == "क" and direct[4] == "ि"
    assert derived[7] == "क्"  # half form from the "half" ligature
    assert derived[8] == _REPH_MARK  # reph is marked for reordering
    assert derived[4] == derived[9] == _I_SIGN_MARK  # both "ि" glyphs
    assert derived[6] == "०"  # ASCII-zero glyph used as the Devanagari zero


def test_unreadable_font_returns_none() -> None:
    assert font_glyph_texts(b"not a font") is None


@pytest.mark.skipif(not RULES_PDF.is_file(), reason="local source copy not available")
def test_rules_2054_pages_match_rendered_text() -> None:
    # Expected strings were checked against the rendered page images.
    pages = extract_pages(RULES_PDF, ocr=False, expected_language="ne")
    rule_23 = pages[16]["text"]
    assert "२३. चालक अनुमतिपत्रको नवीकरणः" in rule_23
    assert "दिने कार्यालयमा अनुसूची-२१ बमोजिमको ढाँचामा दरखास्त दिनुपर्नेछ।" in rule_23
    schedule_3 = pages[42]["text"]
    assert "अनुसूची-३" in schedule_3 and "दस्तुर तालिका" in schedule_3
    assert "८००/-" in schedule_3 and "8००/-" not in schedule_3
    assert all(_I_SIGN_MARK not in page["text"] and _REPH_MARK not in page["text"] for page in pages)
