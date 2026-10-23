---
name: hl-challenge
description: "Test a plan, decision, design, or just-finished work against its goal and agreed reference, using code, evidence, and safe commands, then recommend proceed, fix first, or stop, and name the smaller version if one exists. Returns a verdict, not design questions. --premortem assumes the goal failed and traces present weaknesses to that failure. --lens reviews through one fixed method (minimalist, failure-hunter, data-model, distributed, operability, boring-stack, agent-tooling, teacher, discovery, ambition); --panel runs 3-5 lenses and shows disagreements. Use when the user asks to challenge, stress-test, poke holes in, or run a premortem on a plan, decision, or work just done, or asks for a lens, a panel, or an angle such as simplify, aim higher, failure modes, data modeling, or observability. Not for finding what a spec leaves unsaid (use `hl-grill --gaps`), line-by-line diff review (use `hl-code-review`), checking every requested outcome (use `hl-verify`), or a startup or product idea (use `hl-startup`)."
---
# Challenge

Input: `[plan/decision text, path, diff or ref range, or empty for the last proposal or work] [--premortem | --lens [<lens>] | --panel]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.
- Before drafting, record each executed probe's full command and literal inputs and outputs. Build observed examples and execution counts from those records; label unexecuted examples as predictions.
- For a causal explanation, trace the actual operations through the final result. Keep only explanations consistent with that chain; a general fact about an intermediate operation is not enough.

For material claims examined by the selected mode, check each independently testable effect against current code, a command you ran, cited evidence, an invariant, or a concrete failure case (empty, duplicate, concurrent, stale, partial, hostile). Record the citation and a result: supported, contradicted, or untested. No evidence means untested, never supported. A claim only the user can settle (preference, scope, priority) is a decision, not untested. No numerical confidence; no objections added to reach a count.

Combine each concern's consequence, evidence, and uncertainty. Preserve disagreements and lens attribution where they matter; omit routine narration.

Target: the input, else the most recent assistant proposal or finished work. No target: ask for text or a path.

Read-only: edit no tracked file. Run tests and read-only commands; tool caches are fine. Never install, migrate, or change git state. Commands that reach a live system, a network service, or a paid API need explicit approval.

Take the goal from the user's request or the referenced brief, and the agreed reference (plan, spec, slice, stated requirements) when one exists. Unclear goal: ask.

Your own proposal or work: when subagents exist, a fresh subagent does the steps below from the target, goal, and reference only, without your reasoning. Check each citation it returns, drop any that fail, and report the rest. No subagents: do it yourself and say the challenge is not independent.

## Claims

List the explicit claims and the assumptions the target needs, including that it achieves the goal end to end. For every target, check that no part duplicates existing code or another part, and that no two parts contradict each other. For finished work, also check that nothing unrequested was added; report a missing requirement you see as a blocker, and suggest `hl-verify` for a pass over every requirement. Challenge the user's decisions as hard as your own.

A blocker is a contradicted claim that defeats the goal or a requirement of the reference.

## Report

Reader: the person who wrote the plan or finished the work, deciding whether to keep going. They read line 1 and `**Next:**`.

Settle the verdict before you write it; never revise it later in the answer. Line 1, bold, one plain sentence, limited to what you tested: the answer in everyday words, effect first. Line 1 never opens with the verdict word.

Under line 1, state the decisive untested assumption or limitation, without repeating a finding below. Proven blockers go in the numbered findings. Then:
- A numbered list of the blockers, worst first. Each: a bold plain sentence that states the contradiction, its consequence for the goal and the evidence (a short call path, a calculation, or a quoted line). Do not repeat a fix in the finding paragraph.
- `Risks:` a numbered list of contradicted claims the goal survives and untested assumptions, each with its decisive evidence and how sure you are; say which ones decide the goal. Report each material claim once.
- `Smaller version:` knowing what you know now, the simplest target that still meets the goal, as a `diff` of the target's parts (`-` delete or do not build, `~` change). Omit it when the target is already minimal. This view shows the structural change; Next gives its execution and validation steps.
- Keep supported claims and counterevidence with the blocker or risk they qualify. `What holds:` contains only remaining supported claims, one line each with its citation; omit it when that would repeat evidence.
- `Verdict: <word>` on its own line just before `**Next:**`, one of:
  - `Stop`: the target cannot reach the goal as designed. Only a blocker that needs a different approach or major rework, named. A missing requirement that a small change adds is always `Fix first`, even when the work is marked done.
  - `Fix first`: the goal is reachable after the named changes. Blockers fixable within the target, even in work already marked done; user decisions that can change the verdict; or an untested claim that decides the goal.
  - `Proceed`: go ahead. No blocker, and the claim that the target meets its goal end to end is supported.
- `**Next:**` every prerequisite decision before its dependent changes and checks, in order. Each decision is one question with a recommended answer and its reason. Never assume the user accepts a risk.
- Plain words: no codes, ranks, or tags. Define a technical term at first use in a few words (`p95`: the time 95 % of requests beat). Code, paths, and quoted errors stay exact. Name the cause, never the author. Under line 1, state what you checked against: the goal and where it is written, with any limitation that changes the assessment.
- No target or no goal: line 1 says in plain words what is missing and why it blocks, e.g. `**I need the plan or work before I can assess its goal.**`, then `Verdict: Stopped`. `**Next:**` holds up to 3 numbered ways to unblock, default marked; they appear nowhere else.

````markdown
**The leaderboard misses one-minute freshness, and rebuilds can overlap.**
I checked the plan against the freshness goal in `spec.md:12`; I read the code but did not run it.

1. **New scores never reach the precomputed table until the next rebuild.**
   The plan rebuilds once an hour despite its one-minute promise. `record_score` writes to live `scores` (`scores.py:44`), but a player who beats a record still sees the old table until the next rebuild.
   ```text
   api.py:31        POST /scores --> record_score()   # writes live
   jobs/rank.py:12  rebuild_leaderboard()             # reads once an hour
   api.py:52        GET /leaderboard                  # reads rebuilt table only
   ```

Risks:
1. A 70-minute rebuild on 2 million rows would overlap the next hourly rebuild; that runtime is unverified here.
2. The current query is reported to read every row and take 900 ms; that behavior and timing are unverified here.

Smaller version:
```diff
- hourly rebuild job and leaderboard table
~ add an index on scores(game_id, points DESC)
```

Verdict: Fix first

**Next:**
1. Decide: is one-minute freshness required? Recommended: yes, `spec.md:12` promises it.
2. If yes, apply the smaller version, then run `bench/leaderboard.sh`: 95 % of requests must finish under 200 ms.
3. Confirm the 70-minute rebuild time and 900 ms query time before relying on those figures.
````

## Premortem

With `--premortem`, assume the goal failed at a horizon that fits it: 12 months by default; for a one-off change, just after it runs. Missing goal, actor, or mechanism: ask.

Scenarios to examine, where they apply: insufficient demand, a stronger alternative, a reliability failure, a security failure. Say which events are imagined. Never invent releases, customer quotes, revenue, fines, or probabilities.

For each scenario, trace a present weakness, supported by the input, through a plausible event to the failed goal. Separate demonstrated weaknesses from assumed conditions. No causal evidence: record an unknown, not a fatal flaw.

Rank causes by effect: fatal (defeats the goal alone), serious (materially threatens it), minor (limited impact). Two serious causes are not automatically fatal.

Line 1, bold, one plain sentence, written as if the failure already happened ("Three months after launch, admins still file tickets because a stalled invite has no fix."): the worst cause and its effect, never opening with a rank. Under it, state what you read, its limits, and that the events after the present weakness are imagined. Then a numbered list of supported scenarios, worst first. Each: a bold plain sentence with the cause and its rank in words, then the chain from the present weakness to the failed goal, one link per line; mark only the first link as the fact you found:
```text
plan.md:14  backups run on the same disk as the database   # in the plan today
--> the disk fails
--> the database and every backup are lost together
--> goal failed: restore any day of the last 30
```
Then `Unknowns:` the gaps with no causal evidence yet. Then `Verdict: <worst rank>` on its own line: `Fatal`, `Serious`, `Minor`, or `No supported failure cause`. Then `**Next:**` any questions needed to resolve the gaps, followed by the prioritized mitigations or discriminating tests needed to settle the supported risks.

## Lenses

With `--lens` or `--panel`, follow [references/lenses.md](references/lenses.md) instead of the Claims, Report, and Premortem sections. The read-only, evidence, and detail rules still hold in every mode.

## Checks run (every mode)

When checks were attempted, include `**Checks run:**` before the closing verdict. For each check, copy the full command verbatim, then its result or a marked excerpt, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results. Record denied actions separately as unexecuted.
