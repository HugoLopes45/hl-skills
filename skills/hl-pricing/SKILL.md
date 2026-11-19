---
name: hl-pricing
description: "Propose a price structure from supplied buyer evidence, cost to serve, and the current offer: value metric, packages, a candidate price range, and a test on new buyers first. Works for any product, market, currency, or business model; never sets a number without evidence, never forecasts revenue, and never states a price-change notice rule. Use when the user asks what to charge, how to package plans, whether to raise prices, or how to test a price."
---
# Pricing

Input: `[product or service] [current prices and plans, optional] [cost to serve, optional] [buyer evidence: survey, interviews, win/loss notes, past tests, optional] [market and currency, when they change the basis]`

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.

## Evidence rules

- Every price proposal names its basis: buyer evidence, cost to serve, or a tested result. A proposal with no basis is `Hypothesis`.
- Cost to serve sets a floor. A price below it loses money on each sale. It does not set the price.
- Survey stated intent is not a purchase or a reliable upper bound on demand. Treat it as a hypothesis to test, never as an observed purchase rate or a demand curve. Use a survey only with its sample size, question wording, and method, and label it as stated intent.
- An interview or a sample describes those people. It is not a market share, and it is not a measure of the whole market.
- A competitor's price is a dated observation of its public list. It becomes a benchmark only when its plan, currency, tax basis, and billing period match yours.
- Do not forecast revenue or conversion for a price change. Propose the test that would produce the number.
- A price increase for existing customers is the owner's decision. Notice periods and consent rules differ by market and contract. This skill does not state them; the owner checks the current official rule for each market before any change.
- Write currency and tax as supplied. Do not convert or add tax unless the user gives the rate and its date.
- Do not write a discount, anchor, or "was" price without the dated price history that supports it. Discount rules: see [references/price-changes.md](references/price-changes.md).

## Intent

- Act directly when the product, the current prices, and a basis are supplied.
- Ask focused questions when the product or the current offer cannot be described (see Stop conditions). Group related questions in one message, and ask again when an answer changes the proposal. Do not cap the number of rounds.
- A clear request with partial evidence proceeds on the basis given. Label each missing input `unknown` and each assumption `assumed`.
- Reuse what the user already supplied. Do not ask for it again.
- Give a default only for a choice the user can accept, such as the test length. For a fact (price, cost, customer count, market), write `Default: none`.
- An exact output format the user names replaces the default wrapper. The evidence rules still apply inside it.

## Workflow

1. **Scope.** Record the offer, the current prices with their dates, the cost to serve per unit (or `unknown`), the buyers, and the currency.
2. **Choose the value metric.** Pick the unit that grows with the value the buyer gets: seats, orders, published items, storage, or a fixed package. Reject a metric the buyer cannot predict before buying, and name what you rejected and why.
3. **Shape the packages.** Each plan serves one buyer group with one job. Merge plans whose buyers and jobs are the same. Keep the fewest plans that keep the jobs distinct.
4. **Set a candidate range.** Use evidence specific to each buyer group to assess value and willingness to pay; use costs to check viability and comparable prices as context, not substitutes for demand evidence. Name each buyer group's next best alternative (what that buyer would use if this product did not exist) and its cost to that buyer, place the candidate range against it, and name the value that justifies any price above it. If supported willingness to pay falls below the cost floor, report no viable range under those assumptions. Do not raise the range above the floor and claim buyers will pay it. Show each basis and mark the range `Supported` or `Hypothesis` by the verdict definitions in Output.
5. **Specify a conditional test, not a launch instruction.** Propose a new-buyer experiment with one changed variable, defined outcome measures, decision rule and owner-approved duration. State its population: new-buyer conversion and retention cannot establish existing-customer retention after a price increase. If comparable cost viability is unknown, label the experiment `blocked: cost evidence missing`; describe its design without telling the user to execute it.
6. **Check the floor and the claims.** Confirm the range clears the cost floor on a matching unit and period before calling the test ready to launch. A higher price than today's price does not establish viability. If usage or cost per paying customer is unknown, keep viability unresolved, draft the conditional test, and name the missing cost evidence as a launch gate. Remove each unsupported discount, anchor and forecast.
7. **Write what would change the proposal.** Name the evidence that would move the range or reject the value metric.

## Output

