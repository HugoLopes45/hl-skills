---
name: hl-checkpoint
description: "Before clearing or compacting the conversation context, check that decisions, evidence, pending work, and the next action are saved, and that the worktree state is deliberate. --stuck diagnoses why work is going in circles (repeated fixes, the same failure coming back, a growing diff, no progress) and names the cause and the one change that breaks the loop. Use when a work phase ends, before a context reset, or when the user or agent is stuck, looping, or keeps retrying the same thing."
---
# Checkpoint

Input: `[--stuck]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Keep the saved handoff sufficient to resume without this conversation. Report what is saved, what remains unsaved, and what the next session needs.

Inspect the worktree state and any existing handoff file. A clean tree or a non-Git directory does not prove the context is saved.

Save objective, decisions, evidence, pending work, and next action where the project's handoff rules say. Exclude secrets. Read the complete saved file, continuing truncated reads, and verify every required handoff item before reporting it saved. A preview or successful write is not readback. Compare the saved claims and completion report with the observed files and tool results. Attribute carried history to its originating notes and mark it unverified unless current evidence confirms it. Record file dates as timestamps, not proof of unchanged content or session continuity. Preserve unresolved work; absence of an edit does not prove work never started. No rule: ask the user for a path. Do this before recommending a context reset.

Pre-existing project changes need disposition: honor an explicit instruction to keep them; otherwise ask and wait. In a Git repository, offer commit, stash, leave in place, or abort. Outside Git, offer leave in place or abort; commit and stash are unavailable. The requested handoff update alone needs no separate disposition. Never commit or stash on your own. A requested stash uses `git stash push --include-untracked`, never `--all`, so ignored files such as credentials stay out; then check `git stash list` and `git status` before continuing.

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

Line 1: one bold plain sentence, that answers "is it safe to clear now?" or, with `--stuck`, "why am I going in circles?". Never start it with a label, a verdict word, a path, or a cause name.

Under line 1, plain sentences with no labels: whether the handoff is saved, what happens to the changed files, and anything not checked when that limits the answer.

Before `**Next:**`, one line: `Verdict: <word>`, one of:
- `Saved`: the handoff is written and verified by complete readback. Line 1 names its path.
- `Stopped`: the location is unknown, or writing or complete readback could not be verified.
- `Stuck, <cause>` (`--stuck` only): the cause from the list above, in plain words, e.g. `Verdict: Stuck, missing context`.

Saved:
- `## Changed files`: a tree in a `text` fence, one state per entry (`# modified`, `# new, not committed`).
- When pre-existing changes need a decision, Next holds one disposition question, with the applicable options above and leave in place as default. Define stash as changes set aside and kept, restored with `git stash pop`. The body reports their state without repeating the choice.
- When something is left out of the handoff, name it and explain any effect on resuming the work.

`--stuck`:
- `## Attempts`: a table with columns attempt, what changed, observed result. Short cells. A result never observed is "not run".
- `## Leftover changes`: a file tree of changes from failed attempts.
- One sentence names the input the attempts got wrong, from the files you read.

Stopped: line 1 names the missing location or failed write or readback. Say what remains unverified; do not recommend clearing. Next gives at most 3 ways to resolve that blocker, default marked. Clearing loses unsaved conversation notes, not files on disk.

`**Next:**` holds every reader action, decision, prerequisite, and unblock route once, in order. A reset follows a saved handoff and the agreed handling of changed files, never a missing location or an abort. Then `**Changed:**` names the handoff file, or `none`.

Reader rules:
- Define at first use: "handoff" (notes the next session reads), "stash" (changes set aside and kept), "working copy" (your files on disk).
- Never write that uncommitted files are lost, or that clearing the context loses them.
- In `--stuck`, name the cause in plain words, never "you kept retrying".

Example:

````markdown
**Your handoff is saved in `docs/handoff.md`; your changed files remain on disk.**

## Changed files
```text
invoice/tax.py      # modified
tests/test_tax.py   # new, not committed
```

Verdict: Saved

**Next:**
1. What should happen to the changed files: commit them; leave them in place (default); stash them with `git stash push --include-untracked` (set aside and kept, restored with `git stash pop`); or abort and keep this conversation?
2. After the chosen handling is complete, clear the context unless you chose abort. The handoff keeps the next step.

**Changed:** `docs/handoff.md` (new).
````
