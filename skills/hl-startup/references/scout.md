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

1. First line: the pick and its score, or `NO SHIPPABLE BET`. Then the scope line: inputs, depth, date.
2. Signal digest (`deep` only): clusters, signal count each, dead lanes.
3. Bet table: buyer · promise · gates (solo-ops / AI-build) · score · status.
4. Top 3: full bet block + build sketch assuming boilerplate start (auth/billing/email solved, sketch only the product's own 5%): assumed stack labeled assumption, surfaces/endpoints, entities, external services, fixture, smoke test (setup/input/action/expected output), human-only steps. One economics line each: customers needed for €500/€1k/€3k MRR at hypothesized price, net of variable costs. `quick`: the pick's block only, no build sketch.
5. The pick: one bet, why it beat the runner-up, this-week validation plan with kill-by date. Honest paid CTA (pre-order or paid pilot; waitlist is secondary evidence), one problem post where the buyer hangs out (describe the pain, don't pitch), concierge fulfilment for the first five with money upfront. Each step names its kill signal. `quick`: nothing after the steps but the closing line. Name the pick as input for the `evaluate` mode; nothing gets built before it survives the assumption and problem stages.

Every candidate gated out → print `NO SHIPPABLE BET` with failed conditions, never force a winner. Don't write files unless asked.
