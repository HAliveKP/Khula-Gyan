---
name: guard-calibration
description: 'Calibrates guard_min_score with eval/sweep_threshold.py using verified questions only.'
---
# guard-calibration Skill

Use after a verified evaluation set exists and index is populated.

## Procedure

```bash
.\.venv\Scripts\python.exe eval\sweep_threshold.py --questions eval\questions.jsonl --use-service-filter --use-municipality-filter --fake-llm --include-unverified --note "threshold sweep"
```

Expected: prints score ranges and recommended `guard_min_score`. Currently `config.yaml` has `guard_min_score: 0.35` (uncalibrated). Without index, sweep runs on mock chunks only; results are plumbing, not calibrated.

## Rule

Only calibrate on verified (`verified=true`) questions against a real index. Mock/synthetic results from `--fake-llm` must NOT be used to change `guard_min_score` in `config.yaml`. Current state: `docs/results.md` records `guard_min_score` as uncalibrated (`-`).
