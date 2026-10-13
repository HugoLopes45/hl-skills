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
| Positioning, landing copy, launch plan, channels, content | `launch-marketing` |
| Stack, framework, monolith versus services | `challenge --lens boring-stack` |
| Pricing, offer, acquisition, unit economics | `launch-marketing` |
| Code-level audit, bug hunt | `challenge --lens failure-hunter` |

Several topics: name both, answer the dominant one. "Fastest stack to ship this?" is a `ship` question (speed), not a stack opinion. "Keep building or start something new?" is a `kill` question.

## Options

- `--format answer|debate|playbook` (default `answer`).
- `--depth quick|deep` (default `quick`). `deep` may first ask up to three grounding questions (monthly revenue, hours per week, stage) when the answer depends on them.

## Formats

- **answer**: the decision, the take, one action doable this week, and "flips to <alternative> if <trigger>". Quick: at most 200 words: the decision in one line, the take in at most 70 words (it names what to keep), the action in at most 40, the flip in at most 30; no other paragraphs, sections, or lists. Deep: at most 600.
- **debate**: one verdict line with the reason, then the case for each side in at most 80 words each.
- **playbook**: at most 7 numbered steps, each with action, why, and done-when. More than 7 means the question is too big; split it.

## Rules

- Commit to one answer; qualify it only by the condition that would flip it.
- Be concrete: technology names, amounts, week estimates. Label estimates.
- Prescribe the principle, not a specific person's stack.
