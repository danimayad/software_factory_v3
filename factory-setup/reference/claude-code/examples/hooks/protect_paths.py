#!/usr/bin/env python3
"""Protect chosen paths against any edit. Example of a Claude Code PreToolUse hook on
Edit, Write and NotebookEdit.

Purpose: a project that decides to protect some files (for example a set of tests)
lists them in "protected_paths" in factory-setup/parameters.json. This hook then
blocks every edit to them, by the lead and by helpers alike. To change a protected
file, Daniel removes it from the list first.

Input:  the hook's JSON on standard input (fields used: cwd, tool_input.file_path or
        tool_input.notebook_path) and the environment variable CLAUDE_PROJECT_DIR.
Output: exit 0 to allow. Exit 2 to block; the message on standard error is shown to
        the agent.
If factory-setup/current-milestone exists and names a milestone, that milestone's
protected paths apply; otherwise the defaults do.
"""
import json
import os
import sys


def project_dir(data):
    return os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()


def protected_paths(project):
    try:
        with open(os.path.join(project, "factory-setup", "parameters.json")) as f:
            params = json.load(f)
    except (OSError, ValueError):
        return []
    paths = (params.get("defaults") or {}).get("protected_paths") or []
    try:
        with open(os.path.join(project, "factory-setup", "current-milestone")) as f:
            milestone = f.read().strip()
        override = (params.get("milestones") or {}).get(milestone) or {}
        if "protected_paths" in override:
            paths = override["protected_paths"] or []
    except OSError:
        pass
    return [p.strip("/") for p in paths if p and p.strip("/")]


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        sys.exit(0)
    tool_input = data.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not path:
        sys.exit(0)
    project = os.path.realpath(project_dir(data))
    if not os.path.isabs(path):
        path = os.path.join(data.get("cwd") or project, path)
    path = os.path.realpath(path)
    if not (path + os.sep).startswith(project + os.sep):
        sys.exit(0)  # outside the project: not this hook's business
    rel = os.path.relpath(path, project).replace(os.sep, "/")
    for protected in protected_paths(project):
        if rel == protected or rel.startswith(protected + "/"):
            print("Blocked: %s is protected in factory-setup/parameters.json and is not changed "
                  "during the build. If it looks wrong, stop and report it as a question for "
                  "Daniel." % rel, file=sys.stderr)
            sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
