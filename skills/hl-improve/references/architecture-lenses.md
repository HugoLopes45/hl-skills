# Architecture lenses

Used by the `arch` focus. Judge every lens against what the repository is trying to be: a CRUD API and an event-sourced platform have different bars. Pass available audit evidence to the deps lens. Uploading private dependency metadata requires approval; otherwise report the audit unavailable.

Finding format: `[SEVERITY] file:line | finding | why it matters | effort S/M/L`. CRITICAL defeats a core safety or operational requirement; HIGH causes material failure or change risk; MEDIUM has limited impact; LOW is minor. Support severity with a concrete consequence.

- **dead-code**: apparently unused exports, after checking public consumers, configuration, and dynamic use; files neither imported nor an entrypoint; commented-out blocks older than a few commits (git blame); flags always on or off; a later route, listener, or middleware registration shadowing an earlier one; tests asserting nothing (`expect(true).toBe(true)`, permanent `skip`/`xit`).
- **duplication**: near-identical functions under different names; copy-pasted validation, error handling, transforms; parallel `utils/` and `helpers/`; data kept in sync by hand; one config value hardcoded in several files.
- **coupling**: circular imports; modules whose dependencies cause demonstrated coupling or change risk; reaching into another module's internals; shared mutable state as a channel; files that always change together with no declared dependency; domain logic spread across the call stack.
- **overengineering**: abstractions with one user (factory for one type, interface with one implementor and no test double, plugin system with no plugins); indirection buying nothing (Visitor over a 3-case switch, Observable for a value set once); generics every caller instantiates the same way; wrappers adding no behavior; DI containers with nothing swapped.
- **incoherence**: stated structure vs actual (feature folders that are really layers); one concept under several names (`user`/`account`/`member`); error contract varying per module (throw, Result, null, callback); mixed async styles; catch-all folders (`utils/`, `common/`, `misc/`) with no ownership rule; naming and test-placement conventions that differ per folder; env vars overlapping, undocumented, or read only on a dead path.
- **layering**: routes or components hitting persistence directly; business rules in middleware or migrations; logging, auth, error formatting re-done per handler; dependency direction reversed (repository importing a controller, domain entity importing a DB driver type); permission checks in the view or client.
- **deps**: outdated majors with security fixes behind; two libraries for one job (`moment`+`date-fns`, `axios`+`fetch`); packages with maintenance or deprecation problems confirmed from checked project notices and release history; audit CVEs grouped by severity; license terms that conflict with the verified use and distribution model; dev deps in the prod bundle; no lockfile, linter, or formatter.
- **scalability**: blocking I/O on hot paths of an async runtime; N+1 queries; list endpoints without pagination; in-memory state with no eviction or restart story; pub/sub without backpressure; pure functions tested while the integration path that fails in production is not.

## Report

`arch` writes `arch-report.md` in the repository root instead of the findings table. Every sentence is a finding with evidence or a recommendation with a reason.

```markdown
# Architecture audit: <repo>
Commit <short sha>. Scope: <what was audited, what was skipped>. Mode: quick | standard | deep.

## Executive summary
Supported points a decision-maker can act on: the problem, its cost if left, the fix category.

## Findings
| # | Severity | Finding (lens) | Evidence | Recommendation (effort) |
|---|---|---|---|---|

Sorted by severity, then smallest effort first. Prose under the table only for a finding a cell cannot hold.

## Dependency health
| Package | Status | Current | Latest | Action |
|---|---|---|---|---|

Audit output: <n> vulnerabilities (<n> critical, <n> high).

## Roadmap
Order actions by demonstrated impact, effort, and dependencies. Use dates only when the user's planning horizon supports them. Prefer existing checks for recurring mechanical failures; do not prescribe new CI for every finding. Each selected item gets its own plan via `hl-improve plan <item>`.

## Considered and dismissed
| Finding | Lens | Why dismissed |
|---|---|---|

## Not audited
Directories skipped, lenses not run.
```