Reader: a founder, product owner, or pricing lead who decides what to test this quarter. The decision served: which structure and range to test, and what must be measured before any existing customer sees a change.

Line 1 is one bold plain sentence that states the proposed structure, or what blocks it. It never opens with a label, verdict word, or number.

Under line 1, in plain sentences: the basis of each number, the cost floor, what is `unknown`, and what you did not read.

Cover the value metric (chosen and rejected), packages, candidate range and basis, conditional test, and evidence that would change the proposal. Use a bold plain sentence per point, not a field label. Name each source; state assumptions in the sentence.

Verdict words:
- `Supported`: the candidate range rests on supplied buyer evidence and a cost floor, and the test is designed.
- `Hypothesis`: the range rests on assumed inputs, stated intent, or one source; test before use.
- `Stopped`: the offer cannot be described, or a change request has no current price to start from.
- `Reviewed`: a page audit or paywall review read the supplied page or screen; each gap and its fix are listed in Next.

A page audit or paywall review uses `Reviewed`. Its line 1 is one bold sentence that states the gap to fix first, or that none was found.

Put `Verdict: <word>` on its own line just before `**Next:**`. A short qualifier may follow the word. Separate a proposed test from readiness to launch. If cost viability is unknown, say so in the opening. For a price test, Next contains evidence collection and readiness checks only; omit instructions to run or launch the experiment. A later readiness decision must establish that the proposed price clears the comparable cost floor.

Stopped: line 1 says what is missing and why it blocks the proposal. Then `Verdict: Stopped`. Next holds the grouped questions, each with its default (or `Default: none` for a fact) and what it changes.

Reader rules:
- Define each term once at first use: value metric (the unit the price scales with), packaging (how plans bundle features), cost to serve (what delivering one unit costs), floor (the lowest price that covers cost to serve), stated intent (what buyers say they would pay, not an observed transaction).
- No hype, no promised results, and no "best value" claim without a comparison.

Example (signature only; the domain is not a fixture):

````markdown
**Charge per serviced bicycle, not per mechanic; the workshop interviews support this unit, but costs still block a price test.**
The three interviews describe these workshops, not the whole market. Repair costs per bicycle are unknown, so no candidate price is ready to test.

1. **A serviced bicycle is the unit the workshops can budget for.**
   Interviews 1 and 3 track spending by bicycle, not mechanic. Charging per mechanic would not match their buying decision.
2. **Separate one-off repairs from scheduled fleet maintenance.**
   The notes describe both jobs. These are proposed packages, not tested demand.
3. **The price range must wait for comparable cost and buyer evidence.**
   What interviewees say they would pay is not a purchase. A later new-buyer test would measure conversion and retention for that group, not existing customers.

Verdict: Hypothesis (costs and willingness to pay remain unverified)

**Next:**
1. Send repair costs per bicycle, the services included, and the measurement period to establish a comparable cost floor.
2. Provide the interview questions and price responses to assess the proposed range against that floor.
3. Have the owner check current notice and consent rules for each market before deciding on any existing-customer change.
````

## Stop conditions

- No product and no offer: Stopped. Ask for the product, the current prices, the buyers, and the cost to serve, grouped in one message, each with its default or `Default: none`.
- A change request for existing customers with no current price: Stopped for that change. Offer a new-buyer test if the offer is described.
- A current price with no buyer evidence and no cost: proceed. Mark the range `Hypothesis` and list the missing inputs in Next.

## References

- Read [references/pricing-models.md](references/pricing-models.md) when choosing how to charge on the value metric.
- Read [references/plan-structure.md](references/plan-structure.md) when setting the plan count, the levers between plans, the access model (freemium, trial), or an enterprise plan.
- Read [references/price-research.md](references/price-research.md) when analyzing a price survey, a feature ranking, or usage data.
- Read [references/price-changes.md](references/price-changes.md) when setting the first price, raising a price, or offering a discount.
- Read [references/pricing-page.md](references/pricing-page.md) when auditing or writing a public pricing page.
- Read [references/paywall.md](references/paywall.md) when the user asks about an in-app paywall, an upgrade screen, or a trial-ending prompt.
- Read [references/service-offers.md](references/service-offers.md) when the business is a local trade or service business with a call-out fee, quote levels, a maintenance plan, add-ons, or a guarantee, or when the offer is a retainer or a coaching engagement.
