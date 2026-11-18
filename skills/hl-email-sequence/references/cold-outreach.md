# Cold outreach sequences

Load when the recipients did not opt in: prospects from a list you built, or contacts who never asked for mail. The map rules, exits and "Before the first send" checks in `SKILL.md` apply; this file adds the cold-only rules.

## Lists and consent

- Keep cold prospects out of opt-in list tools. Before any load, check the tool's current terms on sending to addresses without consent.
- Check the current official rule for each prospect's market. This file states no legal requirement. Exclude a prospect whose market's official rule requires prior consent for cold email until consent exists.
- Record the source and collection date of each contact, and the basis the user cites. Do not load a list that lacks them.
- No prospect agreed to mail, so the permission to send is unverified for each one. Under line 1 of the output, state that. Make confirming the permission the first Next step.
- Verify each address before the first send, and re-verify a list older than one week (heuristic default). Never send to an address inferred from a name pattern.
- Send from real person mailboxes, never from aliases of one mailbox.
- Suppress invalid, disposable and spam-trap addresses for good. Exclude role addresses such as info@ or sales@ from personal sequences.
- A catch-all domain accepts any address, so verification cannot confirm one. Send to a catch-all address only after a second check passes, and only from a separate, lower-volume sender; leave the rest out.

## Personalization

- Before a professional-network message, read the recipient's profile and send a connection request only with a one-sentence reason. Check the network's current terms before any automation.
- Write the opener only from a fact the user supplies or a source you cite with its date. Write the fact list first, then the angle from that list only. When no such fact exists, send the segment's message without a personal opener.
- The observation leads into the problem. If the email still works without the opener, the personalization is weak.
- Signals that can support an opener: a funding round, a job posting, a change in the tools the company uses, a published post, or company news.
- Pitch one problem per prospect. When the offer fixes a visible page problem, use it only when the prospect sees it on a phone within seconds, the fix takes days, and its result shows within a window the team sets, in a number the prospect already trusts. Otherwise pick another problem.
- When the evidence is the prospect's own ad or page, quote it with its URL and date, and set the gap between their promise and their page as the evidence. Before the first send, save each evidence item with its URL and capture date; for a visible page problem, save a phone-sized screenshot with the problem marked.
- Name a decision maker only from a published source, such as the company's About page, a signed review reply, or a license record. Rate the name confirmed when two sources agree and likely when one does. Use only a name rated confirmed or likely; for a guessed name, greet the company instead. Never pose as a customer.
- Never claim familiarity the sender does not have.
- Never personalize on health, financial hardship, politics, religion, sexuality or family, even when a public post shows it.

## Map shape

- Heuristic default: 4 to 5 steps over about 3 weeks.
- Assumed timing: steps on day 0, 3, 7, 14 and 21 from the first step. Do not state a best send day or hour.
- Each step is plain text with no images or HTML templates. It carries one point and one ask, not repeated from earlier steps.
- No step that only follows up. Each step adds one new point, such as the problem, a new value, proof the user supplies, a new insight, or a close.
- Each step stands alone. Never write "just checking in", "I never heard back", "following up on my previous message", or "did you see my last email".
- The first step asks for a low-commitment reply, not a meeting.
- Heuristic default: no link before the third step, except the opt-out link. Use at most one link per step, no link shorteners and no attachments.
- Each step carries the marketing footer placeholders from `hl-email`, including the opt-out line.
- The last step closes the loop, offers a one-word reply, and says the sequence ends. Send nothing after it.
- Vary the copy by segment. A swapped first name is not variation.
- Heuristic default: send from a domain separate from the main business domain.

## Replies

- Classify each reply before acting on it: positive, question, objection, referral, out of office, unsubscribe or bounce.
- Positive or question reply --> a named person answers the same working day (heuristic default). Propose two specific times (heuristic default). The sequence stays stopped.
- Price question --> give the price the user supplies, with any proof the user supplies. Never invent a price.
- Objection --> answer once, briefly. For "how did you get my email", give the true source and offer removal.
- Referral --> stop the prospect. The referred person is a new prospect; check permission before any contact.
- A prospect who says a vendor already handles the task --> offer to send the evidence to the prospect's provider. Never criticize the vendor.
- Judge each cold step on its replies.

## Stops and pauses

- Stop each prospect the same day on any bounce, opt-out, booking, or purchase, and on any reply except an out-of-office reply. A reply on any channel stops every channel for that person. An out-of-office reply pauses the prospect until its return date.
- Keep each opt-out on a do-not-contact list that every later load checks. Key the list on each identifier held: email, profile URL and phone. Also add current customers, open deals and competitors to it.
- Honor each opt-out by the method and deadline the current official rule sets for the market, as the exits in `SKILL.md` require. Test the opt-out end to end from a real address before the first send and each quarter (heuristic default); it takes effect without a login.
- Pause the campaign when bounce, complaint, or unsubscribe rates rise. Set the pause thresholds from your own data and the complaint limit in the mailbox providers' current official documentation; this file states no number. Write every threshold down before the first send.
