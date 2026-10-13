---
name: hl-open-pr
description: "Create or preview a pull request from the current branch with why, changes, verification, and risks, as a draft by default. Use only when the user explicitly asks to open a pull request."
---
# Open PR

Input: `[base-branch] [--ready] [--dry-run]`

Base: the input, else the repository's default branch as reported by the remote. Draft unless `--ready`. Invalid base, current branch equal to base, or empty diff: stop.

Read the branch diff, its commits, the repository's PR rules, and existing verification evidence. An open PR for this branch exists: report its URL and stop. Uncommitted changes are not part of the PR; report them without staging or committing.

Title: the repository's convention, normally at most 70 characters. Body:
- Why.
- Changed behavior.
- Shape of the change, when it alters a structure (call flow, file layout, component tree, types): one `diff` of that structure.
- Verification: checks that actually passed, apart from checks proposed for reviewers. Never infer tests from file existence.
- Risks and rollback. Never promise rollback is harmless.
- Migration or breaking-change details, when present.

`--dry-run`: print the title and body and stop. Otherwise the request authorizes a normal push if needed and PR creation. Local and remote branch diverged: stop. Never force-push or bypass repository checks. Pass the body through a file or safely quoted input. Assign as the user's rules say.

## Output

Reader: a developer who asked for a pull request, and the reviewer who receives it. The decision: open now, as draft or ready.

Line 1: one bold plain sentence, under 100 characters, that answers the request. When a pull request exists, line 1 gives its URL. Never start it with a label, a verdict word, a hash, or a path.

Under line 1, plain sentences with no labels:
- Each uncommitted file, named, as not in this pull request.
- Each blocker, in plain words.
- What you did not check, when it limits the answer. Report remote state only as your commands showed it; otherwise say it is unchecked.

Before `**Next:**`, one line: `Verdict: <word>`, one of:
- `Opened, as draft` (or `Opened, ready`): the pull request exists.
- `Preview`: `--dry-run`. The text is printed; nothing was pushed or created. If the remote or `gh` could not be checked, say the text is a draft written from the diff, not a tool preview.
- `Already open`: a pull request for this branch exists. Stop.
- `Stopped`: the base is the current branch, the diff is empty, local and remote branches diverged, or the GitHub command-line tool (`gh`) is missing. Line 1 names which one and what it blocks. `**Next:**` holds at most 3 numbered ways to unblock, default marked; they appear nowhere else. Do not print the body.

Printed or previewed: `## Pull request text`, then the title and body in a `markdown` fence, complete. The body is the exact artifact; never shorten it to fit the reply.

`**Next:**` holds the steps, in order. Then `**Changed:**` names the pushed branch and pull request URL, or `none`.

Reader rules:
- Define at first use: "draft" (not ready for review; reviewers are not asked yet), "base" (the branch the change merges into), "rollback" (how to undo the change, and what the undo costs).
- "Verification" lists checks that ran and passed here, with their result. Never infer a test from a test file's existence.
- No hype in the title or body. Never call a rollback harmless.

Example:

````markdown
**I opened a draft pull request against `main`: <PR URL>. Reviewers are not asked yet.**
`docs/export.md` is not in this pull request; it is an uncommitted change.

## Pull request text
```markdown
Title: Add CSV export for invoices

## Why
Accountants need invoice lists they can open in a spreadsheet.

## Changed behavior
Invoices page: new "Export CSV" button, one row per invoice line.

## Verification
- `pytest tests/test_export.py`: 6 passed.

## Risks and rollback
- Old CSV column names are gone; the accounting import needs the new names.
- Rollback: revert the merge commit. Exports return to the old columns.
```

Verdict: Opened, as draft

**Next:**
1. Commit `docs/export.md` on this branch if it belongs here, then run again.
2. Mark ready when the checks pass: `gh pr ready <PR URL>`.

**Changed:** remote branch `feature/export` and pull request <PR URL>.
````
