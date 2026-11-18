# Offer

Design the offer, pick one acquisition channel and run enough attempts to learn, and check that the unit economics work. Name dollars and rates, not "engagement".

Tier structure and segment pricing belong to `pricing.md`.

## Principles

- Compare the buyer's desired outcome, supporting proof, time to result, and effort. This is a qualitative lens, not a measured value equation.
- Choose an outreach budget that fits the channel, access, and consent. Attempt counts alone prove neither demand nor a stable conversion rate.
- Charge for the outcome, not the time.
- Compare warm outreach, cold outreach, paid ads, and content where they fit the buyer. Start with one testable channel.
- A lead is a contactable person who showed interest, not a follower or a view.
- Unit economics first: customer acquisition cost (CAC) against lifetime value (LTV). Compare payback with the business's cash constraints; a benchmark is not a universal viability rule.
- Bonuses add value against named objections, real scarcity creates urgency, and guarantees reverse risk.
- Repetition with iteration beats cleverness in outreach scripts, ad hooks, and content angles.
- Pick the offer shape from the sales motion: a self-serve signup with a trial, a sales-led deal with a paid diagnostic credited to the first month, or done-for-you work with a fixed-scope sprint before any retainer. Do not borrow the bonus stack or scarcity pattern of another motion.
- Per business type: for a service, fix the scope, timeline, and price before work starts; for lifetime access, define what "lifetime" covers.

## Modes

### `offer` (default)

Before ranking, state the current offer in one plain line. Rank its weakest parts without numeric scores, and fix one part per iteration.

1. **Buyer and outcome gate**: identify a concrete buyer and the state change they want, not a feature. Lift the stated request one level to the outcome behind it, named specifically enough that the buyer can repeat it. Missing or vague buyer/outcome stops analysis before proof, time, effort, bonuses, or price. State the gap; Next owns the missing buyer/result decision and validation. If copy was requested, deliver it completely with explicit `[PLACEHOLDER]` slots, not invented claims.
2. **Proof it works**: proof that it works for this buyer (a checked case study, demo, or niche testimonial); a guarantee is a promise, not observed proof. Name the failure path and how the offer handles it.
3. **Time to first win**: how long until the outcome, and what the first win in 7 days is. Promise only a timeline that delivery can meet; a missed promise lowers trust for later buyers.
4. **Effort for the buyer**: what the buyer must do. Done for them beats done with them beats do it yourself. Write the scope before work starts: what is included, what is excluded, and what is optional.
5. **Bonuses**: each tied to a named objection and the part of the offer it moves.
   - Each bonus has a stated value that the buyer can check against a comparable price.
   - Total bonus value stays under twice the core price (heuristic default).
   - Each bonus is one you would sell on its own.
   - Use at most five bonuses (heuristic default), each closing a different objection; none is fine.
   - Time delivery: speed items on day one, support items after the first week, completion items at the finish.
   - Remove any bonus that closes no named objection. If the offer converts only because of its bonuses, fix the core first.
6. **Guarantee**: choose the guarantee type from the buyer's named risk. Keep the conditions to at most two (heuristic default). Before publishing, check the refund cost at the expected claim rate; a guarantee the business cannot afford to honor fails this step. Offer a guarantee, such as no result, no fee, only after the owner confirms the business can honor it. Write the guarantee as one sentence: the promised result or term, the window, and what the buyer gets if it is missed.
7. **Scarcity**: use scarcity only when a real, verifiable constraint exists, such as seats, a dated cohort, or capacity. Enforce it when reached. Otherwise omit it.
8. **Name**: a name the buyer can repeat to a friend with the outcome in one line: "I just bought the [name]; it does [outcome]." If the buyer cannot repeat it, rename it.
9. **Price and comparison**: something comparable the buyer already accepts as expensive, then the price. State the payment terms the buyer can pay with, and check that they fit the buyer's cash. Offer an upsell or cross-sell only to a buyer with a named use for it; never add it as a hidden charge. Offer add-ons before a discount, and a recurring plan where the buyer needs repeat service. A switching offer, such as free migration or paying out a rival contract, counts its cost in CAC; contract terms go to the owner's legal adviser.
10. **Verdict**: at the end of the reply, `Strong`, `Not yet, fix <term>` (the term in plain words), or `Wrong buyer`; line 1 says the decision in plain words.

