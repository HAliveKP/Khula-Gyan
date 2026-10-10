"""Checks that rows land in the right section of docs/results.md and nothing is deleted."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "eval"))
import results_log  # noqa: E402


def test_rows_go_to_their_own_section(tmp_path, monkeypatch):
    md = tmp_path / "results.md"
    monkeypatch.setattr(results_log, "RESULTS_MD", md)
    results_log.ensure_results_md()
    results_log.add_rows("Commit log", ["| 2026-10-09 | abc1234 | A | feat: x | Day 0 | pass |"])
    results_log.add_rows("Eval table", ["| 2026-10-12 | baseline | v0 | 25 | 60% | - | - | - | - | - | 4.0 |"])
    results_log.add_rows("Commit log", ["| 2026-10-10 | def5678 | A | eval: y | ? | not checked |"])
    assert [r[1] for r in results_log.table_rows("Commit log")] == ["abc1234", "def5678"]
    assert [r[1] for r in results_log.table_rows("Eval table")] == ["baseline"]
    text = md.read_text(encoding="utf-8")
    assert text.index("def5678") < text.index("## Task checklist") < text.index("baseline")


def test_cell_escapes_pipes():
    assert results_log.cell("a | b\nc") == "a \\| b c"
