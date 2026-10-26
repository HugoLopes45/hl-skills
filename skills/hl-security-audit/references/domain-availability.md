# Availability and operator cost

Use with [attack methods](attack-methods.md). This guide covers whether one principal's bounded effort can consume shared capacity or money beyond its allowance. Self-inflicted slowness is not a finding.

## Establish first

Build a table for each untrusted entry: earliest accepted size and cardinality, work done before authentication, downstream fan-out, persisted state, the shared pool consumed, the limit and its owner, cleanup on error or disconnect, and recovery behavior.

Name the shared resource: CPU, memory, disk, connections, worker slots, event-loop time, database capacity, quota or paid third-party calls.

## Review questions

### Amplification

- Can small accepted input drive superlinear work: pathological regular expressions, deep nesting, recursive validation, template expansion, graph traversal or adversarial hashing? Derive the accepted depth or cardinality from source.
- Is a limit enforced after every expansion stage: decompression, archive extraction, image or document decoding, and protocol compression tables?
- Can query parameters produce unbounded scans, joins, sorts, aggregations, page sizes or downstream calls? Confirm the authorization model does not intentionally allow the same scope.

### Retention

- Do bodies, streams, uploads, sessions, unique cache keys, metric labels, subscriptions or pending jobs accumulate without per-item and aggregate limits and expiry?
- Do malformed or cancelled requests leak sockets, files, cursors, timers, subprocesses, temporary files or references from a shared pool?
- Does a client timeout, disconnect or failed authorization leave database, model, network or worker activity running? Is cancellation propagated through each layer?

### Fairness and accounting

- Does expensive parsing, cryptography, decompression or an external call happen before authentication and the earliest size or rate check?
- Is quota accounting keyed on a dimension the requester controls, letting work escape its budget or consume another principal's allowance? Check overflow, distributed races, retries and reconnects.
- Can one principal hold locks, workers, database pools or scheduler priority needed by others beyond a deadline?

### Failure and recovery

- Can untrusted input reach a panic, abort, unhandled exception, process exit, lock cycle or infinite loop in a shared process? What does the supervisor restart?
- Do timeouts or dependency failures trigger synchronized or unbounded retries without ceilings, jitter or deduplication?
- Can one malformed record block a shared queue, partition, startup scan, migration or recovery loop?
- Does restart, restore or fallback rebuild unbounded state, ignore quotas, or replay the input that caused the failure?

## Decide

- Compare the requester's minimal effort with the shared cost. Require impact on other principals, shared quotas or operator spend.
- Missing rate limiting alone is a hardening note when no costly or shared effect follows.
- A restarted isolated worker reduces impact; it does not remove a reachable crash in shared code.
- Upstream limits at a proxy, gateway or platform may be outside source. Record them as `needs_validation` with the owner-observable setting.
- Never propose proof by exhausting a service. A future validation plan uses cost accounting from source, one small fixture or a bounded growth curve in an isolated environment.
