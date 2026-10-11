"""Make clean, human-readable PDF reading copies of downloaded source documents.

Reads data/raw/_manifest.json and, for every entry with status "ok":

* HTML source -> strip site chrome (scripts, styles, menus, header/footer,
  search boxes, social links ...), keep the remaining text VERBATIM and in
  order, write data/readable/_html/<id>.html, then print it to
  data/readable/<service>/<id>.pdf with headless Microsoft Edge.
* PDF source  -> copy the file unchanged (byte-identical) to
  data/readable/<service>/<id>.pdf.

It also writes data/readable/README.md, an index of EVERY manifest entry.

The outputs are local reading copies for the Khula Gyan team only.
data/readable/ is git-ignored. Page numbers of the reading copies are NOT the
page numbers of the original sources.

Run from the repo root:
    .venv/Scripts/python.exe scripts/make_readable_pdfs.py
"""

import html
import json
import shutil
import subprocess
import sys
import tempfile
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

import pymupdf  # PyMuPDF, only used to count pages for the README

REPO = Path(__file__).resolve().parent.parent
RAW_DIR = REPO / "data" / "raw"
OUT_DIR = REPO / "data" / "readable"
MANIFEST = RAW_DIR / "_manifest.json"
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

NOTICE = ("Local reading copy for Khula Gyan team review only. Not for "
          "redistribution. Cite the original URL and the original page, not "
          "this PDF's page numbers.")

# Order in which services appear in the README.
SERVICE_ORDER = ["driving_license", "citizenship", "passport", "reference"]

# Extra, human-written warnings for specific sources (shown in the README).
EXTRA_NOTES = {
    "dl_dotm_portal": (
        "mostly site navigation; no documents/fees listed. Page text is Nepali "
        "(register corrected to lang=ne on 2026-10-11). The only service line is "
        "'Select your respective province portal to log in, apply for a new "
        "license, or renew online.' The list of province portals on the live "
        "page is built by JavaScript, so it is NOT in this reading copy "
        "(scripts are removed). Site-wide notice tickers are kept."
    ),
    "citizenship_kathmandu_requirements": (
        "scanned image PDF: text layer garbled, needs OCR (Tesseract nep+eng). "
        "Copied byte-identical; read the page images."
    ),
}

# ---------------------------------------------------------------------------
# HTML cleaning
# ---------------------------------------------------------------------------

# Tags that are always site chrome (or cannot be printed offline). The whole
# element, including everything inside it, is dropped.
CHROME_TAGS = {
    "script", "style", "noscript", "nav", "header", "footer", "form",
    "iframe", "button", "object", "embed", "svg", "canvas", "template",
    "video", "audio", "select", "textarea", "head",
}

# Tags with no end tag ("void" elements). Some of them are dropped (img, link,
# meta, input load external things or are form controls); br/hr are kept.
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "param", "source", "track", "wbr"}
KEEP_VOID_TAGS = {"br", "hr"}

# If a class or id contains one of these words, the element is chrome.
CHROME_WORDS = ("nav", "menu", "breadcrumb", "social", "search", "footer",
                "skip-link")

# Exception: blocks with these classes are kept even inside a dropped header,
# because they hold the site's notice lists (real content; when unsure, keep).
KEEP_CLASSES = {"marquee-slider"}

# Tags we rename so they print as plain blocks (a <marquee> scrolls and can
# print as an empty strip). The text inside stays the same.
RENAME_TAGS = {"marquee": "div"}

# The only attributes we copy to the output.
KEEP_ATTRS = {"href", "colspan", "rowspan"}


def _class_and_id(attrs):
    """Return (set of class names, combined lower-case class+id string)."""
    d = dict(attrs)
    classes = set((d.get("class") or "").split())
    text = ((d.get("class") or "") + " " + (d.get("id") or "")).lower()
    return classes, text


