---
name: hl-copywriting
description: "Write or rewrite website copy, product copy, taglines, and interface microcopy from a product brief or existing copy. Keeps every claim supported by the brief, leaves placeholders for missing proof, matches the audience's own words without forced slang, and removes AI-sounding patterns. Use when the user asks for website copy, a page rewrite, a tagline, product copy, or interface microcopy."
---
# Copywriting

Input: `[brief or copy file] [--mode draft|rewrite|point]`. Default mode: `draft` for a brief, `rewrite` for existing copy. The request names the format; without one, write a landing page.

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

## What good copy is here

Two failures ruin copy, and the cure for one causes the other. Copy that invents proof is a lie. Copy that only restates the brief around a row of empty slots is true and dead. This skill refuses both: every fact is supplied, and every line is one that only this product could say.

The facts are fixed. The idea, the order, the rhythm, the image, and the joke are yours to make. Evidence rules limit what the copy claims; they never excuse a flat line.

## Evidence rules

- Factual copy uses only facts in the brief or in a source you read. Any other claim is left out. It becomes `[PLACEHOLDER: proof needed]`, naming the proof, only in the two cases under "Placeholders are rare".
- Never invent testimonials, customer names, quotes, ratings, user counts, logos, awards, guarantees, offers, free trials, delivery times, or results. Leave the claim out, or use a placeholder only in the two cases under "Placeholders are rare".
- Keep each fact at its exact grade. "Most" never becomes "every", "may have" never becomes "some have", a bench test done once never becomes "tested", and "four accountants" never becomes "four restaurant specialists".
- Write nothing the business does not do yet: no feature, policy, or term such as "cancel anytime" unless the brief states it.
- A scene, an image, or a joke may show a supplied fact in action. It must not smuggle in a new fact: no invented number, customer, event, or result inside a figure of speech.
- Generation labels such as "Gen Z" describe no individual buyer. Name a segment only when the brief names it.
- Audience words come from supplied sources: reviews, comments, tickets, interviews, creator posts. Without them, write plain, direct sentences, and say in the notes, in a plain sentence, that the voice is unverified; never tag the copy with it.
- A quote keeps its exact words and its source as supplied. "A support email" does not become "a customer", and no permission is stated that the brief does not state. When quoted words come from a private message (an email, a ticket, an order note) and the brief states no permission to publish, ask for it once in Next and name the lines that fall if it is refused. Put no new sentence in a real person's mouth: a line in quotation marks, or attributed to a founder, buyer, or reviewer, is the supplied words only. The page's own "we" may restate an owner's note without quotation marks when no fact, number, or person in it changes.
- Slang, memes, and platform jargon appear only when a supplied source uses them and the context fits. Forced slang is a defect.
- In rewrite and point mode, keep every supplied fact and argument. Add no claim.
- Read [references/proof-and-claims.md](references/proof-and-claims.md) before any factual line, and [references/voice-and-audience.md](references/voice-and-audience.md) before any voice choice.

## What needs no source

The evidence rules fence the claims. Inside the fence, write freely. These need no brief line, and a draft that avoids them out of caution is under-written:

- Speaking to the reader about the situation the brief or the buyer's words describe.
- Stating what follows necessarily from supplied facts: a flat monthly price with no per-invoice fee means the tenth invoice costs the same as the first. A cause is not a consequence: two supplied facts side by side (a 16 mm steel shackle, a 1.4 kg lock) do not say that one explains the other, so "because" needs its own brief line.
- Saying what a supplied fact means for the reader when it follows directly and adds no new behavior of the product.
- Arithmetic on supplied numbers.
- An image, a comparison, or a scene that is plainly a figure of speech and shows a supplied fact.
- Order, emphasis, rhythm, and which fact comes first.
- Answering a supplied buyer sentence in the speaker's voice.

These always need a brief line: how the product behaves, what it includes, what it costs, what it achieved, who uses it, what anyone said, and any promise about the future.

A design intent such as "heavy on purpose" is not a benefit claim; do not turn it into one ("the weight is the security") without a brief line.

When unsure between a live line that stands on a supplied fact and a flat restatement of that fact, prefer the live line only when it adds no fact, cause, or promise.

## Placeholders are rare

A placeholder marks a hole the reader would fall into, not every fact you wish you had.

