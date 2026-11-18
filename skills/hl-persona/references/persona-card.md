# Persona card

Use this file for the card layout. The evidence rules and output are in `SKILL.md`.

## Fields

For observed cards, write each field from evidence. For requested hypothesis cards, label proposed jobs or decision questions `Hypothesis`, identify the supplied assumption or proxy, and leave unsupported observed facts `not in evidence`. Do not invent customer quotations or research counts.

```text
Persona: [a descriptive label from the evidence, not a first name]
Decision role: buyer | user | both | influencer | blocker
Evidence: [count] sources, [count] verbatim quotes, [earliest date] to [latest date], types: [interview, ticket, ...], drawn from: [supplied sources by name or title]
Status: Supported | Hypothesis (proxy: [name the proxy])

Job to be done: [the outcome they want, in their words if quoted]
Triggers: [what made them look for a solution or leave an alternative; quoted or cited, with `appears in X of Y sources`]
Pains: [each pain with its root reason from the source, its quote, its intensity score from 1 to 5, its confidence tier, and `appears in X of Y sources`; a pain with no quote scored 4 or 5 is not a lead pain]
Cost of the problem: [what the problem costs the buyer in time, money or opportunity, quoted or cited]
Passion points: [what they value and would miss, quoted; never a pain]
Dominant emotion: [one word, with the 2-3 quotes that show it (heuristic default)]
Awareness stage: [unaware | problem-aware | solution-aware | product-aware | most aware, with the wording that shows it]
Desired outcome: [what success looks like to them, quoted or cited]
Objections: [what made them hesitate, quoted or cited, with its confidence tier]
Evaluation criteria: [how this role judges the options, quoted or cited]
Buying process: [this role's step in the decision and who it influences, quoted or cited]
Alternatives they use: [each alternative, including doing nothing]
Quotes by source type: [each source type in Evidence, with this card's quote count from it]
Beliefs: [what they state is true about the problem or the options, quoted]
Words they use: ["quoted phrase" (source), with its count when three or more independent sources use it (heuristic default)]
Category words: [the industry term for the same thing, when a supplied source uses one]
Words they reject: ["quoted phrase" (source)]. A desire the negation suggests is an inference: label it `Hypothesis`.
Not a fit: [a mismatch the source states, with its reason, quoted or cited; a departure, a missing-feature request or no purchase is a lead to check, not proof of a mismatch; `not in evidence` otherwise]
```

## Rules for each field

- Triggers, pains, and objections come from the sources. Do not add one a source does not show.
- Words they use is the only place for invented-sounding language. Include only phrases quoted from a source.
- State a field the evidence never covers as `not in evidence`.
- Do not add a channel, a community, or an influencer unless a source names it. Mark it with its source.
- A card below the quote bar in `SKILL.md` reads `Hypothesis` in its Status line.
- Count sources as independent: quotes from one thread, one author, or one review batch count as one source.
- Confidence tier per pain and objection (heuristic defaults): High is three or more independent sources, unprompted, consistent across segments. Medium is two independent sources, or prompted quotes only, or one segment only. Low is one source. Tiers do not change the Status line.
- List pains and triggers by source count, then by intensity.
- Keep passion points out of Pains. Beliefs and passion points come only from quotes; write `not in evidence` when no source gives one.

## Merging and splitting

- Two groups with different decisions are two cards, even when they share a job.
- Two groups whose evidence cannot be told apart are one card, marked `Hypothesis`.
- A hypothetical card is a research proposal, not a validated description of customers. Keep its assumptions separate from observations; remove invented biography and quotations.
