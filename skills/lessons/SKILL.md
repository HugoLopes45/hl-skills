---
name: lessons
description: "Turn what went wrong or right in a session or a merged change into the cheapest durable fix, with evidence: an automated check for mechanical mistakes, a review rule for judgement calls, a navigation pointer, an ADR, or a doc. Use when a session or a merged change ends, or when the user wants a retrospective or to capture what was learned. Not for recording a single decision (use `adr`)."
---
# Lessons

Input: `[session (default) | PR number | branch | ref range]`

Improve the environment the next agent works in, from evidence of what happened.

## Source

Default: the current session. Read the user's corrections, failed attempts, commands that errored, slow searches, information the agent lacked, and mechanisms that worked and are worth reusing. For a PR, branch, or ref range: read the diff, relevant history, tests, review comments, and documented outcomes; ambiguous scope means ask. A commit alone does not prove deployment or user success. Repeated edits do not prove an earlier attempt failed; code does not reveal an undocumented motive. Label inference and omit unsupported lessons.

## Destination

For each lesson, pick the cheapest destination that prevents the repeat:

| What happened | Destination |
|---|---|
| Mechanical mistake: banned API, import shape, file location, fixed pattern | Automated check in the existing linter, tests, pre-commit hook, or CI. Prefer it over prose. |
| A check exists but did not run or is broken | Wire or repair that check; add no rule. |
| No hook or CI runs lint, type, or test commands | A finding on its own. |
| Judgement call a reviewer missed | Rule in the review or coding standards file. |
| The agent could not find a file or fact | One-line pointer in the project instructions to where it lives. |
| Information the agent could not access | The access to add: a log, a read-only command, a doc. |
| Consequential, hard-to-reverse decision | ADR. |
| Guidance for consumers of the code | Docs. |

Project instructions load into every session: add a line there only when no other destination works, and propose deleting lines that change no behavior. Search existing instructions, standards, checks, and ADRs first; report a lesson already covered as covered, with its location.

## Output

First line: the lesson count and the most important lesson. Then a table ordered by cost of a repeat: lesson, evidence, destination, exact change (rule text, check sketch, or pointer line). Then lessons already covered. No quota; small sessions and diffs can hold useful lessons.

Do not write files. A proposed check is sound only if it would fail on the original mistake; say how to show that.