- Use a placeholder in the copy only in two cases: the user asked for a claim the brief cannot support, or the reader cannot act without the fact (what the price includes, what happens after the click, a term beside the button).
- Proof the brief does not have gets no section and no slot. Leave the proof section out and name the missing proof once in Next, with what it would add.
- Cut a section whose content is only placeholders. A thin brief gives a shorter page, not a longer list of slots.
- The same slot appears once in a piece.
- Never add a slot for a claim nobody asked for, such as a customer count on a page that works without one. A missing reason or cause gets no slot either: state the supplied facts side by side and ask for the reason in Next.
- Do not fill the gap with soft invention either. A sentence about what the reader will experience, see, feel, or avoid ("you can see where the money went", "one busy person never delays your month") is a claim, and it needs a brief line like any number, unless it follows necessarily from a supplied fact. With a thin brief, write the short piece the facts carry: the first screen, the facts, the action. State each fact once. A section that restates the first screen in other words ("Your books are closed every month" under a headline that already says so) is filler; cut it.
- When the material list from draft step 2 is empty (no buyer words, no admitted limit, no story, no odd number), deliver the first screen only: headline, one supporting line, the action, the price line. Add no body section, since each one could only restate the first screen or invent a contrast ("not software you run yourself"). Say in line 1 that the brief carries a first screen, and put the questions that would yield material in Next.
- When more than three slots remain in one piece (heuristic default), the brief is too thin for that format. Write the shorter format the facts carry, and say so in line 1.

## Intent

- Act directly when the request names the artifact, its scope, and its depth. A narrow question gets a narrow answer, not the full workflow.
- Ask in focused rounds when essential context is missing (see Stop conditions). Group related questions in one message, and ask again when an answer raises a new decision. Do not cap the number of rounds.
- A clear, limited request proceeds on the supplied brief. Label each inference from it.
- Missing non-essential context does not stop the draft. Write the lines that do not depend on it.
- Reuse what the user already supplied. Do not ask for it again.
- Explain each question's consequence in one line. Give a default only for a choice the user can accept, such as an output format. For a fact (product, buyer, outcome, market, price, proof), write `Default: none`; never presume it.
- Do not invent a market, audience, offer, or proof.
- An exact output format the user names (copy only, JSON only) replaces the default wrapper. Evidence, permission, and safety rules still apply inside it.

## Formats

Read the matching section before writing. Each format has its own job, shape, and traps.

| The request is for | Read |
|---|---|
| Landing page, homepage, pricing page, feature page, about page, comparison page, launch page, long sales page, local service page, waitlist page | [references/formats.md](references/formats.md) |
| Tagline, product name candidates, product description, store or app listing text, packaging or label copy, case card, bio, thank-you page | [references/formats.md](references/formats.md) |
| Buttons, empty states, errors, 404 pages, confirmations, success messages, forms, popups, upgrade and trial-end screens, notifications, cancel flows | [references/microcopy.md](references/microcopy.md) |

Other skills own these formats, so name the skill and stop unless the user asks you to continue: emails (`hl-email`, `hl-email-sequence`), ads (`hl-paid-ads`), social posts (`hl-social`), articles (`hl-article-writing`), video scripts (`hl-short-video`, `hl-explainer-video`). A format in none of these lists is written from the method below, with its job stated first.

## Modes

Pick the mode from the request and the input. A brief with no copy is `draft`. Existing copy with its own voice to restore or fix is `rewrite`. One named line, word, or section is `point`.

### draft (default for a brief)

