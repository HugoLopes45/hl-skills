---
name: hl-startup
description: "Take a software product from no idea to keep or kill. scout finds SaaS ideas a solo developer can ship with an AI coding agent, from live pain signals, scored on evidence. evaluate (default) runs five gated stages (core assumption, problem validation, competition, first 10 customers, two-week MVP test) ending in go, pivot, stop, or insufficient evidence; --stage runs one. ship decides the smallest first version to launch; kill decides whether to continue, pivot, or shut down a product based on traction rather than effort spent. Use when there is no idea yet, when the user wants to evaluate or pressure-test an idea, validate a problem, map competitors, find first customers, or scope an MVP experiment, or asks what to launch, what to cut for a first version, or whether to keep going with a product."
---
# Startup

Input: `[scout | evaluate | ship | kill] [idea or question] [--stage assumption|problem|competition|customers|mvp]`

The first word picks the mode; without one, pick it from the request: no idea yet is `scout`; what to launch or cut is `ship`; whether to continue a product is `kill`; otherwise `evaluate`.

- `scout`: follow [references/scout.md](references/scout.md).
- `ship` or `kill`: follow [references/ship-or-kill.md](references/ship-or-kill.md).
- `evaluate`: the rest of this file.

## Evaluate

Gather the idea, the target buyer or user, and the founder's relevant access or experience. Ask for missing inputs one at a time. Be direct without personal attacks.

Work through five stages and ask before advancing to the next. A stage that ends in stop: report it and advance only if the user asks. For each stage, read its file and follow it. `--stage` runs that stage only and ends with its own return.

1. **Assumption** ([references/pressure-test.md](references/pressure-test.md)): the core assumption, demonstrated weaknesses, and the evidence needed to judge viability.
2. **Problem** ([references/validate-problem.md](references/validate-problem.md)): the specific pain, the early-adopter profile, non-leading questions about past behavior, and proposed validation criteria.
3. **Competition** ([references/competition-map.md](references/competition-map.md)): the current workaround, direct and indirect competitors, switching costs, and differentiation.
4. **Customers** ([references/first-customers.md](references/first-customers.md)): supported channels, manual outreach, a draft message, behavioral signals, and milestones for the first 10 customers.
5. **MVP** ([references/mvp-experiment.md](references/mvp-experiment.md)): a two-week test with the smallest feature set, exclusions, pass and fail criteria, and schedule assumptions.

Do not fabricate people, market numbers, customer quotes, traction, or certainty. Separate evidence from hypotheses and proposed targets. Payments and repeated use are stronger signals than expressed interest. Label every threshold as a proposal.

After the last stage, give the verdict (go, pivot, stop, or insufficient evidence) in the Output layout. Then the decisive evidence, the riskiest assumption, the cheapest test, and the next 14 days as a table: day, action, done when. Do not write files or contact customers unless the user asks.

## Output

Reader: a founder deciding whether to spend the next two weeks on this idea. The decision served: go, change, or stop.

Line 1, bold: one plain sentence, under 100 characters, that answers the founder's question in their words. It never opens with a label, verdict word, or count.

Under line 1, plain sentences without labels: the missing evidence that decides the verdict, each precondition of the first step, and any risk seen outside the question (say so).

Body, one numbered point per idea, each a bold plain sentence, then one or two sentences or one view:
- Evaluate summary: each stage in one line: the stage, its verdict, the evidence that decides it.
- Problem: the questions that mislead, each with why, then the questions to ask instead.
- Competitors: a table of three short columns: alternative, price (with its source, or "no source"), why a customer would switch or stay.
- Customers: a table of week, action, success signal.
- MVP: each cut with its reason; the pass and fail rule; a 14-day table of day, action, evidence collected.
- Final verdict: a 14-day table of day, action, done when.
- Say in words, once per point, how each number or claim is known: "from your numbers", "my estimate", "no source yet", "my proposal" for a threshold. No status codes.

End with `Verdict: <word>` on its own line, one per mode:
- Evaluate: `Go` (the evidence supports the test), `Pivot` (change the customer or problem first), `Stop` (the evidence is against it), `Insufficient evidence` (the stages cannot judge yet).
- Stage: `Proceed`, `Revise`, `Stop`, `Insufficient evidence`, with the same meanings for that stage only. The MVP stage names the riskiest assumption on line 1: `**Whether owners pay to stop plants dying is the riskiest assumption to test.**`
- Kill: `Keep`, `Pivot`, `Kill`. Scout: `Verdict: Pick: <bet>, <score>/10` or `Verdict: No shippable bet`. Ship: `Verdict: Ship`, with the smallest first version on line 1.

Then `**Next:**`, one step per line, each something the founder can do now. A stage run ends with "Reply `next` to run the Competition stage."

Stopped: line 1 says in plain words what is missing and why it blocks; then `Verdict: Stopped`; then `**Next:**` with up to 3 numbered ways to unblock, default marked, listed nowhere else:
- No idea given: `**I need your product idea before I can evaluate it; the request does not describe one.**`, then in Next: 1. Which idea, in one line, and who pays for it? (default). 2. Run `scout` to find ideas first.

Reader rules:
- Define each term once: MRR (monthly recurring revenue), churn (customers who cancel), CAC (cost to win one paying customer), LTV (profit one customer brings over their time), MVP (smallest test that answers one question), cohort (customers who signed up in the same period), pivot (change the customer or problem, keep some assets), sunk cost (money and time already spent).
- Never invent people, market sizes, quotes, traction, or certainty. Say plainly what is not known yet.
- Dollars and days carry units and a source or label.
- No blame, no hype. Say "the plan", not "you".
- No process narration: no "the skill says", "the framework", or "I read".

Example (a stage run):

````markdown
**The pain is a guess until five owners describe a real dead plant.**
No interview has happened yet, so nobody has confirmed the problem.

1. **Two of your questions would give a false yes.**
   - "Would you pay $8 a month?" names your product and price, so people say yes to be polite.
   - "Don't you hate forgetting to water plants?" leads: nearly everyone agrees, and it shows no cost.

2. **Ask about the last time instead.**
   - "Tell me about the last plant in your office that died. What happened?"
   - "What did you do the last time you noticed a dry plant?"
   - "What did it cost, in time or money, when it died?"
   - "What have you tried so far to keep them alive?"
   - "When did you last ask someone else to water them?"

3. **The problem is real if 3 of 5 owners name a dead plant from the last 30 days.**
   That threshold is my proposal; change it if you have a better one.

Verdict: Revise

**Next:**
1. Replace the two questions with the five above before any call.
2. Book 5 calls with office managers this week; ask colleagues for introductions.
3. Reply `next` after the 5 calls to run the Competition stage.
````
