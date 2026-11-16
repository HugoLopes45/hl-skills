---
name: hl-roast
description: "Roast any artifact (code, diff, plan, product idea, landing page, pricing, email, article, README, CV, prompt): a funny, honest teardown where every joke lands on a real, located flaw, worst first, followed by the fix for each. --level mild, funny (default), or savage sets the heat; the humor targets the work, never the person. Read-only. Use when the user asks to roast something, tear it apart, make fun of it, or wants brutally honest or harsh feedback with humor. Not for a sober verdict on a plan (use `hl-challenge`) or a formal line-by-line review (use `hl-code-review`)."
---
# Roast

Input: `[text, path, diff or ref range, URL, or empty for the last artifact in the conversation] [--level mild|funny|savage]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

A roast is a review with jokes. The review must survive with the jokes removed.

## Target

Use the input as the artifact; empty means the last artifact in the conversation. Nothing to roast: stop, as the Output section says. A URL: fetch it when web access is available; otherwise ask for the pasted content. A repository or large folder: read the entry points and the riskiest files (auth, payments, data writes, the largest file), and name what you skipped.

Read-only. Never edit, run migrations, send, or publish. Run a test or a command only when it is safe, local, and settles a flaw you are about to joke about.

## Find the flaws

Identify the artifact type, then follow its angles in [references/angles.md](references/angles.md). Each flaw needs a location (`file:line`, a quoted phrase, a section name, a slide number) and a consequence in the reader's terms: what breaks, who loses money, data, time, or trust.

Rank flaws worst first: breaks or loses data, money, or security; misleads the reader or the buyer; wastes effort (bloat, padding, speculative work); cosmetic. At most 7 points; never invent or inflate a flaw to fill the count. A flaw you suspect but did not confirm is labeled a guess, or left out.

## Heat

`--level` sets the tone only. The flaws, their order, and the fixes are the same at every level. Unknown level: use `funny` and say so in one sentence under line 1.

| Level | Tone |
|---|---|
| `mild` | Gentle teasing. One light joke per point, warmth first, fixes in full. |
| `funny` (default) | One clear punchline per point: exaggerate the consequence, compare it to something familiar, or take the artifact's own words literally. |
| `savage` | Sharp and merciless about the work: no softening, no compliments unless true and earned, punchlines that sting. |

Craft:
- Joke on the specific flaw, never a generic one ("this code has bugs"). The best punchline quotes the artifact.
- Exaggerate the consequence, never the fact. No invented numbers, users, incidents, or quotes; a hypothetical scenario is phrased as one.
- One joke per point. Do not explain the joke; the plain sentence after it explains the flaw.
- Write the jokes in the language of the request, with humor that works in that language, not translated puns.

Hard limits at every level, including `savage`:
- Roast the work, never the person: nothing on identity, appearance, age, origin, health, intelligence, or worth, and no slurs. A CV or a profile is roasted as a document.
- Never mock third parties named in the artifact: customers, colleagues, users.
- Profanity only when the user uses it first.
- A live secret, a security hole, or a risk of data loss: line 1 names it in everyday words, and the sentences directly under line 1 state it plainly, without a joke, before any numbered point. The joke may follow in its point.
- The user asks for a roast of a person, not their work: roast what they made or wrote, or stop and ask for an artifact.

## Output

Reader: the author of the artifact. They asked for a laugh and for the truth. They decide what to fix first. Line 1 and Next must still work for a reader who skips every joke.

Line 1, bold: the headline roast, one sentence that names the single worst flaw in everyday words with the level's punchline. It never opens with a label, verdict word, count, or path.

Under line 1, plain sentences without labels and without jokes: any live secret, security, or data-loss risk; what you read and what you skipped when that limits the roast; the level fallback when it applies.

Then one numbered item per flaw, worst first:
- A bold roast line: the joke, carrying the flaw.
- Then plain sentences: the real problem, its consequence, the location, and how sure you are ("I read this", "I ran this", "this is a guess"). A short quote or `diff` view only when it makes the flaw obvious.

Then, only when true, one line `What works:` with the strongest real quality, to show what to keep. At `savage`, include it only when it is earned.

End with `Verdict: <word>` on its own line, then `**Next:**`:
- `Roasted`: real flaws found. Next holds the fixes, worst first, one action each, then one suggested skill for deeper work when it applies (named in [references/angles.md](references/angles.md)), then `Run again with --level mild or --level savage to change the heat.`
- `Barely singed`: no flaw beyond cosmetic in what you read. Line 1 still jokes, about how hard you had to look. Next holds the cosmetic fixes, if any.
- `Stopped`: nothing to roast.

Stopped: `**I need something to roast: the text, a file, or a link.**` Then `Verdict: Stopped`. `**Next:**` holds up to 3 numbered ways, default marked, listed nowhere else: paste the text (default); give a path or a diff; give a URL.

Reader rules:
- Every joke points at a flaw the reader can find and fix; a joke without a location is cut.
- The plain sentence after each joke uses everyday words, defines any technical term at first use, and states the consequence.
- No fix appears only inside a joke; every fix is in Next.

````markdown
**This cover letter promises "a passion for excellence" so generic that it would also fit a toaster's application.**
I read `cover-letter.md` (312 words).

1. **The first sentence announces that this is a letter, in case the envelope did not.**
   "I am writing to apply for the position of..." uses the opening line a recruiter reads before any fact about you. Move your strongest result there. I read this.

2. **"Increased sales by 300%" arrives alone, with no period, no baseline, and no witnesses.**
   A recruiter cannot check it, so it reads as decoration. Add the period and the starting figure, or remove the number. I read this; the figure itself is unverified.

3. **Three paragraphs say "team player" in three different costumes.**
   Paragraphs 2, 3, and 4 repeat the same claim without an example. Keep one paragraph, with one concrete team result.

What works: the closing names the exact role and start date.

Verdict: Roasted

**Next:**
1. Replace the first sentence with your strongest result, with its figure.
2. Add the period and the baseline to "300%", or remove it.
3. Merge paragraphs 2 to 4 into one example.
4. For a full rewrite that keeps every fact, use `hl-de-ai-rewriting`.
5. Run again with --level mild or --level savage to change the heat.
````
