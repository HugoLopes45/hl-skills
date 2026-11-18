# Method

Use this file for the detailed steps. The workflow and evidence rules are in `SKILL.md`.

## Scope questions

Answer each from the input or the supplied evidence. A missing product or buyer stops the research unless the evidence names them.

- **Product**: one line, in the buyer's terms.
- **Buyer**: who searches, and what they do before they search.
- **Decision**: what the buyer wants after the search: learn, compare, buy, or sign up.
- **Market and language**: the locale of the buyer and the search engine or platform. Record it beside every figure.
- **Existing pages and proof**: when supplied, note which page already answers which phrase.

## Seed sources, in order

1. Search Console query export: queries the site already gets, with measured figures.
2. Buyer language: reviews, support tickets, sales calls, community threads, survey answers. Extract objections, the phrasing customers use for their problem, competitor mentions, and survey themes, not only questions.
3. Competitor pages the user supplied: their titles and headings only.
4. The user's own keyword list.

Record the source of each seed. A seed with no source is `proposed, not checked`.

When the sources run thin, seed through six lenses drawn from the supplied product and buyer facts: what the business sells, the problems it solves, the outcomes it delivers, its positioning, adjacent topics the buyer already reads, and named entities (tools, frameworks, competitors). Label each lens seed `proposed, not checked` until a source shows it.

Use the positioning angle as the answer a seed leads to, never as the target keyword.

## Families

Group the seeds into topic families. A family answers one business question, and two candidate families that answer the same question merge. A heuristic default of 4 to 8 families per business; more usually means the question split is too fine. A family is the unit of the decision queue, and each cluster takes its family's label.

## Intent

| Intent | The searcher wants | Page type |
|---|---|---|
| informational | to learn how or what | guide, glossary entry, help article |
| comparison | to choose between options | comparison, alternatives page |
| transactional | to buy, sign up, or book | product, pricing, or sign-up page |
| navigational | to reach a known brand or product | brand or product page |

Map each intent to a buyer stage: informational to awareness, comparison to consideration, transactional to decision. A how-to-use query after a purchase is implementation: informational intent, aimed at a setup page or tutorial. Stage modifiers are a starting point to check against the export: "what is" and "how to" (awareness); "best", "vs" and "alternatives" (consideration); "pricing", "reviews", "demo" and "trial" (decision); "template", "example" and "setup" (implementation).

Assign one intent per keyword. When a keyword mixes two intents, the first intent the buyer's words show wins; note the second.

## Clustering

- One primary keyword per page.
- Keywords share a page when the same answer satisfies both and the intent matches.
- Give a keyword its own page only when its intent differs from the page it would otherwise join.
- Propose a pillar page with supporting pages only when the site has, or the user plans, the pillar; the pillar aligns with the offer and is broad enough for subtopics; and supplied evidence shows audience interest in search or social. Label it `proposed`.
- Build the pillar page before its supporting pages. Give a pillar its own URL only for a major topic; otherwise place it under an existing path.
- Spot a programmatic pattern (a frame with a slot, such as "X for [industry]") only when two different substitutions of the same frame appear in the evidence. Record the frame and those examples. Never list other substitutions to prove the pattern.
- Match the pattern to assets the business holds: data gives directory or profile pages, integrations give integration pages, and local presence gives location pages. Without a matching asset, the pattern is not a page-set candidate.
- A location page, or any row page, needs facts that differ by row, from that place's or row's own data. A swapped place name is not a page. Before building a page set, apply [page-sets.md](page-sets.md).
- A pattern may combine two patterns, such as a best-of list for one city. Each combined row still needs its own unique facts.

## Prioritization

Order clusters by these criteria, in this order, and state the basis of each:

1. **Buyer fit**: the phrase names the buyer's problem in the buyer's words.
2. **Intent closeness to purchase**: for a product that sells, transactional and comparison rank above informational.
3. **Page fit**: an existing page already answers the phrase (update), no page does (new page), or the page the export names answers another query (check before updating).
4. **Evidence**: measured figures from a supplied export, with their period and market, count as measured evidence. Few impressions or clicks make a figure weak evidence. Without measured figures, use buyer language the user supplied.
5. **Competing results**: only when the user supplied the results page. Otherwise write `not checked`. A family whose supplied AI answers name peers and omit the business ranks above a family with no such gap; say so.

