# Cancel Flow

Read this file when you design or review the cancel path. The evidence rules and Output in `SKILL.md` apply.

## Path and steps

- Put the cancel control on the page where the subscription is managed, one step from the billing or account page.
- Use only these steps, in order. Each one is required by a rule below. Skip step 2 when the reason gives no offer:
  1. Reason: one question with the reason choices below and optional free text. The customer can skip the question and continue.
  2. Save offer: one offer matched to the reason, shown once.
  3. Confirm: the access end date (the last day of the paid period), what happens to the account data under the owner's terms, an offer of a data export before any deletion the owner's terms allow, and two controls of equal weight: cancel and keep.
  4. Complete: the cancel completes when the offer fails, times out, or is declined.
- After completion, show the access end date and, when the owner's terms allow reactivation, a visible reactivation control. Send the cancel confirmation with the same facts, as a transactional message; its copy belongs to `hl-email-sequence`.
- For an account above an MRR threshold the owner sets, notify a named person when the cancel request is made. The cancel does not wait for that person. Any customer contact by that person follows the offer and copy rules below and makes no offer the flow already showed.
- Stop the win-back steps when the customer returns. The win-back sequence belongs to `hl-email-sequence`.

## Reason to save offer

Each rule gives one offer from the owner's supplied list, or no offer.

- Price --> a concession only with dated price history; otherwise a lower plan the owner supplies.
- Not using it --> a pause, only when billing supports pause, with a length the owner sets; otherwise a help session the owner supplies.
- Missing feature --> a dated roadmap statement the owner supplies; otherwise no offer.
- Technical problem --> a route to support, shown as help and not as a save.
- Switching to another tool --> an offer only when the owner supplies one for this reason; otherwise no offer. The optional free text in step 1 records the tool. Make no claim about a rival tool without a dated source.
- Business closed or changed --> no offer; go to confirm.
- Other or no answer --> no offer; go to confirm.

## Offer rules

The reason map picks the offer. The first-30-days and annual-plan bullets below replace only a price concession. When both apply, the first-30-days bullet wins.

- Show at most one save offer per session. A declined offer is not shown again in that session.
- Give no repeat offer of the same kind to a customer who cancels again inside the save window.
- Show a deadline only when the owner's terms set a real end date. No countdown, and no "offer ends when you leave" text.
- Show the amount saved in the billed currency and period, as supplied.
- A customer in the first 30 days gets setup help the owner supplies instead of a price concession; 30 days is a heuristic default.
- A lower plan offer shows what the customer keeps and what the lower plan removes, in plain words, before the customer accepts. After the customer accepts a lower plan, offer no upgrade for the period the owner sets.
- An annual plan gets a pause of the remaining term when billing supports it; otherwise a lower plan, instead of a price concession. Any refund follows the owner's written terms.
- A pause keeps account data and settings. Limit repeat pauses to the number the owner sets. The notice before a paused subscription resumes billing belongs to `hl-email-sequence`.

## Copy and control rules

- No guilt, shame, or loss framing aimed at the customer, such as implying that they abandon the team. State what happens, in plain words. Quote each guilt or loss line in the supplied flow and replace it with that plain statement.
- The keep control has the same size, contrast, and visual weight as the cancel control. No pre-selected upsell and no extra consent to cancel.
- The cancel control is found from the subscription page without search and without a help article.
- Each screen after the reason has a visible control that continues the cancel.
- The access end date comes from the billing period. The flow does not change it.

## Measures

- Save: the account is still active at the end of the owner's later window (heuristic default: 30 days after the cancel request). Report saves with their cancel sessions as the base.
- Count each step: reason chosen, offer shown, offer accepted, cancel completed.
- A drop in completed cancels is a fault in the flow, not a save.

## Law check, not a rule

This file states no cancellation rule. Before any flow ships, check the current official text for each market, and send these questions to the owner's adviser:
- Whether a cancel must be as easy as signup, and which steps that covers.
- Whether a save offer or a second confirmation is allowed before the cancel completes.
- What notice and confirmation the cancel must show, and whether the customer must receive a copy.
- How long account data is kept after the cancel, under the owner's terms and the market's data rule.
