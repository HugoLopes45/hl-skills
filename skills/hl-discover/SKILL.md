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

## Output

Reader: a developer or new team member who just opened this repository and must decide where to read first and what to run first.

Line 1, bold: one plain sentence, under 100 characters, that says what the project is in everyday words, then the fact that changes the next step. Effect before name ("Books garden plot bookings by the season; 2 files have edits not committed."). Never opens with a label, verdict word, count, or path.

Under line 1, plain sentences without labels, only when they change the reader's next step: uncommitted or in-progress git operations, failed or truncated sections, and any credential or security risk seen out of scope ("outside what you asked"), its value never printed. Add one sentence on what was read and what was not run, when that limits the answer: "I read the whole repository at quick depth; I did not install, test, or run project code."

Then the body as numbered points, each a bold plain sentence with one or two sentences and one view:
- Commands: a table of command, what it does, source file. Absent: "No build target in `Makefile` or `README.md`."
- Layout (full): shallow file tree, one responsibility per entry.
- Entry points (full): call tree in a `text` fence, `file:line` per node.
- Module cycles: indented tree with `(cycle -> <module>)`.
- Read order (scoped): numbered list.
- Context pack: YAML, unchanged, placed before the verdict line.

Indent each view under its point.

Stopped: line 1 says what is missing and why it blocks. Then `Verdict: Stopped`, then up to 3 numbered ways to unblock, default marked:
- Not a Git repository: `**This folder is not a Git project (Git is the version-history tool), so I cannot map it.**`, then 1. Run discover from the clone's root (default). 2. Give the path of a Git clone.
- Scope matches several places: `**Scope "<name>" matches several places, so I need you to pick one.**`, the matches as numbered options, one per line, default marked, then "Which one do you mean?"

Reader rules:
- Define each term once: "CI (automated checks on each push)", "cycle (modules that import each other)", "Git (the version-history tool)". Avoid HEAD, upstream, worktree, LOC unless defined.
- Tag each claim once per table column or group, not on every line.
- Exact paths, commands, and error text stay exact.
- Number with unit and meaning: "9 source files, 109 lines of Python (`wc -l`)".
- Name what was not run: "I did not install, test, or run project code."
- Upstream data is the last fetched state of the remote, which may be out of date.
- Never print a credential value. Name the variable and `file:line`.
- No process narration beyond the coverage statement. No alarm words.

End: `Verdict: <word>` on its own line, then `**Next:**`:
- `Mapped`: every requested section ran.
- `Partly mapped (<section>)`: a section failed or was truncated; name it.
- `Stopped`: the map cannot start yet; see Stopped.

`**Next:**` has one step per line, each something the reader can do now: a command to run, a file to open, a question to answer.

Example (plain structure, not a fixed answer):

````markdown
**A Go API that books garden plots by the season; 2 files have edits not committed.**
I read the whole repository at quick depth; I did not install, test, or run project code.
`config/dev.env:3` holds a token-looking value. I did not print it; rotate it if it is live (outside what you asked).

1. **`make test` and `make lint` run the tests and the linter.**
   | Command | What it does | Source |
   |---|---|---|
   | `make test` | runs `go test ./...` | `Makefile:4` |
   | `make lint` | runs `golangci-lint run` | `Makefile:7` |

   No build target in `Makefile`; `go build ./cmd/api` appears only in `README.md:21`.

2. **A booking request reaches the pricing code that has the uncommitted edit.**
   ```text
   cmd/api/main.go:12                 main()          # starts the HTTP server
   `-- internal/booking/handler.go:30 CreateBooking() # reads the request
       `-- internal/pricing/hourly.go:8 Quote()       # changed, not committed
   ```

Verdict: Mapped

**Next:**
1. Run `make test` yourself; discover did not run it.
2. Open `internal/pricing/hourly.go` first: it holds the uncommitted edits.
````
