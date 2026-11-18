# Traffic drop checks

Read this file when the user asks why organic traffic dropped, or supplies an export for a drop. Without an export for both periods, write "not measured" for the drop and its causes.

## Split the drop

Compare the recent period with the period before, for the same length of time. Split the change into three parts, then read each one:

- **Brand demand**: queries that name the business. A fall here suggests lower demand, not a page problem; this is an inference.
- **Serving loss**: pages that stopped returning 200, gained a noindex, or changed their canonical. Without an earlier crawl of the same scope, report the current state only; the change is not confirmed. Run the Indexing checks in [checks.md](checks.md).
- **Rank loss**: non-brand queries that lost position. Compare them with the top results as in [rankings-push.md](rankings-push.md).

Judge recovery on non-brand queries only.

## Match the pattern

- A drop on a few pages points to a change on those pages, a missing redirect, or lost content. Check those pages first. For a moved site, use [migration.md](migration.md).
- A drop across many pages at once is usually a site-wide change, a crawl problem, or lower demand. This is an inference; confirm it with the Indexing checks and the brand split before you act.
- A page whose clicks fall over several periods, with no change to the page, is a content decay candidate. Refresh its stale facts first; see the Stale facts item in [rankings-push.md](rankings-push.md). Then wait the period set in its Measure and stop section before a second change.
