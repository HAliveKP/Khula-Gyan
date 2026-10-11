"""Extract and clean one locally stored PDF/HTML source into page JSONL."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ingest.clean import clean_pages, extraction_rating
from src.ingest.extract import extract_pages


def process_document(
    source_path: str | Path,
    *,
    service: str,
    lang: str,
    source_url: str | None = None,
    output_directory: str | Path = REPO_ROOT / "data" / "processed",
    ocr: bool = True,
) -> Path:
    """Write one cleaned, source-linked JSONL record per page."""
    source = Path(source_path)
    if service not in {"driving_license", "citizenship", "passport", "reference"}:
        raise ValueError("service must be driving_license, citizenship, passport, or reference")
    if lang not in {"ne", "en"}:
        raise ValueError("lang must be ne or en")

    raw_pages = extract_pages(source, ocr=ocr, expected_language=lang)
    pages = clean_pages(raw_pages)
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    destination = output / f"{source.stem}.jsonl"

    with destination.open("w", encoding="utf-8", newline="\n") as stream:
        for item in pages:
            row = {
                "id": f"{source.stem}_p{item['page']}",
                "text": item["text"],
                "source": source.name,
                "page": int(item["page"]),
                "service": service,
                "lang": lang,
            }
            if source_url:
                row["source_url"] = source_url
            for field in ("extraction_status", "extraction_note"):
                if field in item:
                    row[field] = item[field]
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")

    ratings = [extraction_rating(page["text"]) for page in pages]
    counts = {rating: ratings.count(rating) for rating in ("good", "ok", "bad")}
    print(f"Wrote {len(pages)} page record(s) to {destination}")
    print("Preliminary page ratings: " + ", ".join(f"{key}={value}" for key, value in counts.items()))
    unusable = sum(page.get("extraction_status") == "unusable" for page in pages)
    if unusable:
        print(f"Unusable pages: {unusable}; their text was blanked and must not be indexed.")
    print("Review every page against its original before indexing or answering.")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Local PDF or HTML file in data/raw/")
    parser.add_argument("--service", required=True, choices=("driving_license", "citizenship", "passport", "reference"))
    parser.add_argument("--lang", required=True, choices=("ne", "en"))
    parser.add_argument("--source-url", help="Canonical URL recorded with the extracted page")
    parser.add_argument("--no-ocr", action="store_true", help="Skip OCR and keep text-layer extraction only")
    args = parser.parse_args()

    try:
        process_document(args.source, service=args.service, lang=args.lang, source_url=args.source_url, ocr=not args.no_ocr)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
