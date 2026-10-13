---
name: hl-challenge
description: "Test a plan, technical decision, design, or just-finished work against its goal and agreed reference, using the code, evidence, and safe commands, then recommend proceed, fix first, or stop, and name the smaller version if one exists. Returns a verdict, not design questions. --premortem assumes the goal failed and traces present weaknesses to that failure. --lens reviews through one fixed method (minimalist, failure-hunter, data-model, distributed, operability, boring-stack, agent-tooling, teacher, discovery); --panel runs 3-5 lenses in parallel and shows disagreements. Use when the user asks to challenge, stress-test, poke holes in, or run a premortem on a plan, decision, or work just done, or asks for a lens, a panel, or an angle such as simplify, failure modes, data modeling, or observability. Not for finding what a spec leaves unsaid (use `hl-grill --gaps`), line-by-line diff review (use `hl-code-review`), checking every requested outcome (use `hl-verify`), or a startup or product idea (use `hl-startup`)."
---
# Challenge

Input: `[plan/decision text, path, diff or ref range, or empty for the last proposal or work] [--premortem | --lens [<lens>] | --panel]`

Target: the input, else the most recent assistant proposal or finished work. No target: ask for text or a path.

Read-only: edit no tracked file. Run tests and read-only commands; tool caches are fine. Never install, migrate, or change git state. Commands that reach a live system, a network service, or a paid API need explicit approval.

Take the goal from the user's request or the referenced brief, and the agreed reference (plan, spec, slice, stated requirements) when one exists. Unclear goal: ask.

Your own proposal or work: when subagents exist, a fresh subagent does the steps below from the target, goal, and reference only, without your reasoning. Check each citation it returns, drop any that fail, and report the rest. No subagents: do it yourself and say the challenge is not independent.

## Claims

List the explicit claims and the assumptions the target needs, including that it achieves the goal end to end. For every target, check that no part duplicates existing code or another part, and that no two parts contradict each other. For finished work, also check that nothing unrequested was added; report a missing requirement you see as a blocker, and suggest `hl-verify` for a pass over every requirement. Challenge the user's decisions as hard as your own.

Check each claim against current code, a command you ran, cited evidence, an invariant, or a concrete failure case (empty, duplicate, concurrent, stale, partial, hostile). Record the citation and a result: supported, contradicted, or untested. No evidence means untested, never supported. A claim only the user can settle (preference, scope, priority) is a decision, not untested. No numerical confidence; no objections added to reach a count.

A blocker is a contradicted claim that defeats the goal or a requirement of the reference.

## Report

First line of the answer, with no preamble before it, limited to what you tested. Settle the verdict before you write it; never revise it later in the answer:
- `stop`: only a blocker that needs a different approach or major rework, named. A missing requirement that a small change adds is always `fix first`, even when the work is marked done.
- `fix first`: blockers fixable within the target, even in work already marked done, user decisions that can change the verdict, or an untested claim that decides the goal; name each change, decision, or the cheapest check that settles it.
- `proceed`: no blocker, and the claim that the target meets its goal end to end is supported.

Second line: `Judged against: <goal> (<source, or inferred>); reference: <path or none>; independent: yes|no`.

Then `Blockers: none` or the blockers table; then non-blocking risks (contradicted, goal survives); then untested assumptions, marking those that decide the goal. Columns: claim, result (omitted for untested), evidence, consequence. Report each material claim once. Then decisions for the user, one per line with a recommended answer and its reason. Then `Supported:` with each supported claim and its citation, one line each.

Then the smaller version: knowing what you know now, the simplest target that still meets the goal, with what to delete or not build. Omit it when the target is already minimal. Never assume the user accepts a risk.

## Premortem

With `--premortem`, assume the goal failed at a horizon that fits it: 12 months by default; for a one-off change, just after it runs. Missing goal, actor, or mechanism: ask.

Scenarios to examine, where they apply: insufficient demand, a stronger alternative, a reliability failure, a security failure. Label each hypothetical. Never invent releases, customer quotes, revenue, fines, or probabilities.

For each scenario, trace a present weakness, supported by the input, through a plausible event to the failed goal. Separate demonstrated weaknesses from assumed conditions. No causal evidence: record an open question, not a fatal flaw.

Rank causes: S0 defeats the goal alone, S1 materially threatens it, S2 limited impact. Two S1 causes are not automatically an S0.

First line: the worst rank and its cause (`S0: <cause>`), or `No supported failure cause`. Then the frame (goal, actor, mechanism, horizon) on one line; each supported scenario with its rank, as an indented causal chain: the weakness with its citation, then the event, then the failed goal; then up to three prioritized mitigations or discriminating tests.

## Lenses

With `--lens` or `--panel`, follow [references/lenses.md](references/lenses.md) instead of the Claims, Report, and Premortem sections. The read-only rule still holds.
