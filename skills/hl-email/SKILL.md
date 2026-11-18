---
name: hl-email
description: "Write or revise one email from a brief: subject, preview text, body, one call to action, and sender footer placeholders. Keeps each claim tied to the brief, marks missing proof as placeholders, and separates transactional from marketing messages. Writes text only and never sends. Use when the user asks for one email, a single announcement, a journalist pitch, a correction, a reply to a lead or customer, or a revision of an existing email."
---
# Email

Input: `[brief or existing email] [--mode draft|revise]`. Default mode: `draft`.

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

## Evidence rules

- Use only facts in the brief or in the existing email. Any other claim, figure, date, price, discount, deadline, testimonial, or result becomes `[PLACEHOLDER: proof needed]`, naming the proof that replaces it. When the brief supports a narrower line, write that line instead of a placeholder. Never write an invented testimonial.
- Do not create urgency. A deadline, stock count, or "last chance" appears only when the brief gives its date or count.
- Name the message type first. A transactional message answers an action the recipient took, such as a confirmation or a receipt. A marketing message promotes a product, an offer, or an event. A transactional message that carries a promotion or discount is marketing; check the official classification rule for each channel.
- A marketing message gets the footer placeholders: sender identity, unsubscribe link, and postal address. This skill does not state what any law requires. Check the official rule for each recipient's market before sending, and the current official sender requirements for the unsubscribe method and its deadline.
- Do not write a subject that imitates a reply or a forward ("Re:", "Fwd:") unless the message is one.
- Do not assume the recipient's age group, generation, or platform habits. Write for the relationship the brief states.
- Never personalize on health, financial hardship, politics, religion, sexuality or family, even when a public post shows it.
- Keep sensitive details out of the subject and preview. Notifications and lock screens can show them.

## Journalist pitch

- Name the journalist's recent coverage from the brief. Without it, write `[PLACEHOLDER: recent article or beat]`; do not guess the beat.
- State one news hook from the brief. The subject names the specific fact, not the company or the product.
- Offer an embargo only to a journalist whom the brief says has honored one before. State its day, time, and time zone.
- Keep the pitch under 150 words (heuristic default); this cap replaces the draft step 3 length defaults, and the draft step 2 cold-prospect subject rule does not apply. End with one ask, such as an interview or a quote.
- Do not write a "did you get my email" follow-up. Write a follow-up only on request, as its own email, with one further fact from the brief; when the brief shows two follow-ups already sent (heuristic default), write none. Timing of follow-ups belongs to `hl-public-relations`.

## Reply

When the email answers a message from the recipient:
- Answer only the question that message asks, with a fact the user supplies; add nothing else except the one call to action from the brief. When that message asks no question, answer its main point.
- Never criticize another vendor or company.
- When that message asks how the sender got the recipient's address, give the true source from the brief and offer removal.

After a wrong send, write one short correction to each recipient the email reached: name the error and the correct fact, and add no claim or offer beyond the one call to action from the brief.

## Intent

Use targeted questions only when missing context changes the requested deliverable. Group related questions in a round, then continue if essential uncertainty remains; there is no fixed intake checklist or total round limit. Reuse prior answers and do not expand a narrow task into the full workflow.

- Act directly when the brief gives the purpose, the recipient relationship, and the one action.
- Ask in one round when the purpose, the recipient relationship (for example, past customer, trial user, or prospect), or the one action is missing. Explain what each answer changes. Write `Default: none` for each, because each is a fact.
- A missing price, date, or proof does not stop the draft. Use placeholders for those.
- Reuse what the user already supplied. Do not ask again.
- In revise mode, reconcile the brief and the existing email before editing. When asked to keep every supported fact, include supplied facts from both inputs, even if the old email omitted them: price with billing basis, trial terms, feature, and availability date. Check that inventory against the revised copy. Remove only unsupported claims or facts the user explicitly excludes.
- An exact output format the user names, for example only the subject line, replaces the default output. The evidence rules still apply.
- Do not send, schedule, or load the email into a sending tool. If the user asks for that, say that this skill writes text only, and that the send needs its own explicit request.

## Modes

### draft (default)

