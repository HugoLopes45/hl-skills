---
name: hl-checkpoint
description: "Before clearing or compacting the conversation context, check that decisions, evidence, pending work, and the next action are saved, and that the worktree state is deliberate. --stuck diagnoses why work is going in circles (repeated fixes, the same failure coming back, a growing diff, no progress) and names the cause and the one change that breaks the loop. Use when a work phase ends, before a context reset, or when the user or agent is stuck, looping, or keeps retrying the same thing."
---
# Checkpoint

Input: `[--stuck]`

Inspect the worktree state and any existing handoff file. A clean tree or a non-Git directory does not prove the context is saved.

Save objective, decisions, evidence, pending work, and next action where the project's handoff rules say. No rule: ask the user for a path. Do this before recommending a context reset.

Changes remain: offer commit, stash, leave files in place, or abort, and wait for the user's choice. Never commit or stash on your own. A requested stash uses `git stash push --include-untracked`, never `--all`, so ignored files such as credentials stay out; then check `git stash list` and `git status` before continuing.

Never clear the context yourself. Uncommitted files are not lost; do not say they are.

## Stuck

With `--stuck`, diagnose the loop before any other attempt. Edit nothing.

1. List the attempts in this conversation: what changed, the check run, its observed result. A result never observed is "not run".
2. Find the cause, from this list, with the attempts that show it:
   - **Unchecked hypothesis**: fixes target a cause nothing has confirmed. Next: `hl-debug`.
   - **No reliable check**: no command shows pass or fail, or its result varies between runs. Next: build that command first.
   - **Missing context**: a file, doc, log, or version the work depends on was never read. Next: read it, named.
   - **Task too large**: the diff keeps growing, or each fix breaks another part. Next: `hl-tickets` on the goal.
   - **Unclear goal**: done is not defined, or two requirements conflict. Next: one question to the user.
   - **Context saturated**: earlier decisions are repeated or contradicted. Next: the checkpoint above, then a reset.
3. Revert nothing. List the changes from failed attempts that are still in the worktree.

Do not start the next attempt until the user agrees.

## Output

Reader: a person about to clear or compact the conversation. They need to know whether the work is saved, what happens to changed files, and whether clearing is safe now.

Line 1: one bold plain sentence, under 100 characters, that answers "is it safe to clear now?" or, with `--stuck`, "why am I going in circles?". Never start it with a label, a verdict word, a path, or a cause name.

Under line 1, plain sentences with no labels: whether the handoff is saved, what happens to the changed files, and anything not checked when that limits the answer.

Before `**Next:**`, one line: `Verdict: <word>`, one of:
- `Saved`: the handoff file is written. Line 1 names its path.
- `Stopped`: the project rules name no handoff location; ask for one.
- `Stuck, <cause>` (`--stuck` only): the cause from the list above, in plain words, e.g. `Verdict: Stuck, missing context`.

Saved:
- `## Changed files`: a tree in a `text` fence, one state per entry (`# modified`, `# new, not committed`).
- When changes remain, a sentence asks what happens to them, then numbered options, default marked, before the verdict: commit them; leave them in place; stash them with `git stash push --include-untracked` (set aside, kept, restored with `git stash pop`); abort.
- When something is left out of the handoff, one sentence says so and names it.

`--stuck`:
- `## Attempts`: a table with columns attempt, what changed, observed result. Short cells. A result never observed is "not run".
- `## Leftover changes`: a file tree of changes from failed attempts.
- One sentence names the input the attempts got wrong, from the files you read.

Stopped: line 1 says what is missing and why it blocks. Then the question as one sentence, then the verdict. `**Next:**` holds at most 3 numbered options, default marked; they appear nowhere else.

`**Next:**` holds the steps, in order. Then `**Changed:**` names the handoff file, or `none`.

Reader rules:
- Define at first use: "handoff" (notes the next session reads), "stash" (changes set aside and kept), "working copy" (your files on disk).
- Never write that uncommitted files are lost, or that clearing the context loses them.
- In `--stuck`, name the cause in plain words, never "you kept retrying".

Example:

````markdown
**Your handoff is saved in `docs/handoff.md`. You can clear the context; your files stay on disk.**

## Changed files
```text
invoice/tax.py      # modified
tests/test_tax.py   # new, not committed
```

Choose what happens to these files (default: 2):
1. Commit them first; the handoff then needs no file list.
2. Leave them in place. Nothing moves; the next session finds them.
3. Stash them: `git stash push --include-untracked`. Restore with `git stash pop`.
4. Abort. Nothing more is done; the handoff stays.

Verdict: Saved

**Next:**
1. Reply with an option number (default: 2).
2. Clear the context when ready. The handoff keeps the next step.

**Changed:** `docs/handoff.md` (new).
````
