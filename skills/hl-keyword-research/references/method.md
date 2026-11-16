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
2. Buyer language: reviews, support tickets, sales calls, community threads.
3. Competitor pages the user supplied: their titles and headings only.
4. The user's own keyword list.

Record the source of each seed. A seed with no source is `proposed, not checked`.

## Intent

| Intent | The searcher wants | Page type |
|---|---|---|
| informational | to learn how or what | guide, glossary entry |
| comparison | to choose between options | comparison, alternatives page |
| transactional | to buy, sign up, or book | product, pricing, or sign-up page |
| navigational | to reach a known brand or product | brand or product page |

Assign one intent per keyword. When a keyword mixes two intents, the first intent the buyer's words show wins; note the second.

## Clustering

- One primary keyword per page.
- Keywords share a page when the same answer satisfies both and the intent matches.
- Give a keyword its own page only when its intent differs from the page it would otherwise join.
- Propose a pillar page with supporting pages only when the site has, or the user plans, the pillar. Label it `proposed`.

## Prioritization

Order clusters by these criteria, in this order, and state the basis of each:

1. **Buyer fit**: the phrase names the buyer's problem in the buyer's words.
2. **Intent closeness to purchase**: for a product that sells, transactional and comparison rank above informational.
3. **Page fit**: an existing page already answers the phrase (update), no page does (new page), or the page the export names answers another query (check before updating).
4. **Evidence**: measured figures from a supplied export, with their period and market, count as measured evidence. Few impressions or clicks make a figure weak evidence. Without measured figures, use buyer language the user supplied.
5. **Competing results**: only when the user supplied the results page. Otherwise write `not checked`.

The result is an order, not a score. Do not invent a formula that produces numbers.

## Striking-distance screen (optional)

Use this heuristic only when a Search Console export is supplied. Average positions 5 to 20 flag queries close to page one. The band does not prove an opportunity, and it never excludes a row by itself: a row outside it still counts when it fits the product and a page.

1. Read the columns: query, clicks, impressions, position, and page when present. The `position` column is the average position. A missing column is `not in export`.
2. Flag rows whose average position is from 5 to 20, inclusive.
3. Sort the flagged rows by impressions, highest first, then by clicks.
4. Match each row to the page the export names. A row with a matching page is an update candidate; check its fit first. A row with no matching page is a new-page candidate.
5. Report how many rows you flagged out of all rows, for example "4 flagged of 7".
6. Label the figures `Measured (Search Console export)`. Do not call impressions search volume.

## AI-answer flag

A query phrased as a definition, a comparison, or a list is a likely AI-answer query. Label the flag `inferred from query form`. The page then needs a direct answer near the top. Whether an AI system answers the query is not observed in this research.
