import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "eval"))

from check_questions import check  # noqa: E402
import run_eval  # noqa: E402


def question(**changes):
    """A valid draft question; tests change only the fields they care about."""
    q = {"id": "x1", "q": "Synthetic question?", "lang": "en", "service": "driving_license",
         "type": "answerable", "expected": ["TODO"], "must_cite": None, "verified": False,
         "verification_status": "draft"}
    q.update(changes)
    return q


def write_jsonl(path, rows):
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return path


def run_check(tmp_path, capsys, rows):
    code = check(write_jsonl(tmp_path / "q.jsonl", rows))
    return code, capsys.readouterr().out


VERIFIED = dict(expected=["synthetic fact"], must_cite={"source": "mock.pdf", "page": 2},
                verified=True, verification_status="verified")


def test_draft_with_todo_passes(tmp_path, capsys):
    code, out = run_check(tmp_path, capsys, [question()])
    assert code == 0
    assert out.strip().endswith("OK")
    assert "verification_status draft=1" in out


def test_verified_question_passes(tmp_path, capsys):
    code, out = run_check(tmp_path, capsys, [question(**VERIFIED)])
    assert code == 0, out


def test_verified_with_todo_is_a_problem(tmp_path, capsys):
    code, out = run_check(tmp_path, capsys, [question(**dict(VERIFIED, expected=["fact", "todo later"]))])
    assert code == 1
    assert "still has 'TODO'" in out


def test_verified_out_of_scope_with_todo_is_a_problem(tmp_path, capsys):
    q = question(**dict(VERIFIED, type="out_of_scope", service="other", expected=["TODO"], must_cite=None))
    code, out = run_check(tmp_path, capsys, [q])
    assert code == 1
    assert "still has 'TODO'" in out


def test_verified_with_empty_expected_is_a_problem(tmp_path, capsys):
    code, out = run_check(tmp_path, capsys, [question(**dict(VERIFIED, expected=[]))])
    assert code == 1
    assert "needs 'expected' facts" in out


def test_verified_but_status_draft_is_a_problem(tmp_path, capsys):
    code, out = run_check(tmp_path, capsys, [question(**dict(VERIFIED, verification_status="draft"))])
    assert code == 1
    assert "would skip it" in out


def test_unverified_but_status_not_draft_is_a_problem(tmp_path, capsys):
    code, out = run_check(tmp_path, capsys, [question(verification_status="verified")])
    assert code == 1
    assert "verified is false" in out


def test_missing_status_is_allowed(tmp_path, capsys):
    q = question()
    del q["verification_status"]
    code, out = run_check(tmp_path, capsys, [q])
    assert code == 0, out


def test_mock_defaults_to_sample_questions():
    assert run_eval.pick_questions_file(None, mock=True) == run_eval.MOCK_QUESTIONS
    assert run_eval.pick_questions_file(None, mock=False) == run_eval.REAL_QUESTIONS
    assert run_eval.pick_questions_file("mine.jsonl", mock=True) == Path("mine.jsonl")
    assert run_eval.load_questions(run_eval.MOCK_QUESTIONS, include_unverified=True)


def test_only_drafts_gives_clear_message(tmp_path):
    path = write_jsonl(tmp_path / "drafts.jsonl", [question(id="d1"), question(id="d2")])
    result = subprocess.run(
        [sys.executable, str(ROOT / "eval" / "run_eval.py"), "--questions", str(path),
         "--runs-dir", str(tmp_path / "runs"), "--mock", "--fake-llm", "--note", "pytest drafts only"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 1
    assert "2 skipped as drafts" in result.stderr
    assert "--mock" in result.stderr
    assert not (tmp_path / "runs").exists()


def _run_main_with_answer(monkeypatch, tmp_path, fake_answer):
    monkeypatch.setattr(run_eval, "answer_with_trace", fake_answer)
    monkeypatch.setattr(sys, "argv", ["run_eval.py", "--mock", "--fake-llm", "--no-write",
                                      "--runs-dir", str(tmp_path / "runs"), "--note", "pytest llm errors"])
    run_eval.main()


def test_eval_records_a_failed_llm_call_and_continues(monkeypatch, tmp_path, capsys):
    real_answer = run_eval.answer_with_trace
    calls = []

    def flaky_answer(query, chunks):
        calls.append(query)
        if len(calls) == 1:
            raise RuntimeError("LLM call failed on all 1 key(s)")
        return real_answer(query, chunks)

    _run_main_with_answer(monkeypatch, tmp_path, flaky_answer)
    err = capsys.readouterr().err
    assert len(calls) == 3  # every sample question was still asked
    assert "1 LLM call(s) failed" in err


def test_eval_stops_when_the_llm_provider_is_down(monkeypatch, tmp_path):
    def down(query, chunks):
        raise RuntimeError("LLM call failed on all 1 key(s)")

    with pytest.raises(SystemExit) as stop:
        _run_main_with_answer(monkeypatch, tmp_path, down)
    assert stop.value.code == 3


def test_failed_llm_call_has_its_own_category():
    assert run_eval.categorize({"type": "answerable"}, {"status": "error", "hit": True}) == "llm_error"
