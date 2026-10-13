---
name: checkpoint
description: "Before clearing or compacting the conversation context, check that decisions, evidence, pending work, and the next action are saved, and that the worktree state is deliberate. --stuck diagnoses why work is going in circles (repeated fixes, the same failure coming back, a growing diff, no progress) and names the cause and the one change that breaks the loop. Use when a work phase ends, before a context reset, or when the user or agent is stuck, looping, or keeps retrying the same thing."
---
# Checkpoint

Input: `[--stuck]`

Inspect the worktree state and any existing handoff file. A clean tree or a non-Git directory does not prove the context is saved.

Save objective, decisions, evidence, pending work, and next action where the project's handoff rules say. No rule: ask the user for a path. Do this before recommending a context reset.

Changes remain: offer commit, stash, leave files in place, or abort, and wait for the user's choice. Never commit or stash on your own. A requested stash uses `git stash push --include-untracked`, never `--all`, so ignored files such as credentials stay out; then check `git stash list` and `git status` before continuing.

Report the handoff path, what happened to the worktree, and anything not saved. Never clear the context yourself. Uncommitted files are not lost; do not say they are.

## Stuck

With `--stuck`, diagnose the loop before any other attempt. Edit nothing.

1. List the attempts in this conversation: what changed, the check run, its observed result. A result never observed is "not run".
2. Find the cause, from this list, with the attempts that show it:
   - **Unchecked hypothesis**: fixes target a cause nothing has confirmed. Next: `debug`.
   - **No reliable check**: no command shows pass or fail, or its result varies between runs. Next: build that command first.
   - **Missing context**: a file, doc, log, or version the work depends on was never read. Next: read it, named.
   - **Task too large**: the diff keeps growing, or each fix breaks another part. Next: `tickets` on the goal.
   - **Unclear goal**: done is not defined, or two requirements conflict. Next: one question to the user.
   - **Context saturated**: earlier decisions are repeated or contradicted. Next: the checkpoint above, then a reset.
3. Revert nothing. List the changes from failed attempts that are still in the worktree.

First line: the cause and the next action. Then a table: attempt, change, check, observed result. Then the leftover changes. Do not start the next attempt until the user agrees.
