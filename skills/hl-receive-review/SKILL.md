---
name: hl-receive-review
description: "Evaluate review feedback item by item against the code and decide agree, defer, disagree, or clarify, without applying fixes. Use when the user receives code review comments and wants to decide how to respond."
---
# Receive Review

Input: `[review text or review-file path]`

Use the input or fetch current PR review comments with available authenticated GitHub tooling. No review or tooling: ask for the text or a path. No actionable items: say so. Do not edit or post replies.

Split actionable claims, questions, style suggestions, and scope concerns. Check cited source and callers at the relevant revision. A mental trace is not an executed reproducer; label inference. Reviewer confidence, seniority, or unanimity is not evidence.

For each item, report type, claim, evidence, and verdict: agree+fix, agree+defer, disagree+rationale, clarify, or ignore for a duplicate or irrelevant item. "Fix" is a proposed action here, not work performed. An out-of-scope fix remains a user decision.

Count the items before you write any count. Copy each number and quote from the review text again before you repeat it.

## Output

Reader: the developer who received the review and decides how to reply: which comments to act on, and what to say on the rest.

Line 1, bold, one plain sentence, 100 characters at most: what to do first, in the user's words. Never open with a count or a verdict word.

Under line 1, plain sentences only for what limits the answer: a comment that could not be checked, a check not run, a missing input.

Then one numbered point per comment, in the review's order. Each point:
- A bold plain sentence: the comment in plain words, ending with its verdict in words: `Agree, fix it.`, `Agree, fix later.`, `Disagree.`, `Ask first.`, or `Ignore: duplicate of 2.`
- One or two sentences of evidence: `file:line`, or a command you ran ("I ran this"). Code reading is inferred; say "inferred from the code".
- One sentence on the action: the change, the reply, or the question. "Fix" is a proposal, not work done.

When an item needs more than two sentences of argument (usually a disagreement), add a `## <n>. <claim>` section after the list with the evidence.

`Verdict: <word>` on its own line just before `**Next:**`, one word for the whole review:
- `Agree`: every real item is "agree, fix it" or "agree, fix later". Ignored duplicates do not count.
- `Disagree`: every real item is "disagree".
- `Mixed`: the real items differ in verdict. Add the counts: `Verdict: Mixed (2 to fix, 1 to push back, 1 ignored)`.
- `Stopped`: no review text to assess.

`**Next:**` holds each step, in order: changes to make, replies to post, and each open decision as one question with at most 4 options, each saying what it does, the default marked.

Reader rules: never blame the reviewer; state what the code does. Reviewer seniority, confidence, or unanimity is not evidence. Do not disagree with every item to look rigorous, or agree with all of them because the review sounds authoritative.

````markdown
**Fix the expiry day and the typo; push back on the field rename, with the schema as proof.**

1. **The permit expires one day early. Agree, fix it.**
   `permits.py:9` uses `>=`, so the last valid day is rejected. I read this code; I did not run it.
   Change it to `>` and add a test for the last valid day.
2. **Renaming `pid` to `permit_id` breaks other systems. Disagree.**
   `exports/schema.json:4` defines `pid` for every reader of the file.
   Reply with the link to `exports/schema.json:4`; keep the name.
3. **The log message has a typo. Agree, fix it.**
   `permits.py:21` misspells "expiry" (inferred from the code).
   Fix the word.
4. **The expiry is off by one. Ignore: duplicate of 1.**
   It repeats item 1.

Verdict: Mixed (2 to fix, 1 to push back, 1 ignored)

**Next:**
1. Change `permits.py:9` to `>` and add a test for the last valid day.
2. Fix the typo at `permits.py:21`.
3. Reply to item 2 with the link to `exports/schema.json:4`.
````

Stopped, when the review text is missing:

````markdown
**I need the review comments to know what to answer, and none were given.**
I checked for PR access: `gh` is not available here, and the repo has no remote. I edited and posted nothing.

Verdict: Stopped

**Next:**
1. Paste the comments here. (default)
2. Give the path to a file that holds them.
3. Give the pull request number, if this tool can read it.
````
