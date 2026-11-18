# Method

Use this file for the fields of each row, the trigger, the counting rules, the naming rules, and the plan sections. The workflow and evidence rules are in `SKILL.md`.

## Chain

Each row names its parent row.

- **Decision**: the choice the tracking informs, its owner, and its review date when supplied.
- **Metric**: a number that informs a decision. Fields: name, question it answers, numerator, denominator, time window, time zone, unit, owner, and the dedupe key when the metric counts people.
- **Event**: one recorded action that supplies a metric input. Fields: name, trigger, platform (web, app, or server), sender (client or server), consent category, metric, owner.
- **Property**: one detail attached to an event. Fields: name, type, allowed values, required, personal data (yes, no, or `not stated`), consent category, owner.

Name a rate's denominator from the user's input. When the input names none, propose one and label it `Proposed`.

Define each funnel as an ordered list of events, one event per step. Examples only; derive the names from the decision: signup (`signup_started`, `signup_completed`); purchase (`pricing_viewed`, `plan_selected`, `checkout_started`, `purchase_completed`).

## Trigger

The trigger is the user action or system state that sends the event.
- State whether the trigger is an attempt or an outcome. A click on "Submit" is an attempt. A server confirmation is an outcome. Name the outcome when the metric counts completed actions.
- Name the page, control, or state, for example "booking form, server confirmation received".
- When the success state appears without a page change, or the form runs in a frame, hook the success state itself: the success callback, the frame's success message, or a first-party confirmation page. A page view or a button click never proves success.
- Send the event without delaying or failing the user action. Add a `pending` row to Verification that checks the control does not wait for the tracking request, and that a failed tracking request leaves the action completed.
- A soft event, such as a page view or a button click, must not be the primary optimisation target. When an ad platform receives it, mark it reporting-only.

## Counting

- When the metric counts people, count each person once: dedupe repeat events with a key the user supplies. When none is supplied, propose one, label it `Proposed`, and send it through the identifiers check in [privacy-and-consent.md](privacy-and-consent.md).
- Give a value (the amount the metric sums) to an event only when every event the metric counts carries one. A value on some events and none on others makes the total mix units.
- Take a monetary value from the application's numeric amount and a separate currency, never from displayed text. Send no event when the amount is missing or invalid; reserve `0` for an explicitly free item. State whether the amount includes tax and shipping, once for every sender.
- When a client and a server send the same conversion, specify one shared event ID, anything else the destination's current documentation requires to count it once, and its dedupe window. When the input shows both senders and no shared event ID, mark the event `blocked: shared event ID not stated`. Give each purchase a unique transaction ID, the same in every send, so a reload does not count it twice.
- Set the counting unit for each conversion in the `## Conversions` plan section: once per person or session for leads and sign-ups, every occurrence for purchases.
- Only one conversion per outcome is primary. When the plan changes a primary flag, add a Next step: the ad account owner checks which conversions bidding uses.
- Ask the owner for the click-through window of each conversion an ad platform receives, matched to how long buyers take to decide: short for urgent needs, longer for considered purchases. Write `not stated` until the owner answers.
- Treat a modelled or estimated conversion, such as one the platform infers, as reporting-only until a holdout or pause test shows it adds outcomes the business would not get anyway.
- For a call conversion, take the minimum call duration from the owner's call data, so misdials do not count. Write `not stated` until the owner supplies it.
- Plan a downstream outcome, such as a qualified lead or a closed deal, or an offline or CRM-uploaded conversion, as primary only when its expected volume clears the minimum the target platform documents. Estimate a downstream volume as lead volume times close rate. Check the minimum in the platform's official documentation; write it `unknown` until you do. When the volume falls short or the minimum is `unknown`, plan it as reporting-only.

## Naming

