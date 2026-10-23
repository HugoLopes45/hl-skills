---
name: hl-lessons
description: "Turn what went wrong or right in a session or a merged change into the cheapest durable fix, with evidence: an automated check for mechanical mistakes, a review rule for judgement calls, a navigation pointer, an ADR, or a doc. Use when a session or a merged change ends, or when the user wants a retrospective or to capture what was learned. Not for recording a single decision (use `hl-adr`)."
---
# Lessons

Input: `[session (default) | PR number | branch | ref range]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Keep evidence-backed lessons and the cheapest durable prevention for each. Distinguish proposed checks from checks run; do not turn the retrospective into a general policy audit.

Improve the environment the next agent works in, from evidence of what happened.

Read-only, including scratch space: do not create files or apply proposed checks. Put application and scratch-copy demonstrations in Next for the reader.

## Source

Default: the current session. Read the user's corrections, failed attempts, commands that errored, slow searches, information the agent lacked, and mechanisms that worked and are worth reusing. For a PR, branch, or ref range: read the diff, relevant history, tests, review comments, and documented outcomes; ambiguous scope means ask. A commit alone does not prove deployment or user success. Repeated edits do not prove an earlier attempt failed; code does not reveal an undocumented motive. Label inference and omit unsupported lessons.

For a missed check, compare each command's selection pattern, traversal rules, and reachable files. List the selected and excluded project files by basename and depth before naming the cause. A basename pattern can match the same filename in multiple directories. Before proposing prevention, reconcile its claimed coverage and source anchors with numbered reads and actual command results.

## Destination

For each lesson, pick the cheapest destination that prevents the repeat:

| What happened | Destination |
|---|---|
| Mechanical mistake: banned API, import shape, file location, fixed pattern | Automated check in the existing linter, tests, pre-commit hook, or CI. Prefer it over prose. |
| A check exists but did not run or is broken | Wire or repair that check; add no rule. |
| Judgement call a reviewer missed | Rule in the review or coding standards file. |
| The agent could not find a file or fact | One-line pointer in the project instructions to where it lives. |
| Information the agent could not access | The access to add: a log, a read-only command, a doc. |
| Consequential, hard-to-reverse decision | ADR. |
| Guidance for consumers of the code | Docs. |

Project instructions load into every session: add a line there only when no other destination works, and propose deleting lines that change no behavior. Search existing instructions, standards, checks, and ADRs first; report a lesson already covered as covered, with its location.

## Output

Reader: the person who ended a session or merged a change, and who decides which lessons to apply. Each proposed change is theirs to apply.

Line 1: one bold plain sentence, that says in plain words how many lessons there are and the most important one, for example "This session teaches one lesson: ..." or, when nothing is new, "Your rule already covers this, but its automatic code check misses deeper paths.". Never start it with a count, a label, or the verdict word. No quota; small sessions and diffs can hold useful lessons.

Under line 1, a plain sentence for each source you could not read, only when that limits the answer.

Body, one numbered point per lesson, most costly repeat first:
- A bold plain sentence that states the lesson.
- Give the evidence from the session or the change, and the destination (the file or place that changes). Include what makes the proposed lesson checkable.
- The exact change in a fence, indented under the point (rule text, check sketch, or pointer line).
- For a check: state whether it was run and any limitation that affects what it catches. Keep the complete proposed configuration in the fence; put applying it and demonstrating failure on the original mistake only in Next.

Lessons already covered: after the new lessons, one numbered point each, with its `file:line` and the evidence for why it did not stop the repeat. Omit when none.

Before `**Next:**`, one line: `Verdict: <word>`, one of:
- `Lessons`: at least one lesson is new.
- `No new lessons`: every lesson is already covered, even when its rule or check has a gap. Line 1 says so; the gap is a numbered point, and its fix goes in `**Next:**`.

`**Next:**` owns each reader action, decision, prerequisite, and question once, in order. For a proposed check, include applying it, demonstrating that it fails on the original mistake in a scratch copy, and checking the corrected code.

Reader rules:
- Name the mistake and the fix, never the person: "the lint rule did not run", not "the agent ignored it".
- Define at first use: "lint" (the automatic code checker), "project instructions" (the file each session loads, for example `AGENTS.md`), "pointer line" (one line in those instructions).
- A proposed check is sound only if it would fail on the original mistake.

Example:

````markdown
**This session teaches one lesson: a banned import should fail lint (the automatic code checker), not rely on review.**

1. **Lint can catch the repeated `pickle` import.**
   The session fixed a `pickle` import twice, and no check caught it. The proposed rule belongs in the ruff settings in `pyproject.toml`.
   ```toml
   [tool.ruff.lint]
   extend-select = ["TID251"]

   [tool.ruff.lint.flake8-tidy-imports.banned-api]
   "pickle".msg = "Use json; pickle runs code when it loads."
   ```
   The proposed rule has not been run.

Verdict: Lessons

**Next:**
1. Add the block to `pyproject.toml`.
2. In a scratch copy, add `import pickle` to `src/cache.py` and run `ruff check src/cache.py`; confirm it fails with TID251.
3. Run `ruff check .` on the corrected project.
````
