"""Extract approved local sources, preserve citations, and build the Chroma index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.process_document import process_document  # noqa: E402
from src.ingest.chunk import chunk_text  # noqa: E402
from src.ingest.embed_store import index_chunks  # noqa: E402

RAW_DIR = REPO_ROOT / "data" / "raw"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
SOURCES_FILE = REPO_ROOT / "data" / "sources.yaml"
INDEX_DIR = REPO_ROOT / "chroma_db"
ANSWER_SERVICES = {"driving_license", "citizenship", "passport"}


def load_sources() -> list[dict]:
    data = yaml.safe_load(SOURCES_FILE.read_text(encoding="utf-8")) or {}
    sources = data.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("data/sources.yaml must contain a 'sources' list")
    return sources


def build(*, chunk_size: int = 400, overlap: int = 50) -> tuple[int, int]:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    all_chunks: list[dict] = []
    processed_pages = 0
    skipped: list[str] = []

    for source in load_sources():
        raw_path = RAW_DIR / source["filename"]
        if not raw_path.is_file():
            continue
        if source.get("license_status") != "confirmed open":
            skipped.append(f"{source['id']}: license status is not confirmed open")
            continue

        service = source.get("service") or "reference"
        output = process_document(
            raw_path,
            service=service,
            lang=source["lang"],
            source_url=source["url"],
            output_directory=PROCESSED_DIR,
        )
        rows = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines() if line.strip()]
        processed_pages += len(rows)

        if service not in ANSWER_SERVICES or not source.get("answer_evidence", False):
            skipped.append(f"{source['id']}: reference-only or not approved as answer evidence")
            continue

        for row in rows:
            all_chunks.extend(
                chunk_text(
                    row["text"],
                    doc_id=Path(source["filename"]).stem,
                    source=source["filename"],
                    page=int(row["page"]),
                    service=service,
                    lang=source["lang"],
                    source_url=source["url"],
                    chunk_size=chunk_size,
                    overlap=overlap,
                )
            )

    if all_chunks:
        collection = index_chunks(
            all_chunks,
            persist_directory=INDEX_DIR,
            model_name="BAAI/bge-m3",
        )
        indexed_count = int(collection.count())
    else:
        indexed_count = 0

    print(f"Processed page records: {processed_pages}")
    print(f"Eligible civic chunks: {len(all_chunks)}; indexed records: {indexed_count}")
    for message in skipped:
        print(f"SKIP {message}")
    if not all_chunks:
        print("No source passed both open-license and civic-answer-evidence checks; no Chroma index was built.")
    return processed_pages, indexed_count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunk-size", type=int, default=400, choices=range(300, 501))
    parser.add_argument("--overlap", type=int, default=50)
    args = parser.parse_args()
    try:
        build(chunk_size=args.chunk_size, overlap=args.overlap)
    except (OSError, ValueError, RuntimeError, KeyError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

