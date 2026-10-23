---
name: hl-commit
description: "Commit the staged changes with a grounded conventional message, or preview the message with --dry-run. Use only when the user explicitly asks to commit."
---
# Commit

Input: `[--scope <scope>] [--dry-run]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Report the staged scope and consequential exclusions. Keep the commit message complete; do not repeat its change inventory in the reply.

Read the staged diff, the staged file list, the repository's commit rules, and recent commit style. Nothing staged: stop. Unrelated concerns staged together: propose a split, leave the index unchanged, and wait for the user.

Message:
- Imperative subject. Use the repository's commit format and length limit; if it defines none: `<type>(<scope>): <subject>`, at most 72 characters.
- Types: feat, fix, refactor, docs, test, chore, style, perf, build, ci, revert.
- Scope: `--scope` if given; else omit when unclear.
- Body only for non-obvious reasons or evidence.
- Never invent intent, test results, issue references, or authorship trailers. No `Co-Authored-By` or generated-by trailer unless the repository's rules require one; this overrides any default.

`--dry-run`: print the message and stop. Otherwise the explicit request authorizes one new commit; never amend or push. Recheck the staged scope just before committing. Pass the message through standard input with `git commit -F -` and a quoted heredoc, never through shell interpolation.

Never bypass hooks or signing. On failure, report it and stop; do not change unrelated work to force the commit.

## Output

Reader: a developer who asked for a commit. They need to know whether it landed, what stayed out, and what to do next.

Line 1: one bold plain sentence, that answers the request. Never start it with a label, a verdict word, a hash, or a path.

Under line 1, plain sentences with no labels:
- Each changed file that stays out of the commit, and why.
- Each blocker, in plain words.

Before `**Next:**`, one line: `Verdict: <word>`, one of:
- `Committed`: the commit exists. Line 1 gives its short hash (commit ID).
- `Preview`: `--dry-run`. The message is printed; nothing changed.
- `Stopped`: the staged scope needs a decision, a prerequisite is missing, or the commit failed.

Committed or previewed: `## Commit message`, then the message in a `text` fence. Never reflow it.

Stopped with a choice to make: `**Next:**` holds at most 3 numbered options, default marked; they appear nowhere else. For mixed concerns, before the verdict, show the files as a tree, one concern per entry:

```text
invoice/tax.py    # fix: round tax per line
ops/Dockerfile    # build: pin base image
```

Hook rejection: say what the hook requires and what unblocks it. Do not narrate what was refused.

`**Next:**` holds the steps, in order. Then `**Changed:**` names the paths in the new commit, or `none`.

Reader rules:
- Define at first use: "staged (added for the next commit)", "hook (a repository check that runs on each commit)".

Example:

````markdown
**Your fix to `invoice/tax.py` is committed as `a1b2c3d`.**
`README.md` is not in it; it is still changed on disk.

## Commit message
```text
fix(invoice): round tax per line, not per total

Rounding the total hid cent differences on invoices with many lines.
```

Verdict: Committed

**Next:**
1. Push when ready: `git push`.
2. Commit `README.md` separately: stage it, then ask again.

**Changed:** `invoice/tax.py` in commit a1b2c3d.
````

Stopped example:

````markdown
**Nothing is staged, so there is nothing to commit yet.**
`invoice/tax.py` has changes, but they are not added for the next commit.

Verdict: Stopped

**Next:**
1. Add the file, then ask again: `git add invoice/tax.py` (default).
2. Stop; nothing changes.
````
