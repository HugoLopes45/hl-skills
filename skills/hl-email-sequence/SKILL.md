---
name: hl-email-sequence
description: "Plan a multi-email sequence as a map: the trigger that enrolls each person, the timing of each step, the skip rule for each step, and the exits that stop the sequence, such as a purchase, an opt-out, or a complaint. Writes no email copy and starts no sends. Use when the user asks for an onboarding, trial, cold-outreach, billing, win-back, event-follow-up, re-engagement, or post-purchase email sequence, or asks when to send follow-ups and when to stop them."
---
# Email Sequence

Input: `[product event notes, signup or purchase flow, or an existing sequence] [goal, optional]`

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

## Evidence rules

- A trigger is a recorded event or an observable condition on recorded data. For inactivity, specify the missing event, observation window, account-age gate, evaluation time and logging coverage. Missing records do not prove inactivity when tracking is incomplete. A scheduler may evaluate the condition; no new analytics event is required. Label unimplemented conditions `proposed`, and use placeholders only for missing inputs. A behavior trigger with a count or time threshold, such as several page views, names the threshold; the team sets it from its own data and labels it `proposed`.
- Label supplied timing `user-specified`; label timing you propose `assumed`. Neither proves effectiveness. Do not call an interval best practice, or attach an unsupported open rate, click rate or lift. Judge each step on clicks, replies and conversions, never on opens.
- An exit or skip rule is a condition the team must implement. List it as a condition. Do not predict its effect.
- Consent: a sequence sends only the message type and frequency the person agreed to, cold outreach included. For cold outreach, the permission to send stays unverified until the user confirms it; see [cold-outreach.md](references/cold-outreach.md). Keep transactional and marketing messages in separate sequences. Keep a record of each opt-in: its time, its source and the disclosure text shown. Do not make consent a condition of purchase. Keep these records for the period the official rule sets. Check the official rule for each recipient's market; this skill does not state legal requirements.
- Name the message each step needs, and point to `hl-email` for its copy. Do not write the copy here. For a proof step without supplied proof, name a demonstration or a checkable fact, never a testimonial.
- Plan only. Do not start, schedule, import, or enable a sequence in any tool.

## Intent

Use targeted questions only when missing context changes the requested deliverable. Group related questions in a round, then continue if essential uncertainty remains; there is no fixed intake checklist or total round limit. Reuse prior answers and do not expand a narrow task into the full workflow.

- Act directly when the goal, recipient relationship and observable entry condition are supplied. Do not ask again for confirmed event names or invent an event to represent a supplied condition.
- Ask only for inputs needed to define or observe entry, and for a sequence that sells, ask for the price, the free-to-paid bridge, and the top 2-3 objections in the customer's words. Write `Default: none` for missing facts. A missing sales input does not stop the map; list it in the output and ask for it in Next. For a missing goal, offer the first key action named in the notes as a choice.
- Missing timing inputs, such as trial length, do not stop the map. Set each step relative to its trigger and label it `assumed`.
- Reuse what the user already supplied. For an existing sequence, change only the steps the user names, and keep the other steps' triggers, timing, and skip rules.
- For an audit of an existing program, mark each pattern under Sequence patterns as present, missing or stale. A pattern is stale when its trigger, timing or copy no longer matches the recorded events or the terms the user supplies. List first the gaps that serve the result the supplied goal names; with no goal, keep the Sequence patterns order and ask for the goal in Next. In the output, replace the map with one numbered item per missing or stale pattern.
- When the request fits more than one sequence, build the one asked for and map each other reading in one line in the output. Do not expand the asked sequence.
- An exact output format the user names replaces the default output. The evidence rules still apply.

## Map rules

1. **One entry.** One enrollment condition and one re-entry rule per sequence. Keep persistent membership or deduplication state so repeated evaluations cannot enroll the same person again when re-entry is forbidden. This state need not be a new analytics event. A person in one marketing sequence gets no step from another marketing sequence. Enroll each segment from one recorded field, such as plan, role or use case; a person sits in one segment at a time.
2. **Each step has a trigger and a timing.** The timing counts from the entry trigger or the previous step. Name the time zone the send uses: the recipient's local time, or one stated zone. Send marketing steps in a daytime window labeled `assumed`; when the list spans jurisdictions, use the stricter local window, and check each market's hours in its official source. Space early steps closer together and widen later gaps, as an `assumed` default the team measures. Use a daily cadence only for a dated deadline in the supplied facts.
3. **Each step has a skip rule.** A step is skipped when its goal already happened, for example the person already upgraded. A skipped step is not sent late.
4. **Each step has one goal and one call to action.** Name the action the step asks for. Two actions mean two steps or a split. In a sequence that sells, name the step that first makes the offer and the bridge from the free step to it.
5. **Exits stop the whole sequence.** Write each exit once, below the map, with what happens to pending steps.
6. **Use the fewest steps that each have a reason.** Remove any step that repeats the one before it without new information. Set the step count from the decision: use more steps for a higher price, a longer time to decide, or more decision makers, and fewer steps for the opposite. The list size does not set the count. Label the count `assumed` unless the user supplies it.

