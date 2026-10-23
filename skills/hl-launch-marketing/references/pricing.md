# Pricing

Price from the buyer's alternative and segment, not from cost or fear. Show the money math. Label figures as supplied, measured with a method, checked source, unverified, or estimated from stated assumptions.

## Principles

- Compare the buyer's current alternative, expected outcome, and ability to pay; do not infer willingness to pay from a segment name.
- Check which purchasing requirements actually apply, such as single sign-on, audit logs, or support.
- Model whether revenue can cover costs before cash runs out, using explicit assumptions.
- Consider segments, payment terms, and pricing models as hypotheses. Do not promise higher conversion, lower churn, or better customers.

## Modes

### `price` (default)

1. **Buyer**: the segment (solo, small business, mid-market, enterprise).
2. **Current alternative**: what the buyer pays today (tool, staff hours, workaround), with an estimated amount.
3. **Price comparison**: compare the proposed price with the current alternative and explain the difference in outcomes, costs, and switching effort.
4. **Free or paid**: does a free plan drive acquisition or network effects, or does it cannibalize paid plans? Unclear means paid.
5. **Price hypothesis**: propose a price and the buyer test that could support or reject it; acceptance is unknown until observed.
6. **Verdict**: at the end of the reply, `Charge X` (or `Charge X, annual discount Y`, `Wrong segment`, `Do not build`); line 1 gives the price in plain words.

### `tiers`

Table: tier, segment, anchor, gated features or metered usage, monthly price. Gate only what the higher segment needs (single sign-on, audit, SLA), not what everyone needs. Do not assume a top tier changes purchases of the middle tier. Meter what the buyer uses to measure their own return. Enterprise is "contact us" with a starting price. End with the underserved segment and what would capture it.

### `monetize`

Turn a feature into revenue: model (subscription, usage, one-time, outcome-based), revenue per account change, the user action that triggers upgrade intent, the expansion path (seats, usage, tier, add-on), whether it reduces churn, and cost to serve at scale. Label every number.

## Rules

- Show amounts with their assumption: "$50 per seat per month, assuming 20 seats, replacing two hours of manual work per week."
- Never invent market data or relabel an unchecked outside fact as an estimate. Cite a checked source or mark it unverified.

## Stand down

Open-source projects, internal tools, hobby code, or anything without a buyer.
