---
name: hl-discover
description: "Orient in an unfamiliar repository or one area of it: purpose, stack, git state, build and test commands, and, in full mode, a source-backed map of layout, responsibilities, callers, entry points, boundaries, dependencies, and a read order. Use when starting work in a new or unfamiliar codebase, when the user asks how a part of the code is organized or where to start reading, or when another agent needs a context pack."
---
# Discover

Input: `[--depth quick|full] [--scope <path>]`

Defaults: scope is the repository; depth is quick for the repository, full for a narrower scope. Not a Git repository: report it and stop. No commits: continue and make no history claims.

Read-only: no installs, checkout changes, builds, or tests, and never run discovered scripts or executables. Use a code index only if it is current; otherwise targeted search and bounded reads. Never dump the repository. Skip dependency, generated, and build directories unless the scope targets them. Report the scope covered and anything truncated.

## Quick

Report:
- Purpose, from README and manifests.
- Languages and declared tools.
- Branch or detached revision, uncommitted changes, recent commits.
- Upstream comparison, if any, labeled as from remote-tracking refs that may be stale.
- Git operations in progress (merge, rebase, cherry-pick, bisect). In worktrees and submodules `.git` is a file; locate the real directory with `git rev-parse --git-dir`.
- Build, test, and lint commands found in project config or docs, as a table: command, purpose, source file. Never infer a command from the stack name.
- Constraints found in docs or config (for example required runtime versions, contribution rules) and the next action.

Never declare the repository safe from metadata alone.

## Full

`--scope` may name a path, module, or topic. Resolve it to source paths; several matches: list them and ask. For a scoped area, lead with its responsibilities, direct callers and callees, entry points, and a read order; show the flow of each entry point in that order as a call tree with `file:line`, from files you read.

The map, of the scoped area or else the repository, is a shallow file tree, one responsibility per entry. Its size sets its depth: up to 8 nodes, flat; up to 25, grouped by responsibility; more, clusters with drill-down paths. Prefer a compact map with drill-down paths over exhaustive catalogs.

Add only the sections that apply, each with source anchors and its gaps:
- The map, entry points, public interfaces.
- Module dependencies as an indented tree, each cycle marked `(cycle -> <module>)`, only from index or parser output. Regex matches alone are candidates.
- Key types, schemas, contracts, migrations. File order is not deployment state; the last applied migration is unknown without state evidence.
- I/O boundaries: environment variable names, network destinations, persistence, filesystem writes, subprocesses. Never read or print credential values.
- Declared stack and lockfile-resolved versions. Installed does not mean used.
- History or churn when useful; existing architecture docs.

Context pack for another agent: add YAML with `project`, `git_branch`, `git_sha`, `git_dirty`, `manifests`, `scope`, `generated_at`, `sections_ok`, `sections_failed`. Use `null` or `unknown` for fields you cannot determine. Include counts or LOC only when measured, with scope and method. Characters divided by four is a token estimate; label it so.

Label each empty result: absent, not searched, unsupported, failed, or truncated. Never mask a command error (for example `|| true`) or report a failed section as "none detected". After a failure, continue the independent sections and report partial coverage.

With subagents, you may delegate independent bounded questions. Never present inline work as delegated or as independent verification.