Exit conditions to consider, when the product has them:
- Conversion: the person completes the goal action, such as a booking or a payment. Stop marketing steps. Transactional messages the person still needs continue.
- Reply: the person replies to any step. Stop all pending steps; a person answers the reply.
- Opt-out: stop marketing steps for the person. Transactional messages continue. Check the current official rule for the opt-out method and its deadline in each recipient's market, and write the deadline in the map once checked.
- Complaint or hard bounce: stop all sends to that address until the team resolves it.
- Manual stop: the team removes the person, for example after a support case.
- Elapsed time: stop the sequence after the maximum duration the map states. A step due after that point is not sent late.
- Payment recovered or plan changed: stop the billing steps for that subscription.

## Before the first send

Before the first send, check the sending domain against the current official sender requirements:
- one SPF record that includes the sending service;
- a DKIM key at the selector the sending service signs with;
- a DMARC record and a From domain that aligns with the SPF or DKIM domain; on a domain with no DMARC record, start at `p=none` (heuristic default) with a reporting address, and tighten only after reports show legitimate mail stays aligned;
- an MX record, so replies reach an inbox;
- one-click unsubscribe headers on marketing messages, with the opt-out honored within the deadline the current sender requirements set;
- a From domain you own, not a free mail domain; check the current official sender requirements for bulk mail.

Warm each new mailbox for the warm-up period the team sets, labeled `assumed`, before its first stage. Ramp the volume in stages on a domain or mailbox with no sending history: each stage is a messages-per-day limit, labeled `assumed`. Raise the volume to the next stage only while the complaint and bounce checks stay within the limits the official requirements set. Read those limits in the provider's current official sender guidelines and record each figure with its source and check date. Without that check, mark the limit unverified and keep the first stage. This file states no provider-specific limit. The Output reports the check results; list each open check in Next. Set a weekly cap on marketing sends per person and spread large sends over several hours; the cap is `assumed` until complaint data supports it.

## Sequence patterns

- **Re-engagement.** Define inactivity by a click unless the user supplies another event. Send three `assumed` steps in order: the best existing content, a re-permission ask that asks the person to confirm they still want the mail, and a sunset notice with one click to stay or leave. Stop marketing sends to an address that does not answer. The inactivity window is `user-specified` or `assumed`; a 90 to 180 day window is a heuristic default, not a rule.
- **Post-purchase.** Place the first-win step, the first step that shows the product working, inside the refund window the user supplies. Place steps 2 and 3 before that window closes, since the buyer still decides whether to keep the purchase; label this placement `assumed`. If the refund window is missing, write `Default: none` and list it as a missing input.
- **Event follow-ups.** For quotes, missed calls, job completion, reviews, reminders, seasonal reminders and unscheduled treatment plans, read [event-follow-ups.md](references/event-follow-ups.md).
- **Cold outreach.** For recipients who did not opt in, read [cold-outreach.md](references/cold-outreach.md).
- **Usage report.** Send a usage report only when it shows real usage. Skip it when the period has no recorded usage. Send one milestone email per recorded milestone, and name the next one.
- **Subscription review ask.** Trigger on a recorded milestone or renewal, never on a completed job. Send one sentence and one link. Check the review platform's current policy before the ask.
- **Struggle outreach.** Trigger on a struggle event the product records. Name that event only as the data shows it, offer direct help rather than only a documentation link, and send no sales pitch.
- **Billing and win-back.** For a failed payment, card expiry, renewal notice, price change, upgrade, annual switch, cancelled customer, cancellation survey, expired trial, dormant past customer or a paused subscription that resumes billing, read [billing-and-winback.md](references/billing-and-winback.md).
- **Welcome.** Step 1 sends at once: the promised item, one next action, and what the later steps cover. Each later step shows one step of value the person can reach, with one ask. Label the interval `assumed`.
- **Lead nurture.** Step 1 delivers the lead magnet. Later steps cover the buyer's problem, the approach, one proof the user supplies, how the offer differs from alternatives, and one objection. The offer comes last, with one ask per step.
- **Product onboarding.** Each step skips when the in-app step it repeats is done. Email carries what the app does not show: a check-in, an unused feature, and an upgrade ask after the recorded activation event.
- **Setup reminder.** Trigger: a required setup event is absent after a window the team sets (`proposed`). Name the step the person started, link to it, and offer help. Skip when the event exists. Confirm tracking records the setup event before the rule runs.
- **Team invite.** Trigger: an existing user invites a person. The invitee gets one email that names the inviter and what the invitee joins. Send one reminder if the invite is not accepted; skip it once accepted. Treat a message as transactional only when it answers an action the recipient took and carries no offer; otherwise treat it as marketing. The classification stays unverified until the user checks the official rule.
- **Launch or seasonal offer.** Run the steps to the real open and close dates in the supplied facts: an announcement, a midpoint reminder, and a last call that states the true end time. Label the step count `assumed`.
- **Product update.** Send one email per release, only to users of the feature it changes.

