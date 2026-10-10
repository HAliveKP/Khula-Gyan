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
    output_directory: str | Path = REPO_ROOT / "data" / "processed",
    ocr: bool = True,
) -> Path:
    """Write one cleaned, source-linked JSONL record per page."""
    source = Path(source_path)
    if service not in {"driving_license", "citizenship", "passport", "reference"}:
        raise ValueError("service must be driving_license, citizenship, passport, or reference")
    if lang not in {"ne", "en"}:
        raise ValueError("lang must be ne or en")

    raw_pages = extract_pages(source, ocr=ocr)
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
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")

    ratings = [extraction_rating(page["text"]) for page in pages]
    counts = {rating: ratings.count(rating) for rating in ("good", "ok", "bad")}
    print(f"Wrote {len(pages)} page record(s) to {destination}")
    print("Preliminary page ratings: " + ", ".join(f"{key}={value}" for key, value in counts.items()))
    print("Review every page against its original before indexing or answering.")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Local PDF or HTML file in data/raw/")
    parser.add_argument("--service", required=True, choices=("driving_license", "citizenship", "passport"))
    parser.add_argument("--lang", required=True, choices=("ne", "en"))
    parser.add_argument("--no-ocr", action="store_true", help="Skip OCR and keep text-layer extraction only")
    args = parser.parse_args()

    try:
        process_document(args.source, service=args.service, lang=args.lang, ocr=not args.no_ocr)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
