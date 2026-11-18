---
name: hl-churn-prevention
description: "Plan churn prevention from supplied cancellation, billing, and usage data: the voluntary and involuntary split, a cancel flow with reason capture and one matched save offer, failed-payment recovery rules, and risk signals from usage only. Writes the plan; sends nothing and changes no account or billing setting. Use when the user asks why customers cancel, how to cut cancellations, how to recover failed payments, or which accounts are at risk (not for win-back or failed-payment emails: `hl-email-sequence`; not for price changes or paywalls: `hl-pricing`)."
---
# Churn Prevention

Input: `[cancellation export: subscription, account type, request date, effective end date, end reason] [billing export: subscription, event date, event type, decline type] [usage export, optional: subscription, week, key actions] [current cancel and signup flows, optional] [offers you can make, optional] [market and customer type, B2B or B2C]`

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

## Evidence rules

- Split and rates use only supplied records. Name each figure's file, fields, period (by effective end date), market, and denominator. A blank field is `not stated`. A record with no end reason is `unclassified`: count it apart and never assign it to either type.
- A failed one-off charge is not churn. Churn is a subscription that ends. Access follows the provider's subscription status, not a single charge.
- Write no save rate, recovery rate, churn target, or revenue figure without a supplied source. A figure this skill gives as a heuristic default is labeled so in the same sentence; it is a starting setting, not a measured result.
- A save counts only when the account is still active at the end of the owner's later window (heuristic default: 30 days after the cancel request). An accepted offer alone is not a save.
- Risk signals come only from columns in the supplied usage export. Compare each account with its own earlier usage.
- A discount, credit, or price concession enters the plan only with the dated price history that `hl-pricing` requires. Without it, the concession is a hypothesis to test.
- Cancellation, refund, notice, and consent rules differ by market and contract, and they change. This skill states none. Check the current official text for each market before any flow ships, and send each question to the owner's adviser. Legal, tax, and contract questions go to the adviser; list them, never answer them.
- Forecast no save, recovered revenue, or churn change. Propose the test that measures it, labeled `proposed`.

## Intent

- This skill proposes a plan. It never sends, retries a charge, or changes access, billing, or a subscription.
- Write the plan directly when the cancellation and billing exports are supplied with their fields.
- Ask focused questions in one round when no cancellation or billing data and no flow description is supplied. Write `Default: none` for each fact and say what each answer changes.
- Missing usage data removes the risk signals only. The split and the flows still proceed.
- Reuse what the user supplied.
- An exact output format the user names replaces the default output; the evidence rules still apply.
- Refuse a request to make cancelling harder to find, to add pressure or guilt copy, or to state a save or recovery figure with no source. Say why in one sentence, then give the lawful alternative the plan supports: a visible control and a measured test.

## Workflow

1. **Split churn.** Count the subscriptions that ended in the period, by effective end date. Voluntary: the customer asked to cancel. Involuntary: the subscription ended after failed payments. Any other record, including a blank reason, is `unclassified`. Report each count and its share of all churn events. Report the churn rate only when the supplied data carries its inputs: subscriptions that ended in the period, divided by subscriptions active at the period start. Report net revenue churn only when the supplied data carries monthly recurring revenue (MRR): MRR lost to cancellations and downgrades, minus MRR gained from upgrades, divided by starting MRR. Otherwise omit the figure; this is not a gap.
2. **Map account state.** Access follows only the provider's subscription status events. A cancellation with a future effective date keeps access until that date. Read [references/failed-payment.md](references/failed-payment.md) for the event and decline rules.
3. **Design the cancel path.** Read [references/cancel-flow.md](references/cancel-flow.md) when designing or reviewing it. Cover reason capture, one matched save offer, a visible decline, and a cancel that completes when the offer fails. Add no step beyond the ones in that file.
4. **Design failed-payment recovery.** Read [references/failed-payment.md](references/failed-payment.md). Classify each decline, propose retries for soft declines only, route authentication cases to the customer, set the grace rule by customer type, and propose a backup-method ask only after a recovery.
5. **Set risk signals.** Read [references/risk-signals.md](references/risk-signals.md) when the user asks which accounts are at risk. Use supplied usage columns only, and report each unavailable signal.
6. **Set the measures.** For each part, name the count, its base, and the test that would show a change. Targets come from the owner. Split each measure by plan, tenure, and the reason the customer chose in the cancel flow, where a supplied export carries the field; without the field, omit that split. This is not a gap.
7. **Hand off.** Failed-payment and win-back emails, with their copy and timing: `hl-email-sequence`. Price changes, discounts, paywalls: `hl-pricing`. Test design: `hl-ab-test-plan`. Reports after launch: `hl-reporting`. Activation before any cancel: `hl-onboarding`. List each hand-off in Next.

