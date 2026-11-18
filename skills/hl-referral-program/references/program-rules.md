# Program rules

Read this file before writing any reward rule, the adviser list, the fraud checks, or a reconciliation table. Each item is a question or a rule to specify, not an answer.

## Rules to define before quoting a rate

1. Eligible action: one event the program can observe, such as the referred customer's second paid order, taken after the refund window.
2. Base: collected revenue after refunds, excluding taxes, as supplied. Affiliates: the same base unless the owner's terms say otherwise.
3. Rate or amount: a fixed amount or a rate, with currency and rounding stated. With tiers, set each tier's threshold, rate, and the rule for moving between tiers, and check the total reward cost per paying customer in each tier against the max total reward cost (SKILL.md, workflow step 3).
4. Duration: one order, a fixed number of renewals, or the life of the customer, with the cap stated. A launch-period reward also states its start and end dates.
5. Attribution window and duplicates: the number of days after the click or code use that still credits the referrer. The owner sets the number from the sales cycle; otherwise `unknown`. One reward per referred customer, and one referrer per referred customer under the attribution priority the owner sets.
6. Hold window: days from the eligible action until the reward becomes due. The owner sets the number; it must cover the refund window in the owner's terms.
7. Expiry and clawback: the expiry of a credit, and the reversal of a paid reward after a refund or chargeback.
8. Exit: the treatment of pending and accrued rewards when the program ends or the terms change.

## Advocate tiers

Use this block only for a program whose referrers are unpaid or lightly rewarded advocates in tiers.

Each tier needs three owner-stated items: an entry condition counted per advocate from the attribution record, a reward, and a rule for dropping back a tier.
A condition the owner cannot count from records is `unknown`. A missing condition, reward, or drop-back rule for a tier gives the verdict `Stopped`.
No tier promises earnings or income.
The sum of tier rewards for one referred customer stays within the max total reward cost (SKILL.md, workflow step 3).
An advocate offered a paid deal is evaluated by `hl-creator-deal`, not here.

## Adviser checklist

1. Which reward forms the owner offers (cash, store credit, free months, gifts), and how each is treated for tax and accounting in each market where it is paid.
2. The consumer-law rules for promotions in each market: conditions, expiry, change and exit, and how they must be shown.
3. The disclosure a referrer or partner must show next to a link or code, and the current official endorsement guidance for each market.
4. Whether a referrer may send invitations to contacts the referrer chose, and what consent a referred person needs before the program contacts them.
5. The data-protection basis for storing referrer and referred customer details, and how long records are kept.
6. Platform or marketplace rules on referral and review incentives, and whether a reward is allowed there at all.
7. Payouts: threshold, schedule, currency, rounding, and any tax form or withholding for partners paid as contractors.
8. Refund, chargeback, and cancellation effects on paid rewards and commissions, including the clawback right and the notice.
9. Affiliate contract terms: exclusivity, sub-affiliates, brand bidding, coupon publishing, termination, treatment of accrued commissions, and any buyout of future commissions. Do not suggest a buyout multiple.
10. Changes to the terms, the dispute contact, and the record of terms each participant accepted.

## Fraud and self-referral checks

1. Self-referral: the referrer and the referred customer share a payment method, address, device, or email domain. Treat it as a signal; hold the reward until the eligible action and the hold window pass.
2. Referral rings: accounts that refer each other in pairs or groups.
3. Fake or disposable contact details: verify the referred customer's email before the reward becomes due.
4. Shared IP address or device across unrelated customers: a review signal, not proof.
5. A coupon partner publishing a code on public sites: an owner policy decision. It is not fraud by default.
6. A refund or chargeback after a reward is paid: reverse it under the clawback term and record the reason.
7. Apply each rule the same way to every participant, and keep the evidence for each decision.

## Reconciliation states

| State | Enter when |
|---|---|
| pending | A conversion exists and the hold window has not passed. |
| due | The eligible action is done, the hold window has passed, and no refund or dispute is open. |
| paid | A payout record exists in the payment or payout tool. |
| reversed | A refund, chargeback, or fraud finding removes the reward before payment, or a clawback removes it after payment. |
| disputed | The participant or the owner contests the record. Hold it until resolved. |
