---
name: eval-runner
description: 'Runs eval/run_eval.py on verified questions only. Unmeasured stays "-". Mock results never reported as civic quality.'
---
# eval-runner Skill

Use when running evaluation. Only verified (`verified=true`, `verification_status=verified`) questions produce civic metrics.

## Rules (from AGENTS.md and docs/results.md)

1. `eval/run_eval.py --fake-llm` = plumbing check only. Do NOT write results to `docs/results.md` as civic metrics.
2. Real evaluation requires an indexed `chroma_db/` and verified questions with `expected` and `must_cite`.
3. Metrics that were not measured must be `-` (`hit@5`, `citation_acc`, `correct`, `false_refusal`).
4. Draft questions (`verified=false`) must be skipped unless `--include-unverified` passed for plumbing.
5. Never invent evaluation numbers. Never report mock percentages as project quality.

## Verification commands

```bash
# Plumbing check (fake LLM, synthetic fixture, NOT civic metrics):
.\.venv\Scripts\python.exe eval\run_eval.py --questions tests\fixtures\sample_questions.jsonl --fake-llm --use-service-filter --use-municipality-filter --note "plumbing check" --no-write
# Expected: 3 records; metrics printed (mock values); "(not written to docs/results.md)"

# Real questions (requires index; returns not_found when empty):
.\.venv\Scripts\python.exe eval\run_eval.py --questions eval\questions.jsonl --fake-llm --use-service-filter --use-municipality-filter --include-unverified --note "plumbing with drafts" --no-write
# Expected: 40 records; all verified palika questions show not_found (empty index); draft skipped; metrics with "-" for unmeasured.
```

## Verification checklist

- [ ] `eval/check_questions.py eval/questions.jsonl` returns `OK` (40 questions, format valid).
- [ ] Fake-LLM plumbing run writes `.pytest_tmp/eval-runs/*.jsonl` but does NOT modify `docs/results.md` evaluation table.
- [ ] No `docs/results.md` evaluation row contains mock percentages presented as civic quality.
