"""Read and write docs/results.md, which has three sections:

  ## Commit log      date | hash | author | message | blueprint task | check result
  ## Task checklist  one "### Day N" block per day, each task with its evidence
  ## Eval table      one row per eval run, written ONLY by eval/run_eval.py

Rows are only ever added, never deleted or rewritten by these scripts.
"""

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESULTS_MD = REPO / "docs" / "results.md"

COMMIT_HEADER = ("| Date | Hash | Author | Message | Blueprint task | Check result |\n"
                 "|---|---|---|---|---|---|\n")
EVAL_HEADER = ("| Date | Change | Prompt | N | hit@5 | Citation acc. | Correct | Hallucination | "
               "Correct refusal | False refusal | p95 s |\n"
               "|---|---|---|---|---|---|---|---|---|---|---|\n")

TEMPLATE = f"""# Results and work log (Member 3)

Never delete old rows. A change that makes the numbers worse is reverted and logged, not hidden.

## Commit log

`python eval/update_log.py` adds every commit not yet listed. "Blueprint task" and "Check result"
start as `?` / `not checked` and are filled in after reviewing the commit.

{COMMIT_HEADER}
## Task checklist

One block per day from blueprint section 13 (Member 3 column). Each line names its evidence:
a commit hash, file, PR link or command output.

## Eval table

Only numbers produced by `eval/run_eval.py` (it adds the rows itself). `-` = not measured.
Never type or edit numbers by hand.

{EVAL_HEADER}"""


def ensure_results_md() -> str:
    """Create docs/results.md from the template if missing; return its text."""
    if not RESULTS_MD.exists():
        RESULTS_MD.parent.mkdir(parents=True, exist_ok=True)
        RESULTS_MD.write_text(TEMPLATE, encoding="utf-8")
    return RESULTS_MD.read_text(encoding="utf-8")


def _section_bounds(lines: list[str], title: str) -> tuple[int, int]:
    start = next((i for i, ln in enumerate(lines) if ln.strip() == f"## {title}"), None)
    if start is None:
        raise ValueError(f'docs/results.md has no "## {title}" section')
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start, end


def table_rows(title: str) -> list[list[str]]:
    """Return the data rows (cells) of the first table in a section."""
    lines = ensure_results_md().splitlines()
    start, end = _section_bounds(lines, title)
    table = [ln for ln in lines[start:end] if ln.startswith("|")]
    return [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in table[2:]]


def add_rows(title: str, rows: list[str]) -> None:
    """Append rows at the end of the section's table (after its last '|' line)."""
    if not rows:
        return
    lines = ensure_results_md().splitlines()
    start, end = _section_bounds(lines, title)
    last = max((i for i in range(start, end) if lines[i].startswith("|")), default=None)
    if last is None:
        raise ValueError(f'"## {title}" in docs/results.md has no table header')
    lines[last + 1:last + 1] = [r.rstrip("\n") for r in rows]
    RESULTS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cell(text: str) -> str:
    """Make text safe for a markdown table cell."""
    return " ".join(str(text).replace("|", "\\|").split())
