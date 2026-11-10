# Build method

This is the common method of every build. Each project sets its own values in
`factory-setup/parameters.json` and gives its reasons in the build plan.

## The loop, per milestone

1. The lead session reads the product brief, the way of working, the documentation it
   needs and the logs.
2. It builds the milestone's features.
3. It runs the quality gates (`bash scripts/check.sh`) and fixes until they pass.
4. A fresh reviewer, which has not seen how the code was written, checks the result
   against the requirements. It looks at correctness, not style. It also reads the
   list of tests changed in the milestone.
5. The lead sorts the findings and fixes the real problems, then returns to step 3.
   The number of rounds has a cap. Past it, the lead stops and reports.
6. It records progress, decisions and measurement in `logs/`, and merges the work.
7. The next milestone starts. It starts in a new session when the conversation has
   grown long or when the milestone's configuration is different.

The first milestone is the foundation: the shared modules, the quality gates and CI.

Every loop states four things: its done condition, the check that proves it, a cap on
rounds or spend, and what it records.

## Elements

- **Writer.** One lead session writes the code of a milestone and sees the whole
  project. Parts that are independent can have parallel writers when the build plan
  says so.
- **Findings.** The lead judges whether a finding is local or a sign of a pattern. A
  pattern is fixed at its cause and, when possible, turned into an automatic check.
  A suggestion is listed in `logs/decisions.md` and does not start another round.
- **Tests.** Tests can be added and changed. A change to an existing test is recorded
  with its reason. `python3 scripts/test_changes.py --since <ref>` lists the changes
  for the reviewer. A project can protect some tests against any change.
- **State between sessions.** The repository is the record. A new session starts by
  reading the documentation and the logs.
- **Documentation.** It stays alive. The lead corrects it when the build shows an
  error, and records the correction. The build plan says which changes need Daniel.
- **Helpers.** A milestone uses the helpers its configuration names. Each one is
  created from `factory-setup/helper-template.md`.
- **Configuration.** `python3 scripts/params.py <milestone>` prints the configuration
  that applies to a milestone. The settings a milestone runs with are the ones
  approved in the build plan.
- **Measurement.** Work and events are recorded as they happen with
  `python3 scripts/measure.py`. The format is in `logs/FORMAT.md`.
