# Project instructions

This file is read at the start of every session. It stays short. It holds only what
cannot be learned from the code and the documentation.

## Read before working

1. `docs/product-brief/`: what the product is, who it is for, what matters most, what
   is out of scope.
2. `docs/way-of-working.md`: the criteria for working on this project.
3. `logs/progress.md` and `logs/decisions.md`: what is done, what is pending, what was
   decided and why.

Read the rest of the documentation when the task needs it:
`docs/requirements/`, `docs/architecture/`, `docs/build-plan/`.
When building, follow `docs/build-method.md`.

## Commands

- Quality gates (all automatic checks): `bash scripts/check.sh`
  Not configured yet. The foundation milestone fills it in for the chosen stack.
- Effective configuration of a milestone: `python3 scripts/params.py <milestone>`
- Tests changed since a git reference: `python3 scripts/test_changes.py --since <ref>`
- Record and summarize measurement: `python3 scripts/measure.py --help`

## Project facts

Nothing yet. Add here only facts a session cannot find in the repository: a decision
that is not written elsewhere, a place where the code is misleading, something that had
to be corrected twice.
