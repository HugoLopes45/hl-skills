# Page sets

Read this file when a family is a frame with a slot (such as "X for [industry]" or "[product] integration") and the user asks for generated pages. Run the checks in order. The anti-doorway, result pages, demand and unique-facts checks and archetype requirements set the result when they fail; the overlap and spot-check steps and the ramp shape the build.

## Result

State the result in the point for that family, as one plain sentence. The `Verdict:` line of the answer keeps its research word.

- **Build as listed**: all checks pass and the archetype's requirements are met. Record the approved modifier list and the target page count.
- **Build a narrower set**: the frame is right and the scope is wrong. Narrow the modifiers to the rows that have unique facts, or switch to a page type the evidence supports. Phase the plan when the site is small (see Build and launch).
- **Do not build the set**: the anti-doorway test fails, aggregator sites hold every sampled result page with no narrower set left, no row keeps both demand and unique facts, or the archetype's required data is missing. Recommend a few editorial pages on the strongest modifiers instead, a heuristic default of 3 to 5. `hl-content-brief` owns their briefs.
- **Not decided yet**: no check fails, and the anti-doorway, result pages, demand or unique-facts check is `not checked`. Name the check that did not run, and put the input that runs it in Next. Do not build the set before it runs.

## Checks

1. **Anti-doorway.** Pick two random modifiers and write the honest answer for each. If the answers differ only by the noun, do not build the set. A reader who has read one page must learn something on another page that the first page did not give. If no data source can make that true, do not build the set, whatever the search volume. Ask also whether a reader would want the page if search engines did not exist; a page that exists only for search is not built. Check the search engine's current official spam policy on scaled content, or write `not checked`.
2. **Result pages.** Sample the result pages of 3 to 4 modifiers (heuristic default), from results the user supplied. If data-rich aggregator sites hold every sampled page, build a narrower set from modifiers they do not cover, or do not build it. Without result pages, write `not checked`.
3. **Demand per row.** Each row's query shows demand under the demand signal in [method.md](method.md) (Validation). Drop rows without demand; do not pad the set with them. If no row has demand, do not build the set. If only some rows have it, build a narrower set from those rows.
4. **Unique facts.** Each row needs at least three facts (a heuristic default) that no other row has, each with its source. Record a last-verified date with each fact. Drop a row that falls short from the first batch and keep it in a backlog for enrichment. If only the top modifiers qualify, build a narrower set from them. Rank the data source as in [method.md](method.md) (Validation, axis 4). Use only facts from a source the user supplied or a page read in this session. A model writes connecting prose, never a fact.
5. **Overlap.** Before the build, check that no existing page and no other row targets the same intent. Merge rows that share one.
6. **Spot-check.** Trace three rows end to end: each fact to its source, and each page's answer to its own query. If a check fails, fix the data or the template, then check again. Do not patch one page; the same defect remains on every other row.

## Template

- Use 3 to 4 title frames (heuristic default), each chosen by a row attribute. Build each meta description from a unique row field, never one sentence shared by all rows.
- Put row-unique sections first. Keep shared text under half the rendered words (heuristic default). Move a section that reads the same on every row to the pillar.
- Show a data-driven section only when its row has the data. Remove an empty section; never fill it with filler.
- Add an FAQ only from questions observed for that row. Omit it when none exist. Never reuse one question set with the noun swapped.
- The pillar links to every row. Each row links to the pillar and to 3 to 5 related rows that share a data attribute (heuristic default). Keep every row within 3 clicks of the pillar (heuristic default).

## Archetypes

Apply the archetype that matches the frame, after the checks.

- Comparison set: give a verdict per pairing only when each side has 2 facts across 2 dimensions (heuristic default). Otherwise show the matrix with `winner not decided`. Never give the business's own product every verdict.
- Glossary set: each term needs an original worked example and a misconception note. Link terms by real relationships.
- List set (`best [X] for [modifier]`): state the evaluation criteria and the update date. Rank by those criteria, not by commission alone.
- Tool set (converters, calculators): each row needs live or accurate data for the tool to run on. Without it, do not build the set.
- Examples set: show real examples only, each with the reason it works.
- Persona set (`for [industry or role]`): each page needs workflows that differ by persona. Without them, do not build the set.

## Build and launch

- Publish the pillar and the strongest-data rows first. Noindex a thin variant, or leave it out of the set.
- Name who refreshes each row's data and how often. A row with no refresh owner stays out of the first batch.
- Put each generated page type in its own sitemap, listing only indexable URLs.
- Put the set under the main site's path when its pages should share the site's internal links and structure. Check the search engine's current guidance on URL structure, including whether a subdomain needs its own links and sitemap, before publishing.
- Ramp: a heuristic default is 20 to 50 pages per batch. A batch should not multiply the site's indexed page count by more than 2 to 3 times (a heuristic default). A small site with a large set gets a phased plan measured in months; say so before the build.
- Before the next batch, check the indexing report and the search performance of the previous batch. Most pages indexed with impressions: continue. A widespread not-indexed status: stop and improve the pages before adding volume.

## Track after launch

After each batch, track indexed pages, impressions, clicks, average position, traffic, engagement and conversions. Watch the search console for thin-content warnings, manual actions and crawl errors.

A page with 0 impressions 60 days after indexing (heuristic default) gets one treatment: enrich it, consolidate it with a redirect, or remove it. Do not leave it as is.

Each quarter (heuristic default), the user samples query-form prompts for the set's modifiers and supplies which pages are named. `hl-ai-search-visibility` owns the sampling method.
