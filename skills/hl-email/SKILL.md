---
name: hl-email
description: "Write or revise one email from a brief: subject, preview text, body, one call to action, and sender footer placeholders. Keeps each claim tied to the brief, marks missing proof as placeholders, and separates transactional from marketing messages. Writes text only and never sends. Use when the user asks for one email, a single announcement, a reply to a lead or customer, or a revision of an existing email."
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

- Use only facts in the brief or in the existing email. Any other claim, figure, date, price, discount, deadline, testimonial, or result becomes `[PLACEHOLDER: proof needed]`, naming the proof that replaces it.
- Do not create urgency. A deadline, stock count, or "last chance" appears only when the brief gives its date or count.
- Name the message type first. A transactional message answers an action the recipient took, such as a confirmation or a receipt. A marketing message promotes a product, an offer, or an event.
- A marketing message gets the footer placeholders: sender identity, unsubscribe link, and postal address. This skill does not state what any law requires. Check the official rule for each recipient's market before sending.
- Do not write a subject that imitates a reply or a forward ("Re:", "Fwd:") unless the message is one.
- Do not assume the recipient's age group, generation, or platform habits. Write for the relationship the brief states.

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
2. **Write the subject and preview.** The subject states what the email contains. The preview adds one fact the subject does not carry.
3. **Write the body.** Open with the reason the recipient gets this email, in terms of their relationship to the sender. Give each idea one paragraph, and keep each paragraph on one line.
4. **Write one call to action.** Use a verb phrase that names the result, with one link placeholder.
5. **Add the sign-off and footer.** The sign-off holds sender name and role placeholders. Add the footer placeholders from the evidence rules for a marketing message.
6. **Test each line.** Trace each claim to the brief. Ask whether another company could send the line unchanged; if yes, replace it with a fact from the brief or a placeholder.

### revise

1. List each fact and claim in the existing email, with the line it comes from.
2. Mark each claim the brief does not support. Replace it with a placeholder, or remove it.
3. Apply draft steps 2 to 6 to the wording.
4. Report each changed sentence with its reason in one sentence.

## Output

Reader: the person who will send this email and must fill each placeholder before sending. The decision served: whether the email can go out once the placeholders are filled.

Line 1 is one bold plain sentence that says whether the email is ready and what blocks it, for example "**The email is ready once you fill two slots: the opening date and the booking link.**" It never opens with a label, verdict word, or number.

Under line 1, in plain sentences: each placeholder that blocks sending, and each missing input that limited the draft.

The email copy goes in a `text` fence, with `Subject:`, `Preview:`, the body, the sign-off, and any footer. Placeholders stay in square brackets. Keep instructions outside the fence.

Verdict words:
- `Draft`: email complete; unsupported claims are placeholders.
- `Revised`: revision complete; each changed sentence is listed.
- `Stopped`: no purpose, recipient relationship, or action to write from.

Put `Verdict: <word>` on its own line just before `**Next:**`. Each Next line is one action a person can take now, in order. Each placeholder appears in Next with the proof that fills it.

Stopped: line 1 says what is missing and why it blocks the email. Then `Verdict: Stopped`. Next holds the grouped questions, each with `Default: none` and what it changes.

Reader rules:
- Define each term once at first use: placeholder (a marked slot for proof you do not have), footer (the lines at the end of a marketing email that name the sender and offer an opt-out).
- No false urgency, no fake reply threads, no exclamation marks in body copy.

Example (signature only; the domain is not a fixture):

````markdown
**The waitlist email is ready once you fill two slots: the opening date and the booking link.**
The brief gives the garden, the waitlist, and the sender, but no opening date or booking link, so the email holds placeholders for both. It is a transactional message, so it has no marketing footer.

```text
Subject: Your plot waitlist place is confirmed
Preview: Spring bookings open on [PLACEHOLDER: opening date]

Hi [PLACEHOLDER: first name],

You joined the waitlist for a plot at Marsh Lane Garden on [PLACEHOLDER: join date].
Bookings open on [PLACEHOLDER: opening date].

Book your plot when bookings open: [PLACEHOLDER: booking link]

[PLACEHOLDER: sender name], Marsh Lane Garden volunteer team
```

Verdict: Draft

**Next:**
1. Replace the opening date with the date the garden committee sets, and confirm it in writing.
2. Replace the booking link with the live booking page address, and open it to test it.
3. Approve the send in writing before anyone sends it; this skill does not send and does not give that approval.
````

## Stop conditions

- No purpose, recipient relationship, or action in the brief: Stopped. Ask for each in one round.
- Two actions in one brief: Stopped. Ask which action the email leads with.
- Revise mode with no existing email: Stopped. Ask for the email text, pasted in the message.
