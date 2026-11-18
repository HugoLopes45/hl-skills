# Event follow-ups

Load when the trigger is a job event (a quote sent, a job completed or paid, a missed call, an appointment booked), a seasonal date, or an unscheduled treatment plan, instead of a signup or a purchase. The map rules and exits in `SKILL.md` apply.

## Channel

- Use a short message for speed and one-line replies. Use email when the person needs detail, such as a written quote, a checklist, or photos.
- Check the current messaging rules for each channel before you automate it: consent for marketing messages, and any sender registration the channel requires.
- Keep sensitive details out of texts and subjects, as `hl-email` requires.
- Send review asks by email to customers with no mobile number and to commercial accounts.
- Sign each job message with the named person who did the work, such as the technician who quoted it.

## Timing

- Put the first follow-up soon after the event. Map rule 2 sets the later gaps.

## Sequences

- **Quote sent, not accepted:** the quote in writing on day 0; a text on day 1 that asks about it; an email on day 3 that answers the likely objection, price or trust; a direct ask with a real reason to decide on day 7; a close-the-loop email on day 14. Label the days `assumed`. The person who did the work sends each step until yes or no. Stop on acceptance, decline, or reply. Record the reason for each decline.
- **Job completed or paid:** a thank-you text with the review link; one email reminder if no review is posted. Stop on a review, a reply, or the last step.
- **Missed call:** a text that says the call was missed and asks what the person needs; a call back by the team; one more text. Stop when the person replies or a call connects.
- **Seasonal reminder:** trigger on a dated season the user supplies, sent to past customers of that service. Each step has one ask to book; stop on booking. Label the step count and timing `assumed`. Seasonal messages are marketing; send them only within the opt-in.
- **Treatment plan:** the plan in writing, then follow-up steps from the office, each with one ask to book; stop on booking, decline or reply. Label the timing `assumed`. Keep clinical and insurance detail out of every message except the plan in writing (step 1). Check the official health-privacy rule for each recipient's market before the first treatment-plan message. Send a plan-year reminder (a reminder about the insurer's yearly plan period) only after the office confirms the person's remaining benefit period (the coverage time the insurer still allows). The plan-year reminder names the period's end date only, with no benefit amount and no treatment; it is the second exception.

## Reviews

- For a job-based business, ask every customer after each completed job.
- Delay the ask until the open billing issue, complaint or bug report closes, then send it.
- Do not offer an incentive for a review. Do not choose whom to ask by likely rating.
- Check each review platform's current policy before you write the ask.

## Survey scores

- Use a survey score only to route support and follow-up. A low score gets a direct reply from a person.
- A score never chooses who receives the review ask.
- An NPS survey (Net Promoter Score, a rating of how likely the person is to recommend the business) asks one question. Ask the reason in a follow-up whose wording depends on the score band, the score range the team sets.

## Reminders

- Ask for a one-word reply to confirm or reschedule.
- Skip the reminder when the person already confirmed.
- After a missed start, offer a rebook in the next message.
