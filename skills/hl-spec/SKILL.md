---
name: hl-spec
description: "Draft a grounded feature plan: problem, scope, observable acceptance criteria, assumptions, failure scenarios, and open decisions. --handoff writes it as a brief for another agent to implement. --prd instead writes a full sourced product and technical specification (PRD) in sections, with explicit assumptions, research, and review gaps. Use when the user wants to plan a feature before implementing it, to hand a feature to another agent, or a full product requirements document for a new product or major feature. Not for splitting a plan into tickets (use `hl-tickets`)."
---
# Spec

Input: `[feature, selected option, or brief path] [--handoff | --prd]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Build check reports from recorded command/result pairs, copying commands verbatim. Include the directory and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Mark result excerpts and reconcile counts with the records.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Keep the plan complete and separate proposed work from existing behavior. State blocking decisions; the wrapper's Next refers to the plan without repeating its questions or steps.

Plan the input; if empty, the latest selected option, interview summary, or feature the user described. No feature or testable goal: name what is missing and stop. Several independent features: one plan each.

Return, in this order:
- Problem and requested outcome, with its source.
- In-scope behavior and exclusions that matter. State each accepted input domain. Use explicit contracts for required domains; otherwise propose the narrowest domain covering supplied examples. Keep other inputs unspecified and wider support an open decision. Check every invariant, including consumption and mutation, for the proposed domain and each offered mechanism. Keep known-incompatible mechanisms out of current implementation options. No padding to a count.
- Shape of the change, limited to what must be agreed before coding: new or changed types and signatures, and the call tree or file tree with new nodes marked `[new]` (added by this plan). For an existing structure, show a `diff` of it.
- Acceptance checks for the required observable behaviors, as a numbered list in plan order: a bold sentence with the actor and the observable result, then the input or boundary and the verification method on their own lines. The method is a command or an observation a person can make without reading the code; a check without one keeps an empty method and also goes under Decisions needed.
- Assumptions with evidence; open questions separately. Reconcile both with accepted domains and forwarded helper contracts before returning the plan.
- Failure scenarios with a contract-defined response or behavior verified for specific inputs, as a table: scenario, detection, response. Omit unspecified outside-domain inputs from the table. If no failure behavior is established, say so.
- Decisions needed, with owner when known and the evidence that would settle each.

Evidence rules:
- Verify that every cited path and symbol exists.
- External API behavior: cite docs or source for the version in use or proposed. An installed dependency proves nothing about its defaults or guarantees.
- Mark proposed files and tests `[new]`.
- Never invent executed checks, expected log text, metrics, or user requirements.

Domain-check example: valid operations do not establish unchanged input.

```python
choices = iter(('red', 'blue'))
print('red' in choices)  # True
print(tuple(choices))   # ('blue',)

choices = iter(('red', 'blue'))
print(len(set(choices)))  # 2
print(tuple(choices))    # ()
```

Membership and set construction consume their iterators. With no broader contract, built-in set examples and unchanged-input requirements support proposing built-in sets. Iterator support remains an open extension.

Plan only; do not implement. The plan must be usable without running another skill first.

## Handoff

With `--handoff`, rewrite the plan as a brief for an agent that has none of this context. Return it in the reply; save it only to a path the user gives.
- Add what triggers the behavior and the invariants it must keep.
- Keep contract literals exact (field names, status codes, error strings). Drop line numbers and incidental paths; mark kept paths as "recheck".
- Preserve a Checks run block with the recorded command/result pairs, directory, execution count, and marked excerpts. Carry this block unchanged through the handoff rewrite.
- Keep the acceptance check ids: `AC-1`, `AC-2`, ... in plan order. A check without a verification method blocks the handoff: list it and stop.
- Tell the receiving agent: before implementing, inspect current source, recheck preconditions, and report conflicts; choose the smaller interpretation only when it keeps the stated contract.

## PRD

With `--prd`, follow [references/prd.md](references/prd.md) instead of the sections above.

## Output

Reader: the person who will build the feature, or the agent that gets the handoff. They decide whether the plan is safe to start, and what to settle first.

Line 1, bold, one plain sentence, in the user's words where possible. When the plan is ready, it names the feature. It never opens with a verdict word such as `Handoff blocked`: write "**I can't write the brief yet: "feels snappy" has no number anyone can check.**"

Under line 1, plain sentences without labels: each decision that blocks the first step, with its evidence and what it blocks.

Then the plan as `##` sections, in this order: Problem, Scope, Shape of the change, Acceptance checks, Assumptions and open questions, Failure cases, Decisions. Omit Shape when the change has no new or changed structure.

