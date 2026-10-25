## What and why

<!-- Short summary of the change and the reason. Link the issue: "Closes #123". -->

## How it was checked

<!-- Commands you ran and their real output (e.g. "python -m pytest -q -> N passed"). -->

## Checklist

See [CONTRIBUTING.md](https://github.com/HAliveKP/Khula-Gyan/blob/main/CONTRIBUTING.md#pull-request-checklist).

- [ ] Branch is `feature/…`, `fix/…` or `docs/…` from `main`; this PR targets `main`.
- [ ] Commit messages follow Conventional Commits (`feat:`, `fix:`, `docs:`, ...).
- [ ] `python -m pytest -q` passes.
- [ ] No `.env`, API keys or other secrets in the diff, commits or screenshots.
- [ ] No source documents or generated data (`data/raw/`, `data/processed/`, `data/readable/`, `chroma_db/`, `artifacts/`, `eval/runs/`).
- [ ] `docs/results.md`: only rows added, none edited or deleted. Eval numbers come only from `eval/run_eval.py` (`-` if not measured).
- [ ] New or changed expected answers in `eval/questions.jsonl` were checked by a human on the real page. `python eval/check_questions.py` says `OK`.
- [ ] Nepali text comparisons use NFC normalization.
- [ ] Response contract unchanged, or `docs/ask-response.schema.json` + `docs/response-contract.md` updated.
- [ ] README/docs updated, and they describe only behaviour that was actually checked.
