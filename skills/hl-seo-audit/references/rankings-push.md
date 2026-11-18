# Rankings push checks

Read this file when the user asks how to move a page up in results, supplies a search-performance export for that purpose, or plans to publish a new page. Without an export, write "not measured" for positions, impressions, and click-through. Thresholds in this file are heuristic defaults, not facts.

## Buckets

Use query and page pairs for a recent period, compared with the period before to filter spikes. Sort each matching pair into one bucket. `Near the top` takes precedence over `Striking distance` when both match. Leave unmatched pairs `unclassified`.

| Bucket | Filter (heuristic default) | Fix type |
|---|---|---|
| Striking distance | Average position 5 to 20 (heuristic default); impressions above a floor you set from the export size | Content and internal links |
| Weak click-through | Position 1 to 3; click-through low against other pages at similar positions | Title and meta description |
| Near the top | Position 4 to 7 on a query that matters to the business | Content, internal links, and the format the results use |

Rank pairs by business value first, then by impressions. A query that drives sales outranks a higher-impression query that does not.

Before you change a page, run the cannibalization check in [checks.md](checks.md).

## Diagnose against the top results

Open the three results (heuristic default) above the page for its query. Without web access, write that this check was not run. Write what each covers that the page lacks, as an inference. Then match the page to one cause:

| Cause | Evidence | Fix |
|---|---|---|
| Content gap | The top results cover a section or format the page lacks | Add that section or format |
| Intent mismatch | The page answers a neighboring question | Answer the searched question, or target a different page |
| Authority gap | A link export shows the top results have more or stronger links | Record the gap; link acquisition is outside this audit |
| Foundation gap | An indexing or technical finding blocks the page | Fix that finding first |
| Low competition | The top results are thin or off-topic | The page may already fit; check the other causes before changing it |

If no cause fits, do not rewrite the page. Write that the cause is unconfirmed.

Grade each subtopic by how many of the results opened above cover it: expected (all do), common (most do), distinctive (one does) or uncovered (none does). Fill the expected ones first.

## Smallest change

- **Answer first**: when the query calls for an answer, put the answer at the start of the main text.
- **Add the missing section**: add it; do not rewrite the page, because it already ranks.
- **Title and H1 for intent**: when the top results' titles and H1s promise a different page type or answer than this page, rewrite them to match the intent shown by the top results. Leave a title that matches that intent unchanged.
- **Internal links**: add links from the strongest related pages, with anchors that name the target. The link check belongs to `hl-internal-linking`.
- **Stale facts**: update dated facts, figures, screenshots, and broken links on the page.
- **Click-through only**: for weak click-through, change only the title and meta description, so the result is attributable. State the specific outcome in the title, add the audience or format qualifier the searcher filters on, and remove filler words.

## Measure and stop

- **Baseline**: record the position, impressions, and click-through before the change. Wait three to four weeks (heuristic default) before you judge the change or edit the page again.
- **Stop rule**: stop after two rounds with no movement (heuristic default). A round is one change and its waiting period. The page is probably limited by intent or authority, as an inference; on-page edits are then unlikely to help.

## New page launch

Check each item before you publish a new page:

- [ ] At least three internal links from relevant existing pages, with descriptive anchors (heuristic default).
- [ ] Self-referencing canonical.
- [ ] Listed in the sitemap.
- [ ] Indexable: no `noindex`, and not blocked by robots.txt.
- [ ] Main content in the static HTML.
- [ ] Unique title and meta description for the target query; H1 aligned with the title.
- [ ] Links to the conversion path the page serves.
- [ ] Structured data, where the page type supports it: its check belongs to `hl-schema-markup`.

After publishing, request indexing for the URL once. Before you suggest a repeat request, check the search engine's current indexing guidance; without web access, write that this check was not run. If the page stays out of the index, run the Indexing checks in [checks.md](checks.md).
