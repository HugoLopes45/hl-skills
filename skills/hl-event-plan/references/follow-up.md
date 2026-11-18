# Follow-up handoff

Read this file when writing the follow-up for an event. This skill plans the tiers and their owners. `hl-email` writes the copy. `hl-email-sequence` maps any sequence and its exits.

## Tiers

| Tier | Who it is | Owner action |
|---|---|---|
| Hot | a conversation with an agreed next step | a personal message from the person who had the conversation, with the agreed step and a calendar link |
| Warm | a conversation with no commitment | a personal message with one asset matched to what the person said |
| Scan only | a badge scan or sign-in with no conversation | no sales message; one light, owner-approved touch, or none |

- The owner sends hot and warm messages within the follow-up deadline, while the conversation is still warm. Heuristic default: within 2 business days, set by the owner. This is a default, not a measured rate.
- The owner writes each message from the captured context: what the person said, what they care about, and the agreed step. Do not send a message without that context.
- Keep scan-only contacts out of every sales sequence.
- Do not state a response rate or a decay rate for any delay.

## Consent

- Send a marketing message only to a person who agreed to that message type. Keep the record: the time, the source, and the wording shown.
- Check the current official rule for each recipient's market. The owner's adviser answers any question the rule leaves open.

## Handoff

- Hand the Warm contacts who ask to wait to `hl-email-sequence` as a nurture map. Their trigger is the tagged event attendance, never a scan.
- Hand the copy for each message to `hl-email`.
- The owner tags each contact with the event name as its source. The first follow-up message asks the self-reported "heard us at" question.
- The tier counts go to the readout. `hl-reporting` computes the figures from the export.

## Content

- The owner publishes the recording and a written recap only after the adviser's written answer on republishing rights; heuristic default: within a week of the event, set by the owner.
- Hand the clips to `hl-short-video`, the recap to `hl-article-writing`, and approved quotes to `hl-social`.
- Use a quote only with the speaker's approval of that exact wording.
