"""Day 5: pick guard_min_score from a finished run, without new LLM calls.

Run the eval once with the threshold OFF (guard_min_score: 0 in config.yaml), then:
    python eval/sweep_threshold.py                 # uses the newest file in eval/runs/
    python eval/sweep_threshold.py eval/runs/X.jsonl

For each threshold it shows what WOULD happen: a question is refused if its top
retrieval score is below the threshold, or if it was already refused for another reason.
Pick the threshold with correct refusal >= 90% and the lowest false refusal.
"""

import json
import sys
from pathlib import Path

RUNS = Path(__file__).resolve().parent / "runs"


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else max(RUNS.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    recs = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    recs = [r for r in recs if r.get("top_score") is not None]
    ans = [r for r in recs if r["type"] == "answerable"]
    oos = [r for r in recs if r["type"] == "out_of_scope"]
    if not ans or not oos:
        sys.exit("Need both answerable and out_of_scope questions with top_score in the run.")
    print(f"{path.name}: {len(ans)} answerable, {len(oos)} out-of-scope\n")
    print("threshold  correct_refusal  false_refusal  answerable_kept")
    for t in [i / 20 for i in range(0, 20)]:
        def refused(r):
            return r["top_score"] < t or r["status"] == "not_found"
        cr = sum(refused(r) for r in oos) / len(oos)
        fr = sum(refused(r) for r in ans) / len(ans)
        print(f"  {t:4.2f}      {cr:6.0%}          {fr:6.0%}        {len(ans) - sum(refused(r) for r in ans)}")


if __name__ == "__main__":
    main()
