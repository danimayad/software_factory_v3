# Measurement log: format

`logs/measurement.jsonl` holds one JSON object per line. The format is the same in
every project, so projects can be compared. Entries are added with
`python3 scripts/measure.py`, never by hand.

## Common tags

Every entry has `ts` (time, UTC), `type`, and the tags that apply:
`project`, `stage`, `milestone`, `feature`, `role`, `model`, `effort`, `session`, `note`.

- `stage`: `understanding`, `documentation`, `build`.
- `role`: who did the work, in the project's own words (for example the lead, or the
  name of a helper).

## Entry types

| type | Meaning | Extra fields |
|---|---|---|
| `work` | A piece of work and its tokens | `activity` (`understanding`, `documentation`, `building`, `gate_fix`, `review`, `rework`, `other`), `input`, `output`, `cache_write`, `cache_read` |
| `gate` | A run of the quality gates | `result` (`pass`/`fail`), `first_run` (true/false) |
| `review` | A review of a feature or milestone | `round` (1, 2, ...), `result` (`approved`/`changes`) |
| `finding` | One finding of a review | `accepted` (true/false), `scope` (`local`/`pattern`), `reason` |
| `test_change` | An existing test changed or removed | `reason` |
| `question` | A question sent to Daniel | `kind` (`product`/`field`/`engineering`) |
| `doc_correction` | A correction to the documentation | `reason` |
| `cap_hit` | A loop reached its cap | `reason` |
| `limit_cut` | Work cut by the usage limit | |
| `escaped_defect` | A bug found after its milestone closed | `reason` |

## Tokens

There are four kinds: `input` (read for the first time), `output` (written, reasoning
included), `cache_write` (input stored for reuse), `cache_read` (stored input read
again). The weighted total, in input-token units, is

    weighted = input + 5*output + 1.25*cache_write + 0.1*cache_read

The weights are at the top of `scripts/measure.py`. They are Anthropic's API price
ratios as known on 10 November 2026 and should be checked for the model in use.
