---
name: hl-receive-review
description: "Evaluate review feedback item by item against the code and decide agree, defer, disagree, or clarify, without applying fixes. Use when the user receives code review comments and wants to decide how to respond."
---
# Receive Review

Input: `[review text or review-file path]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Give each comment its disposition and decisive evidence together. Keep proposed fixes, replies, and clarification questions in Next; reviewer confidence is not proof.

Use the input or fetch current PR review comments with available authenticated GitHub tooling. No review or tooling: ask for the text or a path. No actionable items: say so. Do not edit or post replies.

Split actionable claims, questions, style suggestions, and scope concerns. Check cited source and callers at one revision and name it: a commit, or the working tree when the files are uncommitted. For a comment on an older revision, check whether later commits changed its code. A mental trace is not an executed reproducer; label inference. Reviewer confidence, seniority, or unanimity is not evidence. Infer numeric domains and units only from a checked contract or validation, not an untyped parameter or example value.

For numeric feedback, build a comparison table from probe output, with each transformation and comparison executed in the probe itself. Label any result supplied by reasoning instead as inferred. Keep intermediate values and current versus proposed results distinct. Unknown accepted input types keep domain-dependent dispositions and new test inputs conditional on clarification.

For each item, report type, claim, evidence, and verdict: agree+fix, agree+defer, disagree+rationale, clarify, or ignore for a duplicate or irrelevant item. "Fix" is a proposed action here, not work performed. An out-of-scope fix remains a user decision. A disposition is a proposal: it resolves no thread, satisfies no required review, and clears no merge gate. Reuse an earlier answer only when its cited evidence still holds at the checked revision; a bare reply, bot resolution, or agreement is not evidence. Recheck changed code or new evidence and name what changed.

Count the items before you write any count. Copy each number and quote from the review text again before you repeat it.

## Output

Reader: the developer who received the review and decides how to reply: which comments to act on, and what to say on the rest.

Line 1, bold, one plain sentence: which concerns are supported or unresolved, in the user's words, without prescribing the reader's actions. Never open with a count or a verdict word.

Under line 1, plain sentences only for what limits the answer: the revision checked, a comment that could not be checked, a check not run, a missing input.

Then one numbered point per comment, in the review's order. Each point:
- A bold plain sentence: the comment in plain words, ending with its disposition: `Agree.`, `Agree, deferred.`, `Disagree.`, `Unresolved.`, or `Ignored: duplicate of comment 2.` (or `Ignored: irrelevant.`). These mean agree+fix, agree+defer, disagree+rationale, clarify, and ignore respectively; no fix has been applied.
- Give the evidence needed to check the disposition: `file:line`, or a command you ran ("I ran this"). Code reading is inferred; say "inferred from the code".
- Keep proposed changes, replies, and clarification questions only in Next; the comment entry gives evidence, not duplicate instructions.

When an item needs a separate trace or comparison to justify its disposition, add a `## <n>. <claim>` section after the list. Put the supporting detail there, without repeating the entry's evidence.

`Verdict: <word>` on its own line just before `**Next:**`, one word for the whole review:
- `Agree`: every real item is agreed or agreed but deferred. Ignored duplicates do not count.
- `Disagree`: every real item is "disagree".
- `Mixed`: the real items differ in verdict, or at least one remains unresolved. Add the counts: `Verdict: Mixed (2 to fix, 1 to push back, 1 ignored)`.
- `No action needed`: the supplied review has no actionable items. It is not merge approval.
- `Stopped`: no review text to assess.

`**Next:**` owns every reader action, prerequisite, reply, and question once, in dependency order. Put a decision before any implementation that depends on it. When the supplied history shows the same root cause still unfixed after three review-and-fix cycles, keep its evidence-backed disposition and state that the defect remains open; an agreed defect stays `Agree.`, not `Unresolved.` merely because it is unfixed. Ask one question about the approach instead of another fix-and-review round. Place that question after any live-secret or data-loss action and before routine fixes. Each open decision is one question with at most 4 options, each saying what it does, the default marked. Changes and replies are proposals, not work performed.

Reader rules: never blame the reviewer; state what the code does. Reviewer seniority, confidence, or unanimity is not evidence. Do not disagree with every item to look rigorous, or agree with all of them because the review sounds authoritative.

````markdown
**The expiry day and log message are wrong; the schema supports keeping `pid`.**
I checked the comments against commit `3f9a2c1`.

1. **The permit expires one day early. Agree.**
   `permits.py:9` uses `>=`, so the last valid day is rejected. I read this code; I did not run it.
2. **Renaming `pid` to `permit_id` is harmless. Disagree.**
   `exports/schema.json:4` defines `pid` for every reader of the file.
3. **The log message has a typo. Agree.**
   `permits.py:21` misspells "expiry" (inferred from the code).
4. **The expiry is off by one. Ignored: duplicate of comment 1.**
   It repeats item 1.

Verdict: Mixed (2 to fix, 1 to push back, 1 ignored)

**Next:**
1. Change `permits.py:9` to `>` and add a test for the last valid day.
2. Fix the typo at `permits.py:21`.
3. Reply to item 2 with the link to `exports/schema.json:4`; keep `pid` unchanged.
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
