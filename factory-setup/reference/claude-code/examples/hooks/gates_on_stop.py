#!/usr/bin/env python3
"""Keep the session working until the quality gates pass. Example of a Claude Code
Stop hook.

Purpose: the agent stops when the work looks done. This hook runs scripts/check.sh
when it tries to stop and sends it back to work while the gates fail.

Input:  the hook's JSON on standard input (fields used: cwd, session_id) and the
        environment variable CLAUDE_PROJECT_DIR.
Output: exit 0 to let the session stop. Exit 2 to keep it working; the message on
        standard error is shown to the agent.
Limits: at most MAX_BLOCKS times per session; after that it lets the session stop, so
        a session can never be held forever. If the file .factory/stop-reason exists
        (the agent writes there a real question or blocker), the session may stop.
"""
import json
import os
import subprocess
import sys
import tempfile

MAX_BLOCKS = 3
TIMEOUT_SECONDS = 1500


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        data = {}
    project = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    if os.path.exists(os.path.join(project, ".factory", "stop-reason")):
        sys.exit(0)
    check = os.path.join(project, "scripts", "check.sh")
    if not os.path.exists(check):
        sys.exit(0)

    counter = os.path.join(tempfile.gettempdir(), "factory-gates-%s" % (data.get("session_id") or "session"))
    try:
        with open(counter) as f:
            attempts = int(f.read() or 0)
    except (OSError, ValueError):
        attempts = 0

    try:
        result = subprocess.run(["bash", check], cwd=project, capture_output=True, text=True,
                                timeout=TIMEOUT_SECONDS)
        passed, output = result.returncode == 0, (result.stdout + result.stderr)
    except subprocess.TimeoutExpired:
        passed, output = False, "The quality gates did not finish in %d seconds." % TIMEOUT_SECONDS

    if passed:
        if os.path.exists(counter):
            os.remove(counter)
        sys.exit(0)
    attempts += 1
    with open(counter, "w") as f:
        f.write(str(attempts))
    if attempts > MAX_BLOCKS:
        sys.exit(0)
    tail = "\n".join(output.strip().splitlines()[-20:])
    print("The quality gates still fail (block %d of %d). Keep working. If you have a real "
          "question or blocker, write it to .factory/stop-reason and stop.\n%s"
          % (attempts, MAX_BLOCKS, tail), file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
