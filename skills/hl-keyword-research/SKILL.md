---
name: hl-keyword-research
description: "Choose search keywords and topic clusters for any product, site, or market from buyer language, Search Console exports, or tool exports. Labels each figure by its source and never invents search volume or difficulty. Use when the user asks which keywords to target, what page to write next, or how to group keywords into pages."
---
# Keyword Research

Input: `[product or topic] [buyer] [language and market, when they change the figures or page] [Search Console or tool export, optional]`

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

## Evidence rules

- Search volume, keyword difficulty, cost per click, and trend data come only from a tool export or the user. Label each as `Measured` (name the tool or export) or `User-provided`. A figure with no source is `not measured`.
- Never write a number the input does not contain. Autocomplete suggestions and "related searches" are ideas, not volume.
- Read the `position` column of a Search Console export as its average position, as given. An average is not a fixed rank: never turn 1.1 into “ranks first.” Distinguish a suggested update from a verified page-content defect; an export alone cannot show what a page says.
- Search Console impressions and clicks are this site's search appearances in that export, for the market it covers. They are not search volume and do not size a keyword's demand.
- Buyer language from reviews, tickets, calls, and community threads is user-provided evidence. Quote short phrases exactly and name the source.
- Each measured figure belongs to one market and language: the one its export or tool used. Never apply a figure from one market to another.
- Platform search (for example a web search engine, social platform or app store) uses the same method with that platform's own data. Its figures come only from that platform's export.
- A keyword list is a hypothesis about demand. Before scaling a cluster, the business must observe a result: clicks, signups, or sales.

## Intent

- Act directly when the request names the artifact, its scope, and its depth. A narrow question gets a narrow answer, not the full workflow.
- Ask in focused rounds when essential context is missing (see Stop conditions). Group related questions in one message, and ask again when an answer raises a new decision. Do not cap the number of rounds.
- A clear, limited request proceeds on the supplied evidence. Label each inference from that evidence.
- Missing non-essential context does not stop the research. Deliver the part that does not depend on it, and name what is pending.
- Reuse what the user already supplied. Do not ask for it again.
- Explain each question's consequence in one line. Give a default only for a choice the user can accept, such as an output format. For a fact (product, buyer, goal, market, proof), write `Default: none`; never presume it.
- Do not invent a market, audience, goal, or proof.
- An exact output format the user names (JSON only, one table) replaces the default wrapper. Evidence, permission, and safety rules still apply inside it.

## Workflow

1. **Scope.** Confirm the product and the buyer from the request or the supplied evidence. Name the decision the buyer makes after searching when known; otherwise mark intent pending. Record the market and language beside each figure; when unknown, write `not stated`.
2. **Seed from buyer language.** Use supplied sources first: Search Console queries, then reviews, tickets, calls, communities, then the titles and headings of competitor pages the user supplied, then the user's own list.
3. **Expand only with supplied modifiers.** Use modifiers that the buyer language or the export shows, such as "alternative", "for teams", "price", or "how to". Mark any other modifier "proposed, not checked".
4. **Classify intent.** Infer intent from wording, then check observed search results when available. Record their date, engine and locale. Note mixed intent rather than forcing one label. Identify the required content type: an article cannot substitute for a tool, product listing or local service when the evidence calls for one.
5. **Map to pages.** Keywords with the same intent and the same answer share one page. Name one primary keyword per page.
6. **Prioritize.** Tie each recommendation to the stated business goal and the offer's actual relevance; traffic alone does not establish value. Rank by the criteria in [references/method.md](references/method.md): buyer fit, intent, page fit, evidence, and competing results. Label the order `Prioritized` when a measured source supports it, otherwise `judgment only`. The striking-distance screen is optional.
7. **Flag AI-answer queries.** Mark queries phrased as a definition, comparison, or list as likely AI-answer queries, labeled inferred. AI answer behavior is not observed here.

Method details, intent definitions, the striking-distance procedure, and the judgment rubric are in [references/method.md](references/method.md).

## Output

Reader: a marketer or founder who must choose the next page to write or update. The decision served: which page first, and which primary keyword it targets.

Line 1 is one bold plain sentence that names the first keyword or cluster to act on and its basis. It never opens with a label, verdict word, or number.

Under line 1, in plain sentences: which figures are measured, which are not measured, and whether the order is judgment only.

Use one numbered point per cluster, in priority order. Start with a bold plain sentence. Include the primary keyword, searcher's goal, page to write or update, and figures with their basis. Use a table only for up to 5 clusters and 3 short fields; do not repeat it in prose.

Verdict words:
- `Prioritized`: the order rests on a measured source.
- `Judgment only`: no measured figures; the order rests on stated judgment.
- `Stopped`: no product or buyer, and no supplied evidence names them.

Put `Verdict: <word>` on its own line just before `**Next:**`. Each Next line is one action a person can take now, in order.

Stopped: line 1 says what is missing and why it blocks the research. Then `Verdict: Stopped`. Next holds the grouped questions, each with its default (or `Default: none` for a fact) and what it changes.

Reader rules:
- Define each term once at first use: intent (what the searcher wants), cluster (keywords one page can answer), striking distance (average positions 5 to 20, close to page one), SERP (the search results page), volume (monthly searches, from a tool).
- Show a keyword only with its figures and their basis, or with `not measured`.
- No hype and no promised rankings.

Example (signature only; the domain is not a fixture):

````markdown
**Write the descaling guide first: your site already ranks at average position 9.4 for "espresso machine descaling".**
The order rests on that one row of your Search Console export; the other two figures are not measured.

1. **A descaling guide answers how to clean the machine.**
   Target "espresso machine descaling". Your Search Console export records average position 9.4 for this query. That supports checking this page first, not a predicted gain. Monthly search volume is not measured.
2. **The product page serves people looking to buy descaling tablets.**
   Target "descaling tablets". Its figures are not measured, so whether new copy is needed remains unconfirmed.
3. **A comparison page can explain the choice between descaler and vinegar.**
   Target "descaler vs vinegar". Its figures are not measured; this is a proposed page, not a measured opportunity.

Verdict: Prioritized

**Next:**
1. Export the query report from Search Console for the last 3 months, with query, clicks, impressions, average position, and page columns, and send it to me.
2. Write the descaling guide with the buyer phrases from your support tickets, then publish it.
3. Measure the guide's average position in the same export after the next crawl, and compare it with the recorded position of 9.4.
````

## Stop conditions

- No product or buyer, and no supplied evidence that names them: Stopped. Ask for both in one round, with what each changes in the list.
- Market or language unknown: proceed. Record it as `not stated` beside each affected figure. Ask only when the answer changes a figure or the page.
