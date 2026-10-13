---
name: hl-grill
description: "Compare structurally different ways to solve a problem, including reuse of what exists, and question the user in rounds, each question with a recommended answer, until a loose idea or a written plan becomes a shared understanding. --gaps instead lists what a written plan or spec is missing (decisions, ambiguous terms, edge cases, acceptance criteria), each with one question. Saves the brief, or with --docs records terms in GLOSSARY.md and proposes ADRs, only when the user explicitly asks. Use when the user wants options, several ways to do something, or trade-offs before planning, wants to brainstorm, wants to be grilled or questioned on an idea or a plan, or asks what a spec is missing. Not for a verdict on a plan or finished work (use `hl-challenge`)."
---
# Grill

Input: `[idea, problem, plan, or path] [--docs | --gaps [--write]]`

Reach a shared understanding of what to build, before any plan or code. The input is the idea; if empty, the idea under discussion. Nothing to work on: ask what the user wants to build, and stop. A written plan or spec is the idea: the decisions it already settles are facts; quote them instead of asking. Never modify the source plan unless the user asks.

## Facts first

Facts are your job; decisions are the user's. Before asking, look up what the code, docs, and tools answer; use subagents for independent lookups when available. A question whose answer you can read is not a question. A running lookup blocks only the questions that depend on it. When the user states how something works and the code disagrees, show both and ask which is right.

Check whether existing code or tools already meet the need. Fully met: line 1 says how the need is met and names the defining file; then ask only whether it meets the need (recommended: yes), and end with `Verdict: Already met`. Weaknesses you notice that the user did not ask about do not make it partly met: list each in one line, with no options. Partly met: under line 1, say what exists and what is missing, with locations; the missing part becomes the idea.

## Design tree

Keep a tree of decisions internally: each decision branches into the decisions that depend on it. Show it only when the user asks. The root is the outcome and who benefits. Below it, these angles become questions only where the input leaves them open and the answer changes what gets built: one case that must work and one that must not, the smallest useful version and non-goals, the signal that proves it done, the failure cases that change scope (empty, duplicate, concurrent, stale, partial, hostile). They are angles, not a checklist.

Ask at the user's level (product, technical, or operational). Record finer how-to (sort order, paging, naming) as an assumed decision for planning. Test a vague or overloaded term with a concrete scenario ("an order is half shipped and the user cancels: what happens?"; "account": customer or user?).

A solution-shaped request ("add a cache") is one option for an outcome. When the request, code, or docs state that outcome, go to an options question with the stated solution as one option. Otherwise ask for the outcome first.

## Options

For a decision about how to solve something, compare up to five structurally different mechanisms, not library or wording variants. Include reuse of repository code, the standard library, the platform, or installed dependencies when it applies. Never pad the count. With three or more, use a table of three short columns: option (what it is, in a few words), main cost, and when to pick it, grounded in a concrete case. Each cell is a few plain words; the reason goes in the recommendation, not in the table. With two, name both in the question. Name a runner-up only when a different condition would make it win.

## Rounds

The frontier is every open decision whose prerequisites are settled. Size the round to the input: a bare topic gets the outcome and one concrete example; a partial idea, the next missing decisions; a detailed one, only the highest-risk decision. At most five questions, highest impact first; the rest wait.

Line 1, bold: one plain sentence saying what the questions settle, each with a recommendation. In round 1, the next line restates the idea in one sentence, keeping the user's uncertainty. Then one plain sentence with the facts you looked up instead of asking, with their source, when there are any. End with `Verdict: Round N, K questions`. When the outcome and the constraints that rank the options are already known and the only open decision is the options question, line 1 is instead `**<option> fits best, because <reason>.**`; then the table; end with `Verdict: Recommended`.

One numbered item per question:

```
1. **<question in plain words, ending with ?>**
   <the options or their table, when there are any>
   Recommended: <answer>, because <reason from the code, the user's goal, or a stated constraint>
```

Word every question so "yes" accepts the recommendation. No basis for a recommendation: say so; never invent one. Then `**Next:** Reply "ok" to accept every recommendation, or answer by number.`

