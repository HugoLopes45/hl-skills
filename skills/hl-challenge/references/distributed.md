# Distributed lens

Assume every component fails in the worst way at the worst moment. Check what the design claims against what it does under partitions, clock skew, crashes, and retries.

## Principles

- Documentation is not behavior. Read the docs, then the issue tracker, then any public fault-injection analysis (for example from jepsen.io). The absence of such testing is a finding. Without web access, list these sources as unchecked.
- The adversary is the network, the clock, the disk, and the pause, not an attacker.
- Linearizability is the strongest common guarantee. A claim of it needs evidence. Name the guarantee the workload actually needs, not the strongest one.
- Reason with happens-before, not wall-clock time. Comparing timestamps across machines is a category error.
- At-least-once delivery plus a non-idempotent handler means duplicate operations in production.
- A lock with a time-to-live is not a lock. Without a fencing token, two holders can act at once.
- Where possible, design to converge after disagreement instead of agreeing before acting.
- "Eventually consistent" is incomplete: under which failure, within which bound, with which read guarantee?

## Modes

### `audit` (default)

1. **The claim**: quote the exact consistency, availability, or durability claim.
2. **Failure table**: ID, failure, current behavior, outcome. Cover at least: partition between nodes, clock skew, crash mid-write, concurrent writers to one key, duplicate delivery, a slow node treated as dead, a disk that lies about fsync, read-your-writes after failover, replication lag. Outcome is one of `safe`, `degraded but correct`, `data loss`, `silent corruption`, `unknown (untested)`.
3. **Deal-breakers**: every `data loss`, `silent corruption`, or `unknown` row that touches user-visible state.
4. **Required invariants**: idempotence keys, monotonic IDs, fencing tokens, quorums; for each, where it is enforced or that it is not.
5. **Verdict**: `safe under <scenarios>` / `unsafe under <scenarios>` / `untested, assume unsafe`.

### `test-plan`

The user claims the system survives failure X. Design the test that would prove them wrong: setup (cluster shape, seed state, invariant), fault to inject and tool (for example Toxiproxy, `tc`, process kill, clock skew), concurrent workload, checker (linearizability, no lost updates, monotonic reads), and the expected result in each case. Prose, not code.

### `sources`

For a piece of infrastructure (database, queue, lock service, consensus library), list up to 5 sources: public fault-injection analyses, failure-related issues, papers on the algorithm, production incident reports. One line each on what to take from it. Never invent a source, title, or URL; say when none exist. Without web access, list only sources you are certain exist, marked unverified.

## Stand down

Single-process programs with no shared state across machines. Do not demand formal specs or fault-injection suites there.
