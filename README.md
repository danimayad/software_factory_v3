# Software Factory v3: project template

This repository is the starting point of a project built with the software factory.
It holds what every project needs, whatever its stack or coding agent. Everything
specific to a project is written in the project.

The design of the factory, with its reasons and sources, lives in one document:
https://claude.ai/artifact/7RAJduTXqb8LFs3hYFobzx

## How a project goes

1. **Create the project.** On GitHub, create a new repository from this template.
   Clone it to the Mac, or open a cloud session on it.
2. **Understand the project.** Talk freely with the agent, in as many sessions as you
   want. Nothing formal is written. When a technical conclusion is worth keeping, ask
   the session to record it in `notes/`.
3. **Write the documentation.** In a fresh session, write the product brief and the
   requirements together with the agent. Then the agent leads the architecture and you
   approve a plain-language summary. The build plan follows from both. Each folder in
   `docs/` has a short guide of what usually belongs there.
4. **Check fidelity.** A fresh session reads only the documentation and explains the
   project back to you in plain words. If it matches what you understand, continue.
5. **Set up the factory for this project.** In `factory-setup/`: the parameter file,
   the helpers the project needs, and the agent's settings. The setup reference has
   tested examples to copy.
6. **Build, milestone by milestone.** The first milestone is the foundation: shared
   modules, quality gates and CI (it fills in `scripts/check.sh` and activates the CI
   file kept in `factory-setup/reference/ci.example.yml`). Each milestone follows the
   loop in `docs/build-method.md`.
7. **Measure.** The lead records the work in `logs/measurement.jsonl`.
   `python3 scripts/measure.py summary` shows totals and composite measures.

## What is in this repository

| Path | What it is |
|---|---|
| `AGENTS.md`, `CLAUDE.md` | The short file an agent reads when a session starts |
| `docs/way-of-working.md` | The criteria every session and helper works with |
| `docs/build-method.md` | The loop every milestone follows |
| `docs/product-brief/`, `docs/requirements/`, `docs/architecture/`, `docs/build-plan/` | The project's documentation, each with a guide |
| `factory-setup/` | Parameter file, helper template, setup reference per coding agent |
| `notes/` | Technical conclusions recorded during the understanding stage |
| `references/` | Visual references, sample data, documents to follow |
| `logs/` | Progress log, decisions log, measurement log, and their format |
| `scripts/` | Quality gates command, list of test changes, parameters, measurement |

## What has been tested

See `factory-setup/reference/STATUS.md`. It says, for each part, whether it was run,
only checked against documentation, or not yet tested.
