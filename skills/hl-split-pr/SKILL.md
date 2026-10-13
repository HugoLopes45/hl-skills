---
name: hl-split-pr
description: "Propose how to split a large diff into coherent, dependency-ordered pull requests without rewriting history. Use when a branch is too large to review as one change."
---
# Split PR

Input: `[base-branch]`

Resolve the input or the verified default branch as base. Read the full diff, changed paths, and commit log; if scope cannot be read, report the limitation rather than claiming a complete partition. No edits or history changes.

Group by independent behavior, separating refactors when they can stand alone. Keep tests and required configuration with their behavior. Assign binaries to their owning change, noting that content was not line-reviewed.

For each group: title, files or hunks, existing commits where applicable, delivered behavior, prior dependencies, verification, and rollback risks. Mark each group's build and test result unverified until run.

Account for every change once. Fewer than two coherent groups: report no clean split. Otherwise lead with a table in merge order: group, title, delivered behavior, depends on. Then each group's remaining fields, with its files as a file tree, and the unresolved coupling. Together, the groups must equal the branch diff against the base; if the base moved, list the differences.
