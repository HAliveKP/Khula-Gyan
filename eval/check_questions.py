"""Check eval/questions.jsonl follows the format in blueprint section 9.5.

Usage:  python eval/check_questions.py [path]
"""

import json
import sys
from collections import Counter
from pathlib import Path

LANGS = {"ne", "en", "mixed"}
TYPES = {"answerable", "out_of_scope"}
SERVICES = {"driving_license", "citizenship", "passport", "other"}


def check(path: Path) -> int:
    problems, ids = [], set()
    counts = {"type": Counter(), "lang": Counter(), "service": Counter(), "verified": Counter()}
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            q = json.loads(line)
        except json.JSONDecodeError as err:
            problems.append(f"line {n}: not valid JSON ({err.msg})")
            continue
        qid = q.get("id", f"line{n}")
        for key in ("id", "q", "lang", "service", "type", "expected", "must_cite", "verified"):
            if key not in q:
                problems.append(f"{qid}: missing '{key}'")
        if qid in ids:
            problems.append(f"{qid}: duplicate id")
        ids.add(qid)
        if q.get("lang") not in LANGS:
            problems.append(f"{qid}: lang must be one of {sorted(LANGS)}")
        if q.get("type") not in TYPES:
            problems.append(f"{qid}: type must be one of {sorted(TYPES)}")
        if q.get("service") not in SERVICES:
            problems.append(f"{qid}: service must be one of {sorted(SERVICES)}")
        if q.get("type") == "answerable" and q.get("verified"):
            if not q.get("expected"):
                problems.append(f"{qid}: verified answerable question needs 'expected' facts")
            mc = q.get("must_cite") or {}
            if not mc.get("source") or not isinstance(mc.get("page"), int):
                problems.append(f"{qid}: verified answerable question needs must_cite {{source, page}}")
        for field in counts:
            counts[field][str(q.get(field))] += 1

    total = sum(counts["type"].values())
    print(f"{total} questions in {path}")
    for field, c in counts.items():
        print(f"  {field:9s} " + ", ".join(f"{k}={v}" for k, v in sorted(c.items())))
    if total:
        print(f"  target mix: ~80% answerable / 20% out_of_scope; ~40% ne, 40% en, 20% mixed "
              f"(now {100 * counts['type']['out_of_scope'] // total}% out_of_scope)")
    for p in problems:
        print("PROBLEM:", p)
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "questions.jsonl"
    sys.exit(check(target))
