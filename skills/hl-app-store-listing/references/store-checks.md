# Store checks

Read this file before judging any listing field. Each line is a check against the store's current document. This file names what to check, not the limits; the store document holds the limits. When the store document and this file differ, the store document wins. Mark each check `Checked` only when the supplied store document states it.

## Title and name

- Check the length limit and the unit it counts in, characters or bytes.
- Check the name rules: emoji, capital letters, performance or call-to-action wording, and other apps' names or trademarks.
- Check that the name matches the app's real name as the store requires.
- A brand-only title passes only with store data showing users search the brand first.

## Subtitle or short description

- Check the length limit and the unit it counts in.
- Check the rules on performance claims, calls to action, and testimonials, including whether testimonials need an attributed source.
- Check whether words repeated from the title add reach.

## Keyword field

- Check whether the store has a hidden keyword field at all. If it does not, skip this section.
- Check the separator format and the limit unit.
- Check that each term names something the app does. Remove terms for features the app lacks.
- Check that the field holds no other app's name, competitor brand, or trademark.

## Long description and promotional text

- Check whether the store indexes the long description. If it does not, judge it for conversion only.
- Check the formatting the store accepts.
- Check whether promotional text is indexed and whether the owner can edit it without a new release.
- Check that "what's new" describes a change the current build contains.

## Screenshots, previews, and icon

- Check the count and size per device.
- Check whether captions are indexed.
- Check that the first screenshots show the main use on a real app screen, one message per caption.
- Check the preview rules: length, count, autoplay behavior, and the content allowed, and whether the opening must work without sound.
- Do not assume autoplay exposure or a conversion lift from a video. Test the video instead.
- Check the icon and feature graphic rules: allowed text and claims.
- Check that every screenshot, caption, and preview shows the app as built, not a planned feature.

## Review prompts and responses

- Check how often the store allows a review prompt and whether the store controls its display.
- Check the rules on custom buttons that request reviews.
- Check whether the prompt appears for every eligible user at the same point in the flow.
- Check the rules on responses: whether they must state only facts the app shows.

## Localization

- Check each supplied market's fields in its own language, against its own limits.
- Re-trace each claim in each language to a supplied fact.
- Check that translated captions describe the screens they label.
- A market with no supplied text is out of scope.

## Variant pages and in-app events

- Where the store offers variant pages, check the count limit and which fields each variant changes.
- Each variant states only claims the app build shows.
- Check the rules for in-app events or promotions: display, duration, and the required content.
- Event metadata must match the event's real name, dates, and content.

## Listing tests

- Check which elements the store lets the owner test.
- Check the current limits on the number of variants, duration, concurrent tests, and the metric the store reports.
- Check the population the store tests. Leave sizing and decision rules to `hl-ab-test-plan`; name it in Next.

## App stability

- Check the crash, freeze and not-responding rates in the supplied store metrics against the thresholds in the store's current document. Mark the check `Not checked` when any of them is missing.
- A rate over its threshold is a finding: name it in the output with its evidence, `Measured` when the export is dated and named.

## Privacy and policy disclosures

- Check that the privacy labels and data disclosures match the app's real data use, as the owner's supplied data inventory states it.
- Legal wording goes to the owner's adviser.

## Competitor listings

- Use only competitor listings the owner supplied. Fetch nothing.
- Compare field by field: the words in each title, the message of the first screenshot, and the review prompt's logic.
- A keyword gap is a hypothesis until the store's own search data shows it.
- Do not copy a competitor's claims, names, or screenshots.
