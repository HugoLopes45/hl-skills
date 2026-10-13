---
name: hl-lessons
description: "Turn what went wrong or right in a session or a merged change into the cheapest durable fix, with evidence: an automated check for mechanical mistakes, a review rule for judgement calls, a navigation pointer, an ADR, or a doc. Use when a session or a merged change ends, or when the user wants a retrospective or to capture what was learned. Not for recording a single decision (use `hl-adr`)."
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

Reader: the person who ended a session or merged a change, and who decides which lessons to apply. The skill writes nothing; each change is theirs to apply.

Line 1: one bold plain sentence, under 100 characters, that says in plain words how many lessons there are and the most important one, for example "This session teaches one lesson: ..." or, when nothing is new, "Your rule already covers this, but its lint check misses deeper paths.". Never start it with a count, a label, or the verdict word. No quota; small sessions and diffs can hold useful lessons.

Under line 1, a plain sentence for each source you could not read, only when that limits the answer.

Body, one numbered point per lesson, most costly repeat first:
- A bold plain sentence that states the lesson.
- One or two sentences: the evidence from the session or the change, and the destination (the file or place that changes).
- The exact change in a fence, indented under the point (rule text, check sketch, or pointer line).
- For a check: one sentence on how to show it fails on the original mistake.

Lessons already covered: after the new lessons, one numbered point each, in one sentence, with its `file:line` and why it did not stop the repeat. Omit when none.

Before `**Next:**`, one line: `Verdict: <word>`, one of:
- `Lessons`: at least one lesson is new.
- `No new lessons`: every lesson is already covered, even when its rule or check has a gap. Line 1 says so; the gap is a numbered point, and its fix goes in `**Next:**`.

`**Next:**` holds each change to apply, in order.

Reader rules:
- Name the mistake and the fix, never the person: "the lint rule did not run", not "the agent ignored it".
- Define at first use: "lint" (the automatic code checker), "project instructions" (the file each session loads, for example `AGENTS.md`), "pointer line" (one line in those instructions).
- Search existing instructions, standards, checks, and ADRs first. Do not write files. A proposed check is sound only if it would fail on the original mistake.

Example:

````markdown
**This session teaches one lesson: a banned import should fail lint, not rely on review.**

1. **Ban `pickle` imports in lint.**
   The session fixed a `pickle` import twice, and no check caught it. Add the rule to `pyproject.toml`, in the ruff settings.
   ```toml
   [tool.ruff.lint]
   extend-select = ["TID251"]

   [tool.ruff.lint.flake8-tidy-imports.banned-api]
   "pickle".msg = "Use json; pickle runs code when it loads."
   ```
   To prove it, add `import pickle` to `src/cache.py` and run `ruff check src/cache.py`. It should fail with TID251.

Verdict: Lessons

**Next:**
1. Add the block to `pyproject.toml`, then run `ruff check .`.
````
