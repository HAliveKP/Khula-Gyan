"""Add every commit not yet in the "Commit log" of docs/results.md, in the team format
(UTC date, full hash in backticks, no merge commits).

Usage:
    python eval/update_log.py            # commits on your current branch
    python eval/update_log.py --all      # commits on every branch you have locally

New rows get Blueprint task "?" and Check result "not checked". Fill those in after
reviewing each commit (`git show --stat <hash>`) and running the tests.
Existing rows are never changed or deleted.
"""

import argparse
import os
import subprocess
import sys

from results_log import COMMIT_SECTION, add_rows, bare_hash, cell, ensure_results_md, hash_listed, table_rows


def git_commits(all_branches: bool) -> list[tuple[str, str, str, str]]:
    cmd = ["git", "log", "--reverse", "--no-merges", "--date=format-local:%Y-%m-%d",
           "--format=%ad%x1f%H%x1f%an%x1f%s"]
    if all_branches:
        cmd.append("--all")
    env = dict(os.environ, TZ="UTC")
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=env)
    if out.returncode != 0:
        sys.exit("git log failed: " + out.stderr.strip())
    return [tuple(line.split("\x1f")) for line in out.stdout.splitlines() if line.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="include commits from all local branches")
    args = ap.parse_args()

    ensure_results_md()
    listed = {bare_hash(row[1]) for row in table_rows(COMMIT_SECTION) if len(row) > 1}
    new = [c for c in git_commits(args.all) if not hash_listed(c[1], listed)]
    rows = [f"| {d} | `{h}` | {cell(a)} | {cell(m)} | ? | not checked |" for d, h, a, m in new]
    add_rows(COMMIT_SECTION, rows)
    print(f"{len(rows)} commit(s) added to docs/results.md" + (":" if rows else "."))
    for d, h, a, m in new:
        print(f"  {h[:7]} {a}: {m}")


if __name__ == "__main__":
    main()
