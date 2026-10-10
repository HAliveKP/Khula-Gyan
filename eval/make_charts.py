"""Draw baseline-vs-final bars from docs/results.md -> docs/results.png (Day 13).

Usage:  python eval/make_charts.py            # first row vs last row
        python eval/make_charts.py 1 5        # row 1 vs row 5 (1 = first data row)
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
METRICS = ["hit@5", "Citation acc.", "Correct", "Hallucination", "Correct refusal", "False refusal"]


def read_rows() -> tuple[list[str], list[list[str]]]:
    """Header and rows of the "Eval runs (eval/run_eval.py)" table only."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from results_log import EVAL_HEADER, EVAL_SECTION, table_rows
    header = [c.strip() for c in EVAL_HEADER.splitlines()[0].strip("|").split("|")]
    rows = table_rows(EVAL_SECTION)
    if not rows:
        sys.exit("The eval runs table has no rows yet. Run eval/run_eval.py first.")
    return header, rows


def to_num(cell: str) -> float:
    """'85%' -> 85.0; '-' (not measured) -> nan, which draws no bar."""
    return float(cell.rstrip("%")) if cell.rstrip("%").replace(".", "").isdigit() else float("nan")


def main() -> None:
    header, rows = read_rows()
    a = int(sys.argv[1]) - 1 if len(sys.argv) > 2 else 0
    b = int(sys.argv[2]) - 1 if len(sys.argv) > 2 else len(rows) - 1
    idx = [header.index(m) for m in METRICS]
    base, final = [to_num(rows[a][i]) for i in idx], [to_num(rows[b][i]) for i in idx]

    x = range(len(METRICS))
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar([i - 0.2 for i in x], base, width=0.4, label=f"Baseline ({rows[a][0]})", color="#9aa5b1")
    ax.bar([i + 0.2 for i in x], final, width=0.4, label=f"Final ({rows[b][0]})", color="#1f6feb")
    for i, (v0, v1) in enumerate(zip(base, final)):
        ax.text(i - 0.2, (0 if v0 != v0 else v0) + 1, "-" if v0 != v0 else f"{v0:.0f}", ha="center", fontsize=8)
        ax.text(i + 0.2, (0 if v1 != v1 else v1) + 1, "-" if v1 != v1 else f"{v1:.0f}", ha="center", fontsize=8)
    ax.set_xticks(list(x), METRICS, fontsize=9)
    ax.set_ylabel("%")
    ax.set_ylim(0, 105)
    ax.set_title("Khula Gyan: baseline vs final (lower is better for hallucination and false refusal)")
    ax.legend()
    fig.tight_layout()
    out = REPO / "docs" / "results.png"
    fig.savefig(out, dpi=150)
    print(f"Saved {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
