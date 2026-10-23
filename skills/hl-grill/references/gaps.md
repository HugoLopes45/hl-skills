# Gaps

Input: `--gaps [path or 'text'] [--write]`

Read the input; if empty, the latest plan, brief, or spec. Nothing to read: use the skill's Stopped form. Never modify the source. A `*-gaps.md` file is never the spec; read one only to compare under `--write`.

Each gap has one category, one severity, an anchor, and one specific question. Anchor: the shortest supporting quote, or "not addressed" for an omission. Never invent implementation requirements.

Categories: unstated assumption, ambiguous term, missing edge case, missing actor, missing failure mode, missing acceptance criterion, missing dependency. One gap per category and anchor.

Severity: blocker (work cannot start or cannot be verified), major (an open implementation decision likely causes rework), minor (precision only). State each gap's consequence; never claim failure is inevitable.

Line 1, bold, one plain sentence in everyday words: what the gaps leave open and whether it blocks the work, e.g. `**The spec leaves two things open that block the work: the speed target and the recipients.**` In a complete report, use one heading per severity present, blockers first. Number gaps across all severities. Each item leads with `**<consequence in plain words>**`, then its category and anchor; preserve one specific question per gap. Do not use tables. None found: say "no gaps identified", not that the spec is complete. Non-Markdown input: say anchors may be imprecise.

Without a saved file, show every gap's consequence, category, and anchor in the reply body; put its question only in Next, matched by the same gap number. End with the counts as `Verdict: Gaps, 2 blockers, 1 major, 0 minor` immediately before `**Next:**`. Use `1 blocker` when there is one; otherwise `blockers`. Keep major and minor counts exact.

With `--write`, save beside the source as `<stem>-gaps.md`, or `gaps.md` for inline text. The saved report is self-contained: retain every gap's severity, category, anchor, question, and consequence, plus the exact totals. If a report exists, compare first: keep questions still open, and show new and closed gaps. A gap is closed only when the source now resolves it; reworded text alone does not close it.

After a successful save, the reply names the saved path and the decisive unresolved consequences, not every saved gap. Repeat the full report only when requested inline; its operational content stays complete. Put reader questions and any route to settle gaps only in Next, without repeating the artifact's advice. End with the count verdict immediately before Next, then `**Changed:** <saved path>`. If saving fails, say so and include the complete report in the reply, with its questions in Next.

Report only; do not wait for answers. When useful, put the route to settle blockers by running without `--gaps` only in Next. Without a saved file, end with `**Changed:** none`.
