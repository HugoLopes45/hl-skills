# Billing and win-back sequences

Load for a failed payment, card expiry, renewal notice, price change, upgrade, annual switch, cancelled customer, cancellation survey, expired trial, dormant past customer, or a paused subscription that resumes billing. The map rules, exits and "Before the first send" checks in `SKILL.md` apply; this file adds the billing and win-back patterns.

Every day offset here is `assumed` unless the user supplies it. Each offset counts from the trigger named in its section. Cancel flows, save offers and in-app dunning are outside this file; the cancellation survey email is inside it.

## Failed payment

- Trigger: a payment fails. Step 1 on day 0 is a friendly notice with one update-payment link. Assume an accident, such as an expired card.
- Step 2 on day 3 is a reminder that access may stop. It says what happens to the data, from the user's terms.
- Step 3 on day 7 says access stops on a stated date and lists what the customer loses.
- Step 4 on day 10 to 14 is the final notice. It states the pause date and how to restore access.
- Each step has one call to action: update the payment method.
- Each step skips when the payment succeeds, the customer cancels, or the plan changes.
- Set the grace-period access rule per customer type and write it in the map. Do not lock the account at once. Pause the account; do not delete its data.
- After a recovered payment, the billing steps stop, so send the backup payment method ask as a separate one-step sequence: trigger on the recovery, send once, skip when a backup method is on file. The customer has just seen the failure.

## Card expiry and renewal

- Send a card-expiry notice before the card expires. Heuristic default: 30, 15 and 7 days before expiry.
- Send a renewal notice before an annual renewal, with the amount, the date and a link to the payment method. Check your terms and the market's rule for any notice period the renewal needs.

## Price change

- Trigger: the new price and its effective date are set.
- Announce the change 30 to 60 days before the effective date (heuristic default). Remind at 14 days and send a final notice at 7 days (heuristic default). Check the notice period the terms require before you set these.
- The first message gives the reason for the change in the customer's terms.
- Offer the options the terms allow, such as keeping the old rate for a period, an annual plan, or a lower plan.
- Skip a step when the customer already changed plan or cancelled.

## Cancelled customers

- Trigger: the cancellation takes effect. The access-end confirmation is transactional and goes at once, outside this sequence.
- Step 1 at 30 days after cancellation says what changed since the customer left.
- Step 2 at 60 days addresses the reason the customer gave, and only when the customer gave one.
- Step 3 at 90 days makes one return offer, when the team has one.
- Use no guilt and no pressure. Make the return one action.
- After the last step without a response, suppress marketing sends for 90 days (heuristic default), then stop the sequence.

## Expired trial

- Trigger: the trial ended without a conversion.
- Step 1 at 1 day after expiry says the trial ended and what the customer keeps or loses.
- Step 2 at 7 days asks what held the customer back.
- Step 3 at 14 days offers an incentive or an extended trial, when the team has one.
- Step 4 at 30 days is the final message. It says the door stays open.
- Segment by recorded trial use. High use: help removing the friction that blocks the purchase. Low use: a fresh start with onboarding help. No use: ask what happened and offer a demo or a call.
- Hold any discount to step 3. Step 1 and step 2 carry no discount.

## Upgrade

- Trigger: a plan limit recorded as reached, or a trial day the team sets. Label the trigger `proposed` until the product records it.
- Step 1 summarizes what the customer did on the plan. Step 2 shows the limit reached and the plan that lifts it. Each step has one upgrade link.
- Skip the steps when the plan has changed.

## Switch to annual

- Trigger: a monthly subscriber reaches a renewal date the team sets.
- One email gives the yearly saving from the current price list, the same features, and one switch link.
- Skip when the plan is annual.

## Dormant past customers

- Trigger: the last recorded job is 12 to 24 months old (heuristic default).
- Step 1 names one recorded fact about the customer's system (the equipment the business recorded at a past job). Step 2 gives one reason to book. Step 3 asks the customer to stay on the list or be removed.
- Skip step 1 for a customer with no recorded system. Label the timing `assumed`.

## Cancellation survey

- Trigger: the cancellation takes effect and the in-app survey was skipped. Send on the cancellation day.
- Ask the primary reason in one question, with one optional free-text line.
- Treat a message as transactional only when it answers an action the recipient took and carries no offer; otherwise treat it as marketing. The classification stays unverified until the user checks the official rule. Confirm that the terms allow a survey after cancellation.

## Paused subscription resumes

- Trigger: a paused subscription is set to resume billing on a date.
- Send one notice before the first charge, with the resume date and the amount. Check the notice period the terms and the market's rule require, and label any lead time you set `assumed`.
- Skip the notice when the customer cancelled or resumed early.

## Offers in billing messages

A billing or win-back message that carries an offer is marketing. Do not send it as a transactional message.
