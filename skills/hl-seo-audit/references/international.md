# International checks

Read this file when the site has pages in more than one language or region. Check each rule against the search engine's current localization documentation before you recommend a change. Without web access, write that the check was not run.

## URLs and codes

- **Locale URLs**: give each language or region version its own URL. Finding: content changes by IP address or Accept-Language header without a visible language choice. For unpublished locale URLs, prefer a subdirectory such as `/en/` (heuristic default); do not recommend moving a live locale URL for this alone. A language set only in a URL parameter, such as `?lang=`, is a Low finding; check the current localization documentation first.
- **Language and region codes**: read each code in the hreflang values. Finding: a code outside ISO 639-1 (language) or ISO 3166-1 alpha-2 (region), such as `en-UK`, unless the current search-engine documentation allows the value; the region code for the United Kingdom is `GB`. Without web access, write that this check was not run.

## Hreflang

- **Locale set**: read the hreflang set on each locale page. Finding: the page is missing from its own set. Fix: add a self-referencing entry.
- **Reciprocal links**: check that every page in a set is linked back by each other page in that set. Finding: a one-way annotation. Check the current localization documentation for its effect before you call it an error.
- **One URL per pair**: check that each language-region pair names the same URL in every method you use (HTML, HTTP header, sitemap). Finding: one pair points to different URLs across methods. Check the current localization documentation for its effect before you call it an error.
- **Canonical in the set**: check that each page's canonical URL is one of the URLs in its hreflang set. Finding: a canonical outside the set. Check the current localization documentation for its effect on hreflang before you call it an error.
- **Protocol and host**: check that canonical, hreflang, and sitemap URLs use the same protocol and host. Finding: a mismatch between them.
- **Where to use it**: From a supplied search or analytics export by country, read which pages users reach in the wrong language. Without one, write "not measured". Finding: such a page with no hreflang annotation to its language versions. For a large locale set, prefer sitemap annotations; check the current localization documentation before you recommend it.
- **Target status**: request each URL in the hreflang set, when you can fetch them. Finding: a target that does not return 200, is not indexable, or does not match its own canonical. Check the current localization documentation for its effect before you call it an error.
- **Other engines**: check the current guidance of any other search engine before you recommend a `content-language` meta tag next to hreflang; without web access, write that this check was not run.

## Canonical

- **Locale canonicals**: read the canonical on each locale page. Finding: a canonical that names a page in another language, which can keep that locale out of results. Same-language regional duplicates may share one preferred canonical; confirm the intent before you flag one.

## Locale content

- **Translated main content**: read the main text, title, and meta description of each locale page. Finding: main text in another language, or an untranslated title or meta description. Check the current localization documentation for which content sets the page language.
- **Thin locales**: read the main text of each locale page for unique content. Finding: a locale page that repeats the original with only its template text translated. Fix: translate the page fully, or stop publishing it. Do not hide it with `noindex` or a canonical to another language; confirm the intent first.
- **Locale signals**: check that currency, phone format, and addresses fit each locale. Finding: one that does not fit its locale.
- **Scaled translation**: flag a set of translations that add no value under the search engine's current scaled content policy; without web access, write that this check was not run.

## Sitemap

- **Sitemap annotations**: read the `urlset` and each `url` entry when they carry hreflang. Finding: no `xmlns:xhtml` namespace on `urlset`, or a `url` entry that lacks a locale of its set, including the page itself.
- **Sitemap URLs**: check that each URL is absolute, with protocol and host. Finding: a relative URL.
- **Sitemap size**: check the file-size and URL limits in the current sitemap guidance; hreflang entries add bytes to each URL. Finding: a file over a limit. Fix: split it by content type, not by locale. Do not restructure a working sitemap.
