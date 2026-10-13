---
name: open-pr
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

`--dry-run`: print the title and body and stop. Otherwise the request authorizes a normal push if needed and PR creation. Local and remote branch diverged: stop. Never force-push or bypass repository checks. Pass the body through a file or safely quoted input. Assign as the user's rules say. Report the URL and any blockers.
