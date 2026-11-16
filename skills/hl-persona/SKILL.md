---
name: hl-persona
description: "Build buyer or user personas from supplied evidence such as interviews, surveys, reviews, support tickets, and sales calls. Each persona states its evidence count, date range, and source type, and never implies a share of the market; no age, generation, or platform habit is assumed. Use when the user asks who the buyer or user is, who a message or product should be designed for, or for a persona card from research notes."
---
# Persona

Input: `[product or service] [evidence: notes, export, or transcript file, optional] [purpose: copy, product, or targeting, optional]`

Ground factual claims in supplied evidence or results you observed in this session.

## Evidence rules

- Build a persona only from evidence the user supplied or you read in this session. Each card names its evidence: the number of sources, their date range, and their type (interview, survey, review, ticket, sales call, or community post).
- The count describes the sample. A persona from six interviews describes those six people, not the market. Never write a share of customers, buyers, or the market unless a survey with its sample size and method supports the figure.
- Do not infer demographics or platform habits. A user-requested segment is proposed scope, not validated audience evidence; retain it as an unvalidated hypothesis without inventing ages, income or stereotyped behavior.
- Quote buyer words exactly, with their source. Never invent quotes, names, biography or observed behavior. Missing observed fields read `not in evidence`; a requested hypothesis may add separately labelled proposed jobs or decision questions, not fictional customer facts.
- Do not average segments. Give each segment the evidence it has. A segment with thin evidence is `Hypothesis`.
- Without first-party evidence, use proxies in this order: the product owner's stated hypothesis; reviews of competitors the user supplied; reviews of comparable products; the other products the same people use. Tag each card with its proxy and mark it `Hypothesis`.
- A persona describes who to design for. It does not authorize outreach, targeting, or any claim about a named person. The owner decides how it is used.

## Intent

- A request for a persona for a named product is enough to draft a hypothesis card. Use a stated design purpose if available; otherwise keep the card exploratory rather than requiring a copy/product/targeting choice.
- Ask before drafting only when the product or intended decision cannot be understood. Missing audience evidence is a limitation, not an automatic stop.
- Without evidence, use supplied hypotheses or proxies and label the card `Hypothesis`. Separate proposed jobs from observed facts and put validation requests in Next. Do not ask permission to produce the requested hypothetical card.
- Reuse what the user already supplied. Do not ask for it again.
- Give a default only for a choice the user can accept, such as the output format. For a fact (product, buyer, evidence source, market), write `Default: none`.
- Decide buyer, user, or both from the evidence. Ask when the evidence does not show it and the answer changes the card.
- An exact output format the user names replaces the default wrapper. The evidence rules still apply inside it.

## Workflow

1. **Scope.** Record the product, the purpose, and whether the card describes the buyer, the user, or both.
2. **Sort the evidence.** List each source with its type and date. Mark undated sources `undated`.
3. **Group by decision and circumstance.** Extract the situation before the decision, the change that prompted it, the alternatives considered and the progress sought. Separate functional, social and emotional motives only where the source supports them. Group buying, use, renewal, recommendation or blocking decisions by these circumstances, not invented demographics. Missing parts remain `not in evidence`.
4. **Fill the card.** Use [references/persona-card.md](references/persona-card.md). Distinguish sourced observations, proposed hypotheses and `not in evidence`. A hypothesis card must not claim a source count, quote or behavior it does not have.
5. **Check the card.** Remove unsupported demographic or behavioral facts. Keep a requested segment only as proposed scope when unvalidated. Confirm each quote appears in its source.

## Output

Reader: a marketer, product owner, or founder who must choose whom to design for this month. The decision served: which card to use, and what evidence is still missing.

Line 1 is one bold plain sentence that names the main buyer or user and the evidence behind them. It never opens with a label, verdict word, or number.

Under line 1, in plain sentences: which cards are `Hypothesis`, the largest gap in the evidence, and what you did not read.

Then one numbered point per card: the segment, its evidence count and date range, its decision role, and its strongest quoted line.

Verdict words:
- `Supported`: every card traces to supplied evidence with its count and dates.
- `Hypothesis`: one or more cards rest on proxies or on a single source.
- `Stopped`: the product or intended decision cannot be understood, so even an exploratory card would be arbitrary.

Put `Verdict: <word>` on its own line just before `**Next:**`. A short qualifier may follow the word. Each Next line is one action a person can take now, in order.

Stopped: line 1 says what is missing and why it blocks the cards. Then `Verdict: Stopped`. Next holds the grouped questions, each with its default (or `Default: none` for a fact) and what it changes.

Reader rules:
- Define each term once at first use: persona (a written description of one group of people, built from evidence), proxy (evidence about a similar group, used when the target group's evidence is missing), evidence count (the number of sources behind a card).
- Show quotes as the source wrote them.
- No hype and no stereotypes. Describe what the evidence shows.

Example (signature only; the domain is not a fixture):

````markdown
**The main buyer is the home brewer who has bought kits before; the evidence is four support tickets and two calls.**
Both cards are `Hypothesis` for the second group, which rests on one review source. The notes name no age, and the cards name none.

1. **Home brewers who have bought a kit before decide on refills.**
   Four tickets and two sales calls from March to May (supplied). Quoted in ticket 2: "the second batch tasted nothing like the first." Decision role: buyer and user.
2. **Gift buyers choose the starter kit; the evidence is one review.**
   One review from the marketplace listing (supplied, undated). Quoted: "bought it for my brother, he already had a fermenter." Hypothesis: the gift buyer is the same person as the brewer only when the review says so.

Verdict: Hypothesis (the gift buyer rests on one review)

**Next:**
1. Send the next ten support tickets with their dates, so the refill card can be counted again.
2. Ask two gift buyers what they bought and for whom; send their words quoted exactly.
3. Use the refill card for the reorder email only after the owner approves it.
````

## Stop conditions

- No understandable product or decision: Stopped. Ask only for the missing context. A named product and a persona request do not need a separate purpose questionnaire.
- Evidence supplied but not readable (a file that cannot be opened, an unreadable export): Stopped. Ask for the text pasted in the message.
- No evidence, but a clear product and persona request: provide a hypothesis card now and identify the evidence needed to validate it.
