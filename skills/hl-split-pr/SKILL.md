---
name: hl-split-pr
description: "Propose how to split a large diff into coherent, dependency-ordered pull requests without rewriting history. Use when a branch is too large to review as one change."
---
# Split PR

Input: `[base-branch]`

Resolve the input or the verified default branch as base. Read the full diff, changed paths, and commit log; if scope cannot be read, report the limitation rather than claiming a complete partition. No edits or history changes.

Group by independent behavior, separating refactors when they can stand alone. Keep tests and required configuration with their behavior. Assign binaries to their owning change, noting that content was not line-reviewed.

For each group: title, files or hunks, existing commits where applicable, delivered behavior, prior dependencies, verification, and rollback risks. Mark each group's build and test result unverified until run.

Account for every change once. Together, the groups must equal the branch diff against the base; if the base moved, list the differences.

## Output

Reader: a developer with one large branch who must choose how to split it into reviewable pull requests, and in which order.

Line 1: one bold plain sentence, under 100 characters, that answers "how do I split this?" in plain words. Never start it with a label, a verdict word, a hash, or a path.

Under line 1, plain sentences with no labels:
- For each link that forces two groups to merge together, one sentence that names the shared item.
- `I did not build or test any group, so their build and tests are unverified.`

Before `**Next:**`, one line: `Verdict: <word>`, one of:
- `Proposed split`: the branch forms two or more coherent groups. Line 1 gives the number of pull requests.
- `No clean split`: the branch forms fewer than two coherent groups. Line 1 names the one reason.
- `Stopped`: the base or the diff cannot be read. Line 1 names what is missing and why it blocks. Before the verdict, at most 3 numbered options, default marked.

Proposed split, in this order:
- `## Merge order`: a table in merge order, columns `Pull request`, `Delivers`, `Waits for`. Number each pull request in its first cell. `Waits for` names the pull request this one needs first, or `-`. Every cell is a short phrase in plain words.
- `## Files`: one `text` block, one file per line, with `# pull request <n>` and the state (`~` changed, `+` added, `-` removed; `# binary, not line-reviewed` for binaries). Every changed file appears once.
- `## Rollback`: a numbered list, one item per pull request: how to undo it, and what breaks if another stays.

`No clean split`: no table and no file list; name the one reason and the next step.

`**Next:**` holds the steps, in order. This skill writes nothing, so there is no `**Changed:**` line.

Reader rules:
- Define at first use: "merge order" (the order the pull requests merge in), "rollback" (how to undo a group's change).
- Name each pull request by its behavior ("rename `send` to `dispatch`"), not by a commit subject or "refactor".
- Say what is shared in one clause when you state a coupling.

Example:

````markdown
**Split this branch into 3 pull requests, merged in the order below.**
Pull request 2 must merge after pull request 1: `retry.py` calls `dispatch`.
I did not build or test any group, so their build and tests are unverified.

## Merge order
| Pull request | Delivers | Waits for |
|---|---|---|
| 1. Rename `send` to `dispatch` | Same alerts, clearer name | - |
| 2. Add a retry limit to webhooks | Stops after 5 tries | 1 |
| 3. Pin the push SDK version | Same build on every machine | - |

## Files
```text
notify/push.py     # pull request 1, ~ rename
notify/email.py    # pull request 1, ~ call site
notify/retry.py    # pull request 2, + added
ios/Podfile.lock   # pull request 3, ~ binary, not line-reviewed
```

## Rollback
1. Pull request 1: revert its commits; no other pull request changes.
2. Pull request 2: revert its commit; webhooks retry without a limit again.
3. Pull request 3: revert its commit.

Verdict: Proposed split

**Next:**
1. Confirm the order and the groups.
2. Say which branches to create; this skill edits nothing.
````
