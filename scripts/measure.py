#!/usr/bin/env python3
"""Record and summarize the measurement of a project.

Purpose: show what the project cost and where rework came from. The raw record is what
must be complete; any indicator can be computed from it later.

Commands:
  work       add a piece of work with its four token counts
  event      add an event (gate, review, finding, test_change, question, ...)
  summary    print totals and composite measures, optionally filtered and grouped
  transcript sum the token counts found in a session record of Claude Code
             (NOT YET VERIFIED against real records; see factory-setup/reference/STATUS.md)

The log is logs/measurement.jsonl, one JSON object per line. Format: logs/FORMAT.md.
"""
import argparse
import datetime
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "measurement.jsonl")

# Weights of each kind of token, in input-token units. Anthropic API price ratios as
# known on 10 November 2026. Check them for the model in use.
WEIGHTS = {"input": 1.0, "output": 5.0, "cache_write": 1.25, "cache_read": 0.1}
TOKENS = list(WEIGHTS)
TAGS = ["project", "stage", "milestone", "feature", "role", "model", "effort", "session", "note"]
STAGES = ["understanding", "documentation", "build"]
ACTIVITIES = ["understanding", "documentation", "building", "gate_fix", "review", "rework", "other"]
EVENTS = ["gate", "review", "finding", "test_change", "question", "doc_correction",
          "cap_hit", "limit_cut", "escaped_defect"]


def weighted(entry):
    return sum(WEIGHTS[k] * (entry.get(k) or 0) for k in TOKENS)


def read_log(path=LOG):
    entries = []
    if not os.path.exists(path):
        return entries
    with open(path) as f:
        for number, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except ValueError:
                raise SystemExit("%s line %d is not valid JSON." % (path, number))
    return entries


