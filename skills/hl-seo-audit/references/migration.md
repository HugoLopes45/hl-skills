# Migration checks

Read this file when the user plans or reviews a move: a new domain, changed URLs, a platform change, or a section served through a proxy. Use the URL lists the user supplies. Without an old-URL list, write that the redirect map was not checked.

## Before the move

- **Old URL list**: read the crawl export of the old site: each URL with its status, title, canonical, and H1. Finding: no list, or a list that misses pages with search clicks or links. Fix: crawl the old site and include every page that gets search clicks or links.
- **One-to-one map**: check that each old URL maps to one new URL, its closest equivalent. Finding: an old URL with no target, or a changed URL with no 301 redirect. Fix: keep the URL where the new site can serve it; otherwise redirect it, or remove it deliberately with a 404 or 410 status.
- **Homepage catch-all**: check that unrelated old URLs do not redirect to the homepage. Finding: an old URL redirected to the homepage or another unrelated page.

## At the switch

- **Redirects at launch**: check that the redirects are live when the new site goes live. Finding: an old URL that returns 404 while its new URL is live.
- **Canonical host**: check that canonical tags and sitemap entries name the new host. Finding: a canonical or sitemap URL on the old or origin host.
- **Top pages**: check that the pages with the most search clicks or links return 200, with the expected title, canonical, and structured data. Finding: a top page that fails any of these.
- **Sitemap**: check that the new sitemap lists only new URLs, and that the old sitemap stays reachable for a short time so search engines see the redirects.

## After the move

- **Errors**: watch not-found and coverage reports for at least two weeks after the switch (heuristic default), then weekly. Fix each missing redirect as it appears.
- **Clicks by page**: compare clicks per page with the same period before the move. Finding: a drop on specific pages, which usually points to a missing redirect or lost content. Judge a site-wide change after the error watch ends.
- **Internal links**: check that internal links point to the new URLs, not to redirects. Finding: an internal link to an old URL that redirects.

## Proxied section

- **Asset paths**: check that the section's CSS, JavaScript, images, and fonts are routed through the proxy too. Finding: a page whose assets fail to load through the proxy.
- **Analytics and consent**: after the switch, check that the analytics tag and the consent choice work on the proxied host. Finding: either one fails to load or is not honored there.
- **Staging test**: test the routing on a staging host before the switch, then run the Indexing checks on that host. A routing gap found after the switch is a live break.
