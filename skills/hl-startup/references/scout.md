# Scout

Input: `scout [niche|audience|skills] [--count N] [--depth quick|deep]`

Find SaaS bets a solo dev can ship with an AI coding agent and run in under two hours a week. Research first, generate second: every idea traces to observed pain or spend, never a brainstorm. AI-buildable: a coding agent can implement, verify, and deploy it from a written packet; the product itself needs no AI feature. Never promise revenue: return hypotheses with evidence, and end every pick with the falsifying test and its kill-by date. Kill fast: a killed bet costs a week, a zombie costs a year.

## Every run

1. Parse args: niche or open field, count (default 8), depth (default deep). They form the scope line (Output item 1).
2. Founder edge: list only assets the user named (domain knowledge, audience, paid tools, painful workflows). Nothing named → edge is zero, say so, move on. Never invent access.
3. Mine signals, cluster, generate bets, gate, score, report.

## Signal mining

`deep` (default): live web research is mandatory; a market claim from training data does not count. No web access: run `quick` and say so. Three lanes:

- **Pain lane**: a specific buyer + spending/behavior words ("too expensive", "alternative to", "manual", "spreadsheet", "takes hours", "missing feature", "looking for a tool"). Sources across ≥3 types: paid-tool reviews, Reddit/HN threads, GitHub issues, job/freelance posts, app-marketplace listings, pricing pages.
- **Transfer lane**: a workflow already paid for in one market that's missing/overpriced/badly localized in another (geography, language, segment). Business-sale marketplaces (Acquire.com, Flippa, Microns, Dotmarket) are idea mines, not proof: listing revenue/traffic are seller claims, asking price is never willingness-to-pay.
- **Open field** (no niche given): seed queries from the boundary of two unrelated industries. Earns bets only with real signals at the boundary; else drop and say so.

Collect 10-15 signals, each with URL + date. Independent = distinct author/company; syndicated copies count once. Search-result count is never market size; a trend explains why-now only, never proves demand (Google Trends is relative interest, not volume). Also search disconfirming evidence: native feature ship, mature free substitutes, declining demand. Two reformulations, nothing found → report the dead lane, don't fabricate one.

`quick`: no live research; every market claim carries `[unverified]`; cap 5 bets. A shortlist to research, not a verdict. At most 400 words, spent as: first and scope lines ≤30 words together; table cells ≤10 words each; the pick's block ≤7 lines of ≤20 words, economics line included; three validation steps ≤20 words each; one closing line.

Cluster signals by buyer + painful event. In `deep`, a bet needs a cluster with two independent signals.

## Bets

Generate through three lenses: **timing arbitrage** (viable now via an API/platform/rule change), **complaint miner** (what buyers hate about tools the signals surfaced), **constraint-first** (shippable from a boilerplate in days). One block each:

- buyer: one person you could DM, not "SMBs"
- painful event and current workaround
- paid promise and the one core feature
- why now: a specific trigger, not "AI is big"
- price hypothesis and channel where this buyer already hangs out
- evidence: signal refs, or `[unverified]` in quick; transfer bets add origin market + local gap (language, currency, integrations, distribution)

Rejected at generation, before any gate: generic AI wrappers with no buyer-specific workflow ("ChatGPT for X"), feature clones with no segment wedge, intersections with no shared workflow, direct clones where the origin company already serves the target market.

## Gates

Both hard: score never overrides; unknown on a core condition is not a pass.

**Solo-ops**: one buyer, one painful event, one core outcome. Paid path shippable in ≤14 solo days (agent-written code does not shrink this; count integration, fixtures, deployment, human setup). Auth/billing/email are boilerplate, not outcomes: the 14 days buy the 5% that's yours. No two-sided liquidity, enterprise procurement, per-result regulated judgment (legal/medical/financial), or brittle scraping. ≤2 essential external APIs. ~80% gross margin after variable costs. Support <2 hours/week at 20 customers.

**AI-buildability**: all six hold or the bet dies:

1. Specifiable: one flow as endpoints, entities, acceptance checks, no product decisions left to the agent.
2. Generatable: conventional primitives, maintained dependencies; every critical API publicly documented with a self-serve test path.
3. Data-accessible: fixture/seed data demonstrates the paid outcome; core value doesn't need private/negotiated data.
4. Verifiable: 3-5 observable acceptance checks + one reproducible happy-path smoke test.
5. Deployable: standard managed target, no custom infra/hardware.
6. Human-bounded: API keys, DNS, billing, store approvals listed human-only, none blocking the core build.

Verdict per bet: PASS · BORDERLINE (one non-core unknown, name the reframe removing it) · KILL.

A product calling a model API additionally needs an eval fixture, an observable quality check, a max variable cost per paid outcome. No fixture → KILL.

## Scoring

Survivors only. Integers, unknown=0, total /10: pain frequency+urgency 0-2 · evidence of existing spend 0-2 · buyer reachability 0-2 · build/ops simplicity 0-2 · why-now tailwind 0-1 · founder fit 0-1. Ties break on reachability.

## Output

Reader: a founder choosing one product to test this month. The decision served: which bet to validate this week.

Line 1, bold: one plain sentence with the bet and why it wins, or the failed gate when no bet passes. End with `Verdict: Pick: <bet>, <score>/10`, or `Verdict: No shippable bet`, just before `**Next:**`. Say what you searched and when in one plain sentence under line 1.

Body, in this order, one heading per point:
1. Signal digest (`deep` only): table of cluster, signals found, dead lanes.
2. Bet table: buyer, promise, gates (solo-ops / AI-build), score, status. Legend once above the table: `PASS` holds, `BORDERLINE` has one non-core unknown, `KILL` fails.
3. Top 3 (`deep`): one block per bet, one field per line: buyer, pain, current workaround, promise, why now, price and channel, evidence. Economics as one line: customers needed for €500, €1k, and €3k a month at the hypothesized price, net of variable costs, marked `derived`.
4. The pick: one bet, why it beat the runner-up, then a numbered validation list. Each step names its kill-by date and kill signal. The honest paid offer comes first (pre-order or paid pilot; a waitlist is weaker evidence).

`quick`: step 3 shows the pick's block only, with no build sketch. Market claims tagged `[unverified]`. At most 400 words. Last line names `evaluate` as the next step.

Reader rules:
- Define once: solo-ops (one person can run it), AI-buildable (a coding agent can build it from a written spec), fixture (sample data that tests the core outcome), pilot (a paid trial with a few users).
- Search results are not market size. A trend shows why now, not demand.
- Every candidate gated out: say `No shippable bet` with the failed conditions. Never force a winner.
- Write no files unless asked.
