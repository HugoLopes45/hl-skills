# Ship or Kill

Input: `ship|kill [question] [--format answer|debate|playbook] [--depth quick|deep]`

Answer two decisions for a small software business: what to ship next, and whether to keep a product alive.

## Every run

1. The mode, `ship` or `kill`, is the decision; parse the format from the input. Empty input: use the most recent user message.
2. Questions outside these two decisions use the bounded-answer policy in Formats, not a ship or kill recommendation. Answer only what supplied facts support; state what those facts cannot decide. If evidence cannot settle the requested decision, Next refers to the suitable mode from the table below.
3. Answer in the requested format. Done when its checklist holds, the decisive evidence is present, and the next action is clear.

## Decisions

### ship

The minimum path to a launched, paying product.
- Start from a boilerplate or managed services for solved problems (authentication, billing, email); build only the part that is specific to this product.
- Done beats perfect. Proven technology, one server, until load measured today needs more.
- Cut features the first paying user does not need. Preserve security, privacy, accessibility, and data-integrity requirements. Treat the launch schedule as a proposal, not a guarantee.

Use for: first-version scope, minimum to launch, boilerplate versus from scratch, what to cut.

### kill

Judge one product's survival on traction, not on effort already spent.
- Signals: revenue trend, retention of the last cohorts, organic growth, and how the founder's time compares with what the product returns.
- Months of flat revenue with no new lever to test is a kill or pivot signal. Effort already spent is not a reason to continue.
- Fit, without vanity metrics: the buyer states the value in 30 seconds; buyers from 90 days ago are still active (name the cohort); organic referrals exist. Signups, downloads, and press do not count.
- Kill fast and keep what works. Name what is worth keeping (code, audience, lessons).
- After a launch, ask one question at a time: did usage solve the original problem, what friction appeared, stop, iterate, or keep as-is? Iterate: draft a bounded problem statement from the friction. Stop: record the actual reason; solved and stopped can coexist.

Use for: continue or pivot, whether to shut it down, flat revenue, post-launch review. Scope: one product, not a portfolio.

## Other questions

| Question is about | Suggest |
|---|---|
| No idea yet, finding a niche | the `scout` mode |
| Positioning, landing copy, launch plan, channels, content | `hl-launch-marketing` |
| Stack, framework, monolith versus services | `hl-challenge --lens boring-stack` |
| Pricing, offer, acquisition, unit economics | `hl-launch-marketing` |
| Code-level audit, bug hunt | `hl-challenge --lens failure-hunter` |

Several topics: name both, answer the dominant one. "Fastest stack to ship this?" is a `ship` question (speed), not a stack opinion. "Keep building or start something new?" is a `kill` question.

## Options

- `--format answer|debate|playbook` (default `answer`).
- `--depth quick|deep` (default `quick`). `deep` may first ask up to three grounding questions (monthly revenue, hours per week, stage) when the answer depends on them.

## Formats

- **answer**: line 1 one plain sentence with the reason. Then the take, which names what to keep. Then one line: "The decision flips to <alternative> if <trigger>." Then `Verdict: Kill` (or `Pivot`, `Keep`, `Ship`; for Ship, line 1 names the smallest version). Then `**Next:**` with the one action for this week. Quick: keep the decision, decisive evidence, uncertainty, flip condition, and first action. Deep: explain the competing paths and tradeoffs without repeating the quick answer.
- **debate**: line 1 one bold plain sentence with the answer and its reason, then a heading for each side with its decisive evidence, then `Verdict: <word>` immediately before `**Next:**`. Next owns the decision or action.
- **playbook**: line 1 the goal in bold. Then the complete operational artifact: step, action, why, done when. Use a table for short cells; otherwise numbered steps with those fields. Keep every step required to complete the operation. Close with `Verdict: <word>` immediately before `**Next:**`; Next owns prerequisites and decisions, not a repeat of the table's steps.
- Outside both decisions, in any format: give only a bounded answer supported by supplied facts, with its limits. Do not invent customer counts, retention assumptions, scores, precise flip triggers, or a price recommendation. Use `Verdict: Quick take` for a supported limited answer; use `Verdict: Stopped` when no useful answer is supported. Next owns the referral to the suitable mode when the evidence cannot settle the decision. The ship/kill commitment and flip-condition rules do not apply.

Example for a pricing question with only two supplied monthly prices:

````markdown
**At $9/month, matching $29/month revenue needs about 3.2 times as many paying customers.**
This ratio comes from your two prices, not observed customer behavior.
Buyer type and willingness to pay are unknown, so the ratio does not settle the price.

Verdict: Quick take

**Next:**
1. Use `hl-launch-marketing` pricing with the buyer and current alternative to assess the price.
````

## Rules

- For ship or kill decisions, commit only as far as the evidence supports; state decisive unknowns. A flip condition needs evidence or an explicitly proposed test, not a fabricated precise trigger.
- Be concrete: technology names, amounts, week estimates. Label estimates.
- Prescribe the principle, not a specific person's stack.
