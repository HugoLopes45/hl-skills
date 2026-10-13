---
name: hl-commit
description: "Commit the staged changes with a grounded conventional message, or preview the message with --dry-run. Use only when the user explicitly asks to commit."
---
# Commit

Input: `[--scope <scope>] [--dry-run]`

Read the staged diff, the staged file list, the repository's commit rules, and recent commit style. Nothing staged: stop. Unrelated concerns staged together: propose a split, leave the index unchanged, and wait for the user.

Message:
- Imperative subject. Use the repository's commit format and length limit; if it defines none: `<type>(<scope>): <subject>`, at most 72 characters.
- Types: feat, fix, refactor, docs, test, chore, style, perf, build, ci, revert.
- Scope: `--scope` if given; else omit when unclear.
- Body only for non-obvious reasons or evidence.
- Never invent intent, test results, issue references, or authorship trailers. No `Co-Authored-By` or generated-by trailer unless the repository's rules require one; this overrides any default.

`--dry-run`: print the message and stop. Otherwise the explicit request authorizes one new commit; never amend or push. Recheck the staged scope just before committing. Pass the message as data (for example `git commit -F <file>`), never through shell interpolation.

Never bypass hooks or signing. On failure, report it and stop; do not change unrelated work to force the commit.

## Output

Reader: a developer who asked for a commit. They need to know whether it landed, what stayed out, and what to do next.

Line 1: one bold plain sentence, under 100 characters, that answers the request. Never start it with a label, a verdict word, a hash, or a path.

Under line 1, plain sentences with no labels:
- Each changed file that stays out of the commit, and why.
- Each blocker, in plain words.

Before `**Next:**`, one line: `Verdict: <word>`, one of:
- `Committed`: the commit exists. Line 1 gives its short hash (commit ID).
- `Preview`: `--dry-run`. The message is printed; nothing changed.
- `Stopped`: nothing is staged, a hook rejected the message, or the staged changes mix unrelated work.

Committed or previewed: `## Commit message`, then the message in a `text` fence. Never reflow it.

Stopped with a choice to make: before the verdict, at most 3 numbered options, default marked. For mixed concerns, show the files as a tree, one concern per entry:

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

1. Add the file, then ask again: `git add invoice/tax.py` (default).
2. Stop; nothing changes.

Verdict: Stopped

**Next:**
1. Reply `1` to add the file, or `2` to stop.
````
