#!/usr/bin/env python3
"""Print the configuration that applies to one milestone.

Purpose: factory-setup/parameters.json holds a default block and, per milestone, only
what differs. This script merges the two, so nobody has to do it by reading.

Input:  the milestone name (optional). Without it, prints the defaults.
Output: the effective configuration as JSON on standard output.
Rule:   a value set for the milestone replaces the default. Objects are merged key by
        key; lists and simple values are replaced whole.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "factory-setup", "parameters.json")


def merge(base, over):
    out = dict(base)
    for key, value in over.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = merge(out[key], value)
        else:
            out[key] = value
    return out


def effective(params, milestone=None):
    config = dict(params.get("defaults", {}))
    if milestone is not None:
        milestones = params.get("milestones", {})
        if milestone not in milestones:
            names = ", ".join(sorted(milestones)) or "none defined"
            raise SystemExit("Milestone '%s' is not in parameters.json (defined: %s). "
                             "Use the defaults or add it." % (milestone, names))
        config = merge(config, milestones[milestone])
    return config


def main():
    with open(PATH) as f:
        params = json.load(f)
    milestone = sys.argv[1] if len(sys.argv) > 1 else None
    print(json.dumps(effective(params, milestone), indent=2))


if __name__ == "__main__":
    main()
