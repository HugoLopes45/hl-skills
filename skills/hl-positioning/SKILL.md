---
name: hl-positioning
description: "Write a positioning canvas and one positioning statement from buyer evidence: the alternatives buyers use, including the status quo, the product's attributes with proof status, and the segment that values them most. Works for any product, service, market, or business model; never invents proof, rankings, or market size. Use when the user asks how to position a product or service, what it should be compared with, or which claims it can make; not for taglines or page copy."
---
# Positioning

Input: `[product or service] [buyer segment, optional] [buyer evidence or proof, optional] [market and language, when they change the wording]`

Ground factual claims in supplied evidence or results you observed in this session.

## Evidence rules

- Use only the product facts, buyer evidence, and proof the user supplied, or a source you read in this session. Name the source and its date for each.
- Label each assumption `assumed` and each missing fact `unknown`. Never present an assumption as a fact.
- Build alternatives from buyer evidence. Include the status quo: doing nothing, a spreadsheet, a manual process, an in-house fix, or a different product category. A list of named vendors alone is incomplete.
- Give each attribute one proof status: `proof supplied` (name the document, demo, or measured result and its method), `proof needed` (write `[PLACEHOLDER: proof needed]`), or `not distinctive` (alternatives offer it too, or the buyer does not value it).
- A comparative claim ("faster", "cheapest", "the best", "only") is `proof needed` unless a dated, reproducible test or a public price list the user supplied backs it.
- Write no market size, share, rank, award, customer count, rating, or quote that the user did not supply.
- Quote buyer words exactly, with their source.
- The canvas recommends a position. It does not approve, publish, or price anything; the owner decides.

## Intent

- Act directly when the request names the product and asks for a canvas or a statement.
- Ask focused questions when the product cannot be described from the request or the supplied evidence (see Stop conditions). Group related questions in one message, and ask again when an answer raises a new decision. Do not cap the number of rounds.
- A clear, limited request proceeds on the supplied evidence. Label each inference `assumed`.
- Reuse what the user already supplied. Do not ask for it again.
- Give a default only for a choice the user can accept, such as the output format. For a fact (product, buyer, alternatives, proof, market), write `Default: none`.
- Route, do not write, the neighbouring work: taglines and page copy to `hl-copywriting`; buyer profiles to `hl-persona`; competitor profiles to `hl-competitor-analysis`; prices to `hl-pricing`. Launch planning and timing are outside this skill's scope.
- An exact output format the user names replaces the default wrapper. The evidence rules still apply inside it.

## Workflow

1. **Scope.** Record the product, the candidate segments, the decision the buyer makes, and the market when it changes the wording. Mark each missing item `unknown`.
2. **List the alternatives** buyers use now, from the evidence, with the status quo first.
3. **List the attributes** the product has that the alternatives lack or do better. Give each a proof status. The method is in [references/canvas.md](references/canvas.md).
4. **Chain each attribute** to the buyer benefit and the outcome it serves. Drop any attribute that no segment values.
5. **Name the segment** that values the attributes most and can be reached. Mark it `assumed` unless the evidence shows it.
6. **Choose the frame of reference**, after alternatives, value and segment. Compare familiar categories against the buyer's actual alternatives; choose the one that makes the supported value easiest to understand. Mark an untested category as a hypothesis. Summarize the decision only after completing the evidence chain; use [references/canvas.md](references/canvas.md), not a fill-in-the-blanks discovery exercise.
7. **Run the distinctiveness test.** Name the alternative that could honestly claim the same value for the same segment. If one could, revisit the evidence chain or mark the position unproven; cosmetic wording is not differentiation.
8. **Write what would change the position**: the evidence that would show the statement is wrong.

## Output

Reader: a founder or marketer who decides what the market should hear first. The decision served: which position to test or use, and which claims must wait for proof.

Line 1 is one bold plain sentence that states the position, or what blocks it. It never opens with a label, verdict word, or number.

Under line 1, in plain sentences: each claim that lacks proof, each alternative the evidence did not show, and what you did not read.

Then one numbered point per item, worst or most important first: the statement, each attribute with its proof status, the segment, and the open test. Each point states its evidence source.

Verdict words:
- `Supported`: every line traces to supplied or read evidence, and no comparative claim is unqualified.
- `Hypothesis`: one or more lines rest on `assumed` or `unknown` facts; test before use.
- `Stopped`: the product cannot be described from the request or the evidence.

Put `Verdict: <word>` on its own line just before `**Next:**`. A short qualifier may follow the word. Each Next line is one action a person can take now, in order.

Stopped: line 1 says what is missing and why it blocks the canvas. Then `Verdict: Stopped`. Next holds the grouped questions, each with its default (or `Default: none` for a fact) and what it changes.

Reader rules:
- Define each term once at first use: alternative (what buyers use instead of the product), status quo (doing nothing or the current workaround), attribute (a feature or fact the buyer can check), proof (evidence the buyer or reader can check), positioning statement (one sentence that places the product against an alternative).
- Quote supplied wording exactly; do not improve it.
- No hype and no blame for the current product or its team.

Example (signature only; the domain is not a fixture):

````markdown
**Lead with same-day mobile repair: the buyers' alternative is a shop with a waiting list.**
The segment is `assumed`, drawn from six interview notes you pasted. The market is not stated, so the statement makes no local price claim.

1. **Three of six interview notes name the waiting shop as the alternative.**
   Notes 1, 3, and 4 describe it (supplied). Outcome for the buyer: the rider who needs the bike this week chooses the van. Proof: the notes; no survey.
2. **"Same-day repair" has proof supplied.**
   The March dispatch log you attached records the close date of each job (supplied). Method: count the jobs closed on the day they came in, divided by all jobs in the log.
3. **"Cheapest in the city" is unqualified.**
   It reads `[PLACEHOLDER: proof needed]`. No price list for the other shops was supplied or read.

Verdict: Hypothesis (the segment is assumed)

**Next:**
1. Export the March dispatch log with the close date and time of each job, and send it, so the same-day line can be counted.
2. Read two shops' current price lists with their capture dates, and send them, before any price claim is written.
3. Test the segment with three riders who wait for a shop now; send their words, quoted exactly.
4. Give the statement to the owner, who decides whether it leads the next launch.
````

## Stop conditions

- No product description in the request or the evidence: Stopped. Ask for the product in one line, the buyer, the alternatives buyers use now, and any proof, each with `Default: none` and what it changes.
- No buyer evidence, but a clear product: proceed. Mark the segment `assumed` and the statement `Hypothesis`.
- Market or language unknown: proceed. Write `not stated` in the statement's basis. Ask only when the answer changes the wording.
