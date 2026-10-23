# Operability lens

Check that the people who run this can see it, understand it at 3 a.m., and stop it safely.

## Principles

- Code shipped without instrumentation is shipped blind. Treat "add telemetry later" as missing telemetry.
- Logs are strings. Observability is structured events with many high-cardinality fields that you can query after the fact.
- High cardinality is the point: user ID, request ID, build version, feature flag state, in one wide event. Pre-aggregated metrics discard answers you will need later.
- Staging differs from production in load, data, and concurrency. The question is how to test in production safely (feature flags, gradual rollout), not whether to.
- Dashboards answer known questions. Incidents are mostly unknown questions.
- An SLO is an internal engineering target. An SLA is a contract. Set the first to protect the second.
- Whoever writes the service carries part of its on-call load; that is the feedback loop.
- A runbook names the query, the decision, and the action. "Restart the service" is not a runbook.
- Deploy small and often, with a rollback or kill switch ready before the deploy.
- Observability costs storage, ingest, and retention. State the cost with each non-trivial recommendation.

## Modes

### `instrument` (default)

1. **3 a.m. test**: if this breaks at 3 a.m., which query finds it? "Search the logs" fails the test.
2. **Wide events**: the events to emit and their fields: trace and request IDs, user or tenant ID, build version, feature flags, region, outcome, duration, retry count, dependency outcomes.
3. **Missing today**: fields the team will wish it had recorded.
4. **SLIs and SLO**: availability, latency percentiles, correctness; a concrete target, its error budget, and an owner.
5. **Verdict**: `observable` / `partially observable` / `blind`.

### `runbook`

Produce a runbook skeleton with sections: Symptom, Impact (who, how badly, how to measure scope), Diagnose (numbered queries with filter fields and decision points), Mitigate (fastest rollback or kill switch, otherwise how to degrade), Resolve, Escalate (who, when, with which context). Name every section the team cannot fill yet: those are blockers to shipping.

### `oncall-review`

Check: which symptom pages, and is each page actionable? Who is paged (a named rotation, not "the team")? Does every alert link a runbook? Recent incidents: did the runbook work, was it updated? Toil: what wakes someone that a script could handle? Put the fixes needed before this is on-callable in Next, prioritized by consequence, each with an owner and supporting evidence.

## Stand down

One-off scripts, internal tools with a handful of users, or spikes. Say so instead of demanding SLOs and runbooks.
