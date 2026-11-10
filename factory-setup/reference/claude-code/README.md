# Setup reference: Claude Code

How each part of the factory setup is configured in Claude Code, with examples to copy
and adjust. Nothing here is active: a project copies what it needs into `.claude/`.

Each part says where the information comes from:
- **Documentation**: read in Claude Code's documentation on 10 November 2026.
- **First factory**: used in the first factory in October 2026 (the trading learning
  app), not read again in the documentation.
- **Simulated**: the script was run here with made-up input, not inside Claude Code.

Claude Code changes often. Check a part again before relying on it for a new kind of
use. Documentation: https://code.claude.com/docs

## Instruction files

Claude Code reads `CLAUDE.md` and does not read `AGENTS.md`. The documented way to
share one text with other agents is a `CLAUDE.md` that imports it: a line `@AGENTS.md`.
Imported files are loaded when the session starts. Helpers load `CLAUDE.md` too, unless
their definition sets `omitClaudeMd: true`. *(Documentation.)*

The first time Claude Code meets imports in a project it shows an approval dialog. If
it is declined, the imports stay off. *(Documentation.)*

## Helpers

A helper is a "subagent": a Markdown file in `.claude/agents/`, with a header of
variables and the instructions as the body. *(Documentation.)*

| Helper template variable | Field in the file |
|---|---|
| Name | `name` |
| Purpose, when it is used | `description` (Claude uses it to decide when to delegate) |
| What it reads first, task, report, what it must not do | The body of the file |
| Tools | `tools` (allowed) and `disallowedTools` (denied) |
| Model and effort | `model` (`sonnet`, `opus`, `haiku`, `fable`, a full model name, or `inherit`), `effort` (`low` to `max`) |
| Limits | `maxTurns`; `isolation: worktree` gives it its own copy of the repository; `permissionMode` |

Other fields exist (`skills`, `mcpServers`, `hooks`, `memory`, `background`,
`omitClaudeMd`). Field names must be exact: an unknown field is ignored without an
error.

- Edits to an existing helper file are picked up within seconds. Creating the first
  helper file in a folder that did not exist when the session started needs a restart.
- A helper does not see the conversation of the session that starts it. Give it what
  it needs in the task.
- Examples: `examples/helper-reviewer.example.md`, `helper-check-runner.example.md`,
  `helper-writer.example.md`. They follow the definitions of the first factory, made
  general. The fields `effort`, `maxTurns` and `isolation` were not used in the first
  factory. *(Format: documentation. These exact files: not run.)*

## Settings: permissions, sandbox, hooks

They live in `.claude/settings.json`, committed with the project. Example:
`examples/settings.example.json`.

**Permissions.** `allow` lists what runs without asking, `deny` what never runs.
A rule names a tool and a pattern, such as `Bash(git push *)` or `Read(**/.env)`.
Lists from several settings files are combined. *(Documentation for the syntax; the
deny rules for `.env` and for the settings and hooks files come from the first
factory.)*

**Sandbox.** Limits what shell commands can write and reach on the Mac. The first
factory used `enabled`, `excludedCommands` (commands that run outside it, such as git
commands that reach GitHub) and `network.allowedDomains`. *(First factory. The sandbox
page of the documentation was not read again.)*

**Hooks.** A hook is a script Claude Code runs at a fixed moment. Exit code 0 allows;
exit code 2 blocks and shows the script's error text to the agent. *(First factory.)*
- `examples/hooks/protect_paths.py`: blocks edits to the paths listed as
  `protected_paths` in `factory-setup/parameters.json`. *(Simulated.)*
- `examples/hooks/gates_on_stop.py`: when the session tries to stop, runs
  `scripts/check.sh` and keeps it working while the gates fail, at most three times.
  *(Simulated.)*
- The first factory found that a hook attached inside a helper's own definition did
  not run in cloud sessions, so hooks are configured in `settings.json`.

**When changes apply.** Claude Code reloads settings files while it runs, including
permissions and hooks. The model and the effort level are read once, at session
start. *(Documentation.)*

**Cloud sessions.** A cloud session on one repository reads the committed
`.claude/settings.json`. It does not read personal settings from the Mac. In a cloud
thread inside a claude.ai Project, the repository's permission rules and hooks do not
apply. *(Documentation.)*

**Running without permission prompts.** New terminal and VS Code sessions start in
"auto mode", where a classifier reviews risky actions; this removes most prompts.
*(Documentation. Not checked for the desktop app or for cloud sessions.)* The
values `auto` and `bypassPermissions` for the default permission mode do not take
effect from a project's settings file; they are set in the user's settings or when the
session starts. *(Documentation.)*

## The loop

- The goal command (`/goal <condition>`) keeps the session working until a separate
  model judges the condition met, or a turn limit is reached. *(Documentation.)*
- A Stop hook does the same with a script, enforced by Claude Code. *(Documentation;
  example above.)*
- Limits for a run started from a script: `--max-turns` and `--max-budget-usd`.
  *(Documentation.)*

## Tokens

- The usage screen (`/usage`) shows, for the session, the four token counts per model:
  input, output, cache read, cache write. *(Documentation.)*
- A breakdown per helper is not documented. Each helper's record is stored on the Mac
  under `~/.claude/projects/<project>/<session>/subagents/`. `python3
  scripts/measure.py transcript <file>` sums the counts in one record, on an assumption
  about its format that is not yet verified. *(To confirm in the first project.)*

## One-time setups (from the first factory)

- **Keys in the cloud:** add them in the cloud environment's settings, never in the
  chat.
- **@claude on GitHub** (optional, per repository): needs a token saved as a
  repository secret and a workflow file. The first factory's workflow file can be
  copied from that project when needed.

## Known limits (from the first factory)

- A script that changed after a session started was not picked up when it was called
  by name through a saved workflow; the session kept the copy it had read.
- The first factory's guard on git commands read commands as typed, so an alias or a
  script that runs git by itself was not recognised.
- On GitHub, @claude can only push the branch it was started on.
