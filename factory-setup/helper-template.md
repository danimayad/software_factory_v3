# Helper template

The factory has no fixed list of helpers. A project creates the ones it needs from
this template. A helper is a separate agent started by the lead session for one task.
It starts without the lead's conversation, which is what makes a reviewer independent.

A helper is worth its tokens when it gives parallel work, a fresh pair of eyes, or
keeps long output out of the main session. It does not give a better answer than the
main session on the same task.

## Variables

| Variable | What to write |
|---|---|
| Name | A short name, in the project's own words |
| Purpose | What it is for, in one or two sentences |
| When it is used | The moment of the loop, or the condition, that calls for it |
| What it reads first | The product brief and the way of working, then what its task needs |
| Task | What it does, step by step when the order matters |
| Tools | What it may use. A reviewer usually reads and runs, and does not edit |
| Model and effort | In proportion to the difficulty of the task |
| Limits | A cap on turns, and whether it works in its own copy of the repository |
| Report | The form of what it returns: verdict, findings, evidence |
| What it must not do | Limits that protect the project, stated with their reason |

## Notes for writing one

- Give the purpose and the criteria, and let the helper judge. A long list of cases
  makes it rigid.
- Ask a reviewer for problems that affect correctness against the requirements, and to
  skip style. A reviewer asked to find problems always finds something.
- Ask it to say whether a finding is local or a sign of a pattern, and to report one
  finding for several cases that share a cause.
- Ask for evidence: the command it ran and its output.

How these variables become a file for each coding agent: see `reference/`.
