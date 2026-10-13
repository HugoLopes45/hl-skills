# Gaps

Input: `--gaps [path or 'text'] [--write]`

Read the input; if empty, the latest plan, brief, or spec. Nothing to read: report it and stop. Never modify the source. A `*-gaps.md` file is never the spec; read one only to compare under `--write`.

Each gap has one category, one severity, an anchor, and one specific question. Anchor: the shortest supporting quote, or "not addressed" for an omission. Never invent implementation requirements.

Categories: unstated assumption, ambiguous term, missing edge case, missing actor, missing failure mode, missing acceptance criterion, missing dependency. One gap per category and anchor.

Severity: blocker (work cannot start or cannot be verified), major (an open implementation decision likely causes rework), minor (precision only). State each gap's consequence; never claim failure is inevitable.

First line: totals by severity. Then one table per severity, blockers first, rows sorted by category: category, anchor, question, consequence. None found: say "no gaps identified", not that the spec is complete. Non-Markdown input: say anchors may be imprecise.

With `--write`, save beside the source as `<stem>-gaps.md`, or `gaps.md` for inline text. If a report exists, compare first: keep questions still open, and show new and closed gaps. A gap is closed only when the source now resolves it; reworded text alone does not close it. Report the saved path.

Report only: the questions go in the report; do not wait for answers. To settle the blockers with the user, run without `--gaps`.
