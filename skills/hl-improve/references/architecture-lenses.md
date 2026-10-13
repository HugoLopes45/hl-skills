# Architecture lenses

Used by the `arch` focus. Judge every lens against what the repository is trying to be: a CRUD API and an event-sourced platform have different bars. Run the package manager's audit command during recon and pass its output to the deps lens.

Finding format: `[SEVERITY] file:line | finding | why it matters | effort S/M/L`. CRITICAL blocks scaling or causes production bugs; HIGH hurts every future change; MEDIUM is a smell to fix this quarter; LOW is minor.

- **dead-code**: exports with zero inbound imports repo-wide; files neither imported nor an entrypoint; commented-out blocks older than a few commits (git blame); flags always on or off; a later route, listener, or middleware registration shadowing an earlier one; tests asserting nothing (`expect(true).toBe(true)`, permanent `skip`/`xit`).
- **duplication**: near-identical functions under different names; copy-pasted validation, error handling, transforms; parallel `utils/` and `helpers/`; data kept in sync by hand; one config value hardcoded in several files.
- **coupling**: circular imports; god modules (fan-out over 10, high fan-in, both is a crisis); reaching into another module's internals; shared mutable state as a channel; files that always change together with no declared dependency; domain logic spread across the call stack.
- **overengineering**: abstractions with one user (factory for one type, interface with one implementor and no test double, plugin system with no plugins); indirection buying nothing (Visitor over a 3-case switch, Observable for a value set once); generics every caller instantiates the same way; wrappers adding no behavior; DI containers with nothing swapped.
- **incoherence**: stated structure vs actual (feature folders that are really layers); one concept under several names (`user`/`account`/`member`); error contract varying per module (throw, Result, null, callback); mixed async styles; catch-all folders (`utils/`, `common/`, `misc/`) with no ownership rule; naming and test-placement conventions that differ per folder; env vars overlapping, undocumented, or read only on a dead path.
- **layering**: routes or components hitting persistence directly; business rules in middleware or migrations; logging, auth, error formatting re-done per handler; dependency direction reversed (repository importing a controller, domain entity importing a DB driver type); permission checks in the view or client.
- **deps**: outdated majors with security fixes behind; two libraries for one job (`moment`+`date-fns`, `axios`+`fetch`); abandoned packages (no publish in 18 months, no successor); packages the ecosystem left (`request`, `tslint`); audit CVEs grouped by severity; GPL/AGPL in proprietary code; dev deps in the prod bundle; no lockfile, linter, or formatter.
- **scalability**: blocking I/O on hot paths of an async runtime; N+1 queries; list endpoints without pagination; in-memory state with no eviction or restart story; pub/sub without backpressure; pure functions tested while the integration path that fails in production is not.

## Report

`arch` writes `arch-report.md` in the repository root instead of the findings table. Every sentence is a finding with evidence or a recommendation with a reason.

```markdown
# Architecture audit: <repo>
Commit <short sha>. Scope: <what was audited, what was skipped>. Mode: quick | standard | deep.

## Executive summary
Three to five bullets a decision-maker can act on: the problem, its cost if left, the fix category.

## Findings
| # | Severity | Finding (lens) | Evidence | Recommendation (effort) |
|---|---|---|---|---|

Sorted by severity, then smallest effort first. Prose under the table only for a finding a cell cannot hold.

## Dependency health
| Package | Status | Current | Latest | Action |
|---|---|---|---|---|

Audit output: <n> vulnerabilities (<n> critical, <n> high).

## Roadmap
1. This sprint: every CRITICAL, plus HIGH with effort S.
2. This quarter: remaining HIGH, each with the guardrail (lint rule, boundary check, CI step) that stops it coming back.
3. This half: MEDIUM, dependency migrations, structural moves. Each item gets its own plan via `hl-improve plan <item>`.

## Considered and dismissed
| Finding | Lens | Why dismissed |
|---|---|---|

## Not audited
Directories skipped, lenses not run.
```