def append(entry, path=LOG):
    entry = {k: v for k, v in entry.items() if v is not None}
    entry["ts"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry


def add_tags(parser):
    for tag in TAGS:
        if tag == "stage":
            parser.add_argument("--stage", choices=STAGES)
        else:
            parser.add_argument("--" + tag)


def yes_no(value):
    if value.lower() in ("yes", "true", "1"):
        return True
    if value.lower() in ("no", "false", "0"):
        return False
    raise argparse.ArgumentTypeError("use yes or no")


def ratio(part, whole):
    return "n/a (no data)" if not whole else "%.0f%% (%s of %s)" % (100.0 * part / whole, fmt(part), fmt(whole))


def fmt(number):
    return "{:,.0f}".format(number)


def cmd_work(args):
    entry = {"type": "work", "activity": args.activity}
    for tag in TAGS:
        entry[tag] = getattr(args, tag)
    for kind in TOKENS:
        entry[kind] = getattr(args, kind)
    append(entry, args.log)
    print("Recorded work: %s weighted tokens." % fmt(weighted(entry)))


def cmd_event(args):
    entry = {"type": args.type}
    for tag in TAGS:
        entry[tag] = getattr(args, tag)
    for field in ("result", "first_run", "round", "accepted", "scope", "kind", "reason"):
        entry[field] = getattr(args, field)
    needs = {"gate": ["result", "first_run"], "review": ["result"], "finding": ["accepted"],
             "test_change": ["reason"], "question": ["kind"]}
    missing = [f for f in needs.get(args.type, []) if entry.get(f) is None]
    if missing:
        raise SystemExit("A '%s' event needs: %s" % (args.type, ", ".join("--" + m.replace("_", "-") for m in missing)))
    append(entry, args.log)
    print("Recorded event: %s." % args.type)


def summarize(entries, group=None):
    lines = []
    work = [e for e in entries if e.get("type") == "work"]
    raw = {k: sum(e.get(k) or 0 for e in work) for k in TOKENS}
    total_raw = sum(raw.values())
    total_w = sum(weighted(e) for e in work)

    lines.append("TOKENS")
    for kind in TOKENS:
        lines.append("  %-12s %15s" % (kind, fmt(raw[kind])))
    lines.append("  %-12s %15s" % ("raw total", fmt(total_raw)))
    lines.append("  %-12s %15s  (input-token units)" % ("weighted", fmt(total_w)))

    if group:
        lines.append("")
        lines.append("WEIGHTED TOKENS BY %s" % group.upper())
        groups = {}
        for e in work:
            key = str(e.get(group) or "(not set)")
            groups[key] = groups.get(key, 0) + weighted(e)
        for key, value in sorted(groups.items(), key=lambda kv: -kv[1]):
            share = 100.0 * value / total_w if total_w else 0
            lines.append("  %-28s %15s  %3.0f%%" % (key, fmt(value), share))

    def count(entry_type, **conditions):
        return sum(1 for e in entries if e.get("type") == entry_type
                   and all(e.get(k) == v for k, v in conditions.items()))

    rework = sum(weighted(e) for e in work if e.get("activity") == "rework")
    build = sum(weighted(e) for e in work if e.get("stage") == "build")
    before = sum(weighted(e) for e in work if e.get("stage") in ("understanding", "documentation"))
    first_gates = count("gate", first_run=True)
    first_reviews = count("review", round=1)
    findings = count("finding")
    accepted = count("finding", accepted=True)
    questions = count("question")
    sessions = len({e.get("session") for e in entries if e.get("session")})

    lines.append("")
    lines.append("COMPOSITE MEASURES")
    lines.append("  Cost")
    lines.append("    Rework share (of build)       %s" % ratio(rework, build))
    lines.append("    Share before the build        %s" % ratio(before, total_w))
    lines.append("    Cache-read share (raw)        %s" % ratio(raw["cache_read"], total_raw))
    lines.append("  Quality")
    lines.append("    First-run gate rate           %s" % ratio(count("gate", first_run=True, result="pass"), first_gates))
    lines.append("    First-review approval rate    %s" % ratio(count("review", round=1, result="approved"), first_reviews))
    lines.append("    Reviewer precision            %s" % ratio(accepted, findings))
    lines.append("    Pattern share                 %s" % ratio(count("finding", accepted=True, scope="pattern"), accepted))
    lines.append("    Escaped defects               %d" % count("escaped_defect"))
    lines.append("  Definition")
    lines.append("    Documentation corrections     %d" % count("doc_correction"))
    lines.append("    Tests changed or removed      %d" % count("test_change"))
    lines.append("    Questions to Daniel           %d, product questions: %s"
                 % (questions, ratio(count("question", kind="product"), questions)))
    lines.append("  Flow")
    lines.append("    Sessions                      %d" % sessions)
    lines.append("    Review rounds                 %d" % count("review"))
    lines.append("    Cap hits                      %d" % count("cap_hit"))
    lines.append("    Cuts by the usage limit       %d" % count("limit_cut"))
    return "\n".join(lines)


def cmd_summary(args):
    entries = read_log(args.log)
    filters = {tag: getattr(args, tag) for tag in TAGS if tag != "note" and getattr(args, tag)}
    for tag, value in filters.items():
        entries = [e for e in entries if e.get(tag) == value]
    title = "MEASUREMENT SUMMARY"
    if filters:
        title += " (" + ", ".join("%s = %s" % kv for kv in sorted(filters.items())) + ")"
    print(title)
    print("%d entries" % len(entries))
    print()
    print(summarize(entries, args.by))


def cmd_transcript(args):
    """Sum the usage fields of a Claude Code session record (a .jsonl file).

    Assumption, not yet verified on a real record: each line is a JSON object, and the
    lines written for the model's replies hold message.usage with input_tokens,
    output_tokens, cache_creation_input_tokens and cache_read_input_tokens, and
    message.model. Lines without them are skipped.
    """
    names = {"input": "input_tokens", "output": "output_tokens",
             "cache_write": "cache_creation_input_tokens", "cache_read": "cache_read_input_tokens"}
    per_model, seen = {}, set()
    with open(args.path) as f:
        for line in f:
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            message = obj.get("message") if isinstance(obj, dict) else None
            usage = message.get("usage") if isinstance(message, dict) else None
            if not isinstance(usage, dict):
                continue
            ident = message.get("id")
            if ident and ident in seen:
                continue  # the same reply can be written on several lines
            seen.add(ident)
            model = message.get("model") or "(unknown model)"
            totals = per_model.setdefault(model, {k: 0 for k in TOKENS})
            for kind, name in names.items():
                totals[kind] += usage.get(name) or 0
    if not per_model:
        print("No usage fields found in %s. The record format may differ from the assumption." % args.path)
        return
    print("NOT YET VERIFIED against real records. Compare with the session's own usage screen.")
    for model, totals in per_model.items():
        print(model)
        for kind in TOKENS:
            print("  %-12s %15s" % (kind, fmt(totals[kind])))
        print("  %-12s %15s" % ("weighted", fmt(weighted(totals))))


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--log", default=LOG, help="log file (default: logs/measurement.jsonl)")
    sub = parser.add_subparsers(dest="command", required=True)

    work = sub.add_parser("work", help="add a piece of work with its token counts")
    add_tags(work)
    work.add_argument("--activity", required=True, choices=ACTIVITIES)
    for kind in TOKENS:
        work.add_argument("--" + kind.replace("_", "-"), dest=kind, type=int, default=0)
    work.set_defaults(func=cmd_work)

    event = sub.add_parser("event", help="add an event")
    add_tags(event)
    event.add_argument("--type", required=True, choices=EVENTS)
    event.add_argument("--result", choices=["pass", "fail", "approved", "changes"])
    event.add_argument("--first-run", dest="first_run", type=yes_no)
    event.add_argument("--round", type=int)
    event.add_argument("--accepted", type=yes_no)
    event.add_argument("--scope", choices=["local", "pattern"])
    event.add_argument("--kind", choices=["product", "field", "engineering"])
    event.add_argument("--reason")
    event.set_defaults(func=cmd_event)

    summary = sub.add_parser("summary", help="print totals and composite measures")
    add_tags(summary)
    summary.add_argument("--by", choices=["stage", "milestone", "feature", "role", "model", "activity", "session"],
                         help="also group weighted tokens by this tag")
    summary.set_defaults(func=cmd_summary)

    transcript = sub.add_parser("transcript", help="sum token counts in a Claude Code session record (not yet verified)")
    transcript.add_argument("path")
    transcript.set_defaults(func=cmd_transcript)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