Example when the buyer and result are unknown; if one line of offer copy was requested:

````markdown
**BakeScale's offer does not yet name a buyer or a concrete result.**

```text
BakeScale helps [BUYER] achieve [CONCRETE RESULT] through [MECHANISM].
```

Verdict: Not yet, fix the buyer and outcome

**Next:**
1. Which buyer and concrete result should replace the placeholders? (default)
2. Validate that result with the named buyer before publishing the copy.
````

### `acquire`

Match the channel to the price point and to where the buyer already is. Record attempts, outcomes, sampling limits, and the agreed budget on the chosen channel. Funnel math: leads, conversations, close rate, CAC, each measured or labeled estimate. Test a changed offer on a small sample before scaling it. State any projected lift as a range with its basis. The verdict names one channel, an attempt target, and the next move this week.

The lead magnet shows the outcome in five minutes. It leads into the paid offer, not a separate product. Run each candidate through these tests; fix or drop each failure:

- Specific: names the buyer, outcome, timeframe, and method. A competitor could not use the same title unchanged.
- Bridge: using it creates the want for the paid offer. If the connection needs explaining, drop it.
- Quick win: solves one problem completely in one sitting. Work that takes weeks is homework.
- Value: the outcome and proof outweigh the delay and effort of using it. Judge qualitatively, as in Principles.
- Defensible: an AI assistant or a search result cannot replace it. Personal or interactive output, original data, and working tools pass; known advice in a document fails.

Match the format to the funnel step: a checklist or quiz for awareness, a comparison or assessment for consideration, a template or trial for decision. Gate the full asset only at the decision step; leave awareness teaching open. A personal result, such as a quiz result or checker band, may be gated at any step. Ask for the fields the follow-up needs, starting with email. For a local service magnet, the follow-up may need a phone number or postcode; ask for it only when the follow-up uses it. Check the magnet copy against this bar: gives before it asks, curiosity with a stated benefit, and no false scarcity or fake loss. Judge a magnet by lead quality: replies, progress to a trial or demo, unsubscribes after delivery, and fit with the buyer; sign-up count alone is not a result. Test one magnet variable at a time (headline, format, gate level, field count, call to action, or delivery). For the test plan, suggest `hl-ab-test-plan`.

### `economics`

Table: CAC, LTV, gross margin, payback period, monthly burn and runway, each marked measured or estimated. Count CAC blended: all acquisition cost in the period, including staff time and tools, divided by new paying customers; label a paid-only figure as paid-only. Compare figures with supplied business constraints. Any benchmark threshold is a proposed heuristic, not a universal pass/fail rule; refunds alone do not establish their cause. Set a CAC ceiling at the payback limit the cash constraint allows; a CAC above the ceiling triggers an immediate review of the channel and the offer. The first line states the number that hurts the business most, as a figure (for example `LTV $180 < CAC $250`), and the one move that changes it.

### `constraint`

List what limits growth (sales capacity, support, product limits, delivery, hiring), then pick the single constraint. If acquisition is the constraint, propose a bounded experiment with its attempt budget, cost, success criterion, and stop condition. If the next step needs a hire: who, doing what, paid how, freeing which task. The verdict is optimize or push volume.

## Stop-list

Remove these from the offer and its copy:

- "Limited time" without a real deadline.
- "Worth $X" without a comparable product the buyer can check.
- "100% guaranteed" without stated conditions.

## Stand down

Questions with no intended buyer (open source, internal tools, hobby projects). An unspecified commercial buyer uses the buyer/outcome gate instead.
