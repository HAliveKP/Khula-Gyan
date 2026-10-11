"""Read and write the team log docs/results.md (format set by the Leader on main):

  ## Commit log                 Date (UTC) | Hash | Author | Message | Blueprint task | Check result
  ## Day checklist and evidence Day | Owner | Status | Evidence / remaining work
  ## Evaluation results         a milestone summary table, then
  ### Eval runs (eval/run_eval.py)   one row per run, written ONLY by eval/run_eval.py

Rows are only ever added, never deleted or rewritten by these scripts.
"""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESULTS_MD = REPO / "docs" / "results.md"

COMMIT_SECTION = "Commit log"
EVAL_SECTION = "Eval runs (eval/run_eval.py)"

COMMIT_HEADER = ("| Date (UTC) | Hash | Author | Message | Blueprint task | Check result |\n"
                 "|---|---|---|---|---|---|\n")
EVAL_HEADER = ("| Date | Change | Prompt | N | hit@5 | Citation acc. | Correct | Hallucination | "
               "Correct refusal | False refusal | p95 s |\n"
               "|---|---|---|---|---|---|---|---|---|---|---|\n")
EVAL_BLOCK = (f"### {EVAL_SECTION}\n\n"
              "Rows are added only by `eval/run_eval.py`; `-` = not measured. Never type numbers by hand.\n\n"
              + EVAL_HEADER)

TEMPLATE = f"""# Project work log and results

This file keeps previous entries and reports only checks that were actually run.

## Commit log

{COMMIT_HEADER}
## Day checklist and evidence

| Day | Owner | Status | Evidence / remaining work |
|---|---|---|---|

## Evaluation results

{EVAL_BLOCK}"""


def ensure_results_md() -> str:
    """Create docs/results.md if missing, add the eval-runs block if absent; return its text."""
    if not RESULTS_MD.exists():
        RESULTS_MD.parent.mkdir(parents=True, exist_ok=True)
        RESULTS_MD.write_text(TEMPLATE, encoding="utf-8")
    text = RESULTS_MD.read_text(encoding="utf-8")
    if f"### {EVAL_SECTION}" not in text:
        text = text.rstrip("\n") + "\n\n" + EVAL_BLOCK
        RESULTS_MD.write_text(text, encoding="utf-8")
    return text


def _section_bounds(lines: list[str], title: str) -> tuple[int, int]:
    """Find a '## title' or '### title' heading; the section ends at the next heading of the same or higher level."""
    for i, ln in enumerate(lines):
        m = re.match(r"^(#{2,3}) (.*)$", ln.strip())
        if m and m.group(2).strip() == title:
            level = len(m.group(1))
            end = next((j for j in range(i + 1, len(lines))
                        if re.match(r"^#{1,%d} " % level, lines[j])), len(lines))
            return i, end
    raise ValueError(f'docs/results.md has no "{title}" section')


def _table_span(lines: list[str], start: int, end: int) -> tuple[int, int] | None:
    """(first, last) line of the section's table. Blank lines between row groups
    belong to the table (the team log has them); any other text ends it."""
    first = next((i for i in range(start + 1, end) if lines[i].startswith("|")), None)
    if first is None:
        return None
    last = first
    for i in range(first + 1, end):
        if lines[i].startswith("|"):
            last = i
        elif lines[i].strip():
            break
    return first, last


def table_rows(title: str) -> list[list[str]]:
    """Return the data rows (cells) of the section's table, across blank-line gaps."""
    lines = ensure_results_md().splitlines()
    span = _table_span(lines, *_section_bounds(lines, title))
    if span is None:
        return []
    table = [ln for ln in lines[span[0]:span[1] + 1] if ln.startswith("|")]
    return [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in table[2:]]


def add_rows(title: str, rows: list[str]) -> None:
    """Append rows after the last row of the section's table."""
    if not rows:
        return
    lines = ensure_results_md().splitlines()
    span = _table_span(lines, *_section_bounds(lines, title))
    if span is None:
        raise ValueError(f'"{title}" in docs/results.md has no table header')
    last = span[1]
    lines[last + 1:last + 1] = [r.rstrip("\n") for r in rows]
    RESULTS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cell(text: str) -> str:
    """Make text safe for a markdown table cell."""
    return " ".join(str(text).replace("|", "\\|").split())


def bare_hash(text: str) -> str:
    """'`fcb094b9d0...`' -> 'fcb094b9d0...' so short and full hashes can be compared."""
    return text.strip().strip("`").lower()


def hash_listed(full_hash: str, listed: set[str]) -> bool:
    return any(h and (full_hash.startswith(h) or h.startswith(full_hash)) for h in listed)
