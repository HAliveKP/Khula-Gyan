"""Tests for the Devanagari ToUnicode repair in src/ingest/extract.py."""

from __future__ import annotations

import io
from pathlib import Path

import pytest

from src.ingest import extract
from src.ingest.extract import (
    _I_SIGN_MARK,
    _REPH_MARK,
    _join_components,
    _parse_tounicode,
    _write_tounicode,
    extract_pages,
    font_glyph_texts,
    reference_glyph_texts,
    restore_logical_order,
)

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
RULES_PDF = RAW / "dl_vehicle_transport_rules_2054.pdf"
GHORAHI_PDF = RAW / "palika_ghorahi.pdf"
HETAUDA_PDF = RAW / "palika_hetauda_2083_84.pdf"
DOTM_PDF = RAW / "dl_dotm_procedure_directive_2060.pdf"


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


def test_reference_fills_glyphs_of_matching_font(monkeypatch: pytest.MonkeyPatch) -> None:
    font = _tiny_font()
    _derived, direct = font_glyph_texts(font)
    reference = {"1": "क", "2": "र", "3": "्", "4": "ि", "5": "०", "8": _REPH_MARK, "9": _I_SIGN_MARK}
    monkeypatch.setattr(extract, "_MIN_REFERENCE_CHECKS", 3)
    monkeypatch.setattr(extract, "_font_references", lambda: {"Tiny": {"glyph_count": 10, "glyphs": reference}})
    # The reference's "ि" marker agrees with the plain "ि" in the subset's cmap.
    assert reference_glyph_texts(font, direct)[9] == _I_SIGN_MARK


@pytest.mark.parametrize(
    "references",
    [
        {"Tiny": {"glyph_count": 11, "glyphs": {"1": "क", "2": "र", "3": "्", "4": "ि", "5": "०"}}},  # other glyph count
        {"Tiny": {"glyph_count": 10, "glyphs": {"1": "ख", "2": "र", "3": "्", "4": "ि", "5": "०"}}},  # cmap disagrees
        {"Other": {"glyph_count": 10, "glyphs": {"1": "क", "2": "र", "3": "्", "4": "ि", "5": "०"}}},  # other family
    ],
)
def test_reference_is_not_used_for_a_different_font(monkeypatch: pytest.MonkeyPatch, references: dict) -> None:
    font = _tiny_font()
    _derived, direct = font_glyph_texts(font)
    monkeypatch.setattr(extract, "_MIN_REFERENCE_CHECKS", 3)
    monkeypatch.setattr(extract, "_font_references", lambda: references)
    assert reference_glyph_texts(font, direct) == {}


def test_reference_needs_enough_cmap_checks(monkeypatch: pytest.MonkeyPatch) -> None:
    font = _tiny_font()
    _derived, direct = font_glyph_texts(font)
    monkeypatch.setattr(extract, "_font_references", lambda: {"Tiny": {"glyph_count": 10, "glyphs": {"1": "क"}}})
    assert reference_glyph_texts(font, direct) == {}  # default needs 20 Devanagari cmap glyphs


def test_shipped_kalimati_reference_reads_reordered_glyphs() -> None:
    glyphs = extract._font_references()["Kalimati"]["glyphs"]
    assert glyphs["128"] == "क"
    assert glyphs["91"] == _REPH_MARK  # reph, which Word mapped to "य" in the Ghorahi charter
    assert {glyphs[str(gid)] for gid in range(464, 469)} == {_I_SIGN_MARK}  # "ि" width variants
    assert glyphs["566"] == "े" + _REPH_MARK  # "े" with reph above


@pytest.mark.skipif(not GHORAHI_PDF.is_file(), reason="local source copy not available")
def test_ghorahi_charter_matches_rendered_text() -> None:
    # Expected strings were checked against the rendered page image (page 2).
    page = extract_pages(GHORAHI_PDF, ocr=False, expected_language="ne")[1]["text"]
    assert "गर्ने व्यक्तिको नागरिकता प्रमाणपत्र" in page
    assert "नाता कायम गर्ने निवेदकले हालसालै खिचेको पासपोर्ट साईजको फोटो ३ प्रति" in page
    assert "पत्रको प्रतिलिपि र १६ वर्षभन्दा कम उमेरको भएमा जन्म दर्ता प्रमाण–पत्र" in page
    assert "नागररकता" not in page and "लसफाररस" not in page


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


# --- Preeti-family legacy fonts -------------------------------------------
# Each pair was checked against rendered pages of the Hetauda charter, the
# DoTM directive or the Pokhara rates charter.


