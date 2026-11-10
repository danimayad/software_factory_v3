#!/usr/bin/env python3
"""List the tests that were added, changed or removed since a git reference.

Purpose: tests are not frozen, so every change to them must be visible. The reviewer
of a milestone reads this list and judges whether each change was justified.

Input:  --since <git reference>  the commit, tag or branch where the milestone started.
        --paths <dir> ...        test folders (default: "test_paths" in
                                 factory-setup/parameters.json, else "tests").
Output: one line per test file: its status, the lines added and removed, and its path.
        Exit code 0 always; this script informs and does not block.
Needs:  git, run from inside the repository.
"""
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS = {"A": "added", "M": "changed", "D": "REMOVED", "T": "changed"}


def git(*args):
    result = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit("git failed: " + result.stderr.strip())
    return result.stdout


def default_paths():
    try:
        with open(os.path.join(ROOT, "factory-setup", "parameters.json")) as f:
            return json.load(f).get("test_paths") or ["tests"]
    except (OSError, ValueError):
        return ["tests"]


def main():
    parser = argparse.ArgumentParser(description="List test changes since a git reference.")
    parser.add_argument("--since", required=True, help="git reference where the milestone started")
    parser.add_argument("--paths", nargs="*", help="test folders")
    args = parser.parse_args()
    paths = args.paths or default_paths()

    # --no-renames: a renamed test shows as one removed and one added, which is what
    # the reviewer needs to see.
    names = git("diff", "--name-status", "--no-renames", args.since, "--", *paths).splitlines()
    counts = {}
    for line in git("diff", "--numstat", "--no-renames", args.since, "--", *paths).splitlines():
        added, removed, path = line.split("\t", 2)
        counts[path] = (added, removed)

    if not names:
        print("No test changes since %s in: %s" % (args.since, ", ".join(paths)))
        return
    print("Test changes since %s in: %s" % (args.since, ", ".join(paths)))
    for line in names:
        parts = line.split("\t")
        status = STATUS.get(parts[0][0], parts[0])
        path = parts[-1]
        added, removed = counts.get(path, ("?", "?"))
        print("  %-8s +%s -%s  %s" % (status, added, removed, path))
    print("Each change to an existing test needs a recorded reason "
          "(python3 scripts/measure.py event --type test_change --reason ...).")


if __name__ == "__main__":
    sys.exit(main())
