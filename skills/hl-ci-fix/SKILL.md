---
name: hl-ci-fix
description: "Diagnose failing required checks on a pull request and apply bounded fixes without weakening tests or CI policy. Use only when the user explicitly asks to fix CI on a pull request."
---
# CI Fix

Input: `[pr-number, or empty for current PR]`

Resolve the input or the current branch's PR. Verify checkout matches its head and is not the base branch. Missing PR, access, or matching checkout: stop. Preserve unrelated changes.

Explicit invocation authorizes scoped fixes, commits, and normal pushes for this PR, not merging branches, force-pushing, or deployment changes. Confirm additional authority when the required action exceeds that scope.

Inspect required checks through available GitHub tooling. Wait for pending runs up to 20 minutes; still pending: report them as pending. For failures, read the actual failing check's logs; not every check is GitHub Actions.

Fix one evidenced cause, run the relevant local check, commit only scoped changes, and push without bypassing hooks. Re-query checks for the new head. Do not weaken tests, assertions, or required-check policy to obtain green.

Suspected flakes need evidence; retry once and report both outcomes. Stop after two unsuccessful scoped attempts, unavailable logs, or an infrastructure or permission blocker.

Lead with the PR, its head, and whether the required checks are green. Then a table, one row per check and attempt: attempt, check, status, cause and fix, commit. Links follow the table, then retries and unresolved checks. Green applies only to the required checks observed for that revision.
