# Persona card

Use this file for the card layout. The evidence rules and output are in `SKILL.md`.

## Fields

For observed cards, write each field from evidence. For requested hypothesis cards, label proposed jobs or decision questions `Hypothesis`, identify the supplied assumption or proxy, and leave unsupported observed facts `not in evidence`. Do not invent customer quotations or research counts.

```text
Persona: [a descriptive label from the evidence, not a first name]
Decision role: buyer | user | both | influencer | blocker
Evidence: [count] sources, [earliest date] to [latest date], types: [interview, ticket, ...]
Status: Supported | Hypothesis (proxy: [name the proxy])

Job to be done: [the outcome they want, in their words if quoted]
Triggers: [what made them look for a solution; quoted or cited]
Pains: [each pain with its quote]
Desired outcome: [what success looks like to them, quoted or cited]
Objections: [what made them hesitate, quoted or cited]
Alternatives they use: [each alternative, including doing nothing]
Words they use: ["quoted phrase" (source)]
```

## Rules for each field

- Triggers, pains, and objections come from the sources. Do not add one a source does not show.
- Words they use is the only place for invented-sounding language. Include only phrases quoted from a source.
- Omit a field the evidence never covers only when the card would otherwise be padded; state it as `not in evidence` otherwise.
- Do not add a channel, a community, or an influencer unless a source names it. Mark it with its source.

## Merging and splitting

- Two groups with different decisions are two cards, even when they share a job.
- Two groups whose evidence cannot be told apart are one card, marked `Hypothesis`.
- A hypothetical card is a research proposal, not a validated description of customers. Keep its assumptions separate from observations; remove invented biography and quotations.