class ChromeStripper(HTMLParser):
    """Walk the HTML and copy only the content elements to self.out.

    We keep a stack with one entry per open element: (tag, emitting).
    'emitting' says whether that element (and so its text) is copied.
    """

    def __init__(self, base_url):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.stack = []      # list of (tag, emitting)
        self.out = []        # pieces of output HTML
        self.dropped = {}    # what we removed, for the report: label -> count

    def _parent_emitting(self):
        # Outside every element nothing is emitted; <body> turns emitting on.
        return self.stack[-1][1] if self.stack else False

    def _note_drop(self, label):
        self.dropped[label] = self.dropped.get(label, 0) + 1

    def handle_starttag(self, tag, attrs):
        classes, cls_id = _class_and_id(attrs)

        if tag in VOID_TAGS:
            if self._parent_emitting():
                if tag in KEEP_VOID_TAGS:
                    self.out.append(f"<{tag}>")
                else:
                    self._note_drop(f"<{tag}>")
            return

        if tag in ("html",):
            self.stack.append((tag, False))
            return
        if tag == "body":
            self.stack.append((tag, True))
            return

        parent = self._parent_emitting()
        if classes & KEEP_CLASSES:
            emitting = True                      # rescued content block
        elif tag in CHROME_TAGS:
            emitting = False
            if parent:
                self._note_drop(f"<{tag}>")
        elif any(w in cls_id for w in CHROME_WORDS):
            emitting = False
            if parent:
                self._note_drop(f"class/id '{cls_id.strip()}'")
        else:
            emitting = parent

        self.stack.append((tag, emitting))
        if emitting:
            name = RENAME_TAGS.get(tag, tag)
            kept = []
            for key, value in attrs:
                if key in KEEP_ATTRS and value is not None:
                    if key == "href":
                        value = urljoin(self.base_url, value.strip())
                    kept.append(f' {key}="{html.escape(value, quote=True)}"')
            self.out.append(f"<{name}{''.join(kept)}>")

    def handle_startendtag(self, tag, attrs):
        # <br/>, <img .../> and so on: treat like a start tag with no content.
        if tag in VOID_TAGS:
            self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        # Find the matching open element (tolerates sloppy HTML).
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                # Close everything opened after it, then the element itself.
                while len(self.stack) > i:
                    open_tag, emitting = self.stack.pop()
                    if emitting and open_tag != "body":
                        self.out.append(f"</{RENAME_TAGS.get(open_tag, open_tag)}>")
                return
        # An end tag with no matching start tag is ignored.

    def handle_data(self, data):
        if self._parent_emitting():
            self.out.append(html.escape(data, quote=False))


PRINT_CSS = """
@page { size: A4; margin: 2cm; }
html { font-family: "Nirmala UI", "Mangal", sans-serif; font-size: 12pt;
       line-height: 1.5; color: #000; background: #fff; }
body { margin: 0; }
.kg-meta { border: 1px solid #555; padding: 8px 12px; margin-bottom: 18px;
           font-size: 10pt; background: #f4f4f4; }
.kg-meta h1 { font-size: 14pt; margin: 0 0 6px 0; }
.kg-meta p { margin: 2px 0; word-break: break-all; }
.kg-meta .kg-notice { font-weight: bold; margin-top: 6px; word-break: normal; }
h1, h2, h3, h4 { font-size: 13pt; margin: 12px 0 4px 0; }
a { color: #003366; text-decoration: none; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; }
th, td { border: 1px solid #444; padding: 4px 6px; vertical-align: top; }
"""


def build_clean_html(entry, raw_html):
    """Return a full, printable HTML page for one manifest entry."""
    parser = ChromeStripper(entry["url"])
    parser.feed(raw_html)
    parser.close()
    body = "".join(parser.out)

    e = lambda s: html.escape(str(s if s is not None else "—"))  # noqa: E731
    meta = (
        '<div class="kg-meta">'
        f"<h1>{e(entry['title'])}</h1>"
        f"<p><b>Publisher:</b> {e(entry['publisher'])}</p>"
        f"<p><b>Original URL:</b> {e(entry['url'])}</p>"
        f"<p><b>Fetched (UTC):</b> {e(entry['fetched_at_utc'])}</p>"
        f"<p><b>Licence status:</b> {e(entry['licence_status'])}</p>"
        f"<p><b>sha256 (first 12):</b> {e((entry['sha256'] or '')[:12])}</p>"
        f'<p class="kg-notice">{e(NOTICE)}</p>'
        "</div>"
    )
    # The CSP meta tag blocks every external request (images, fonts, CSS),
    # so Edge prints offline and never downloads anything.
    page = (
        "<!DOCTYPE html>\n<html lang=\"ne\">\n<head>\n"
        '<meta charset="utf-8">\n'
        "<meta http-equiv=\"Content-Security-Policy\" "
        "content=\"default-src 'none'; style-src 'unsafe-inline'\">\n"
        f"<title>{e(entry['title'])}</title>\n"
        f"<style>{PRINT_CSS}</style>\n</head>\n<body>\n"
        f"{meta}\n{body}\n</body>\n</html>\n"
    )
    return page, parser.dropped


