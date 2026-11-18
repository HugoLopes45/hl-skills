# Failed Payment Recovery

Read this file when a payment fails, a card expires, or a renewal is near. The evidence rules and Output in `SKILL.md` apply. Email copy, notice timing, the backup-method ask, and renewal notices belong to `hl-email-sequence`.

## Account state

- Access follows only the provider's subscription status events: past due, cancellation scheduled, cancelled at the effective date, and ended.
- Verify each event name and its meaning in the provider's current documentation before wiring it.
- A failed one-off charge changes no access and counts as no churn.
- A cancellation scheduled for a later date keeps access until that date.
- Write the owner's map: each provider event goes to one account state.

## Decline types

Map each provider decline code to one type, using the provider's current documentation.

- Soft (temporary, such as low balance or a processing error) --> retry on the schedule below.
- Hard (permanent, such as a card reported lost or stolen, a closed account, or an expired card) --> no retry; ask for a new payment method.
- Authentication (the bank needs the customer to confirm) --> send the customer to confirm; check in the provider's current documentation whether a server-side retry can clear it.
- Code not in the documentation --> `unclassified`: no retry until the owner classifies it as soft using verified provider guidance. Ask for that guidance or a new payment method.

## Retry schedule

- The owner sets a spaced schedule for soft-decline retries; heuristic default: about four retries over seven to ten days, on different days, then stop.
- Run one retry schedule per subscription. If the provider runs its own retries, turn off the second schedule so that two systems do not retry the same payment.
- Each retry stops when a payment succeeds, the subscription changes, or the customer cancels.
- `proposed`: test whether retry on the day of the month the payment first succeeded, avoiding weekends, recovers more than the spaced schedule above. Keep the spaced schedule until a test shows the gain.

## Grace period and pause

Set proposed access by customer type only when an event in the owner's verified provider-status map permits the change. Preserve existing access without that event. Immediate lockout is never the first step.

- B2B: full access during the grace period (heuristic default). The owner sets the length; heuristic default: 7 to 14 days after the last failed attempt.
- Consumer: read-only access (heuristic default), with a visible notice that the payment is past due and how to fix it, on every page until the payment succeeds.
- Blank customer type on a record --> the grace rule is `unavailable` for that account. No customer type field and no customer type stated --> `Gaps found`.
- After the grace period, propose a pause only when the owner's verified provider-status map permits it. Do not delete account data. Deletion follows the owner's stated retention terms.

## Timeline rules

- Payment fails, soft --> schedule retries; the failure alone changes no access.
- A mapped subscription-status event arrives --> apply the mapped account state and its grace rule for the customer type.
- Retry succeeds --> stop the billing messages; restore access only when the mapped subscription-status event confirms it.
- Last retry fails --> follow the mapped account state and grace rule; the failure alone changes no access.
- Payment fails, hard --> no retry; the notice asks for a new method.
- Payment fails, authentication --> the notice asks the customer to confirm.
- Customer cancels or changes plan --> stop retries and notices.

## Card expiry and renewal

- Card expiry: propose a notice before expiry only when the billing export carries the expiry date. Without it, the notice is `unavailable`; this is not a gap.
- Annual renewal: check the market's notice rule with the owner's adviser. This file states no notice period.

## Measures

- Recovery: payments that succeed after a failure, per decline type, over the failures of that type.
- Report the failure count as the base. A failure with no recorded outcome is `not stated`, not a failure.
- Time to recovery: the median days from the first failure to a successful payment, per decline type.
- Involuntary share: from the split in `SKILL.md`, over all churn events.
