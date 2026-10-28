# Report contract

`security-audit.json` is the authoritative record; `security-audit.md` is derived from it. [`report-example.json`](report-example.json) shows a valid incomplete MEDIUM run with one confirmed, one unresolved and one rejected finding, and blocked units for checks that could not run. `scripts/validate_report.py` is the executable form of this contract. When this page and the script disagree, the script decides and the page needs a correction.

## Validator

```text
python3 <skill-directory>/scripts/validate_report.py <report-directory>/security-audit.json
```

- Exit 0: structure and cross-references are consistent. Exit 1: the report is invalid. Exit 2: nothing was checked (usage error, missing, unreadable, linked, special or oversized file).
- Uses the Python standard library only. Reads the named file and nothing else: no cited paths, no network, no report content executed.
- Diagnostics name locations such as `findings[0].reviewer`, never values or unexpected keys.
- Input limits: regular UTF-8 JSON file, at most 2 MiB and 64 nesting levels, no repeated keys, no NaN or infinite numbers, no fields outside this contract.
- A pass proves internal consistency only. It cannot prove that a finding is true, that cited lines say what the record claims, that a check is relevant or repeatable, or that two reviewer IDs are different people.

## Values

- Text: a string with visible characters; tab and newline are the only control characters; no bidirectional controls.
- Identifier: 1 to 128 ASCII letters, digits, `.`, `_` or `-`, starting with a letter or digit. Keep IDs stable across re-audits.
- Path: repository-relative POSIX path of at most 1,024 characters, or `.` for the whole repository. No leading `/` or `~`, backslash, colon, surrounding whitespace, or empty, `.` or `..` segment. Paths are recorded, never opened by the validator.
- Lists of text, paths or identifiers have unique entries.
- `A within B`: B is `.`, or A equals B, or A starts with `B/`.

## Root

| Field | Value |
|---|---|
| `schema_version` | `1` |
| `source_ref` | Text: reviewed revision and worktree state, or a statement that it is unknown |
| `scope` | Nonempty paths. `.` stands alone; no entry lies within another |
| `profile` | `quick`, `standard` or `deep` |
| `run_status` | `complete` or `incomplete` |
| `assurance` | `HIGH`, `MEDIUM` or `LOW` |
| `limitations` | Text list; nonempty when incomplete |
| `prior_runs` | Text list of earlier reports used, or `[]` |
| `coverage_review` | `{reviewer: text or null, uncovered: text list, notes: text}` |
| `units`, `findings`, `scanners` | Arrays of the records below |

## Units

Fields: `id`, `surface`, `boundary`, `category`, `paths` (nonempty), `status`, `checks`, `finding_ids`, `reason` (text or null). Each check is `{method: source|scanner|supplied, evidence, author, paths}`. `source` is a read of the cited paths that another reviewer can repeat from the record; `supplied` is owner-supplied runtime evidence whose revision, input and provenance were checked; `scanner` is a recorded scanner result.

| Status | `reason` | `checks` | `finding_ids` | `paths` |
|---|---|---|---|---|
| `planned` | null | none | none | within scope |
| `reviewed` | null | at least one | allowed | within scope |
| `blocked` | required | allowed | allowed | within scope |
| `deferred` | required | allowed | allowed | within scope |
| `not_applicable` | required | at least one `source` or `supplied` | none | within scope |
| `out_of_scope` | required | none | none | no overlap with scope |

- Check paths lie within the unit's paths.
- IDs are unique. Two units with the same surface, boundary, category and paths are one unit.
- A `scanner` check needs at least one scanner record with status `ran`.

## Findings

Shared fields: `id`, `title`, `state`, `unit_ids` (nonempty), `author`, `attacker`, `boundary`, `impact`, `conditions` (text list), `trace`, `evidence_basis` (`source` or `observed`), `evidence`, `reviewer`.

- `reviewer` is null or `{id, decision, reason}`. A non-null reviewer differs from the author, and `decision` equals `state`.
- `trace` is a nonempty list of `{path, line, role, detail}`, with `line` a positive integer. One hop is an `entry` or a `sink`; a longer trace starts at `entry`, ends at `sink` and has only `step` between. Every hop path lies within the scope and within a linked unit's paths.
- `observed` needs a `supplied` check in a linked unit. It means checked supplied runtime evidence, not execution by the audit.
- Units and findings link both ways: every `unit_ids` entry lists the finding, and every `finding_ids` entry lists the unit.

State-specific fields; no others are allowed:

| State | Fields |
|---|---|
| `confirmed` | `severity` (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`), `cwe` (`CWE-<n>` or `unmapped`), `cvss` (`unscored` or a CVSS 3.0, 3.1 or 4.0 vector), `remediation`, `regression`, `disposition` (`active` or `accepted_risk`), `exception` |
| `needs_validation` | `blocker`, `next_check` |
| `rejected` | `reason` |

- `confirmed` needs a non-null reviewer.
- The `cvss` check is lexical only: a `CVSS:3.0`, `CVSS:3.1` or `CVSS:4.0` prefix followed by `/metric:value` pairs. It does not check metric names, required metrics, allowed values or any score.
- `active` needs a null `exception`. `accepted_risk` needs `exception: {source: path, rationale: text, expires: YYYY-MM-DD}`, with `expires` after the current UTC date. An expired exception makes the report invalid; restore the finding to `active` instead.

## Scanners

Fields: `kind` (`deps`, `secrets`, `sast`, `patterns`), `command`, `directory` (path), `executions` (integer from 0), `status` (`ran`, `skipped`, `failed`, `denied`), `scope` (nonempty paths), `preflight`, `result`.

- `ran` and `failed` need at least one execution; `skipped` and `denied` have zero.
- Scanner records never set assurance. Record failed, denied and skipped attempts as they happened.

## Run status and assurance

`complete` requires all of the following:

- the profile is not `quick`;
- at least one unit is `reviewed`, and none is `planned`, `blocked` or `deferred`;
- no finding is `needs_validation`, and every finding has a reviewer;
- `coverage_review.reviewer` is set and `uncovered` is empty.

A non-null coverage reviewer differs from every check author and finding author, whatever the run status.

| Assurance | Requires |
|---|---|
| `HIGH` | `complete`, and every `reviewed` or `not_applicable` unit has a `source` or `supplied` check |
| `MEDIUM` | At least one `reviewed` unit with a `source` or `supplied` check |
| `LOW` | Nothing; always allowed |

A lower assurance than the record supports is allowed. Units whose checks are all `scanner` support neither HIGH nor MEDIUM, and no scanner kind is required. HIGH states coverage of the declared scope; it is not runtime proof or a claim of global safety.
