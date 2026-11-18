# Profile method

Use this file for the profile layout. The evidence rules and output are in `SKILL.md`.

## Groups

For a market-wide analysis, build the consideration set from buyers' observed alternatives, including doing nothing. A seller's rival list is a hypothesis until supported by buyer evidence. For a named-rival comparison, respect that scope and note missing consideration evidence without expanding it. Sort the selected alternatives into three groups before profiling:

1. **Direct**: sells the same outcome to the same buyer.
2. **Indirect**: solves the same problem another way, such as a different product type or a service.
3. **Status quo**: what buyers do now without a vendor, such as a spreadsheet or a manual process. Profile it from buyer evidence, not from a competitor's pages.

## Profile layout

Use the same fields for every profile so the profiles can be compared side by side. Omit the fields of dimensions out of scope.

```text
Name: [competitor or alternative]
Group: direct | indirect | status quo
Sources: [name, capture date] for each source
Company (observed): [founding year, headquarters, team size, and funding, each with its source and date; or unavailable]
Offer (observed): [what is sold, as the source states it]
Integrations (observed): [count and main integrations, with source and date; or unavailable]
Fit (observed): [best for and not ideal for, as the source states each, with its source; or not observed]
Positioning (observed): [headline, subhead, and primary CTA label, quoted verbatim; or first claim]
Proof (observed): [logos, counts, testimonials, review badges, each with its source]
Price (observed): [each price string verbatim, with currency and tax basis as shown; or unavailable]
Terms (observed): [trial length, annual-only, seat minimums, usage meters, support terms with response times, where "contact sales" appears; or unavailable]
Switching (observed): [what transfers from the buyer's current setup and what needs rework, with its source; or unavailable]
Plan gates (observed): [features locked to each tier, and the free features, each with its source]
Pages (observed): [secondary pages that name a segment or compare with a rival, with URL; each page family (pages sharing a URL pattern, such as /compare/) with its earliest archived date, and each removed page family or partner listing, dated]
Channels (observed): [where it advertises or sells; each ad's hook quoted verbatim, its format, and the first and last date seen; paid placements outside ad libraries that the placement itself labels as paid, such as sponsorships, coupon listings, and affiliate links, each with its placement, offer or code, and date seen]
Lead magnets (observed): [format, gating depth, location, and any free tool, each with its source]
Strengths (observed): [each with its source]
Weaknesses (observed): [each with its source; no weakness without a source]
Reviews (observed): [complaints and praise, each with its count, window, source, and verbatim wording; switching posts about the rival, each dated; `unavailable` (not searched) where the host cannot search]
Roundups (observed): [roundups or comparison pages captured in this session that name the rival, with URL and capture date; or not observed on the pages read]
Metrics: [each metric with its tool, window, and date, or unavailable: organic keywords in the top 10, referring domains with their trend, top organic pages by estimated traffic, and public counters the rival publishes (community members, listing installs, package downloads); release counts for a window and the same window before it (heuristic default: 90 days), counting only releases that change the product]
Hiring (observed): [open roles counted by function, each dated by its first posting, and the plan each full job post states; or unavailable]
Inferred: [each inference with its confidence and the fact it rests on; each infrastructure or paid-placement signal with its date, until a second source confirms it; for pricing, a top-tier gate suggests what top payers value, a free feature suggests little price weight, and a usage meter suggests cost exposure]
Threats (inferred): [areas where the rival improves or enters the user's offer, each with its confidence and the dated fact it rests on]
Implications: [questions or options for the user's business; for a table-stakes claim, propose only a specific, checkable differentiator; for an over-bought hook, an adjacent angle to test]
Moves (observed): [each change in offer, price, page, or channel, with its date and source; or `unavailable` (one capture)]
Gaps: [each dimension with no source, and its last check date]
```

Do not write battle cards; suggest `hl-sales-enablement` in Next, with each fact's last-verified date.

## Rules

- Give each fact a last-verified date: the capture date of its source, or a later date on which you checked it against that source.
- Re-capture a page before you call its content current. A single capture supports only "as of its date".
- Keep one profile per rival as the only source of its facts in any page, deck, or battle card. When a fact changes, update the profile, then list each document that uses it for the owner.
- Keep the status quo profile short. Its facts come from buyer evidence, with the source named.
- A strength or weakness that is not observed in a dated source is an inference. Move it to the inferred line.
- Price is recorded as shown. Do not convert currency or add tax unless the source states the basis.
- Record each price, tier, or trial change as a delta: from [value] on [date] to [value] on [date], with the URL.
- Hidden pricing (`contact sales` only) stays `unavailable`; record pricing complaints from reviews under Reviews, each with its count, window, and source.
- Compare price floor and ceiling across profiles. A recent discount or cheaper tier is an observed dated delta; any reading of it as a price move is an inference to test, not a finding.
- Treat a claim as strategy only when it repeats across the headline, ads, pricing header, or other surfaces. Do not build a counter-position on a claim that appears on one surface.
- Copy that names no audience on the pages read is recorded as `no audience named as of [date]`, not as a broad strategy.
- Compare each ad or headline claim with the page it sends buyers to. A claim the page omits, or reviews contradict, is recorded as an inferred mismatch, with its confidence.
- Read each headline's history across captures. A headline unchanged across captures is observed as stable; each change is recorded as a dated delta. Several changes in a short span is an inference of an unsettled message, with its confidence.
- Weigh each complaint by recurrence, recency, and the reviewer's tier, and keep the reviewer's wording verbatim. Sort a complaint as structural when fixing it would change the rival's price or product model, and as fixable otherwise; record the sort as an inference.
- Count a complaint theme only with five or more 1-2 star reviews across more than one month (heuristic default).
- Quote reviews without the reviewer's name, handle, or photo. Profile the company, not its staff, customers, or reviewers.
- Compare review pace over the same window and count each review once, recording the window and source. Rank by pace, not total count; a large total with a falling pace is an inference to test, not a finding.
- Praise that comes despite a flaw marks an inferred opening; record it with its quote and its confidence.
- List angles that reviews or organic pages raise but no rival runs as a paid hook. Label each as a hypothesis.
- Propose a complaint-based differentiator only where the user's business already delivers it.
- Classify each hook as direct, question, proof, or contrarian, so hooks compare across rivals. A hook that every rival runs is over-bought; do not counter it with the same claim louder. Name a hook or content pattern for a channel only from 24 or more items posted at least 10 days earlier (heuristic defaults); below that, list the items without a pattern. Rank items only within one channel.
- For one channel that meets the 24-item floor above, compare the top and bottom thirds of items ranked by a measure the source shows, such as views, on each trait you counted, such as hook type or format. Describe a thumbnail or cover only after you open the file; otherwise state that you did not open it.
- Keep a dated move log per rival in the Moves line. Group moves on one area inside one window (heuristic default: 90 days) into a cluster, a roadmap hint recorded as an inference with its confidence, never as a cause.
- Record a public growth claim, including a leader's statement, under Proof as reported, with its date and quote; test it as a scale claim. Do not profile the leaders.
- Read a rival's growth or decline only from two or more dated signals together, recorded as an inference with its confidence; state the change in the signals, never that the rival is failing.
- For a lead magnet, infer the funnel stage it covers from its format and gate depth. Record it as an inference with its confidence, citing the capture.
- Model memory is not evidence here. A rival missing from the roundups read is a flag to check live, not a finding of weakness.
