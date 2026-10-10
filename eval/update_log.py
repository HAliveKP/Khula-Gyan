"""Add every commit not yet in the "Commit log" of docs/results.md.

Usage:
    python eval/update_log.py            # commits on your current branch
    python eval/update_log.py --all      # commits on every branch you have locally

New rows get Blueprint task "?" and Check result "not checked". Fill those in after
reviewing each commit (`git show <hash> --stat`) and running the tests.
Existing rows are never changed or deleted.
"""

import argparse
import subprocess
import sys

from results_log import add_rows, cell, ensure_results_md, table_rows


def git_commits(all_branches: bool) -> list[tuple[str, str, str, str]]:
    cmd = ["git", "log", "--reverse", "--date=short", "--format=%ad%x1f%h%x1f%an%x1f%s"]
    if all_branches:
        cmd.append("--all")
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        sys.exit("git log failed: " + out.stderr.strip())
    return [tuple(line.split("\x1f")) for line in out.stdout.splitlines() if line.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="include commits from all local branches")
    args = ap.parse_args()

    ensure_results_md()
    listed = {row[1] for row in table_rows("Commit log") if len(row) > 1}
    new = [c for c in git_commits(args.all) if c[1] not in listed]
    rows = [f"| {d} | {h} | {cell(a)} | {cell(m)} | ? | not checked |" for d, h, a, m in new]
    add_rows("Commit log", rows)
    print(f"{len(rows)} commit(s) added to docs/results.md" + (":" if rows else "."))
    for d, h, a, m in new:
        print(f"  {h} {m}")


if __name__ == "__main__":
    main()
