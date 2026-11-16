---
name: hl-copywriting
description: "Write or rewrite landing page copy from a product brief or existing copy. Keeps every claim supported by the brief, leaves placeholders for missing proof, matches the audience's own words without forced slang, and removes AI-sounding patterns. Use when the user asks for landing page copy, a page rewrite, or copy that sounds less generated."
---
# Copywriting

Input: `[brief or copy file] [--mode draft|rewrite]`. Default mode: `draft`.

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

## Evidence rules

- Factual copy uses only facts in the brief or in a source you read. Any other claim becomes `[PLACEHOLDER: proof needed]`, naming the proof.
- Never invent testimonials, customer names, quotes, ratings, user counts, logos, awards, guarantees, delivery times, or results. Use a placeholder.
- Generation labels such as "Gen Z" describe no individual buyer. Name a segment only when the brief names it.
- Audience words come from supplied sources: reviews, comments, tickets, interviews, creator posts. Without them, write plain, direct sentences and label the voice `unverified`.
- Slang, memes, and platform jargon appear only when a supplied source uses them and the context fits. Forced slang is a defect.
- In rewrite mode, keep every supplied fact and argument. Add no claim.
- Read [references/proof-and-claims.md](references/proof-and-claims.md) before any factual line, and [references/voice-and-audience.md](references/voice-and-audience.md) before any voice choice.

## Intent

- Act directly when the request names the artifact, its scope, and its depth. A narrow question gets a narrow answer, not the full workflow.
- Ask in focused rounds when essential context is missing (see Stop conditions). Group related questions in one message, and ask again when an answer raises a new decision. Do not cap the number of rounds.
- A clear, limited request proceeds on the supplied brief. Label each inference from it.
- Missing non-essential context does not stop the draft. Write the lines that do not depend on it, and mark the rest as placeholders.
- Reuse what the user already supplied. Do not ask for it again.
- Explain each question's consequence in one line. Give a default only for a choice the user can accept, such as an output format. For a fact (product, buyer, outcome, market, price, proof), write `Default: none`; never presume it.
- Do not invent a market, audience, offer, or proof.
- An exact output format the user names (copy only, JSON only) replaces the default wrapper. Evidence, permission, and safety rules still apply inside it.

## Modes

### draft (default)

1. **Lock the facts.** List the brief's product, buyer, outcome, price, availability, and proof, each with its source line. Ask for a missing product, buyer, or outcome before drafting; do not invent it.
2. **Pick one angle.** The buyer's problem in the buyer's words, then the outcome. Do not present a menu of angles.
3. **Write the sections:** hero (a headline that names the problem or outcome, a subhead that says what the product does, one call to action), problem (three bullets in buyer language), how it works (three steps), proof (placeholders where proof is missing), objections (three to five questions the brief or buyer sources raise), and a final call to action.
4. **Test each line.** Can the reader picture it? Can it be proved true or false? Could a competitor use it unchanged? Rewrite each line that fails.
5. **Run the pattern check** in [references/ai-tells.md](references/ai-tells.md).

### rewrite

1. **List the claims.** Each claim in the copy either survives, is narrowed to what it proves, or becomes a placeholder.
2. **Review clarity and specificity** with [references/ai-tells.md](references/ai-tells.md). Correct demonstrated padding or unsupported claims, not presumed authorship. Keep the writer's own words where they work.
3. **Leave a line alone** when the change is not clearly better. Report each changed line with its reason in one sentence.

## Output

Reader: a founder or marketer who will publish the copy this week. The decision served: whether the copy can ship, and which placeholders must be filled first.

Line 1 is one bold plain sentence that states whether the copy is ready and what blocks it. It never opens with a label, verdict word, or number.

Under line 1, in plain sentences: each placeholder that blocks publishing, and each missing input that limited the draft.

The copy is the artifact. For an ordinary report, put it in a `markdown` fence with its own section headings and `[PLACEHOLDER: ...]` slots. For copy-only requests, output only the requested copy, without fences, headings added for presentation, explanations, or the signature. Deliver only the requested sections. In an ordinary rewrite report, put the changed-line reasons after the copy.

Verdict words:
- `Draft`: copy complete; unsupported claims are placeholders.
- `Rewritten`: rewrite complete; each change is listed.
- `Stopped`: no product, buyer, or outcome to write from.

Put `Verdict: <word>` on its own line just before `**Next:**`. Each Next line is one action a person can take now, in order. Placeholders go in Next with the proof that replaces each one.

Stopped: line 1 says what is missing and why it blocks the copy. Then `Verdict: Stopped`. Next holds the grouped questions, each with its default (or `Default: none` for a fact) and what it changes.

Reader rules:
- Define each term once at first use: CTA (the button or link readers press), hero (the top section of a page), placeholder (a marked slot for proof you do not have yet).
- Use the buyer's words over marketing phrases. Label invented voice as invented.
- No hype, no unsupported superlatives, no blame for the product's current state.

Example (signature only; the domain is not a fixture):

````markdown
**The resole page is ready once you fill one slot: the turnaround time.**
The brief gives no turnaround time, so the page holds a placeholder for it. The headline uses the words from your pasted support emails.

```markdown
## Resole your hiking boots instead of replacing them

[PLACEHOLDER: turnaround in working days, from your repair log]

Book a resole
```

Verdict: Draft

**Next:**
1. Replace the turnaround placeholder with the figure from your repair log, and check it against that log before publishing.
2. Publish the page once that slot is filled.
````

## Stop conditions

- No product, buyer, or outcome in the brief: Stopped. Ask for each in one round, with what each changes in the copy.
- A copy file that cannot be read: Stopped. Ask for the text pasted in the message.
