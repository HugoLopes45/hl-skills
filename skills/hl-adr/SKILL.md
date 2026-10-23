---
name: hl-adr
description: "Draft an architecture decision record (ADR): context, options actually considered, decision, consequences, and reversal cost. Use when a consequential technical decision needs to be recorded."
---
# ADR

Input: `[decision summary or context path]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Lead with the decision and its consequence. Keep the ADR complete; the reply need not repeat the record.

Use the input as the decision or context path. Missing decision: stop, as the Output section says. Several decisions: draft the first, and name each other one in the sentence under line 1 (see Output).

Line 1 names the file and the decision; the status goes on the verdict line, as the Output section shows. Then one ADR: title, status, date, context, options actually considered, decision and reason, consequences, and reversal cost. Cite current source where relevant. Use Proposed unless the input cites a recorded approval, such as a merged change or meeting notes; "we chose" alone is not one.

Do not invent alternatives, criteria, weights, or scores to fill a matrix. Include a comparison only when supported by the discussion. Keep each claim's evidence, predictive wording, estimates, and unknowns inside the ADR itself, including consequences and reversal cost. A qualifier outside the copyable record does not qualify its contents.

Use the requested file name. Otherwise follow a checked repository convention; do not call this skill's default a project rule. Default: `<NNNN>-<kebab-case-title>.md`, using the next number in an existing ADR sequence. No sequence: keep `<NNNN>` unknown, never invent `0001`. An explicitly unnumbered draft needs no number. Do not write the file.

## Output

Reader: the person who made the decision, or a reviewer. They check the draft, then save it as the record. An ADR (architecture decision record) is a short file that explains one technical choice.

Line 1, bold, one plain sentence: what was drafted and its proposed file name (`<NNNN>` only for a numbered draft whose sequence is unknown). Use the user's words for the decision.

Under line 1, plain sentences without labels: unresolved information and approval status only when they limit the draft. Name missing information, including an unknown number, date, or reversal cost, without filling it in. Do not retell the artifact's decision, reason, or known reversal cost. Name any additional decisions here without asking the reader to act.

Then the ADR in one `markdown` fence, complete, so it can be saved as is once placeholders are resolved. Only the ADR goes in the fence; line 1 and the sentences around the fence are plain text. Placeholder-filling instructions belong only in Next.

End with `Verdict: <word>` on its own line, then `**Next:**`:
- `Proposed`: a draft the team has not agreed to.
- `Stopped`: no decision to record.

Stopped, no decision: line 1 says in plain words what is missing and why it blocks: `**I need the decision before I can draft the record: what was chosen, and why.**` Then `Verdict: Stopped`, then `**Next:**` with up to 3 numbered ways to send it, default marked, listed nowhere else: a sentence such as "we chose X over Y because Z" (default); a path to meeting notes or a pull request. Naming the options you rejected also helps; the record shows only the ones you name.

Reader rules:
- Explain each option: what it is, what it costs, and the evidence or uncertainty behind the trade-off. Spell out reversal cost at first use.
- Name each option as the source names it. Options and reasons come only from the input; a missing one stays a placeholder.

End: `**Next:**` owns every reader action, question, and prerequisite, once: resolve every placeholder, including the number, date, or reversal cost when unknown; check the decision and its reason; save the block as the proposed file name in the repository's ADR folder; change `Proposed` to `Accepted` only after recorded team approval. If additional decisions were found, offer drafting the next one here.

````markdown
**I drafted the GraphQL decision record as `0004-use-graphql-for-the-mobile-api.md`.**

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
3. Change `Proposed` to `Accepted` only after recording the team's approval.
````
