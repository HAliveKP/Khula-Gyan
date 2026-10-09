"""Run the evaluation and append one row to docs/results.md (blueprint section 11).

Examples
  python eval/run_eval.py --mock --note "harness check"          # no search(), no key needed with LLM_PROVIDER=fake
  python eval/run_eval.py --note "baseline: dense only"          # real search() from Member 2
  python eval/run_eval.py --judge --note "prompt v1 + reranker"  # adds LLM judge (correctness, hallucination)
  python eval/run_eval.py --retrieval-only --note "BM25 + RRF"   # hit@5 only, for Member 2's experiments
"""

import argparse
import json
import statistics
import sys
import time
import unicodedata
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.generation.answer import answer_with_trace  # noqa: E402
from src.generation.guard import citations_grounded  # noqa: E402
from src.generation.prompt import PROMPT_VERSION  # noqa: E402
from src.generation.settings import setting  # noqa: E402

RESULTS_MD = REPO / "docs" / "results.md"
RUNS_DIR = REPO / "eval" / "runs"
HEADER = ("| Date | Change | Prompt | N | hit@5 | Citation acc. | Correct | Hallucination | "
          "Correct refusal | False refusal | p95 s |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")


def load_questions(path: Path, include_unverified: bool) -> list[dict]:
    qs = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return qs if include_unverified else [q for q in qs if q.get("verified")]


def get_retriever(mock: bool, use_service: bool):
    k = setting("final_k", 5)
    if mock:
        chunks = json.loads((REPO / "tests" / "fixtures" / "sample_chunks.json").read_text(encoding="utf-8"))

        def mock_search(q: dict) -> list[dict]:
            same = [c for c in chunks if c["service"] == q["service"]]
            if same:
                return sorted(same, key=lambda c: -c["score"])[:k]
            return [dict(c, score=c["score"] * 0.2) for c in chunks][:k]  # off-topic: weak scores
        return mock_search
    try:
        from src.retrieval.search import search
    except ImportError:
        sys.exit("src/retrieval/search.py is not available yet. Use --mock until Member 2's PR is merged.")
    return lambda q: search(q["q"], k=k, service=q["service"] if use_service else None)


def _norm(s: str) -> str:
    return " ".join(unicodedata.normalize("NFC", s).lower().split())


def keyword_correct(expected: list[str], resp: dict) -> bool:
    """Cheap correctness: at least half the expected facts appear as text. Use --judge for the real number."""
    if not expected:
        return False
    blob = _norm(resp["answer"] + " " + json.dumps(resp["checklist"], ensure_ascii=False))
    found = sum(_norm(fact) in blob for fact in expected)
    return found / len(expected) >= 0.5


def categorize(q: dict, rec: dict) -> str:
    """First guess at the failure category for docs/error-analysis.md ('' = no failure)."""
    answered = rec["status"] == "answered"
    if q["type"] == "out_of_scope":
        return "guard_error: answered out-of-scope" if answered else ""
    if not answered:
        if not rec["hit"]:
            return "retrieval_miss"
        if rec["reason"].startswith("guard_score") or rec["reason"] == "support_check_failed":
            return f"guard_error: {rec['reason'].split(':')[0]}"
        return f"generation_error: {rec['reason'].split(':')[0]}"
    if rec.get("hallucinated"):
        return "generation_error: hallucination"
    if not rec["correct"]:
        return "retrieval_miss" if not rec["hit"] else "generation_error: wrong/incomplete answer"
    return ""


