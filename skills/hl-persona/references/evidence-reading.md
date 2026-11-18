# Evidence reading

Use this file before sorting, scoring or screening supplied evidence. The rules it applies are in `SKILL.md`.

## Weight by conversation type

- Reviews show judgment after buying. Read the 2-4 star reviews first (heuristic default): they weigh trade-offs ("I like X but Y"), so buying criteria appear in the buyer's words.
- Five-star reviews are thin. Use them for desire wording only, not as pain evidence.
- One-star reviews hold dealbreakers and objections, but anger hides the reasoning. Quote the objection, not the rant.
- A competitor one-star review names the moment the reviewer left. Record that moment as a switching trigger, quoted whole.
- For each competitor review set, record the job to be done, the praise (Passion points), the complaints (Pains), the desires (Desired outcome; see Desires) and the switching triggers (Triggers), each quoted with its source.
- Forum threads show comparison before buying. The poster's question shows how the poster describes the problem before any product is named.
- A reply that asks whether a product works in a case ("does it work if I...?") is an objection.
- A long-running member's complaint outweighs a one-off post, because the member has tried the workarounds.
- Comments on category or competitor content show aspiration and doubt. Comments on the supplier's own content probably come from people already convinced; weight them lower.
- Social posts show identity and mood. Use them for the dominant emotion and wording, not for buying criteria.
- Do not rely on an inactive source (no recent posts, no replies). Say so in the output.
- Unprompted talk, where a customer raises the problem without a question asking for it, carries the most weight. Interview samples are small and skew toward engaged customers.
- Prompted quotes, from a survey, an interview question or a form, count lower. Survey answers are primed by the question asked (see Surveys).
- Support tickets carry medium weight. They skew toward problems, not value; sort them first (see Support tickets).
- Public reviews can skew toward extremes; count their star spread first. Read public reviews and forum posts as voices in a segment, not as the market.
- Job postings carry low weight. They state what a company wants, not what a customer does; use one only as a trigger lead, never as proof of a pain.

## Score intensity

Score each quote you will cite from 1 to 5:

| Score | Meaning |
|---|---|
| 1 | Mild preference, polite wording |
| 2 | Stated annoyance, no cost named |
| 3 | A cost named: time, money or rework |
| 4 | Emotional wording, or reputation at stake |
| 5 | The customer acted: left, switched, asked for a refund, or warned others |

Many quotes at score 2 describe a common complaint, not a lead pain. A lead pain needs at least one quote at 4 or 5 (heuristic default).

Before scoring a pain, follow its stated reasons ("because", "so") in the same quote or thread to the deepest one the source gives. Record that root reason beside the surface complaint; if the source gives none, write `root: not in evidence`.

## Calibration

Invented example, not evidence: Wickfield, a fictional invoicing app.

Specificity:
- Weak: "Great app, would recommend." Reason: it names no situation, cost or feature, so any app could carry it.
- Strong: "Wickfield sent a client a total with the tax missing, and I had to re-issue twelve invoices." Reason: it names the product, the failure and the cost, so it proves a pain and a stake.

Intensity:
- Weak, score 2: "Kind of annoying that exports take a while." Reason: stated annoyance with no cost.
- Strong, score 4: "The client saw the wrong total and I looked careless in front of my boss." Reason: reputation at stake.

## Screen for pollution

Flag a quote that shows any sign below. Keep the specific complaints from an incentivized source on the card; they stay flagged and outside the quote bar.

- Several reviews in one week with the same phrasing.
- Stock marketing praise in a customer's mouth, or the supplier's feature names spelled as on its own site.
- Generic praise with no use detail. Real users describe a situation; advertising copy does not.
- A reviewer with one review, or a run of five-star reviews across one supplier's products.
- A commenter who may be affiliated with the supplier: a new account, or praise for one product only.
- A disclosed free product or payment for the review.
- A quote about another variant, size or model than the one being researched.

## Desires

Tag "I wish it...", "if only it...", and "the only thing missing is..." as `desire`. Quote the whole sentence. Read it as the condition for the next purchase.

## Awareness stage

Read the stage from the wording the source shows:

- Unaware: describes the situation without calling it a problem; silent sources read `not in evidence`.
- Problem-aware: describes symptoms, or asks whether the result is possible at all, and names no category.
- Solution-aware: names a type of fix, not a product.
- Product-aware: compares named products.
- Most aware: asks about a specific offer, price or term.

Tag one stage per segment: the stage that most of its quotes show. When the quotes split, name the split with each stage's quote count.

## Surveys

- Read a choice answer as limited to the options offered. A count of choices shows what the options captured, not what customers want.
- Read open answers for the buyer's words. Check each open answer against the same respondent's closed answer, and name any conflict in the output.
- When a survey asks how much the respondent would miss the product, segment the answers by that answer. Read the group that would miss it only somewhat for the fixes it names.
- For a Net Promoter Score (NPS, a 0 to 10 recommendation score), read each score with its comment. For improvement work, passives and detractors (the middle and low scores) that name a complaint outweigh promoters with no complaint.

## Support tickets

- Sort each ticket into one group before counting: bug, confusion, missing feature, or expectation mismatch. Count each group on its own; a ticket count shows complaints, not what most customers value.
