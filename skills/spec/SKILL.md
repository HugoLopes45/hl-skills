---
name: spec
description: "Draft a grounded feature plan: problem, scope, observable acceptance criteria, assumptions, failure scenarios, and open decisions. --handoff writes it as a brief for another agent to implement. --prd instead writes a full sourced product and technical specification (PRD) in sections, with explicit assumptions, research, and review gaps. Use when the user wants to plan a feature before implementing it, to hand a feature to another agent, or a full product requirements document for a new product or major feature. Not for splitting a plan into tickets (use `tickets`)."
---
# Spec

Input: `[feature, selected option, or brief path] [--handoff | --prd]`

Plan the input; if empty, the latest selected option, interview summary, or feature the user described. No feature or testable goal: name what is missing and stop. Several independent features: one plan each.

Return, in this order:
- Problem and requested outcome, with its source.
- In-scope behavior and exclusions that matter. No padding to a count.
- Shape of the change, limited to what must be agreed before coding: new or changed types and signatures, and the call tree or file tree with new nodes marked `[new]`. For an existing structure, show a `diff` of it.
- Acceptance criteria as a table: id (`AC-1`, `AC-2`, ...), actor, input or boundary, observable result, verification method. The method is a command or an observation a person can make without reading the code; a criterion without one keeps an empty method and also goes under Decisions needed.
- Assumptions with evidence; open questions separately.
- Failure scenarios that apply (malformed input, dependency failure, retries, races, partial writes), as a table: scenario, detection, response.
- Decisions needed, with owner when known and the evidence that would settle each.

Evidence rules:
- Verify that every cited path and symbol exists.
- External API behavior: cite docs or source for the version in use or proposed. An installed dependency proves nothing about its defaults or guarantees.
- Mark proposed files and tests `[new]`.
- Never invent executed checks, expected log text, metrics, or user requirements.

Plan only; do not implement. The plan must be usable without running another skill first.

## Handoff

With `--handoff`, rewrite the plan as a brief for an agent that has none of this context. Return it in the reply; save it only to a path the user gives.
- Add what triggers the behavior and the invariants it must keep.
- Keep contract literals exact (field names, status codes, error strings). Drop line numbers and incidental paths; mark kept paths as "recheck".
- Keep the `AC-N` ids. A criterion without a verification method blocks the handoff: list it and stop.
- Tell the receiving agent: before implementing, inspect current source, recheck preconditions, and report conflicts; choose the smaller interpretation only when it keeps the stated contract.

## PRD

With `--prd`, follow [references/prd.md](references/prd.md) instead of the sections above.
