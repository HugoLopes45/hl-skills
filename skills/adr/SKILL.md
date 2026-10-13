---
name: adr
description: "Draft an architecture decision record (ADR): context, options actually considered, decision, consequences, and reversal cost. Use when a consequential technical decision needs to be recorded."
---
# ADR

Input: `[decision summary or context path]`

Use the input as the decision or context path. Missing decision: ask for it. Several decisions: list them, draft the first, and offer one ADR for each other.

First line: the suggested file name and its status, together. Then one ADR: title, status, date, context, options actually considered, decision and reason, consequences, and reversal cost. Cite current source where relevant. Use Proposed unless the input cites a recorded approval, such as a merged change or meeting notes; "we chose" alone is not one.

Do not invent alternatives, criteria, weights, or scores to fill a matrix. Include a comparison only when supported by the discussion.

Name the file `<NNNN>-<kebab-case-title>.md`, with the next number in the repository's ADR sequence; no numbered ADR file in the repository: the number is unknown, so write `<NNNN>` literally in the file name and the title, never `0001`. Do not write the file.
