---
name: hl-receive-review
description: "Evaluate review feedback item by item against the code and decide agree, defer, disagree, or clarify, without applying fixes. Use when the user receives code review comments and wants to decide how to respond."
---
# Receive Review

Input: `[review text or review-file path]`

Use the input or fetch current PR review comments with available authenticated GitHub tooling. No review or tooling: ask for the text or a path. No actionable items: say so. Do not edit or post replies.

Split actionable claims, questions, style suggestions, and scope concerns. Check cited source and callers at the relevant revision. A mental trace is not an executed reproducer; label inference. Reviewer confidence, seniority, or unanimity is not evidence.

For each item, report type, claim, evidence, and verdict: agree+fix, agree+defer, disagree+rationale, clarify, or ignore for a duplicate or irrelevant item. "Fix" is a proposed action here, not work performed. An out-of-scope fix remains a user decision.

First line: the count per verdict. Then the item table and unresolved decisions. Do not force disagreement because all feedback appears correct, or agreement because it sounds authoritative.