Wait for the answers. Record each decision and add the decisions it opens. When an answer conflicts with a settled decision, confirm which stands. Recompute the frontier and ask the next round. Never ask a settled decision again, nor a decision that settled ones leave with one answer: record it as assumed.

## Done

When the frontier is empty or the user stops, line 1, bold, one plain sentence saying what is settled and what is open. Then one paragraph someone who missed the conversation can act on; the decisions as a numbered list, each with its answer and source (you, the code, a doc, or assumed with its reason); open questions with who decides each; for a written plan, the plan updated with the confirmed decisions; the next step (`hl-spec`, `hl-tickets`, or `hl-spike` for an unknown only an experiment settles). End with `Verdict: Shared understanding` or `Verdict: Stopped, K open decisions`, then `**Next:**`: the next step, then `Confirm, correct a decision, or continue on an open question.`

A correction reopens that decision and the decisions that depend on it. The understanding is shared only when the user confirms it, assumed rows included. Never invent evidence. Do not plan or implement until the user confirms.

Write nothing unless the user asks to save or passes `--docs`. To save, write the confirmed brief to the path the user names, else propose `docs/briefs/<yyyy-mm-dd>-<slug>.md` and wait; ask before overwriting a file.

## Docs

With `--docs`, keep the project language as you go:
- Challenge a term that conflicts with `GLOSSARY.md`.
- When a term is resolved, add or update its `GLOSSARY.md` entry at once: term, one-sentence meaning, terms to avoid. No implementation details. Create the file only when the first term is resolved.
- Propose an ADR only when the decision is hard to reverse, surprising without context, and the result of a real trade-off. After the user agrees, draft it with context, options considered, decision, consequences, and reversal cost; suggest `hl-adr` to record it.

## Gaps

With `--gaps`, follow [references/gaps.md](references/gaps.md) instead of the rounds.

## Output

Reader: someone with a rough idea or a written plan. They must decide what to build and answer the questions now. Line 1 and the question blocks tell them what to do next.

Line 1, bold, one plain sentence in everyday words. The reply ends with `Verdict: <word>` on its own line just before `**Next:**`, by state:
- `Round N, K questions`: answer these now. Each comes with a recommendation to accept.
- `Recommended`: the best option, with the table.
- `Already met`: existing code covers the need. The only question: does it fit?
- `Shared understanding`: every decision is settled. Confirm the summary or correct one.
- `Stopped, K open decisions`: the conversation ended first. List what is still open.
- `Gaps, N blockers, N major, N minor`: `--gaps` totals. Details follow [references/gaps.md](references/gaps.md).

Views: a table of three short columns for three or more options, with the question naming both options when there are two. No codes such as Q1: number the questions 1, 2, 3.

Stopped, nothing to work on: `**I need an idea, a problem, a plan, or a file to work on: what do you want to build?**` Then up to 3 numbered ways, default marked: a sentence such as "a CLI that does X" (default); a path to a written plan or spec; `--gaps` to list what a plan misses. Then `Verdict: Stopped`.

Reader rules:
- Say "decision" and "option", not "frontier", "prerequisite", or "design tree".
- Spell out ADR (architecture decision record: a short note on one hard-to-reverse technical choice) and GLOSSARY.md (the project's word list) at first use.
- Word each question so "yes" accepts its recommendation. Give the reason from the code, the goal, or a stated constraint.
- A conflict shows both sources side by side, with no blame: "the code uses SQLite; the idea says Postgres. Which is right?"

End: `**Next:** Reply "ok" ...` for a round, or the next skill named in the done summary. Never end on a question without a recommendation. `**Changed:** <paths>` when a file was saved (GLOSSARY.md, a brief, or a `*-gaps.md` report); otherwise `**Changed:** none`.

````markdown
**Two questions settle what a room booking allows; each has a recommended answer.**
The idea: students book a library study room for up to two hours, without calling the front desk.
I checked the repository: it has no room or booking code yet.

1. **Should only students with a library card book a room?**
   Recommended: yes, because a card ties each booking to one student.

2. **Should an unused room become free 15 minutes after its start?**
   Recommended: yes, because an empty room blocks others for up to two hours.

Verdict: Round 1, 2 questions

**Next:** Reply "ok" to accept every recommendation, or answer by number.
````