The result is an order, not a score. Do not invent a formula that produces numbers.

## Decision queue

Rate each family high, medium, or low on three axes: business value (closeness to the offer's revenue), opportunity (evidence and page fit, including striking distance), and AI visibility (from answers the user supplied only; write `not observed` otherwise). Apply these rules in order; the first rule that matches sets the label.

1. Drop: the family fails two or more validation checks and no single article is worth writing.
2. Hold: a service the business cannot deliver, at any volume; or an informational family that a supplied AI answer fully answers, when the answer cites no source or only sources the business cannot be listed in, at any volume; or low business value.
3. Act now: high business value with high opportunity, or a striking-distance fix. At most two families (a heuristic default). When more qualify, rank them by business value, then opportunity, and move the rest to Act next.
4. Act next: every other family.

Each Act next family names the observation that would move it to Act now. Each Hold family names the unlock that would lift its hold. Start work on a family only after the user approves it. Before a family's first move, record its baseline: average position, impressions, clicks, and any supplied AI answers. Re-check at 2, 4 and 8 weeks after the first move (heuristic default).

## Striking-distance screen

Use this heuristic only when a Search Console export is supplied. Average positions 5 to 20 flag queries close to page one. The band does not prove an opportunity, and it never excludes a row by itself: a row outside it still counts when it fits the product and a page.

1. Read the columns: query, clicks, impressions, position, and page when present. The `position` column is the average position. A missing column is `not in export`.
2. Flag rows whose average position is from 5 to 20, inclusive. Among those, flag only rows with at least 50 impressions (a heuristic default floor); a row in the band below that floor is weak evidence, not a flag.
3. Sort the flagged rows by impressions, highest first, then by clicks.
4. Match each row to the page the export names. A row with a matching page is an update candidate; check its fit first. A row with no matching page is a new-page candidate. A flagged update candidate ranks above a new page of equal value.
5. Report how many rows you flagged out of all rows, for example "4 flagged of 7".
6. Label the figures `Measured (Search Console export)`. Do not call impressions search volume.
7. On a refresh, act on a flagged row only when its page has had no edit in the last 4 weeks (heuristic default). Ask the user for the edit date when the export does not show it. A row whose page was edited more recently is not a striking-distance fix yet: it does not make its family Act now. When the Decision queue rules put that family in Act next, name the next export as its observation.

## Validation

Check each family on four axes. Record each as `PASS`, `FAIL`, or `not checked`; a check that did not run is not a pass. In the output, write passes, fails or not checked in a sentence, not the codes.

1. **Demand signal**, strongest first: Search Console impressions, then a volume source, then autocomplete richness, then visible competitor investment. Impressions and autocomplete show a signal, not a size. Autocomplete richness: a heuristic default of 30 or more distinct completions suggests demand; about 2 does not. Supplied conversational questions count. No signal in either space fails.
2. **Market, not product.** A family named after the product fails. A family named after the buyer's problem or the category passes.
3. **Competitive reality**, from results the user supplied only; without them, write `not checked`. Dominant brands across fresh, thorough results: FAIL; look for an adjacent or longer-tail family. Otherwise PASS: a mix of large and niche sites is winnable with better content; thin, dated, or generic results are an opportunity. A forum or community thread in the top five (a heuristic default): a possible open gap; check whether any adequate article ranks there. Before building around that thread, name the engine whose results or answers cite it. Named competitor domains: record what each covers and skips per family, from the supplied results.
4. **Proprietary advantage**: original data, a method, or practitioner experience that competitors cannot copy. Rank the data source, strongest first: proprietary (the business created it), product-derived (from its users), user-generated, licensed, public. With a proprietary advantage, PASS and prioritize the family; without one, FAIL. Public data alone is not an advantage; pair it with a field from a higher rank.

A family that fails two or more axes shrinks to one article or drops. A failed family with a real advantage becomes an angle inside a family the market searches.

## AI-answer flag

A query phrased as a definition, a comparison, or a list is a likely AI-answer query. Label the flag `inferred from query form`. The page then needs a direct answer near the top. Whether an AI system answers the query is not observed in this research.
