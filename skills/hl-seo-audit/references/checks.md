# Audit checks

Each item lists what to read, the rule for a finding, and the evidence to quote. Use the tools you have. Without a fetch tool, use the HTML and exports the user supplied, and mark header checks "not read".

## Indexing

- **Status and final URL**: read the response status and the URL after redirects. Pass: 200 on the intended URL. Finding: 4xx or 5xx, a redirect chain, or a redirect to an unrelated page.
- **Robots meta**: read `<meta name="robots">` and any `googlebot` meta. Finding: `noindex` or `none` on a page intended for search. If intent is unknown, report the exclusion and confirm intent before recommending removal.
- **X-Robots-Tag header**: read it when you have response headers. Finding: `noindex` on a page intended for search; preserve intentional exclusions.
- **robots.txt**: read the rules that match the page path. Finding: a disallow on a page that should rank. A robots.txt disallow stops the crawler from reading a noindex tag on that page, so the page can still appear without its content. Never recommend noindex and disallow on the same URL.
- **Canonical**: read `<link rel="canonical">`. Finding: it points to an error page or conflicts with the intended canonical. Another URL can be correct for a duplicate; confirm the page's live URL and intended canonical before changing it. Search engines treat a canonical as a hint; say so.
- **Sitemap**: when supplied, check that the URL is listed. Finding: the sitemap lists a noindex or noncanonical URL. Absence alone is not an indexing blocker; assess discovery through internal links too.

## Technical

- **HTTPS**: read the URL scheme. Finding: `http://`, or HTTPS pages that load `http://` resources.
- **Primary content in HTML**: check that the main text and links appear in the static HTML. If missing from static HTML, mark rendered content unconfirmed. Call it rendered-only only after observing it in the rendered DOM.
- **Viewport**: read `<meta name="viewport">`. Finding: missing on a page meant for phones.
- **Field speed**: when Search Console or Chrome UX Report data is supplied, compare LCP (2.5 s or less), INP (200 ms or less), and CLS (0.1 or less) with "good". Lab results are labeled lab data.
- **Duplicate URLs**: parameter or trailing-slash variants that serve the same content. Finding: duplicates with no canonical.

## On-page

- **Title**: read `<title>`. Finding: missing, empty, duplicated across pages, or only the brand name. Judge truncation in a search preview; a character count is a rough guide only.
- **Meta description**: read `<meta name="description">`. Finding: missing or duplicated. Search engines may write their own snippet, so rate this Low unless the copy itself is weak.
- **H1**: read the visible `<h1>` elements and the document outline. Multiple H1s are valid; different section labels do not prove competing topics. Without established target intent or a demonstrated outline problem, report the headings as observations, not defects. Do not recommend keeping one H1 or converting another to H2 based on count or different labels alone. A finding needs evidence that the outline misrepresents the content or hides its main topic.
- **Heading order**: read the H2 and H3 sequence. Finding: heading levels chosen for size, not structure.
- **Internal links**: read the anchor text of links into and out of the page. Finding: anchors such as "click here", or no links in or out.
- **Images**: read `alt` on informative images. Finding: missing alt text on an image that carries meaning.

## Content

- **Target match**: read the first screen. It should state what the page is, who it is for, and the answer to its target query. Finding: the page answers a different query.
- **Supported facts**: check each specific claim for a source or a first-party fact the user supplied. Finding: unsourced statistics, rankings, or "best" claims.
- **Expertise signals**: check for an author, dates, and sources on topics that depend on expertise, such as health, money, or law. Search engines describe these signals in their quality guidance; none is a single score.
- **Depth**: judge depth against the query's intent, not word count. Without a target query or established intent, leave adequacy unconfirmed; short copy and multiple headings alone do not establish a content defect.

## AI-answer readiness (GEO)

- **Direct answer**: assess this only when established query intent calls for an answer. With no target intent, mark answer fit unconfirmed: do not rate absent question-led copy as a defect, even Low, or infer snippet or AI effects. Question headings and one- or two-sentence answers are optional formats, not universal search requirements. A finding needs a demonstrated mismatch with the known intent.
- **Checkable facts**: each factual sentence has a number with its unit, a date, or a source. Finding: numbers with no unit or source.
- **Structure**: recommend lists, tables or definitions only where they improve a demonstrated readability problem. Prose alone is not a search or AI-answer defect.
- **Limits**: one page does not show whether AI systems retrieve or cite it. State that limit when you recommend GEO work.

## Structured data

- **JSON-LD in static HTML**: read `<script type="application/ld+json">`. Found: list each type and check that it matches visible content. Not found: write "not in static HTML"; never write "absent".
- **Rendered check**: needed before you claim markup is absent. Ask the user for a rendered-DOM read, or for the output of a rich-results test.
- **Mismatch**: markup describes content the page does not show. Finding: High, because it misleads search engines and readers.
