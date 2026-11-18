# Area checks

Read the section for each area you check. Each check names the record it needs; without that record, the status is `unknown`.

## Business listing profile

- Name: matches the trading name in the business's own records. Flag extra search terms, service lists, or places in the name.
- Address: the place where customers visit. Flag an address the business does not occupy, a virtual office, or a home address published where customers do not visit.
- Service area: the places the business serves. Flag an area it does not serve.
- Category: describes the services delivered. Flag a category for a different kind of business.
- Phone and website: the number customers use and the page for this location. Flag an old number, or a generic homepage where a location page exists.
- Hours: match the recorded hours. Flag a conflict.
- Status: flag unverified, suspended, closed, or duplicate listings.
- Links: check that the website link carries a campaign tag (a tracking code in the link's address), and that every button works. Also check whether calls from the listing can be told apart from other calls in the supplied records.
- Posts: give each post one action button. Check the platform's current post rules and name the document.

Check each platform's current eligibility, hidden-address, and category rules, and name the document. Write `unknown` when you did not check it.

Route a near-me query to business-profile work (name, categories, hours, service area), not to a content page.

## Name, address, and phone

- Source of truth: one row per location with its trading name, public address, public phone, website URL, owner, and date.
- Compare each listing and directory row with the source. Classify each value as `matches`, `differs` (quote the value), or `unknown` (no value in the record).
- Not conflicts: abbreviations such as "St" and "Street", punctuation, and a legitimate branch or department number. Name each such number once.
- Priority: a number or address that sends customers to the wrong place first, then duplicate listings, then the rest. For each duplicate, check the review export for reviews split across its listings; write `unknown` without an export.
- Duplicates: merge only through each platform's supported process. List each duplicate with its listing row.

## Reviews

- Send requests to every genuine customer who reaches a defined experience milestone. Set eligibility before anyone reads the feedback.
- Ask past customers once, in small batches spread over weeks, never in one burst. Check the platform's current review policy first.
- The person on site makes the ask at the end of the job. Walk-in businesses add a scannable link or a counter card to the ask.
- Offer no incentive, reward, or discount for a review. Do not ask for a rating or for particular words.
- Use a neutral request with the link for the correct location. Draft:

  > Thank you for choosing [business]. If you would like to share your experience, you can leave a review here: [location review link]. Your honest feedback helps us improve.

- Do not ask for removal of a genuine critical review. Check the platform's current review policy for removal, and report a suspected rule breach through the platform's process.
- Replies: thank or acknowledge the customer, answer the point, and offer a private route for details. Keep names, health, money, and job details out of public replies. Do not dispute a customer's facts in public.
- A health business's reply never confirms that the reviewer was a patient or visited.
- After reporting a suspected fake review, draft one short neutral reply for the owner to post.
- Count reviews, average rating, and replies per location with the date range. Write `unknown` for any count the export lacks.
- List each low-rating review with no owner reply, using the low-rating level the owner sets. Record the date of the newest review.
- Record each review you keep: URL, date, platform, and exact text. Separate the reviewer's claim from checked facts. Name an owner and a status.
- Reuse a quote only with recorded permission, allowed channels, disclosure, and an expiry date. Never merge quotes. Never imply a platform badge.
- Legal review and testimonial rules go to the owner's adviser.

## Location and service-area pages

- Each page shows its address when the business operates there, or the service area it covers; hours; phone; services offered there; a booking or enquiry path; and evidence specific to that place, such as a job or team photo used with permission.
- A town gets its own page only when the records show all of: the business serves it, demand and recurring jobs there, one local condition that changes the job, and a first screen that differs from sibling pages.
- Before writing a town page, state in one line what it has that its sibling pages lack. Give each other town one line on the location index.
- Before a page claims work in a service or place, count its paid jobs per service after merging duplicate records. Grade each proof as a record, a note, or a review.
- A service-area page names the area served. It shows no street address the business does not occupy.
- Doorway test: if the page reads the same with another place name, it is a doorway page. Merge it, or add facts that differ for that place.
- Check the search engine's current doorway-page rule and name the document. Write `unknown` when you did not check it.
- Each page is linked from its location index and from the relevant service page. Write `unknown` for a link the export does not show.
- Crawling, indexing, and redirects belong to `hl-seo-audit`. Structured data for the page belongs to `hl-schema-markup`. Keyword choice for the page belongs to `hl-keyword-research`.

## Map results and local questions

- Read map results from supplied records only. Record the query, place, date, and device of each map check.
- A map check that fails or lacks a record is `unknown`, never "not ranking".
- Where supplied records show a map pack above the organic results, note which queries it takes clicks from; write `unknown` without click records.
- Compare the listing with the three top map-result rivals (heuristic default) on category, review pace, newest review age, reply rate, unanswered low reviews, photos, posts, hours, services, and landing page. For each rival, record its map position for the buyer's search, with place and date, and whether it shows prices. Write `unknown` for any figure the records lack. State the review window used for the reply rate.
- List the questions a local buyer would ask an AI assistant, including one from a buyer who needs the service today. Record each supplied answer, from an AI assistant, a map assistant or a listing page, with its date and query; otherwise write `unknown`.

## Lead response path

- Map each channel (call, form, listing message, booking, email) to one role and its first human reply.
- Measure per channel from arrival in the record to the first human reply. Count the leads with no reply, with the total.
- A lead with no time stamp is `unknown`. Do not estimate its reply time.
- Name who covers leads that arrive outside opening hours. The owner sets the cover.
- Stage definitions and scoring belong to `hl-lead-lifecycle`.

## Questions for the owner's adviser or the platform's current rules

- Consumer rules on reviews and testimonials in each country where the business trades.
- Advertising rules that require a license number or a disclosed term.
- Consent rules for calls and texts sent to customers.
- Data protection for lead records and review data.
- Platform listing eligibility, hidden addresses, categories, and review policy: check the current official document.
