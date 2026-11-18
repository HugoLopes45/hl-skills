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
- Ads competition and cost per click describe the paid auction, not how hard a keyword is to rank for.
- Keep three states apart. A query that returned no results observed zero for its place and period. A phrase missing from the returned rows is unknown, not zero. A failed request or task is a failure: name it as a gap, and do not repeat a paid call only to fill it.
- Read each status an export reports, at the top level and per request or task, before its rows. A failed task is not an empty result.
- Never write a number the input does not contain. Autocomplete suggestions and "related searches" are ideas, not volume.
- Read the `position` column of a Search Console export as its average position, as given. An average is not a fixed rank: never turn 1.1 into “ranks first.” Distinguish a suggested update from a verified page-content defect; an export alone cannot show what a page says.
- Search Console impressions and clicks are this site's search appearances in that export, for the market it covers. They are not search volume and do not size a keyword's demand.
- Buyer language from reviews, tickets, calls, and community threads is user-provided evidence. Quote short phrases exactly and name the source.
- Each measured figure belongs to one market, language, and place: the one its export or tool used. A results check for a local buyer names the city or region; a national check for that buyer is mislabelled. Never apply a figure from one market to another.
- A figure shown as a floor, such as the lowest reporting tier, is a minimum, not a count. Close variants may come back merged, and geographic panels (metro, county, city) overlap; never add their figures.
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

1. **Scope.** Confirm the product and the buyer from the request or the supplied evidence. Name the decision the buyer makes after searching when known; otherwise mark intent pending. Record the market and language beside each figure; when unknown, write `not stated`. For a local buyer, read the monthly series when the export has one, and do not judge a family on a single month, because demand can be seasonal.
2. **Seed from buyer language.** Use supplied sources first: Search Console queries, then reviews, tickets, calls, communities, then the titles and headings of competitor pages the user supplied, then the user's own list. Collect conversational questions too: full questions from forums, reviews, tickets, and sales notes, and Search Console queries of six or more words (a heuristic default). Drop off-topic, other-market and job-seeking rows before judging the rest, and report how many you dropped. After each publication, add the questions and objections from replies and tickets to the next seed list.
3. **Expand only with supplied modifiers.** Use modifiers that the buyer language or the export shows, such as "alternative", "for teams", "price", or "how to". Mark any other modifier "proposed, not checked".
4. **Group into families.** Group the seeds into topic families. Each family answers one business question; merge two candidate families that answer the same question.
5. **Classify intent.** Infer intent from wording, then check observed search results when available. Record their date, engine and locale. For mixed intent, label the first intent the buyer's words show and note the second. Identify the required content type: an article cannot substitute for a tool, product listing or local service when the evidence calls for one. When supplied AI answers cite outside sources the business is absent from, the first move is getting listed in those sources, not a new page.
6. **Map to pages.** Keywords with the same intent and the same answer share one page. Name one primary keyword per page. A definition family takes one page per term, a glossary index, or one guide; choose by the number of terms and their intent.
7. **Validate and queue families.** Check each family on the four axes in [references/method.md](references/method.md) (Validation). When a Search Console export is supplied, apply the striking-distance screen. When a family is a frame with a slot and the user asks for generated pages, apply [references/page-sets.md](references/page-sets.md) and record its page-set result. Then set its queue label (Decision queue).
8. **Prioritize.** Tie each recommendation to the stated business goal and the offer's actual relevance; traffic alone does not establish value. A service the business cannot deliver is Hold at any volume. Rank by the criteria in [references/method.md](references/method.md): buyer fit, intent, page fit, evidence, and competing results. Label the order `Prioritized` when a measured source supports it, otherwise `judgment only`.
9. **Flag AI-answer queries.** Mark queries phrased as a definition, comparison, or list as likely AI-answer queries, labeled inferred. AI answer behavior is not observed here. Treat conversational questions as a second demand space beside search queries. A family strong in conversational questions and weak in search can be ordered above a high-volume keyword's family when the goal is to be the cited answer; say why. When no volume source exists, label their phrasing `observed phrasing, no volume`.
10. **Play.** For a family the user approves, add its moves to that family's point in plain sentences: the pillar page, the supporting pages, and the outside sources to get listed in. Each move names its target, its evidence, an owner the user confirms, and an acceptance check.

Work breadth first. Give every family a cheap check from the supplied sources. Run deep checks (supplied search results and competitor pages) on at most five families (a heuristic default), and name why each other family was skipped. Without those inputs, write the deep checks as `not checked`.

Before any paid call, state the call count and cost; make no paid call without explicit approval. Batch checks for several keywords into one request.

Read [references/method.md](references/method.md) before seeding families (step 2), grouping them (step 4), and validating and queuing them (step 7). It holds the intent definitions, the striking-distance procedure, and the judgment rubric.