@pytest.mark.parametrize(
    ("preeti", "unicode_text"),
    [
        ("l;kmfl/;", "सिफारिस"),  # "ि" typed before its consonant; k+m = फ
        ("sfo{ljlwM", "कार्यविधिः"),  # reph typed after its syllable
        ("lgb]{lzsf", "निर्देशिका"),  # reph after a vowel sign, "ि" before
        ("lgMz'Ns", "निःशुल्क"),
        ("cfjZos kg]{ sfuhft", "आवश्यक पर्ने कागजात"),  # c+f = आ; Z+f = श
        ("k|df0fkq", "प्रमाणपत्र"),  # "्र" sign; ण् + ा = ण
        ("hgzlQm", "जनशक्ति"),  # Q+m = क्त, "ि" before the conjunct
        ("e'mqf] a'e\\mg'", "झुत्रो बुझ्नु"),  # hook typed after a vowel sign / halant
        ("qm=;+= @)^)", "क्र.सं. २०६०"),  # shifted digits are Devanagari digits
        ("ug]{]{", "गर्ने"),  # "]{" typed twice is drawn once
        ("kmFf6sf", "फाँटका"),  # "ँ" typed before "ा"
        ("cWoIf÷j8f", "अध्यक्ष/वडा"),
        ('d"NofÍg', "मूल्याङ्कन"),
        ("……P]gÚÚ", "‘‘ऐन’’"),
    ],
)
def test_preeti_to_unicode(preeti: str, unicode_text: str) -> None:
    assert extract.preeti_to_unicode(preeti) == unicode_text


def test_legacy_font_names() -> None:
    for name in ["ABCDEE+Preeti", "Kantipur Regular", "PCS NEPALI"]:
        assert extract._PREETI_FONT.search(name)
    for name in ["ABCDEE+Mangal", "Kalimati", "Kokila", "TimesNewRomanPSMT", "Fontasy Himali"]:
        assert not extract._PREETI_FONT.search(name)
    assert extract._HIMALI_FONT.search("FONTASY_ HIMALI_ TT")
    assert extract._himali_to_unicode("(10)") == "(१०)"


def test_only_legacy_font_spans_are_converted() -> None:
    fitz = pytest.importorskip("fitz")
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "l;kmfl/;", fontname="helv")  # stands in for Preeti
    page.insert_text((72, 100), "IEE l", fontname="tiro")  # an ordinary font
    page.insert_text((72, 128), "kg]{", fontname="helv")
    plain = page.get_text("text")
    assert extract._page_text(page, {}) == plain  # no legacy font: text unchanged
    text = extract._page_text(page, {"Helvetica": extract.preeti_to_unicode})
    assert text.splitlines() == ["सिफारिस", "IEE l", "पर्ने"]


@pytest.mark.skipif(not HETAUDA_PDF.is_file(), reason="local source copy not available")
def test_hetauda_charter_matches_rendered_text() -> None:
    # Expected strings were checked against the rendered page images (pages 3 and 15).
    pages = extract_pages(HETAUDA_PDF, ocr=False, expected_language="ne")
    assert "१) निवेदन पत्र र नागरिकता प्रमाणपत्रको प्रतिलिपि" in pages[2]["text"]
    assert "२) वडा अध्यक्ष/वडा सदस्य/वडा सचिवले सम्बन्धित" in pages[2]["text"]
    assert "सम्बन्धित   फाँटका कर्मचारी" in pages[2]["text"]
    assert "सम्झौता पत्र र बहाल कर" in pages[14]["text"]
    assert all(page.get("extraction_status") != "unusable" for page in pages)


@pytest.mark.skipif(not DOTM_PDF.is_file(), reason="local source copy not available")
def test_dotm_directive_matches_rendered_text() -> None:
    # Page 107 is quoted in docs/extraction-notes.md; page 4 is the contents page.
    pages = extract_pages(DOTM_PDF, ocr=False, expected_language="ne")
    assert "यातायात व्यवस्थापन कार्यविधि निर्देशिका, २०७४" in pages[106]["text"]
    assert "अनुसूचीहरू" in pages[106]["text"]
    assert "बाझिएमा गर्ने" in pages[3]["text"]
    assert "निर्देशक (जनशक्ति व्यवस्थापन शाखा) को जिम्मेवारी" in pages[3]["text"]
    assert "१०" in pages[3]["text"]  # Fontasy Himali page numbers
