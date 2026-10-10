"""Download source files to ignored data/raw/ according to sources.yaml."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCES_FILE = REPO_ROOT / "data" / "sources.yaml"
RAW_DIR = REPO_ROOT / "data" / "raw"
MAX_DOWNLOAD_BYTES = 50 * 1024 * 1024


def load_sources() -> list[dict]:
    data = yaml.safe_load(SOURCES_FILE.read_text(encoding="utf-8")) or {}
    sources = data.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("data/sources.yaml must contain a 'sources' list")
    return sources


def fetch(source: dict, *, overwrite: bool = False) -> Path:
    url = source["url"]
    if urlparse(url).scheme != "https":
        raise ValueError(f"Refusing non-HTTPS source URL: {url}")
    filename = Path(source["filename"]).name
    if filename != source["filename"] or filename in {"", ".", ".."}:
        raise ValueError(f"Unsafe source filename: {source['filename']!r}")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    destination = RAW_DIR / filename
    if destination.exists() and not overwrite:
        print(f"SKIP exists: {destination.relative_to(REPO_ROOT)} (use --overwrite)")
        return destination

    request = Request(url, headers={"User-Agent": "Khula-Gyan-source-fetcher/1.0"})
    try:
        with urlopen(request, timeout=30) as response:
            body = response.read(MAX_DOWNLOAD_BYTES + 1)
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"Could not fetch {url}: {exc}") from exc
    if len(body) > MAX_DOWNLOAD_BYTES:
        raise RuntimeError(f"Refusing source larger than {MAX_DOWNLOAD_BYTES} bytes: {url}")
    if not body:
        raise RuntimeError(f"Source returned an empty response: {url}")
    destination.write_bytes(body)
    print(f"FETCHED {source['id']}: {len(body)} bytes -> {destination.relative_to(REPO_ROOT)}")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--include-unclear",
        action="store_true",
        help="also fetch sources marked unclear; never fetch all-rights-reserved sources",
    )
    parser.add_argument("--overwrite", action="store_true", help="replace an existing local copy")
    args = parser.parse_args()

    try:
        sources = load_sources()
        allowed = {"confirmed open"}
        if args.include_unclear:
            allowed.add("unclear")
        selected = [s for s in sources if s.get("license_status") in allowed]
        skipped = len(sources) - len(selected)
        print(f"Eligible source files: {len(selected)}; skipped by license status: {skipped}")
        for source in selected:
            fetch(source, overwrite=args.overwrite)
    except (KeyError, OSError, RuntimeError, ValueError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