1. **Fix the message type, recipient, and action.** One action only. If the brief names two actions, ask which one leads; the other moves to a separate message.
2. **Write two subjects and a preview.** The first subject states what the email contains. The second uses a different mechanism, such as a question or a stake the brief supports. Keep each subject 40 to 60 characters and each preview about 90 to 140 characters (heuristic defaults), and pay the subject off in the first 100 words (heuristic default). Put the concrete value first in the subject and the preview. The preview adds one fact the subject does not carry and does not repeat the subject. For a prospect who did not opt in, the subject is 2 to 4 lowercase words (heuristic default), the range above does not apply, and the subject uses no first name, number, urgency, emoji, or pitch; if it is a question, it names a specific problem. Never use a generic question such as "quick question", and never imitate a reply or an internal message.
3. **Write the body.** Open with the reason the recipient gets this email, in terms of their relationship to the sender. Give each idea one paragraph of one to three sentences (heuristic default), and keep each paragraph on one line. Heuristic default lengths: 50 to 125 words for a transactional message, 150 to 300 for an educational marketing email, and 300 to 500 for a story. For a message to a prospect who did not opt in, keep the body under 80 words (heuristic default) and use one shape: an observation from the brief or a user-supplied source, the one problem it implies, the result figure the user supplies (or its placeholder), and one reply ask. Leave out any sentence that needs a recipient detail (name, company, role) the brief lacks; other missing values stay placeholders. When the brief gives no first name, use a greeting with no name. Never imply a closer relationship than the brief states. Do not vary the copy by a trait you inferred about the recipient. Vary it only by a segment the brief states. When the user supplies sample emails, match their register; use no stock greeting, opener, or emoji unless the samples use them.
4. **Write one call to action.** Use a verb phrase that names the result, with one link placeholder or a reply ask. Use one primary button or one link.
5. **Add the sign-off and footer.** The sign-off holds sender name and role placeholders. Add the footer placeholders from the evidence rules for a marketing message.
6. **Test each line.** Trace each claim to the brief. Ask whether another company could send the line unchanged; if yes, replace it with a fact from the brief or a placeholder. Remove these AI tells: contrast reveals ("it's not X, it's Y"), "no X, no Y" lists, trailing pile-on clauses, questions you answer yourself, colon reveals, stock phrases, jargon such as "synergy" or "leverage", dashes in the subject and preview, fake Re: or Fwd: prefixes, clickbait subjects, stock openers, and sign-off filler. Check each dimension in [the calibration reference](references/email-calibration.md) and rewrite the weakest first.

### revise

1. List each fact and claim in the existing email, with the line it comes from.
2. Mark each claim the brief does not support. Replace it with a placeholder, or remove it.
3. Run draft steps 2 to 6 as checks on the wording. Change only the sentences the revision needs; keep the rest of the copy as written.
4. Report each changed sentence with its reason in one sentence.

## Output

Reader: the person who will send this email and must fill each placeholder before sending. The decision served: whether the email can go out once the placeholders are filled.

Line 1 is one bold plain sentence that says whether the email is ready and what blocks it, for example "**The email is ready once you fill two slots: the opening date and the booking link.**" It never opens with a label, verdict word, or number.

Under line 1, in plain sentences: each placeholder that blocks sending, and each missing input that limited the draft.

The email copy goes in a `text` fence, with `Subject:`, `Alternate subject:`, `Preview:`, the body, the sign-off, and any footer. In revise mode, include `Alternate subject:` only when the revision rewrites the subject. Placeholders stay in square brackets. Keep instructions outside the fence.

Verdict words:
- `Draft`: email complete; unsupported claims are placeholders.
- `Revised`: revision complete; each changed sentence is listed.
- `Stopped`: a stop condition applies; the email is not written.

Put `Verdict: <word>` on its own line just before `**Next:**`. Each Next line is one action a person can take now, in order. Each placeholder appears in Next with the proof that fills it.

Stopped: line 1 says what is missing and why it blocks the email. Then `Verdict: Stopped`. Next holds the grouped questions, each with `Default: none` and what it changes.

Reader rules:
- Define each term once at first use: placeholder (a marked slot for proof you do not have), footer (the lines at the end of a marketing email that name the sender and offer an opt-out).
- No false urgency, no fake reply threads, no exclamation marks in body copy.

Example (signature only; the domain is not a fixture):

````markdown
**The waitlist email is ready once you fill four slots: the join date, the opening date, the booking link, and the sender name.**
The brief gives the garden, the waitlist, and the sending team, but no join date, opening date, booking link, or sender name, so the email holds a placeholder for each. It is a transactional message, so it has no marketing footer.

```text
Subject: Your Marsh Lane waitlist place is confirmed for spring
Alternate subject: When can you book your spring plot at Marsh Lane?
Preview: You joined the waitlist on [PLACEHOLDER: join date]. Bookings open on [PLACEHOLDER: opening date]; the link is below.

Hi,

You joined the waitlist for a plot at Marsh Lane Garden on [PLACEHOLDER: join date]. This email confirms your place on the list.

Bookings open on [PLACEHOLDER: opening date]. Use the booking link below on that day to book your plot. Keep this email until then, so the link is easy to find.

Book your plot when bookings open: [PLACEHOLDER: booking link]

[PLACEHOLDER: sender name], Marsh Lane Garden volunteer team
```

Verdict: Draft

**Next:**
1. Choose one subject line before the send; the alternate subject is an option, not a second email.
2. Fill the join date for each recipient from the waitlist record.
3. Replace the opening date with the date the garden committee sets, and confirm it in writing.
4. Replace the booking link with the live booking page address, and open it to test it.
5. Replace the sender name with the name of the person who sends the email, as the garden team approves it.
6. Approve the send in writing before anyone sends it; this skill does not send and does not give that approval.
````

## Stop conditions

- No purpose, recipient relationship, or action in the brief: Stopped. Ask for each in one round.
- Two actions in one brief: Stopped. Ask which action the email leads with.
- Revise mode with no existing email: Stopped. Ask for the email text, pasted in the message.
