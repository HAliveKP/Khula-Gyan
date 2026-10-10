"""Checks the team log format: rows land in the right section, nothing is deleted,
and short/full hashes are recognised as the same commit."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "eval"))
import results_log  # noqa: E402

LEADER_STYLE = """# Project work log and results

## Commit log

| Date (UTC) | Hash | Author | Message | Blueprint task | Check result |
|---|---|---|---|---|---|
| 2026-10-06 | `fcb094b9d06c024d39f0058cf83e67691f072663` | H | Initial commit | Repository baseline | ok |

## Day checklist and evidence

| Day | Owner | Status | Evidence / remaining work |
|---|---|---|---|
| Day 0 | Member 3 | Partial | drafts |

## Evaluation results

| Run / build | Date | Questions | hit@5 | Citation accuracy | Answer correctness | Refusal rate | Notes |
|---|---|---:|---:|---:|---:|---:|---|
| Day 0-2 baseline | - | - | - | - | - | - | none yet |
"""


def setup(tmp_path, monkeypatch, text=None):
    md = tmp_path / "results.md"
    if text:
        md.write_text(text, encoding="utf-8")
    monkeypatch.setattr(results_log, "RESULTS_MD", md)
    return md


def test_eval_runs_block_added_under_leader_table(tmp_path, monkeypatch):
    md = setup(tmp_path, monkeypatch, LEADER_STYLE)
    results_log.add_rows(results_log.EVAL_SECTION, ["| 2026-10-12 | baseline | v0 | 25 | 60% | - | - | - | - | - | 4.0 |"])
    text = md.read_text(encoding="utf-8")
    assert "| Day 0-2 baseline |" in text  # Leader's summary row untouched
    assert text.index("Day 0-2 baseline") < text.index("### Eval runs") < text.index("| baseline |")
    assert [r[1] for r in results_log.table_rows(results_log.EVAL_SECTION)] == ["baseline"]


def test_commit_rows_append_to_commit_log_only(tmp_path, monkeypatch):
    md = setup(tmp_path, monkeypatch, LEADER_STYLE)
    results_log.add_rows("Commit log", ["| 2026-10-10 | `abc1234` | A | feat: x | ? | not checked |"])
    rows = results_log.table_rows("Commit log")
    assert [results_log.bare_hash(r[1])[:7] for r in rows] == ["fcb094b", "abc1234"]
    text = md.read_text(encoding="utf-8")
    assert text.index("abc1234") < text.index("## Day checklist")


def test_short_and_full_hash_match():
    listed = {results_log.bare_hash("`fcb094b9d06c024d39f0058cf83e67691f072663`"), "d2aa3fb"}
    assert results_log.hash_listed("fcb094b9d06c024d39f0058cf83e67691f072663", listed)
    assert results_log.hash_listed("d2aa3fb1234567890abcdef1234567890abcdef1", listed)
    assert not results_log.hash_listed("1234567890abcdef1234567890abcdef12345678", listed)


def test_template_when_file_missing(tmp_path, monkeypatch):
    setup(tmp_path, monkeypatch)
    results_log.ensure_results_md()
    assert results_log.table_rows("Commit log") == []
    assert results_log.table_rows(results_log.EVAL_SECTION) == []


def test_cell_escapes_pipes():
    assert results_log.cell("a | b\nc") == "a \\| b c"
