"""Extract page text from official HTML or PDF files without losing page IDs."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from typing import Any


class _VisibleTextParser(HTMLParser):
    """Small standard-library HTML reader that skips script/style contents."""

    _BLOCK_TAGS = {"address", "article", "br", "div", "footer", "h1", "h2", "h3", "li", "p", "section", "table", "tr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self._ignored_depth += 1
        elif self._ignored_depth == 0 and tag in self._BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self._ignored_depth:
            self._ignored_depth -= 1
        elif self._ignored_depth == 0 and tag in self._BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._ignored_depth == 0:
            self.parts.append(data)


def _extract_html(path: Path) -> list[dict[str, Any]]:
    raw = path.read_text(encoding="utf-8", errors="replace")
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


def _extract_pdf(path: Path, *, ocr: bool, ocr_languages: str) -> list[dict[str, Any]]:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PDF extraction needs PyMuPDF. Install the project requirements first.") from exc

    pages: list[dict[str, Any]] = []
    with fitz.open(path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")
            used_ocr = False
            if ocr and len(text.strip()) < 40:
                text = _ocr_page(page, languages=ocr_languages)
                used_ocr = True
            pages.append({"page": page_number, "text": text, "ocr": used_ocr})
    return pages


def extract_pages(
    path: str | Path,
    *,
    ocr: bool = True,
    ocr_languages: str = "nep+eng",
) -> list[dict[str, Any]]:
    """Extract one record per PDF page, or one record for an HTML page.

    OCR runs only when a PDF page has fewer than 40 extracted characters. The
    original source should remain in ignored ``data/raw/``; this function does
    not download, modify, or redistribute source files.
    """
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"Source file does not exist: {source}")
    suffix = source.suffix.lower()
    if suffix in {".html", ".htm"}:
        return _extract_html(source)
    if suffix == ".pdf":
        return _extract_pdf(source, ocr=ocr, ocr_languages=ocr_languages)
    raise ValueError("Supported source formats are PDF (.pdf) and HTML (.html/.htm)")