## Output

Reader: the owner of the subscription, who decides which cancel and recovery changes to build and test first. The decision served: what to change, and what to measure before any change ships.

Line 1 is one bold plain sentence that gives the main finding: the split, or the largest gap. It never opens with a label, verdict word, or number.

Under line 1, in plain sentences: the period and market covered, each `unclassified` count, each missing field, and each part you did not read or set.

Then numbered points, most decision-relevant first. Each point has one bold plain sentence, its count or rule, its basis (measured from the export, or a heuristic default), and its limit. A split with up to 5 rows fits a table with the fields Type, Count, and Basis.

Verdict words:
- `Planned`: the split, cancel path, recovery rules, and signals are set from supplied data. Each measure is `proposed` until a test reads it. A blank field, a short usage history, or an owner number that is not set is not a gap: it makes a record `unclassified`, or an account or signal `unavailable`.
- `Gaps found`: a field the plan needs is absent from the supplied data, or a rule the owner must supply is missing, so at least one part is not set. Next lists each gap.
- `Stopped`: no cancellation or billing data and no flow description to plan from.

Put `Verdict: <word>` on its own line just before `**Next:**`. Each Next line is one action a person can take now, in dependency order, including each hand-off.

Stopped: line 1 says what is missing and why it blocks the plan. Then `Verdict: Stopped`. Next holds the grouped questions, each with `Default: none` for a fact and what the answer changes.

Reader rules:
- Define each term once at first use: voluntary churn (the customer ends the subscription), involuntary churn (failed payments end it), save offer (a concession shown before a cancel completes), grace period (access kept after a failed payment), decline type (soft: temporary; hard: permanent; authentication: the customer must confirm).
- Quote field names and values exactly.
- Promise no saves or recoveries. Write "payment failed", never "you failed to pay".
- Blame no one for the current flow.

Example (signature only; the domain is not a fixture):

````markdown
**Roast Club lost 40 subscriptions in October: 18 voluntary, 14 involuntary, and 8 with no end reason.**
The export covers 1 to 31 October 2026 by effective end date, consumer accounts in the UK. I read the cancellation and billing exports; I did not read usage, so no risk signal is set.

| Type | Count | Basis |
|---|---|---|
| Voluntary | 18 (45.0% of 40) | measured, `end_reason` = customer_cancel |
| Involuntary | 14 (35.0% of 40) | measured, `end_reason` = payment_failed |
| Unclassified | 8 (20.0% of 40) | blank `end_reason`, not split |

1. **The cancel page asks for no reason, so the 18 voluntary cancellations have none on record.**
   Add one reason question before the cancel completes. Its save offer comes only from offers you supplied; a price concession also needs dated price history.
2. **The 14 failed payments cannot be routed yet.**
   The export has no decline type, so a soft decline cannot be told from a hard one. No recovery figure is stated, and none is set.

Verdict: Gaps found

**Next:**
1. Add the decline type to the billing export for the 14 involuntary records.
2. Fill the blank `end_reason` on the 8 unclassified records from the provider record, then recount the split.
3. Send the usage export for these 40 subscriptions, with the columns it holds, so risk signals can be set.
4. Send the failed-payment and win-back emails to `hl-email-sequence` for copy and timing.
````

## Stop conditions

- No cancellation or billing data, and no description of the cancel or billing flow: Stopped. Ask for the exports with the fields named in Input, or for the flow. Default: none.
- The cancellation export has no end reason field, and no other field separates voluntary from involuntary: `Gaps found` for the split. The flow and recovery parts still proceed.
- Risk signals requested and no usage export supplied: `Gaps found`. Name the columns the export must carry.