1. **Lock the facts.** List the brief's product, buyer, outcome, price, availability, and proof, each with its source line. Ask for a missing product, buyer, or outcome before drafting; do not invent it. If the copy answers an ad, email, or post, list its exact promise text and its traffic source.
2. **Mine the material.** Before any sentence, list what only this brief contains: the number that is not round, the thing the product does not do, the flaw the owner admits, the sentence a buyer said, the founder's moment, the step the owner calls obvious. Follow [references/originality.md](references/originality.md). This list, not the product category, is what the copy is made from. Mark the strongest find. It belongs in the headline or on the first screen; strong material left unused or buried in a late section is a defect. A supplied line of the owner's own writing, from a page the brief presents as live, is finished copy: when the piece needs that subject (returns, shipping, sign-off), use the line as written instead of a new line or a placeholder. It carries only what it says; add no term, period, or condition around it. A sample given for tone only, or from another product, sets the voice and is not reused as a claim. A buyer sentence that shows who buys for whom, or for what occasion, may change who one piece addresses (the pack, a gift line); the brief's stated buyer stays the page's addressee. Decide that here, and state the inference with its count ("one of three order notes") in the notes.
3. **Find the concept.** Write three concepts (heuristic default), each one sentence that states what the piece says and the supplied fact that makes it true. The three must differ in what they claim, not in wording. Keep the one that passes the swap test (a competitor could not run it unchanged) and that the facts carry furthest. Do not present a menu of angles; name the runner-up in one line after the copy.
4. **Set the register and decide on humor.** Take the voice from supplied evidence, and take the lead from the buyer's awareness level, meaning how much the buyer already knows ([references/voice-and-audience.md](references/voice-and-audience.md)). Then run the humor gate in [references/humor.md](references/humor.md): humor is a choice made per piece and per moment, never a default and never banned by habit.
5. **Shape the piece.** Name the job first: the one thing the reader must do or know after reading. If the brief names none, state the job you infer. Take the skeleton from the format's section, then let the material bend it: a section exists only when the brief gives it something to say, and the section the material is richest in runs longest. Set the length by the decision: short for an urgent or small one, longer for a planned one with more doubts. Persuasion moves and their limits are in [references/persuasion.md](references/persuasion.md).
6. **Write it as one person.** Decide who is speaking and write every line in that voice. Each heading states a claim; a heading that only labels its section ("How it works", "Pricing", "The problem") is rewritten or removed. Then write the body: a section is prose that talks to the reader and does something with the material. A heading over a bare quote, or over one brief line restated, is not a section. A supplied quote is a heading, whole, or sits inside a paragraph that answers it, turns it, or builds on it. Write candidates for the headline and for the one or two lines that carry the concept (heuristic default), keep the best, and write the rest once. The candidate count is in [references/headlines.md](references/headlines.md), which you read before the headline.
7. **Cut and test.** Run the pattern check in [references/ai-tells.md](references/ai-tells.md), then these tests on every line. Rewrite or delete each line that fails.
   - Swap test: could a competitor use it unchanged?
   - Echo test: does it only repeat a brief line in the brief's order and words? Then it informs and does not sell; rebuild it from the reader's side. Quotes and the owner's own lines are exempt.
   - Picture test: can the reader see it, or check it?
   - Aloud test: would the speaker say it to one buyer across a table?
   - Deletion test: does the piece lose anything without it?
   - Skeleton test, for a page: do the headings alone make the argument?
   - Under-written test: is any section only a heading and one restated fact, or quotes stacked with no prose around them? Then it is an outline. Write it, or cut it when the brief holds nothing more to say.
   - Quote test: use the one supplied quote that hits hardest, in full, where it lands. Two quotes are the ceiling on one screen, a quote used as a heading included (heuristic default). Introduce a quote the way a person would ("One email to our support read:"), not as a record ("A support email said:"). A quote appears once: as a heading, whole and in quotation marks, with its supplied source in the first line under it, or inside a paragraph. Never reword a quote into a heading. The strongest buyer sentence appears whole somewhere on the page; cutting its last clause cuts the reason to quote it.
   - Repeat test: does any fact, slot, or sentence appear twice without a reason? Keep the stronger place.
   - Register test: does the copy match the supplied voice samples in word choice, sentence length, and formality? Copy stiffer or looser than the samples is a defect; without samples, write plainly.
   - Delegation test: did Next hand the owner a line the brief already lets you write? A "not for you if" line comes from a supplied limit and names only what the product does not do, include, or serve; write it.
8. **Run the evidence gate.** Trace every factual line to its source line. Apply the placeholder rules. Then go back to the step 2 list: each supplied buyer sentence and each line of the owner's own writing is either in the copy or covered by one notes sentence that groups the ones left out and gives the reason. Put the sending ad's promise beside the first screen; the same words must appear when the brief supports the promise.
9. **Judge it.** Score the dimensions in [references/calibration.md](references/calibration.md), rewrite the weakest, and score again. If a dimension stays weak, name the blocker in one line: missing proof, offer, or material, or a step the reader cannot take. Never add a claim to raise a score. Scores stay out of the deliverable.

### rewrite

1. **List the claims.** Each claim in the copy either survives, is narrowed to what it proves, or becomes a placeholder.
2. **Find what is already alive.** Mark the lines only this writer could have written, and keep them word for word. Keep the writer's vocabulary, punctuation habits, and sentence length; do not upgrade a plain word to a formal one.
3. **Fix what is dead.** Use [references/ai-tells.md](references/ai-tells.md) and [references/calibration.md](references/calibration.md). Correct demonstrated padding, label headings, echo lines, and unsupported claims, not presumed authorship. Replace a generic line with material from the copy or the brief, per [references/originality.md](references/originality.md); when neither has any, cut the line.
4. **Leave a line alone** when the change is not clearly better. Add no section the writer did not ask for. Report each changed line with its reason in one sentence.

### point