## Output

Reader: a marketer or founder who must choose the next page to write or update. The decision served: which page first, and which primary keyword it targets.

Line 1 is one bold plain sentence that names the first keyword or cluster to act on and its basis. It never opens with a label, verdict word, or number.

Under line 1, in plain sentences: which figures are measured, which are not measured, and whether the order is judgment only.

Use one numbered point per cluster, ordered by queue label (Act now, then Act next, then Hold, then Drop) and then by the criteria in [references/method.md](references/method.md). Start with a bold plain sentence. Include the primary keyword, searcher's goal, page to write or update, and figures with their basis. Name each validation result in plain words: passes, fails, or not checked. State each point's confidence in its sentence: high when demand shows in both search and conversational questions and competitor results were checked and passed; low when no demand shows in either space; medium otherwise. Give each point its family's queue label (rules in [references/method.md](references/method.md), Decision queue). Use a table only for up to 5 clusters and 3 short fields; do not repeat it in prose.

Queue labels, in plain words: Act now means act first; Act next means act after the observation named in its point; Hold means wait for the unlock named; Drop means do not pursue.

A refresh of a supplied earlier output re-checks its Act now, Act next, and Hold families. Report what moved as new, moved, dropped, or no movement.

Before the verdict, close with `Sources and assumptions`: the data sources, their date ranges, market and language, the baseline recorded before a family's first move, and what the reader should confirm, at most 10 lines. When the oldest source is a month old or older (a heuristic default), add one refresh step to Next.

Verdict words:
- `Prioritized`: the order rests on a measured source.
- `Judgment only`: no measured figures; the order rests on stated judgment.
- `Stopped`: no product or buyer, and no supplied evidence names them.

For a page-set family, state its result in a plain sentence in its point: build the set as listed; build a narrower set, naming the rows kept; do not build it and write a few editorial pages; or not decided yet, naming the check that did not run. Do not print a label.

Put `Verdict: <word>` on its own line just before `**Next:**`. Each Next line is one action a person can take now, in order.

Stopped: line 1 says what is missing and why it blocks the research. Then `Verdict: Stopped`. Next holds the grouped questions, each with its default (or `Default: none` for a fact) and what it changes.

Reader rules:
- Define each term once at first use: intent (what the searcher wants), cluster (keywords one page can answer), family (clusters that answer one business question), striking distance (average positions 5 to 20, close to page one), SERP (the search results page), volume (monthly searches, from a tool).
- Show a keyword only with its figures and their basis, or with `not measured`.
- No hype and no promised rankings.

Example (signature only; the domain is not a fixture):

````markdown
**Write the descaling guide first: your site already ranks at average position 9.4 for "espresso machine descaling".**
The order rests on that one row of your Search Console export; the other two figures are not measured.

1. **A descaling guide answers how to clean the machine.**
   Target "espresso machine descaling". Your Search Console export records average position 9.4 and 120 impressions for this query. That supports checking this page first, not a predicted gain. The demand signal passes: the export shows 120 impressions. Competitor results are not checked: you supplied no results page. Monthly search volume is not measured. Confidence is medium: one search row shows demand.
   Queue: Act now.
2. **The product page serves people looking to buy descaling tablets.**
   Target "descaling tablets". Its figures are not measured, so whether new copy is needed remains unconfirmed. Validation not checked: the export has no row for this phrase. Confidence is low: no figure supports it.
   Queue: Act next, after the guide's average position is measured in the export.
3. **A comparison page can explain the choice between descaler and vinegar.**
   Target "descaler vs vinegar". Its figures are not measured; this is a proposed page, not a measured opportunity. Validation not checked: the export has no row for this phrase. Confidence is low: no figure supports it.
   Queue: Act next, after the export records a figure for this query.

**Sources and assumptions**
- Search Console query export: query, clicks, impressions, average position, and page columns. Date range, market, and language not stated.
- Measured baseline, before the first move: average position 9.4, 120 impressions, and clicks not stated for "espresso machine descaling", one row of the export. Striking-distance screen: 1 flagged of 4 rows.
- Not measured: "descaling tablets" and "descaler vs vinegar".

Verdict: Prioritized

**Next:**
1. Export the query report from Search Console for the last 3 months, with query, clicks, impressions, average position, and page columns, and send it to me.
2. Confirm the export's date range, market, and language before acting on the position.
3. Write the descaling guide with the buyer phrases from your support tickets, then publish it.
4. Re-check the guide's average position in the same export 2 weeks after publishing (heuristic default), and compare it with the baseline of 9.4.
````

## Stop conditions

- No product or buyer, and no supplied evidence that names them: Stopped. Ask for both in one round, with what each changes in the list.
- Market or language unknown: proceed. Record it as `not stated` beside each affected figure. Ask only when the answer changes a figure or the page.
