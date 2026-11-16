---
name: hl-email-sequence
description: "Plan a multi-email sequence as a map: the trigger that enrolls each person, the timing of each step, the skip rule for each step, and the exits that stop the sequence, such as a purchase, an opt-out, or a complaint. Writes no email copy and starts no sends. Use when the user asks for an onboarding, trial, re-engagement, or post-purchase email sequence, or asks when to send follow-ups and when to stop them."
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

- A trigger is a recorded event or an observable condition on recorded data. For inactivity, specify the missing event, observation window, account-age gate, evaluation time and logging coverage. Missing records do not prove inactivity when tracking is incomplete. A scheduler may evaluate the condition; no new analytics event is required. Label unimplemented conditions `proposed`, and use placeholders only for missing inputs.
- Label supplied timing `user-specified`; label timing you propose `assumed`. Neither proves effectiveness. Do not call an interval best practice, or attach an unsupported open rate, click rate or lift.
- An exit or skip rule is a condition the team must implement. List it as a condition. Do not predict its effect.
- Consent: a sequence sends only the message type the person agreed to. Keep transactional and marketing messages in separate sequences. Check the official rule for each recipient's market; this skill does not state legal requirements.
- Name the message each step needs, and point to `hl-email` for its copy. Do not write the copy here.
- Plan only. Do not start, schedule, import, or enable a sequence in any tool.

## Intent

Use targeted questions only when missing context changes the requested deliverable. Group related questions in a round, then continue if essential uncertainty remains; there is no fixed intake checklist or total round limit. Reuse prior answers and do not expand a narrow task into the full workflow.

- Act directly when the goal, recipient relationship and observable entry condition are supplied. Do not ask again for confirmed event names or invent an event to represent a supplied condition.
- Ask only for inputs needed to define or observe entry. Write `Default: none` for missing facts. For a missing goal, offer the first key action named in the notes as a choice.
- Missing timing inputs, such as trial length, do not stop the map. Set each step relative to its trigger and label it `assumed`.
- Reuse what the user already supplied.
- An exact output format the user names replaces the default output. The evidence rules still apply.

## Map rules

1. **One entry.** One enrollment condition and one re-entry rule per sequence. Keep persistent membership or deduplication state so repeated evaluations cannot enroll the same person again when re-entry is forbidden. This state need not be a new analytics event.
2. **Each step has a trigger and a timing.** The timing counts from the entry trigger or the previous step. Name the time zone the send uses: the recipient's local time, or one stated zone.
3. **Each step has a skip rule.** A step is skipped when its goal already happened, for example the person already upgraded. A skipped step is not sent late.
4. **Each step has one goal.** Name the action the step asks for. Two actions mean two steps or a split.
5. **Exits stop the whole sequence.** Write each exit once, below the map, with what happens to pending steps.
6. **Use the fewest steps that each have a reason.** Remove any step that repeats the one before it without new information.

Exit conditions to consider, when the product has them:
- Conversion: the person completes the goal action. Stop marketing steps. Transactional messages the person still needs continue.
- Opt-out: stop marketing steps for the person. Transactional messages continue.
- Complaint or hard bounce: stop all sends to that address until the team resolves it.
- Manual stop: the team removes the person, for example after a support case.

## Output

Reader: the marketer or product owner who builds the sequence in a tool. The decision served: whether the map is ready to build, and which events or consent facts to confirm first.

Line 1 is one bold plain sentence that says whether the map is ready and what blocks it, for example "**The sequence is ready to build once the purchase event is confirmed in the product data.**" It never opens with a label, verdict word, or number.

Under line 1, in plain sentences: each missing input to the entry condition, each consent fact the sequence depends on, and each assumed interval that drives the sequence length.

Map: a table when the sequence has up to 5 steps, with the fields Step, Trigger and timing, and Skip when. With more steps, use one numbered item per step with the same three fields.

After the map, a numbered list of exits, each with its condition and its effect.

Verdict words:
- `Planned`: map complete; timing is identified as user-specified or assumed, and unimplemented conditions are marked proposed.
- `Gaps found`: the supplied sequence has at least one missing trigger, skip rule, or exit. List each gap.
- `Stopped`: no observable entry condition and no description of the flow to plan from.

Put `Verdict: <word>` on its own line just before `**Next:**`. Each Next line is one action a person can take now, in order.

Stopped: line 1 says what is missing and why it blocks the map. Then `Verdict: Stopped`. Next holds the grouped questions, each with its default (or `Default: none`) and what it changes.

Reader rules:
- Define each term once at first use: trigger (the observable condition that enrolls a person), exit (a condition that stops the sequence for a person), hard bounce (an address that the mail system permanently rejects).
- Name the event exactly as the product records it.
- No promised results. No "best time to send".

Example (signature only; the domain is not a fixture):

````markdown
**The care sequence is ready to build once the delivery event is confirmed in the order data.**
The order system records `order_delivered` and `order_placed`, so every skip rule uses a recorded event, and the map is complete. The step timings are assumptions until the team measures them.

| Step | Trigger and timing | Skip when |
|---|---|---|
| 1. Care guide | `order_delivered` plus 1 day (assumed) | `order_placed` after delivery |
| 2. Watering check | step 1 plus 6 days (assumed) | `order_placed` after delivery |
| 3. Repotting tips | step 2 plus 14 days (assumed) | `order_placed` after delivery |

1. **A reorder stops all remaining sequence steps.** The reorder confirmation continues as a transactional message.
2. **Opting out stops marketing messages for this person.** Delivery and care-support messages continue.
3. **A complaint or permanent delivery rejection stops all sends to this address.** Sending stays off until the team resolves the issue.

Verdict: Planned

**Next:**
1. Confirm that `order_delivered` and `order_placed` each fire once per order, in the order data.
2. Confirm the customer agreed to care tips as marketing, or move the steps to a transactional message type.
3. Build the three steps in your email tool and keep sending off until the map is checked.
4. Measure each step with `hl-ab-test-plan` before changing an interval.
````

## Stop conditions

- No observable entry condition and no description of the signup, purchase, trial or re-engagement flow: Stopped. Ask for one of them.
- A sequence supplied with no steps: Stopped. Ask for the list of messages.
