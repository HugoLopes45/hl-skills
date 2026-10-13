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

Reader: the person who wrote the plan or finished the work, deciding whether to keep going. They read line 1 and `**Next:**`.

Settle the verdict before you write it; never revise it later in the answer. Line 1, bold, one plain sentence within 100 characters, limited to what you tested: the answer in everyday words, effect first. Line 1 never opens with the verdict word.

Under line 1, one plain sentence each, no labels: every blocker (a claim that breaks the goal), and every untested claim or arithmetic on the target's own numbers that alone defeats the goal. Then:
- A numbered list of the blockers, worst first. Each: a bold plain sentence that states the contradiction, one sentence on its consequence for the goal, the evidence (a short call path, a calculation, or a quoted line) and the change that fixes it.
- `Risks:` a numbered list of contradicted claims the goal survives and untested assumptions, each one plain sentence with its evidence and how sure you are; say which ones decide the goal. Report each material claim once.
- `Smaller version:` knowing what you know now, the simplest target that still meets the goal, as a `diff` of the target's parts (`-` delete or do not build, `~` change). Omit it when the target is already minimal.
- `What holds:` the supported claims, one line each with its citation.
- `Verdict: <word>` on its own line just before `**Next:**`, one of:
  - `Stop`: the target cannot reach the goal as designed. Only a blocker that needs a different approach or major rework, named. A missing requirement that a small change adds is always `Fix first`, even when the work is marked done.
  - `Fix first`: the goal is reachable after the named changes. Blockers fixable within the target, even in work already marked done; user decisions that can change the verdict; or an untested claim that decides the goal.
  - `Proceed`: go ahead. No blocker, and the claim that the target meets its goal end to end is supported.
- `**Next:**` every change needed, in order, including steps stated earlier; then each decision for the user as one question with a recommended answer and its reason. Never assume the user accepts a risk.
- Plain words: no codes, ranks, or tags. Define a technical term at first use in a few words (`p95`: the time 95 % of requests beat). Code, paths, and quoted errors stay exact. Name the cause, never the author. Under line 1, say in one plain sentence what you checked against: the goal and where it is written.
- No target or no goal: line 1 says in plain words what is missing and why it blocks, e.g. `**I need the plan or work to challenge: send its text or a file path.**`, then `Verdict: Stopped`. `**Next:**` holds up to 3 numbered ways to unblock, default marked; they appear nowhere else.

````markdown
**The leaderboard can be up to an hour old, and a rebuild can overlap the next one.**
The plan promises scores fresh within one minute, but the table is rebuilt once an hour.
One rebuild takes 70 minutes on 2 million rows, so two rebuilds can run at the same time.

1. **New scores never reach the precomputed table until the next rebuild.**
   A player who beats a record sees the old leaderboard for up to an hour. I read this code; I did not run it.
   ```text
   api.py:31        POST /scores --> record_score()   # writes live
   jobs/rank.py:12  rebuild_leaderboard()             # reads once an hour
   api.py:52        GET /leaderboard                  # reads the rebuilt table only
   ```
   Fix: drop the hourly job and read the live scores with an index.

Smaller version:
```diff
- hourly rebuild job and leaderboard table
~ add an index on scores(game_id, points DESC); the query now reads every row (900 ms)
```

What holds: `record_score` writes to `scores` (`scores.py:44`).

Verdict: Fix first

**Next:**
1. Add the index. Then run `bench/leaderboard.sh`: 95 % of requests must finish under 200 ms.
2. Decide: is one-minute freshness required? Recommended: yes, `spec.md:12` promises it.
````

## Premortem

With `--premortem`, assume the goal failed at a horizon that fits it: 12 months by default; for a one-off change, just after it runs. Missing goal, actor, or mechanism: ask.

Scenarios to examine, where they apply: insufficient demand, a stronger alternative, a reliability failure, a security failure. Say which events are imagined. Never invent releases, customer quotes, revenue, fines, or probabilities.

For each scenario, trace a present weakness, supported by the input, through a plausible event to the failed goal. Separate demonstrated weaknesses from assumed conditions. No causal evidence: record an open question, not a fatal flaw.

Rank causes by effect: fatal (defeats the goal alone), serious (materially threatens it), minor (limited impact). Two serious causes are not automatically fatal.

Line 1, bold, one plain sentence within 100 characters, written as if the failure already happened ("Three months after launch, admins still file tickets because a stalled invite has no fix."): the worst cause and its effect, never opening with a rank. Under it, one plain sentence: what you read, and that the events after the present weakness are imagined. Then a numbered list of supported scenarios, worst first. Each: a bold plain sentence with the cause and its rank in words, then the chain from the present weakness to the failed goal, one link per line; mark only the first link as the fact you found:
```text
plan.md:14  backups run on the same disk as the database   # in the plan today
--> the disk fails
--> the database and every backup are lost together
--> goal failed: restore any day of the last 30
```
Then `Open questions:` the gaps with no causal evidence yet, one line each. Then `Verdict: <worst rank>` on its own line: `Fatal`, `Serious`, `Minor`, or `No supported failure cause`. Then `**Next:**` up to three prioritized mitigations or discriminating tests.

## Lenses

With `--lens` or `--panel`, follow [references/lenses.md](references/lenses.md) instead of the Claims, Report, and Premortem sections. The read-only rule still holds.
