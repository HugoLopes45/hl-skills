---
name: hl-de-ai-rewriting
description: "Rewrite general prose such as articles, reports, notices, and bios so each sentence states its fact plainly, keeping every claim, number, name, and condition the author wrote. Flags patterns that read as generated and gives the reason for each. Makes no promise about AI-detection results. Use when the user asks to make a text read less generated, remove stock phrasing or filler, or review a draft for vague or padded sentences."
---
# De-AI Rewriting

Input: `[text, file, or pasted prose] [--mode rewrite|flag]`. Default mode: `rewrite`.

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

## Evidence rules

- The supplied text is the only evidence. Do not add facts, examples, names, numbers, sources, anecdotes, or opinions the author did not write.
- Before any edit, list what the text claims: each claim, number with its unit, name, date, condition, negation, opinion, and cause-and-effect link. The rewrite keeps every item. A style edit is not a fact-checking mandate: retain an unsupported opinion in neutral wording and flag it outside the rewrite rather than silently deleting it.
- Flag a sentence only for a pattern in [references/patterns.md](references/patterns.md). Give the reason in terms a reader feels: vague, padded, unclear, or unsupported. "It sounds generated" is not a reason.
- Do not claim, promise, or aim for any AI-detection result. Detector output does not measure clarity or accuracy. Do not add typos, odd word choices, or random variation to change how a text scores.
- Keep the author's language, register, and terms. Do not translate.

## Intent

- Act directly when text is supplied. A request to make a text read less generated needs no question.
- Stop only when the text is missing or unreadable (see Stop conditions). A missing audience or purpose does not stop the work: keep the audience the text already shows, and label it as inferred.
- An exclusive output request, such as only the rewritten text or JSON only, replaces the default output. A request for a code block followed by reasons is not exclusive: keep the default Verdict and Next after those parts. Evidence rules apply in every format.
- When the user asks for a detection result, say in one sentence that this skill does not target detector scores, then rewrite for clarity.

## Modes

### rewrite (default)

1. **List the claims.** Number each item of the claim list, with the sentence it comes from.
2. **Flag the sentences.** Mark each sentence that matches a pattern in the reference. Name the pattern and give one reason.
3. **Rewrite each flagged sentence.** Preserve meaning, not padded wording. Replace vague claims with plain equivalents, such as easy setup instead of seamless setup, without adding proof or removing the author's view. Keep negation, condition, cause, and order. Remove a hedge only when it does not qualify a claim.
4. **Check the meaning.** Compare the rewrite with the list. Each item survives, no item is added, and each qualifier is kept.
5. **Leave a sentence alone** when the change is not clearly better. Report each changed sentence with its reason.

### flag

Run steps 1 and 2 only. Return the flagged sentences with their patterns and reasons. Return no rewrite.

## Output

Reader: an author or editor who will publish or send the text next. The decision served: whether the text can go out as rewritten, and which sentences the author must still check.

Line 1 is one bold plain sentence that states the result, for example "**The notice keeps its 3 facts and changes 3 of its 5 sentences.**" It never opens with a label, verdict word, or number.

Under line 1, in plain sentences: each claim the rewrite could not state without more information from the author, and each sentence whose meaning you could not confirm. Omit both when none apply.

Rewrite mode puts the full text in a `text` fence with no added headings. After the fence, list each changed sentence: the original in quotes, its pattern, and one sentence of reason. List each flagged sentence you left unchanged the same way, with what the author must supply.

Verdict words:
- `Rewritten`: rewrite mode complete; each change is listed, or none was needed; the claim list is kept.
- `Flagged`: flag mode complete.
- `Stopped`: no text to work on.

Put `Verdict: <word>` on its own line just before `**Next:**`. Each Next line is one action a person can take now, in order.

Stopped: line 1 says what is missing and why it blocks the work. Then `Verdict: Stopped`. Next asks for the text, with `Default: none`.

Reader rules:
- Define each term once at first use: pattern (a sentence shape that weakens a claim), hedge (a word such as "may" or "could" that marks uncertainty).
- Quote the original sentence exactly.
- No praise of the rewrite, no blame for the author's draft.

Example (signature only; the domain is not a fixture):

````markdown
**The notice keeps its 3 facts and changes 3 of its 5 sentences.**

```text
Starting 2 June, flour deliveries move from Tuesdays to Thursdays.
Orders placed by Wednesday at 6 p.m. arrive the following Thursday.
The change helps us serve bakers better.
Contact us with any questions.
```

1. "We are excited to share some important news about our delivery schedule." Pattern: empty announcement. Reason: it states no fact; the next sentence carries the change. Removed.
2. "This thoughtful change allows us to better serve our valued community of bakers." Pattern: vague praise. Reason: it claims a benefit with no fact behind it. Rewritten in neutral wording.
3. "Feel free to get in touch with any queries." Pattern: closing filler. Reason: it adds no instruction. Rewritten to the call to action.

Verdict: Rewritten

**Next:**
1. Check the three facts in the rewrite (2 June, Tuesday to Thursday, Wednesday 6 p.m.) against the supplier notice.
2. Confirm that "The change helps us serve bakers better." is your view, or remove it.
3. Put the text in the newsletter yourself.
````

## Stop conditions

- No text, or a file that cannot be read: Stopped. Ask for the text pasted in the message.
