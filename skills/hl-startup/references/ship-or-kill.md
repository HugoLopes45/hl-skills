# Ship or Kill

Input: `ship|kill [question] [--format answer|debate|playbook] [--depth quick|deep]`

Answer two decisions for a small software business: what to ship next, and whether to keep a product alive.

## Every run

1. The mode, `ship` or `kill`, is the decision; parse the format from the input. Empty input: use the most recent user message.
2. Questions outside these two decisions: name the better fit from the table below and stop, with no advice on the question itself.
3. Answer in the requested format. Done when that format's checklist holds and the answer is within its word limit.

## Decisions

### ship

The minimum path to a launched, paying product.
- Start from a boilerplate or managed services for solved problems (authentication, billing, email); build only the part that is specific to this product.
- Done beats perfect. Proven technology, one server, until load measured today needs more.
- Cut everything the first paying user does not need. Launch in days or weeks, not months.

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

- **answer**: line 1 one plain sentence with the reason, under 100 characters. Then the take, which names what to keep. Then one line: "The decision flips to <alternative> if <trigger>." Then `Verdict: Kill` (or `Pivot`, `Keep`, `Ship`; for Ship, line 1 names the smallest version). Then `**Next:**` with the one action for this week. Quick: at most 200 words: take at most 70, action at most 40, flip at most 30; no other sections or lists. Deep: at most 600.
- **debate**: line 1 one plain sentence with the verdict and its reason, then a heading for each side, at most 80 words each, then `Verdict: <word>`.
- **playbook**: line 1 the goal. Then a table of at most 7 steps: step, action, why, done when. More than 7 means the question is too big; split it.
- Outside both decisions: still answer the question. Line 1 is your direct answer in plain words ("**Charge $29: at $9 you need three times the customers to earn the same.**"). Then at most 3 sentences with the reason and what would change it, each assumption named as a guess. Then one sentence naming the better skill from the table for a full answer, then `Verdict: Quick take`, then `**Next:**` with one action. At most 150 words.

## Rules

- Commit to one answer; qualify it only by the condition that would flip it.
- Be concrete: technology names, amounts, week estimates. Label estimates.
- Prescribe the principle, not a specific person's stack.
