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

Never bypass hooks or signing. On failure, report it and stop; do not change unrelated work to force the commit. Report the new commit's hash and subject.
