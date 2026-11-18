# Site Launch QA

Use before a site launch, redesign, or migration goes live, and before any new section that changes the site's public pages. Product launches fail quietly when the site underneath breaks, and these failures are often invisible from the homepage.

Run three passes: before the switch, at the switch, and in the first two weeks after it.

Suggest running `hl-seo-audit` for search visibility (indexing, titles, canonicals, sitemap, structured data); this file does not check them.

## Before the switch

Content and links:

- Every planned page exists with final copy: no placeholder text, test prices, or "TBD".
- Crawl the staging site for broken internal links and missing images.
- Legal pages (privacy, terms, cookies) are present and current.
- Prices, plan names, and contact details match what sales and support say.
- For a migration: the redirect map is loaded and tested on a sample of old addresses.

Forms and conversions:

- List every form for the owner to submit with a test entry, and check that each reaches the inbox or tool it should.
- Confirmation messages and redirects work, and spam protection does not block real entries.
- Conversion tracking counts the confirmed submission, not the button click.
- Analytics is installed once per page, with internal traffic filtered out. Consent settings govern the tags.

Performance and access:

- Key page templates meet the page-speed and layout-stability measures the search engine documents, on mobile.
- Pages work on mobile and in the in-app browsers of the social apps your buyers use.
- Images have alt text, forms have labels, and keyboard navigation works.
- Social-share previews show the right title and image when a URL is shared.

Rollback:

- Know how to roll back on your host, and have the owner rehearse the rollback once before launch.
- For a DNS change, have the owner lower the record's TTL (how long resolvers cache it) a day before the switch (heuristic default), so a rollback takes effect quickly.

## At the switch

- The owner deploys redirects in the same step as the new site; check that they are live.
- Confirm HTTPS works on each hostname, with and without `www`, and that one redirects to the other.
- Load the highest-traffic pages and check content and status.
- The owner submits one real form; check that it arrives everywhere it should.

## The first two weeks

- Watch crawl errors and 404s daily in the first week, then weekly; list the missing redirects for the owner to add as they appear.
- Compare traffic and conversions to the same period before, page by page, not only in total.
- Confirm conversions arrive in each paid channel at the expected rate.
- List internal links that still point to redirected addresses for the owner to fix.
- Collect the bugs the team and customers report, and decide which are urgent.
- If a data source fails or stops updating, report its data as stale and do not infer a trend from it.