def pct(values: list[bool]) -> str:
    return f"{100 * sum(values) / len(values):.0f}%" if values else "n/a"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", default=str(REPO / "eval" / "questions.jsonl"))
    ap.add_argument("--note", required=True, help="what changed since the last row")
    ap.add_argument("--mock", action="store_true", help="use tests/fixtures chunks instead of search()")
    ap.add_argument("--judge", action="store_true", help="use the LLM judge for correctness + hallucination")
    ap.add_argument("--retrieval-only", action="store_true", help="only measure hit@5")
    ap.add_argument("--use-service-filter", action="store_true")
    ap.add_argument("--include-unverified", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--no-write", action="store_true", help="print only; do not touch docs/results.md")
    args = ap.parse_args()

    questions = load_questions(Path(args.questions), args.include_unverified or args.mock)
    if args.limit:
        questions = questions[: args.limit]
    if not questions:
        sys.exit("No questions to run. Add verified questions or pass --include-unverified.")
    retrieve = get_retriever(args.mock, args.use_service_filter)
    if args.judge:
        from judge import judge

    records = []
    for q in questions:
        t0 = time.perf_counter()
        chunks = retrieve(q)
        mc = q.get("must_cite") or {}
        rec = {"id": q["id"], "type": q["type"], "lang": q["lang"], "service": q["service"],
               "hit": any(c["source"] == mc.get("source") and int(c["page"]) == mc.get("page") for c in chunks),
               "retrieved": [f'{c["source"]}#p{c["page"]} ({float(c.get("score", 0)):.3f})' for c in chunks]}
        if not args.retrieval_only:
            resp, trace = answer_with_trace(q["q"], chunks)
            rec.update(status=resp["status"], reason=trace["reason"], top_score=trace["top_score"],
                       answer=resp["answer"],
                       citations=resp["citations"],
                       cited_must_page=any(c["source"] == mc.get("source") and c["page"] == mc.get("page")
                                           for c in resp["citations"]),
                       grounded=citations_grounded(resp, chunks) if resp["status"] == "answered" else None)
            if args.judge and resp["status"] == "answered" and q["type"] == "answerable":
                verdict = judge(q["q"], q.get("expected", []), resp, chunks)
                rec.update(correct=verdict["correct"], hallucinated=verdict["hallucinated"],
                           judge_reason=verdict["reason"])
            elif args.judge and resp["status"] == "answered":  # out-of-scope answered: still check support
                verdict = judge(q["q"], [], resp, chunks)
                rec.update(correct=False, hallucinated=verdict["hallucinated"], judge_reason=verdict["reason"])
            else:
                rec.update(correct=resp["status"] == "answered" and keyword_correct(q.get("expected", []), resp))
            rec["category"] = categorize(q, rec)
        rec["seconds"] = round(time.perf_counter() - t0, 2)
        records.append(rec)
        print(f'{rec["id"]:6s} {rec.get("status", "-"):9s} hit={int(rec["hit"])} {rec.get("category", "")}')

    ans = [r for r in records if r["type"] == "answerable"]
    oos = [r for r in records if r["type"] == "out_of_scope"]
    answered_ans = [r for r in ans if r.get("status") == "answered"]
    answered_all = [r for r in records if r.get("status") == "answered"]
    secs = sorted(r["seconds"] for r in records)
    p95 = secs[min(len(secs) - 1, int(0.95 * len(secs)))] if secs else 0
    metrics = {
        "hit@5": pct([r["hit"] for r in ans]),
        "citation_acc": "-" if args.retrieval_only else pct([r["cited_must_page"] for r in answered_ans]),
        "correct": "-" if args.retrieval_only else pct([r.get("correct", False) for r in ans]),
        "hallucination": pct([r["hallucinated"] for r in answered_all]) if args.judge else "n/a (no judge)",
        "correct_refusal": "-" if args.retrieval_only else pct([r["status"] == "not_found" for r in oos]),
        "false_refusal": "-" if args.retrieval_only else pct([r["status"] == "not_found" for r in ans]),
        "p95_s": f"{p95:.1f}",
    }
    print("\n" + json.dumps(metrics, indent=2))
    cats = {}
    for r in records:
        if r.get("category"):
            cats[r["category"]] = cats.get(r["category"], 0) + 1
    if cats:
        print("Failures by category:", json.dumps(dict(sorted(cats.items(), key=lambda x: -x[1])), indent=2))

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    run_file = RUNS_DIR / f"{stamp}.jsonl"
    run_file.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")
    print(f"Per-question details: {run_file.relative_to(REPO)}")

    if args.no_write or args.mock:
        print("(not written to docs/results.md)")
        return
    if not RESULTS_MD.exists():
        RESULTS_MD.write_text("# Results\n\nOne row per eval run. Newest at the bottom. "
                              "Never delete rows; a change that hurts the numbers is reverted, not hidden.\n\n"
                              + HEADER, encoding="utf-8")
    row = (f"| {stamp[:10]} | {args.note} | {PROMPT_VERSION} | {len(records)} | {metrics['hit@5']} | "
           f"{metrics['citation_acc']} | {metrics['correct']} | {metrics['hallucination']} | "
           f"{metrics['correct_refusal']} | {metrics['false_refusal']} | {metrics['p95_s']} |\n")
    with open(RESULTS_MD, "a", encoding="utf-8") as f:
        f.write(row)
    print("Row added to docs/results.md")


if __name__ == "__main__":
    main()