## Output

Reader: the marketer or product owner who builds the sequence in a tool. The decision served: whether the map is ready to build, and which events or consent facts to confirm first.

Line 1 is one bold plain sentence that says whether the map is ready and what blocks it, for example "**The sequence is ready to build once the purchase event is confirmed in the product data.**" It never opens with a label, verdict word, or number.

Under line 1, in plain sentences: each missing input to the entry condition, each consent fact the sequence depends on, each assumed interval that drives the sequence length, and each missing sales input (price, the free-to-paid bridge: the step that leads a free user to the paid offer, and objections) for a sequence that sells.

Map: a table when the sequence has up to 5 steps, with the fields Step, Trigger and timing, and Skip when. With more steps, use one numbered item per step with the same three fields.

After the map, a numbered list of exits, each with its condition and its effect. After the exits, the check results for the sending domain and each volume stage, with each proposed volume marked `assumed` and each unread check marked `unverified`. Then one line per other reading of the request, if any.

Verdict words:
- `Planned`: map complete, or an audited program with no missing or stale pattern; timing is identified as user-specified or assumed, and unimplemented conditions are marked proposed.
- `Gaps found`: the supplied sequence or audited program has at least one missing or stale pattern, trigger, skip rule, or exit. List each gap.
- `Stopped`: no observable entry condition and no description of the flow to plan from.

Put `Verdict: <word>` on its own line just before `**Next:**`. Each Next line is one action a person can take now, in order.

Stopped: line 1 says what is missing and why it blocks the map. Then `Verdict: Stopped`. Next holds the grouped questions, each with its default (or `Default: none`) and what it changes.

Reader rules:
- Define each term once at first use: trigger (the observable condition that enrolls a person), exit (a condition that stops the sequence for a person), hard bounce (an address that the mail system permanently rejects).
- Name the event exactly as the product records it.
- No promised results. No "best time to send".

Example (signature only; the domain is not a fixture):

````markdown
**The care sequence is ready to build once you supply the refund window and confirm the delivery event.**
The order system records `order_delivered` and `order_placed`, so every skip rule uses a recorded event. The refund window is missing, so the placement of the steps against it is not set yet. The care tips are marketing messages, so the steps need the customer's marketing consent, which the notes do not confirm. The step timings are assumptions until the team measures them.

| Step | Trigger and timing | Skip when |
|---|---|---|
| 1. First win: care guide | `order_delivered` plus 1 day (assumed) | `order_placed` after delivery |
| 2. Watering check | step 1 plus 6 days (assumed) | `order_placed` after delivery |
| 3. Repotting tips | step 2 plus 14 days (assumed) | `order_placed` after delivery |

1. **A reorder stops all remaining sequence steps.** The reorder confirmation continues as a transactional message.
2. **Opting out stops marketing messages for this person.** Delivery and care-support messages continue. The opt-out deadline is not set yet.
3. **A complaint or permanent delivery rejection stops all sends to this address.** Sending stays off until the team resolves the issue.

Sending domain: SPF, DKIM, DMARC and MX are unverified (I did not read the DNS records). The unsubscribe headers and the From domain are unverified (I did not send a test message). No volume stage is set yet (assumed).

Verdict: Planned

**Next:**
1. Supply the refund window in days, then place the first-win step inside it and steps 2 and 3 before it closes.
2. Confirm that `order_delivered` and `order_placed` each fire once per order, in the order data.
3. Confirm the customer agreed to care tips as marketing, or move the steps to a transactional message type.
4. Check the current official opt-out rule and its deadline for your market, then write the deadline into the opt-out exit.
5. Check the sending domain's SPF record (the list of servers allowed to send), DKIM key (the signature that shows the mail was not altered), DMARC policy (what receivers do with mail that fails those checks) and MX record (the route that lets replies reach an inbox), plus the one-click unsubscribe headers and the From domain, against the current official sender requirements before the first send.
6. Build the three steps in your email tool and keep sending off until the map is checked.
7. Measure each step with `hl-ab-test-plan` before changing an interval.
````

## Stop conditions

- No observable entry condition and no description of the signup, purchase, trial or re-engagement flow: Stopped. Ask for one of them.
- A sequence supplied with no steps: Stopped. Ask for the list of messages.