Views:
- Shape: a file tree with `[new]`, or a `diff` of an existing structure.
- Acceptance checks: a numbered list, one check per item (see Return).
- Failure cases: a table when there are up to 5 cases and each cell is short.
- Decisions: a numbered list of plain questions, each with up to 4 options and the default marked. Wider options remain conditional until their invariant checks pass.

Stopped, no feature: line 1 `**I need the feature to plan: what it does, and who uses it.**`, then `Verdict: Stopped`, then `**Next:**` with up to 3 numbered ways to send it, default marked, listed nowhere else: a sentence naming the feature (default); a path to notes or a brief.

Reader rules:
- Spell out acceptance check (a test or observation that proves a part works), `[new]` (added by this plan), and handoff brief (a brief for an agent that has none of this context) at first use.
- A check is checkable when someone can see it pass or fail. "Feels snappy" is not a check: propose a number or a check, and ask.
- Ask each decision as a plain question with at most 4 options and the default marked. "How long may a code stay valid?", not "expiry TTL".
- Never state a number, metric, or log text that no source gave.

End: `Verdict: <word>` on its own line, then `**Next:**`:
- `Plan ready`: no open decision blocks the first step. Line 1 names the feature.
- `Plan blocked`: the first step cannot start. Line 1 names the decision or missing check, in plain words.
- `Handoff blocked`: the brief is not written. A check with no way to check it blocks the handoff. Line 1 names those checks.
- `Stopped`: no feature or testable goal to plan. Line 1 says what is missing.
- `PRD draft`: `--prd` only, as [references/prd.md](references/prd.md) says.

`**Next:**` refers to decisions by number without repeating their questions or options, in dependency order, then `hl-tickets` after the blocking decisions are settled. `**Changed:** none`, unless a brief was saved to a path the user gave.

````markdown
**I need one decision before step 1 can start: how long a booking code stays valid.**
The validity period sets the expiry check and the text message, so step 1 waits for it.

## Problem
A gardener books a community plot for a season, then enters a code at the gate.
The booking page makes no code yet, and nothing stores one.

## Shape of the change
```text
gate/
|-- codes.py     make_code, check_code  # [new]
|-- booking.py   book_plot              # ~ changed: store code_hash
`-- sms.py       send_code              # [new]
```

## Acceptance checks
1. **A gardener enters a valid code and the gate opens.**
   Input: the code from the text message.
   Verify: `pytest tests/test_codes.py -q`.
2. **A used code keeps the gate closed.**
   Input: the same code a second time.
   Verify: `pytest tests/test_codes.py -q`.
3. **Three wrong codes lock the gate for 10 minutes.**
   Input: three wrong codes in a row.
   Verify: none yet; this check waits for decision 2.

## Failure cases
| Case | How it is detected | Response |
|---|---|---|
| three wrong codes | counter on `booking.py` | lock the gate; show "try later" |

## Decisions
1. **How long may a code stay valid?** Options: 15 minutes (default), 1 hour, 1 day.
   Gardeners enter the code at the gate, so 15 minutes covers a first visit.
2. **How do we check the lock after three wrong codes?** Options: a fake-clock test (default), a manual gate test.

Verdict: Plan blocked

**Next:**
1. Answer decisions 1 and 2 above.
2. After those decisions are settled, run `hl-tickets` on this plan.
````
