# Results and work log (Member 3)

Never delete old rows. A change that makes the numbers worse is reverted and logged, not hidden.

## Commit log

`python eval/update_log.py` adds every commit not yet listed. "Blueprint task" and "Check result"
start as `?` / `not checked` and are filled in after reviewing the commit.

| Date | Hash | Author | Message | Blueprint task | Check result |
|---|---|---|---|---|---|
| 2026-10-06 | fcb094b | Harikrishna Pokhrel | Initial commit | ? | not checked |
| 2026-10-08 | 01527a8 | Harikrishna Pokhrel | feat: scaffold Khula Gyan Day 0 setup | ? | not checked |
| 2026-10-08 | 2394b88 | Harikrishna Pokhrel | fix: preserve gitignore line endings | ? | not checked |
| 2026-10-08 | 521830d | Harikrishna Pokhrel | Merge pull request #1 from HAliveKP/Hkp | ? | not checked |
| 2026-10-09 | d2aa3fb | aash-crest01 | feat: Member 3 generation + eval starter (answer, guard, run_eval) | ? | not checked |
| 2026-10-10 | c0603ca | aash-crest01 | eval: three-section results log (commit log, task checklist, eval table) + update_log.py | ? | not checked |

## Task checklist

One block per day from blueprint section 13 (Member 3 column). Each line names its evidence:
a commit hash, file, PR link or command output.

### Day 0 — Thu-Fri Oct 8-9

- [ ] Get an LLM API key — waiting on the Leader's provider choice
- [ ] Make one successful test call — `scripts/smoke_test_llm.py` is ready; not yet run with a real key
- [x] Draft prompt v0 — `src/generation/prompt.py` (`PROMPT_VERSION = "v0"`), starter commit
- [x] Eval question format (section 9.5) — `eval/questions.jsonl` (10 drafts, `verified: false`); `python eval/check_questions.py` → OK
- [x] Extra: `answer()`, guard and eval harness — `python -m pytest -q` → 12 passed; fake-LLM run of `eval/run_eval.py --mock` completed
- [x] Branch `feature/aashish-generation` pushed; draft PR opened

### Day 1 — Sat Oct 10

- [x] Write `src/generation/answer.py` (hardcoded passages) — done early in the starter commit; tested on `tests/fixtures/sample_chunks.json`. Real-LLM check pending (playbook Day 0 Step 7)
- [x] Fix the JSON output schema — every response is validated against `docs/ask-response.schema.json` (`validate_response()`; tests `test_fixtures_match_schema`, `test_not_found_is_valid_in_every_language`)
- [ ] Write 15 eval questions together with M1 — 10 drafts so far, 0 verified

## Eval table

Only numbers produced by `eval/run_eval.py` (it adds the rows itself). `-` = not measured.
Never type or edit numbers by hand.

| Date | Change | Prompt | N | hit@5 | Citation acc. | Correct | Hallucination | Correct refusal | False refusal | p95 s |
|---|---|---|---|---|---|---|---|---|---|---|
