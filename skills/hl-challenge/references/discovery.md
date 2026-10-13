# Discovery lens

Before building, push the proposal back to the problem: which outcome, for whom, with what evidence, and what is the riskiest assumption.

## Principles

- Outcome over output. "Shipped 12 features" is not a result; a metric that moved is.
- Discovery is continuous, with real users every week, not a phase at kickoff. A team that cannot name a customer it spoke to recently is guessing.
- Stakeholder requests are inputs to discovery, not assignments.
- A feature factory has a roadmap of features, output metrics, and no learning loop. It ships the wrong thing efficiently.
- Four risks: value (will they want it), usability (can they use it), feasibility (can we build it), viability (does it work for the business). Test the riskiest first.
- Outcome at the top, opportunities below it, solutions at the leaves. A solution with no opportunity above it is an orphan.
- Prototypes exist to kill bad ideas cheaply, not to be shipped.
- Label every claim as hypothesis or validated, with the evidence.

## Modes

### `discover` (default)

1. **Outcome**: the metric ("better UX" is not a metric; "trial-to-paid conversion +X%" is).
2. **Whose problem**: the segment and the job to be done, not "users".
3. **Evidence**: interviews, support tickets, behavioral data, past experiments. None means unvalidated.
4. **Riskiest assumption**: value, usability, feasibility, or viability; pick the one most likely to kill it.
5. **Cheapest test**: hours to days, not weeks.
6. **Verdict**: `validated` / `unvalidated` / `unfalsifiable`.

### `validate`

Pressure-test the evidence claimed: sample (how many, which segment, recruited how), method (open interview or leading questions, usability test or demo, experiment or anecdote), falsifiability (which result would have killed the idea), causation (one variable or several at once). Output up to three things the evidence shows, up to three it does not, and `holds` / `weak` / `absent`.

### `kill`

Argue against building: opportunity cost, maintenance cost forever after, harder measurement with more features, duplication of something existing. Verdict: `kill` / `cut scope to X` / `build only after Y validates`.

### `prioritize`

Table: item, outcome it serves, main risk, evidence and discovery done, verdict (`keep` / `back to discovery` / `kill`). Overall verdict: the count per item verdict. The outcome decides, not stakeholder rank.

## Stand down

Internal-only engineering decisions (refactor, infrastructure, tooling) where users are not the deciding factor.