- Event names: `object_action` in snake_case, past tense for a completed action, such as `booking_form_submitted`.
- Property names: snake_case nouns, such as `service_type`.
- Put a value in a property, not in the event name. Send `placement` with the value `header`; do not create `header_button_clicked`.
- Keep one name for one concept across all events.
- Give every enumerated property its complete list of allowed values.
- Do not rename a name that is already in use. Record a rename as a change in the plan.
- Build campaign link values from one shared list of allowed values: lowercase, hyphens between words, one spelling per source.
- For partner links, `utm_medium` names the deal type (`newsletter`, `creator`, `podcast`, `affiliate`, `community`) and `utm_source` names the partner or platform. When the user supplies no list of deal types, label these `Proposed`. For paid creator deals, propose `creator`, not `social` or `video`.
- Never put personal data in a URL parameter. Referrer logs and reports keep it.
- Test each campaign link's final landing URL after redirects and shorteners before launch.
- Create one link per placement and date, so each placement's clicks stay separate.

## Channels

- Map each campaign medium to a channel group in the analytics tool before launch, so its traffic does not land in an unassigned bucket. Check the tool's current default grouping for each medium; do not assume it.
- Track visits from AI assistants in one channel, matched by assistant referrers from the tool's current documentation or the referrer log.
- Report that channel as a floor. Visits without a referrer are missed, so the channel undercounts.

## Property rules

- Reuse one property name each for page, referrer, campaign, product, and timing before you create another. Add a property only when a named metric needs it. Starter names, for a metric that needs them: `page_path`, `page_referrer`, `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`, `product_id`, `unit_price` with `currency`, `event_timestamp`. Do not duplicate a property the analytics tool already sends automatically; check its documentation.
- Store the ordered touch path (channel and timestamp per touch) only when a named decision uses it, such as a multi-touch model. Treat it as a personal-data candidate until the legal owner decides.
- Ask the owner whether the attribution signals (an ad click identifier, campaign parameters, and the referrer) are captured at first touch and stored with the lead record. Without them, a later offline or CRM match fails. Run the click identifier through the identifiers check in [privacy-and-consent.md](privacy-and-consent.md). Store each source with its basis: verified, self-reported, or fallback.
- For a B2B decision that counts accounts, plan an account key from the company's email domain. Exclude free-mail domains (consumer mailbox providers); match those contacts by hand, or leave them unmatched and record the unmatched share as a rate. Treat the email domain as a personal-data candidate.

## Verification checks

- For each event, check four failures, each with its check: the event does not fire (trigger, tag or call, consent state); a property has a wrong value (the payload field); the event fires twice (count the events for one test action); the conversion does not arrive (the destination shows it).
- Before go-live, check duplicate fires, exclusion of internal and test traffic, mobile and in-app browsers, and leftover test values.
- After each deploy or campaign launch, the tester repeats the checks for the events and links it touched, and escalates a broken purchase conversion to its owner at once. Add one `pending` row to `## Verification` for this repeat check.
- Give each test record a searchable marker. The tester runs it in a real browser on the real page with no real personal data, then removes it from the destination. A local or staging run, or a missing request in a network log, does not show whether the deployed page sends the event. The agent does not run these tests. A synthetic test proves transport only, never attribution.

## Plan sections

- `## Decisions and metrics`: decision, owner, metric, numerator, denominator, window, time zone, unit, dedupe key when the metric counts people.
- `## Events`: event, trigger, platform and sender, consent category, metric, owner, status (`specified`, `not implemented`, or `blocked: <reason>`).
- `## Conversions`: conversion, event, primary or reporting-only, counting unit, metric it feeds, click-through window, minimum call duration (call conversions), path and ad-platform action (paid-channel leads).
- `## Properties`: event, property, type, allowed values, required, personal data, owner.
- `## Owners`: item, owner, consumer (the report or decision that reads it).
- `## Privacy and consent`: item, finding, status (`open`, `closed`, or `not stated`), owner who decides.
- `## Verification`: event, test action, expected fields, where the payload is checked, `fired` status, `arrived` status (each `pending` until its check runs).
- `## Open questions`: question, what it blocks, default or `Default: none`.