1. Change only the named line, word, or section, plus the minimum around it that the edit needs to read cleanly.
2. Keep every other line exactly as written.
3. Give each changed line one reason in one sentence.
4. Name a serious problem elsewhere in one line. Do not fix it.

## Output

Reader: a founder or marketer who will publish the copy this week. The decision served: whether the copy can ship, and what must be settled first.

Line 1 is one bold plain sentence that states whether the copy is ready and what blocks it. It never opens with a label, verdict word, or number.

The copy comes next, directly under line 1. It is the artifact. For an ordinary report, put it in a `markdown` fence with its own headings. For copy-only requests, output only the requested copy, without fences, headings added for presentation, explanations, or the signature. Deliver only the requested pieces.

After the copy, write the notes as one paragraph of at most five sentences (heuristic default), the way a writer hands work to a client. No labels such as "Concept:", "Voice:", "Inference:" or "Withheld:", and no list. Say only what the reader must know to decide, each only when it applies: the idea the piece rests on and the runner-up; what evidence set the voice; any inference that could be wrong; the slot that blocks publishing; the supplied buyer sentences and owner lines left out, grouped in one sentence with the reason. Mention humor only when the user asked for it and you withheld it, or when it was a close call. Do not narrate the method, restate the brief, list claims you chose not to make, repeat what Next already says, or show scores.

- Draft: list the headline variants after the notes, pick first ([references/headlines.md](references/headlines.md)). For a piece with no headline, list the variants of its main line.
- Rewrite and point: list the changed lines after the notes, each with its reason, and for a point edit the serious problem named in point step 4.
- When humor was a close call, give the plain version and one humor variant of the same line, labelled, with the variants so the owner picks.

Verdict words:
- `Draft`: copy complete; no unsupported claim, and each remaining slot is named.
- `Rewritten`: rewrite or point edit complete; each change is listed.
- `Stopped`: no product, buyer, or outcome to write from; a copy file that cannot be read; a format another skill owns, unless the user asks you to continue; or a promise the business cannot keep.

Put `Verdict: <word>` on its own line just before `**Next:**`. The order is fixed: line 1, copy, notes, variants or changed lines, verdict, Next. Each Next line is one action a person can take now, in order. A line that asks the reader to choose marks the default: in a Draft or Rewritten report, what the delivered copy already does; in a Stopped report, each question's `Default:` (or `Default: none` for a fact). A line that is only an action carries no `Default:`. Missing proof, bold ideas, and the questions that would give the copy better material go in Next, each with what it would add.

Stopped: line 1 says what is missing and why it blocks the copy. Then `Verdict: Stopped`. Next holds at most 3 numbered question groups (heuristic default), each with its default (or `Default: none` for a fact) and what it changes.

Reader rules:
- In the notes, say "the button" and "the top of the page", not CTA or hero, or define the term once at first use.
- Use the buyer's words over marketing phrases. Label invented voice as invented.
- No hype, no unsupported superlatives, no blame for the product's current state.

Example (signature only; the domain is not a fixture). The brief, the pasted reviews, and the product notes it cites are invented for this example; in real use each such line must exist in the user's input:

````markdown
**The sock page can go live once you add the delivery time under the button.**

```markdown
## One sock. Black, mid-calf, three sizes.

Lose one and the pair survives, because there are no pairs.

Send me 10 for 30 EUR

[PLACEHOLDER: delivery time, from your shipping policy]

## Ten of our socks make forty-five possible pairs

One review read: "I own forty socks and no two of them know each other." Every one of those forty-five pairs matches.

## We do not make a second colour

The answer is in the headline.
```

The page says one thing: with a single model, a lost sock does not break a pair. The runner-up was the price per sock.

Headline variants, pick first:
- Pick: "One sock. Black, mid-calf, three sizes." Why: it is the product fact the page is built on.
- "I own forty socks and no two of them know each other." (a buyer's sentence from your pasted reviews; as the headline it keeps the review as its source and leaves the second section)
- "Lose one sock and the pair survives." (the page's own line; no new fact)

Verdict: Draft

**Next:**
1. Replace the delivery slot with the figure from your shipping policy.
2. Ask five customers what they did with their old socks; a true answer would make a stronger third section than the colour one.
````

## Stop conditions

- No product, buyer, or outcome in the brief: Stopped. Ask for each in a focused round, with what each changes in the copy.
- A copy file that cannot be read: Stopped. Ask for the text pasted in the message.
- A format another skill owns: Stopped. Name the skill, unless the user asks you to continue.
- An ad, email, or post promise the business cannot keep: Stopped. Say so; do not soften the headline to fit.
