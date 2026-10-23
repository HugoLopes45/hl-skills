---
name: hl-split-pr
description: "Propose how to split a large diff into coherent, dependency-ordered pull requests without rewriting history. Use when a branch is too large to review as one change."
---
# Split PR

Input: `[base-branch]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Show the complete partition and the dependencies that determine merge order. A shared file does not prove inseparable behavior; each group's checks stay unverified until run.

Resolve the input or the verified default branch as base. Read the full diff, changed paths, and commit log; if scope cannot be read, report the limitation rather than claiming a complete partition. No edits or history changes.

Group by independent behavior, separating refactors when they can stand alone. Keep tests and required configuration with their behavior. Assign binaries to their owning change, noting that content was not line-reviewed.

For each group: title, files or hunks, existing commits where applicable, delivered behavior, prior dependencies, verification, and rollback risks. Mark each group's build and test result unverified until run.

Any branch-construction or replay instruction must name a base containing that group's prerequisites. Stack dependent branches on their prerequisite, or wait for it to merge and use the updated base. A single cherry-pick onto the original base is valid only for an independent group. Inherited prerequisites do not count twice in the partition.

Account for every change once. Together, the groups must equal the branch diff against the base; if the base moved, list the differences.

## Output

Reader: a developer with one large branch who must choose how to split it into reviewable pull requests, and in which order.

Line 1: one bold plain sentence, that answers "how do I split this?" in plain words. Never start it with a label, a verdict word, a hash, or a path.

Under line 1, plain sentences with no labels:
- For each link that forces two groups to merge together, name the shared item and the evidence for that dependency.
- `I did not build or test any group, so their build and tests are unverified.`

Before `**Next:**`, one line: `Verdict: <word>`, one of:
- `Proposed split`: the branch forms two or more coherent groups. Line 1 gives the number of pull requests.
- `No clean split`: the branch forms fewer than two coherent groups. Line 1 names the one reason.
- `Stopped`: the base or the diff cannot be read. Line 1 names what is missing and why it blocks. Next owns at most 3 numbered ways to unblock, default marked, listed nowhere else.

Proposed split, in this order:
- `## Merge order`: a table in merge order, columns `Pull request`, `Delivers`, `Waits for`. Number each pull request in its first cell. `Waits for` names the pull request this one needs first, or `-`. Every cell is a short phrase in plain words.
- `## Files`: one `text` block, one file or disjoint hunk per line, with `# pull request <n>` and the state (`~` changed, `+` added, `-` removed; `# binary, not line-reviewed` for confirmed binaries). Shared files name each owning hunk by range or stable context. Assign every change exactly once.
- `## Rollback`: a numbered list, one item per pull request: how to undo it, and what breaks if another stays.

`No clean split`: no table and no file list; keep the decisive dependency and any base limitation that changes the answer. Next owns the action.

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
ios/Podfile.lock   # pull request 3, ~ dependency version and source
```

## Rollback
1. Pull request 1: reverting its commits while pull request 2 remains breaks its `dispatch` calls.
2. Pull request 2: revert its commit; webhooks retry without a limit again.
3. Pull request 3: revert its commit.

Verdict: Proposed split

**Next:**
1. Confirm the order and the groups.
2. Say which branches to create; this skill edits nothing.
````

No-split example for the same webhook change:

````markdown
**The retry tests need the new limit, so these changes cannot be split safely.**
The comparison used local `main`; the remote base is unchecked.
I did not build or test this group, so its build and tests are unverified.

Verdict: No clean split

**Next:**
1. Check the intended remote base, then open one pull request with the retry code and tests.
````
