# Results and work log (Member 3)

Never delete old rows. A change that makes the numbers worse is reverted and logged, not hidden.

## Commit log

`python eval/update_log.py` adds every commit not yet listed. "Blueprint task" and "Check result"
start as `?` / `not checked` and are filled in after reviewing the commit.

| Date | Hash | Author | Message | Blueprint task | Check result |
|---|---|---|---|---|---|
| 2026-10-06 | fcb094b | Harikrishna Pokhrel | Initial commit | Day 0 Leader: create repo | pass: README + LICENSE present |
| 2026-10-08 | 01527a8 | Harikrishna Pokhrel | feat: scaffold Khula Gyan Day 0 setup | Day 0 Leader: repo setup (README, .env.example, config.yaml, folders) | pass: files present |
| 2026-10-08 | 2394b88 | Harikrishna Pokhrel | fix: preserve gitignore line endings | Day 0 Leader: repo setup | pass: .gitignore covers .env, data/, chroma_db/ |
| 2026-10-08 | 521830d | Harikrishna Pokhrel | Merge pull request #1 from HAliveKP/Hkp | Day 0 Leader: merge setup into main | pass |
| 2026-10-09 | d2aa3fb | aash-crest01 | feat: Member 3 generation + eval starter (answer, guard, run_eval) | Day 0–1 M3: prompt v0, eval format, answer.py, schema validation | pass: 12 tests passed |
| 2026-10-10 | c0603ca | aash-crest01 | eval: three-section results log (commit log, task checklist, eval table) + update_log.py | Day 1 M3: results log (Leader's LOG request) | pass: 14 tests passed |
| 2026-10-10 | 27318a3 | aash-crest01 | docs: fill commit log | Day 1 M3: results log (Leader's LOG request) | pass: commit log filled by update_log.py |
| 2026-10-10 | f71b696 | aash-crest01 | docs: check commit log rows | Day 1 M3: results log | pass: 6 rows reviewed and filled |
| 2026-10-10 | 6d5702a | aash-crest01 | feat: OpenRouter key pool (round robin + failover across several API keys) | Day 0 M3: LLM API key + test call (OpenRouter, key loop) | pass: 21 tests passed; smoke test passed |
| 2026-10-10 | 5455e2f | aash-crest01 | feat: scripts/try_answer.py to test answer() with Nepali questions from a UTF-8 file | Day 0 M3: real-AI test of answer() | pass: try_answer.py, 4/4 questions behave correctly |

## Task checklist

One block per day from blueprint section 13 (Member 3 column). Each line names its evidence:
a commit hash, file, PR link or command output.

### Day 0 — Thu-Fri Oct 8-9

- [x] Get an LLM API key — OpenRouter key created Oct 10 (Leader chose OpenRouter); stored only in .env
- [x] Make one successful test call — `python scripts/smoke_test_llm.py` passed with nvidia/nemotron-3-super-120b-a12b:free (Nepali 5.0 s, English 0.9 s); gemma-4-31b-it:free was rate-limited upstream; commit 6d5702a
- [x] Draft prompt v0 — `src/generation/prompt.py` (`PROMPT_VERSION = "v0"`), commit d2aa3fb
- [x] Eval question format (section 9.5) — `eval/questions.jsonl` (10 drafts, `verified: false`); `python eval/check_questions.py` → OK; commit d2aa3fb
- [x] Extra: `answer()`, guard and eval harness — `python -m pytest -q` → 12 passed; fake-LLM run of `eval/run_eval.py --mock` completed; commit d2aa3fb
- [x] Branch `feature/aashish-generation` pushed; draft PR opened

### Day 1 — Sat Oct 10

- [x] Write `src/generation/answer.py` (hardcoded passages) — done early, commit d2aa3fb; tested on `tests/fixtures/sample_chunks.json` with the real AI (see next lines)
- [x] Fix the JSON output schema — every response is validated against `docs/ask-response.schema.json` (`validate_response()`; tests `test_fixtures_match_schema`, `test_not_found_is_valid_in_every_language`); commit d2aa3fb
- [x] Extra: results log set up as the Leader asked (commit log, task checklist, eval table) — commit c0603ca; `python -m pytest -q` → 14 passed
- [x] Extra: real-AI test of `answer()` — `python scripts/try_answer.py` (commit 5455e2f): English, Nepali and Romanized questions answered with grounded citations; cricket question refused. Nepali has Hindi words and spelling slips (to fix in prompt v1, Day 4)
- [ ] Write 15 eval questions together with M1 — 10 drafts so far, 0 verified

## Eval table

Only numbers produced by `eval/run_eval.py` (it adds the rows itself). `-` = not measured.
Never type or edit numbers by hand.

| Date | Change | Prompt | N | hit@5 | Citation acc. | Correct | Hallucination | Correct refusal | False refusal | p95 s |
|---|---|---|---|---|---|---|---|---|---|---|