def print_with_edge(html_path, pdf_path):
    """Print a local HTML file to PDF with headless Edge."""
    if pdf_path.exists():
        pdf_path.unlink()
    profile = tempfile.mkdtemp(prefix="kg_edge_")  # throw-away Edge profile
    cmd = [
        str(EDGE), "--headless", "--disable-gpu", "--no-first-run",
        f"--user-data-dir={profile}",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path.resolve()}",
        html_path.resolve().as_uri(),
    ]
    # Passing a list lets Python quote paths with spaces correctly.
    subprocess.run(cmd, capture_output=True, timeout=120)
    if not pdf_path.exists():
        # Older Edge versions use a different flag name.
        cmd[cmd.index("--no-pdf-header-footer")] = "--print-to-pdf-no-header"
        subprocess.run(cmd, capture_output=True, timeout=120)
    # Wait (up to 30 s) for the file to appear and stop growing.
    last = -1
    for _ in range(60):
        if pdf_path.exists() and pdf_path.stat().st_size == last > 0:
            break
        last = pdf_path.stat().st_size if pdf_path.exists() else -1
        time.sleep(0.5)
    shutil.rmtree(profile, ignore_errors=True)
    if not pdf_path.exists():
        raise RuntimeError(f"Edge did not produce {pdf_path}")


# ---------------------------------------------------------------------------
# README index
# ---------------------------------------------------------------------------

def md_cell(text):
    """Make text safe for one Markdown table cell."""
    return " ".join(str(text).split()).replace("|", "\\|")


def write_readme(entries, results):
    lines = [
        "# Readable copies of source documents",
        "",
        "Local reading copies only. This folder is git-ignored and must not be "
        "redistributed. Generated by `scripts/make_readable_pdfs.py` from "
        "`data/raw/_manifest.json`. Page numbers of these PDFs are NOT the "
        "original pages: cite the original URL and the original page.",
        "",
    ]
    services = SERVICE_ORDER + sorted(
        {x["service"] for x in entries} - set(SERVICE_ORDER))
    for service in services:
        rows = [x for x in entries if x["service"] == service]
        if not rows:
            continue
        lines += [f"## {service}", "",
                  "| service | id | title | publisher | lang | licence status "
                  "| status | readable copy | pages | notes |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for x in rows:
            res = results.get(x["id"], {})
            notes = []
            if x["status"] == "suspect_content":
                notes.append("SKIPPED: no PDF made (suspect content).")
            elif x["status"] == "skipped_rights":
                notes.append("SKIPPED: rights.")
            elif x["status"] == "failed":
                notes.append("FAILED download.")
            if res.get("error"):
                notes.append("ERROR making copy: " + res["error"])
            if x["id"] in EXTRA_NOTES:
                notes.append(EXTRA_NOTES[x["id"]])
            if x.get("note"):
                notes.append("Manifest note: " + x["note"])
            cells = [service, x["id"], x["title"], x["publisher"], x["lang"],
                     x["licence_status"], x["status"],
                     res.get("path", "—"), res.get("pages", "—"),
                     " ".join(notes)]
            lines.append("| " + " | ".join(md_cell(c) for c in cells) + " |")
        lines.append("")
    (OUT_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))
    (OUT_DIR / "_html").mkdir(parents=True, exist_ok=True)
    results = {}  # id -> {"path": ..., "pages": ..., "error": ...}

    for x in entries:
        if x["status"] != "ok":
            continue
        src = RAW_DIR / x["filename"]
        out_pdf = OUT_DIR / x["service"] / f"{x['id']}.pdf"
        out_pdf.parent.mkdir(parents=True, exist_ok=True)
        try:
            if src.suffix.lower() == ".pdf":
                shutil.copyfile(src, out_pdf)  # byte-identical copy
            else:
                raw = src.read_text(encoding="utf-8", errors="replace")
                page, dropped = build_clean_html(x, raw)
                out_html = OUT_DIR / "_html" / f"{x['id']}.html"
                out_html.write_text(page, encoding="utf-8")
                print_with_edge(out_html, out_pdf)
                print(f"[{x['id']}] removed:", dropped)
            with pymupdf.open(out_pdf) as doc:
                pages = doc.page_count
            results[x["id"]] = {
                "path": out_pdf.relative_to(OUT_DIR).as_posix(),
                "pages": pages,
            }
            print(f"[{x['id']}] -> {out_pdf} ({pages} pages)")
        except Exception as exc:  # keep going; record the error in README
            results[x["id"]] = {"error": f"{type(exc).__name__}: {exc}"}
            print(f"[{x['id']}] ERROR {exc}", file=sys.stderr)

    write_readme(entries, results)
    print("Wrote", OUT_DIR / "README.md")


if __name__ == "__main__":
    main()
