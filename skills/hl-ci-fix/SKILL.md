---
name: hl-ci-fix
description: "Diagnose failing required checks on a pull request and apply bounded fixes without weakening tests or CI policy. Use only when the user explicitly asks to fix CI on a pull request."
---
# CI Fix

Input: `[pr-number, or empty for current PR]`

Resolve the input or the current branch's PR. Verify checkout matches its head and is not the base branch. Missing PR, access, or matching checkout: stop. Preserve unrelated changes.

Explicit invocation authorizes scoped fixes, commits, and normal pushes for this PR, not merging branches, force-pushing, or deployment changes. Confirm additional authority when the required action exceeds that scope.

Inspect required checks through available GitHub tooling. Wait for pending runs up to 20 minutes; still pending: report them as pending. For failures, read the actual failing check's logs; not every check is GitHub Actions.

Fix one evidenced cause, run the relevant local check, commit only scoped changes, and push without bypassing hooks. Re-query checks for the new head. Do not weaken tests, assertions, or required-check policy to obtain green.

Suspected flakes need evidence; retry once and report both outcomes. Stop after two unsuccessful scoped attempts, unavailable logs, or an infrastructure or permission blocker.

## Report

Reader: the PR author or maintainer, who asked for green checks and decides whether to merge. They may not know CI. Define each term at first use: required check (a check that must pass before merge), head (the commit the PR points at), attempt (one fix and its re-run; the first run, before any fix, is attempt 0).

- Line 1, bold: one plain sentence that says whether the required checks pass now, and why, within 100 characters. It never starts with a label or the verdict word.
- Under line 1, plain sentences: each blocker or precondition, for example `The PR is not checked out, so I made no fix.`; the scope of the result, for example `This covers only the required checks I saw on head 4f0b2d1.`; each pending or unresolved check.
- A numbered list, one item per check: a bold sentence with its result before and after the fix, then the cause and the fix, then the commit. Name each check as CI shows it. Name each retry with both outcomes in one sentence.
- Links follow the list, one per line.
- `Verdict: <word>` on its own line just before `**Next:**`, one of:
  - `Green`: every required check passed on that head. It covers only the required checks observed for that head.
  - `Red`: a required check still fails on that head. Say how many of how many (for example `1 of 3 required checks still fails`).
  - `Pending`: a required check still runs after the 20-minute wait.
  - `Stopped`: the PR, its logs, or access is missing. Use the Stopped form below.
- `**Next:**` the steps a person can do now, in order, including the merge decision when one remains.
- `**Changed:** <paths>` with each commit pushed, or `**Changed:** none`.

````markdown
**All 3 required checks pass on PR 41 now, after one fix in `rates.py`.**
This covers only the required checks I saw on head `4f0b2d1`.

1. **unit / rates failed, and passes after one fix.**
   `rates.py:22` rounds half to even; the fix rounds half up. Commit `4f0b2d1`.
2. **lint and build passed before any change.**

Verdict: Green

**Next:**
1. Review `rates.py:22` in `4f0b2d1`, then merge PR 41. Merging is yours to decide.

**Changed:** `rates.py`, commit `4f0b2d1` pushed to PR 41
````

Stopped, when the PR or its logs cannot be read: line 1 says what is missing and why it blocks (for example `**I can't read the checks of PR 12, so I can't find the failure.**`). Under it, the plain sentence `I changed nothing.` Then at most 3 numbered ways to unblock, the default marked `(default)`:
1. Sign in to the GitHub CLI with `gh auth login`, then rerun the skill. (default)
2. Paste the failing log lines of each check.
3. Name the PR to use, when the current branch has none.

Then `Verdict: Stopped`, then `**Changed:** none`.

Reader rules: name each check as CI shows it. Never write that CI is green without the head and the check list. No blame on the person who broke the check.
