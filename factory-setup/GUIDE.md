# Factory setup: guide

This folder holds how the factory is configured for this project: which helpers it
uses, with which models and tools, and what the agent is allowed to do. It is decided
after the documentation is written and before the build starts. Daniel approves it
together with the build plan.

## What is here

- `parameters.json`: the values of this project's loop.
- `helper-template.md`: the variables that describe any helper.
- `reference/`: tested examples for each coding agent, to copy and adjust. They are
  not active. `reference/STATUS.md` says what was tested and when.

The project adds here, when it needs them: a short description of each helper it
uses, and notes on the settings chosen and why.

## parameters.json

It has a `defaults` block and a `milestones` block. A milestone lists only what
differs from the defaults. `python3 scripts/params.py <milestone>` prints the
configuration that applies. A value set for a milestone replaces the default; objects
are merged key by key; lists and simple values are replaced whole.

| Field | Meaning |
|---|---|
| `project` | Name of the project, used as a tag in the measurement log |
| `test_paths` | Folders that hold tests, for `scripts/test_changes.py` |
| `writer.model`, `writer.effort` | Model and effort level of the lead session that writes the code |
| `review.reviewers` | Names of the helpers that review at the end of a milestone. An empty list means the quality gates alone |
| `review.max_rounds` | Cap on correction rounds after a review. Past it the lead stops and reports |
| `helpers` | Names of other helpers the milestone uses |
| `protected_paths` | Files or folders nobody may change during the build (for example tests the project decides to protect). Empty by default |
| `caps.max_turns`, `caps.max_spend_usd` | Limits for an unattended run, when the agent supports them |
| `settings` | Permissions, sandbox and hooks that differ from the project's base settings, described in the agent's own terms |

The milestone names, the helper names and every value are this project's own. The
build plan gives the reason for each difference between a milestone and the defaults.

## Change of configuration between milestones

A milestone whose configuration differs starts in a new session. The build plan marks
those points, and the lead reminds Daniel when one is reached. The settings a milestone
runs with are the ones approved in the build plan. An agent does not widen its own
permissions during the build.
