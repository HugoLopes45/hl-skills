---
name: hl-adr
description: "Draft an architecture decision record (ADR): context, options actually considered, decision, consequences, and reversal cost. Use when a consequential technical decision needs to be recorded."
---
# ADR

Input: `[decision summary or context path]`

Use the input as the decision or context path. Missing decision: stop, as the Output section says. Several decisions: draft the first, and name each other one in the sentence under line 1 (see Output).

Line 1 names the file and the decision; the status goes on the verdict line, as the Output section shows. Then one ADR: title, status, date, context, options actually considered, decision and reason, consequences, and reversal cost. Cite current source where relevant. Use Proposed unless the input cites a recorded approval, such as a merged change or meeting notes; "we chose" alone is not one.

Do not invent alternatives, criteria, weights, or scores to fill a matrix. Include a comparison only when supported by the discussion.

Name the file `<NNNN>-<kebab-case-title>.md`, with the next number in the repository's ADR sequence; no numbered ADR file in the repository: the number is unknown, so write `<NNNN>` literally in the file name and the title, never `0001`. Do not write the file.

## Output

Reader: the person who made the decision, or a reviewer. They check the draft, then save it as the record. An ADR (architecture decision record) is a short file that explains one technical choice.

Line 1, bold, one plain sentence within 100 characters: what was drafted, and the file name to save it as (`<NNNN>` when the number is unknown). Use the user's words for the decision.

Under line 1, plain sentences without labels: the decision, the reason the input gave, and the reversal cost (the work to undo the choice). When the input gives no reversal cost, say it is not stated and needs filling in. Then, only when the input holds more decisions, one sentence: `I also found: <decision>. Say "next" to draft it.`

Then the ADR in one `markdown` fence, complete, so it can be saved as is. Only the ADR goes in the fence; line 1 and the sentences around the fence are plain text. Above the fence, one plain line per `<...>` placeholder the block still holds.

End with `Verdict: <word>` on its own line, then `**Next:**`:
- `Proposed`: a draft the team has not agreed to.
- `Stopped`: no decision to record.

Stopped, no decision: line 1 says in plain words what is missing and why it blocks: `**I need the decision before I can draft the record: what was chosen, and why.**` Then `Verdict: Stopped`, then `**Next:**` with up to 3 numbered ways to send it, default marked, listed nowhere else: a sentence such as "we chose X over Y because Z" (default); a path to meeting notes or a pull request. Naming the options you rejected also helps; the record shows only the ones you name.

Reader rules:
- Write each option as one sentence: what it is and what it costs. Spell out reversal cost at first use.
- Name each option as the source names it. Options and reasons come only from the input; a missing one stays a placeholder.

End: `**Next:**` with these steps, in order: when the reversal cost is not stated, fill it in; check the decision and its reason; save the block as the file name in the repository's ADR folder; change `Proposed` to `Accepted` once the team agrees.

````markdown
**I drafted the record of the GraphQL choice. Save it as 0004-use-graphql-for-the-mobile-api.md.**
The team chose GraphQL for the mobile API, so the order screen makes one request instead of four.
The web app keeps its REST endpoints.
Reversal cost is medium: the mobile screens call GraphQL directly, so a move back rewrites those calls.

```markdown
# 0004. Use GraphQL for the mobile API

Status: Proposed. Date: 2025-03-04.

## Context
The mobile order screen calls four REST endpoints. Each returns fields the screen does not show.

## Options considered
- Keep REST and add one endpoint per screen: no new tool; one endpoint to maintain per screen.
- GraphQL: one query for the fields the app shows; the team learns a schema language.

## Decision
Use GraphQL for the mobile API. The web app keeps its REST endpoints.

## Consequences
- The order screen makes one request.
- The mobile team writes queries and schema types.

## Reversal cost
Medium. Mobile screens call GraphQL directly, so a move back rewrites those calls.
```

Verdict: Proposed

**Next:**
1. Check the decision and its reason. Correct any line that is wrong.
2. Save the block as `0004-use-graphql-for-the-mobile-api.md` in the ADR folder.
3. Change `Proposed` to `Accepted` once the team agrees.
````
