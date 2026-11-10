# What has been tested

Date of this status: 10 November 2026. Update it when something is tested or changes.

| Part | Status |
|---|---|
| `scripts/measure.py` (work, event, summary) | Run on sample data in a Linux cloud workspace; totals and composite measures checked by hand |
| `scripts/measure.py transcript` | Run on made-up records only. The real record format of Claude Code is assumed, not verified |
| `scripts/params.py` | Run on sample data in a Linux cloud workspace |
| `scripts/test_changes.py` | Run in a temporary git repository in a Linux cloud workspace |
| `scripts/check.sh` | Placeholder; fails on purpose until the foundation fills it in |
| Example hooks for Claude Code | Run with made-up input. Not run inside Claude Code |
| Example helper definitions for Claude Code | Format checked against the documentation. Not run |
| `settings.example.json` | Valid JSON. Permission and sandbox patterns come from the first factory. Not run in this form |
| `CLAUDE.md` importing `AGENTS.md` | The documented way. Not run in a session yet |
| `ci.example.yml` | Not run on GitHub |
| All scripts on the Mac | Not run on the Mac yet |
| Weights of the token formula | From memory of Anthropic's API prices. Not checked against the price page |
| Other coding agents | No reference yet. Added the first time another agent is used |
