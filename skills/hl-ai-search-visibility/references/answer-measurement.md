# Answer measurement

Read when building the query sample, classifying captured answers, reading repeated runs, or naming delayed outcomes (workflow step 8). An answer capture is one observed answer from one engine, with its prompt, locale, and date.

## Visibility rungs

| Rung | Meaning | How to see it |
|---|---|---|
| Cited | The answer lists the page as a source | Answer captures that show sources |
| Mentioned | The answer names the brand | Answer captures |
| Recommended | The answer puts the brand on the buyer's shortlist | Answer captures, read with the framing |

Report each rung on its own. Retrieval is not a rung: a server-log fetch shows a request, not use in an answer, so report retrieval as `not measured`. A rise in citations with no rise in recommendations is a separate result, not a partial success.

## Cited source kinds

Classify each cited source as a roundup or list, community thread, reference site, review site, marketplace or listing, video, press item, institutional page, competitor page, or the brand's own page. Count the source kinds for each fact family. The dominant kind sets the fix: a roundup, list, or community thread points to that third-party source; a reference site points to that site's facts about the entity; the brand's own page points to that page; for any other kind, the fix lies with its owner.

## Mention framing

- Favorable: the answer presents the brand as a fit for a stated need.
- Neutral: the answer names the brand with no judgment.
- Hedged: the answer names the brand with a caveat that limits the buyer's choice.
- Recommended against: the answer advises the buyer to avoid the brand for a stated need.

Quote the sentence that shows the framing.

## Query sample

- List the facts a buyer needs to answer the target question, such as price, compatibility, location, or evidence. Call each group a fact family.
- Give each fact family one owning page. Use an existing page when it can hold the fact; create a page only where no page holds it.
- Never create one page per query variant. A set of such pages is the scaled-content risk named in the Evidence rules.
- Before the question set, ask each engine "what is <brand>?" and "what is <domain>?". An answer that describes another company is a wrong identity: report it under line 1.
- Give the frozen question set a version number and log each change to it. Compare two runs only when they used the same version.
- For a business that serves several places, write the place into every question, for example "Who is the best [service] company in [city]?"
- For a buying conversation, write one opening prompt and two or three follow-ups in buyer order, and freeze them. Record each turn by rung and framing, or write `absent` when the brand does not appear in it. Report the first turn where the brand is absent.

## Reading results

- Name each business that appears in two or more observed answers, even when the buyer did not ask about it; those are the competitors to compare.
- Before you score a gap, check the category the engine read the question as. A different category is a query-sense finding, not a visibility gap.
- Compare each question across runs as gained, lost, held, or `not measured`. A failed capture is `not measured`, never a loss. Call a loss a pattern only under the trigger in Recurring check.
- Group the prompts by fact family and count appearances per family across runs. For a family the brand loses, record the sources cited and the competitors named.
- For a page in another language, name each gap as translation (the page is missing in that language), information (a fact is missing for that market), or entity (outside profiles describe the brand differently; listing fixes belong to `hl-local-visibility`).

## Recurring check

Use when the owner repeats the same question set over time.

- Look at each frozen question on each engine and language: whether the brand appears, how the answer describes it, which sources it cites, and each wrong fact (claim rows, as in `answer-claims.md`).
- Recommend a change only when the same change appears in two runs in a row (heuristic default), when an answer describes the brand as another company, or when a critical wrong fact appears. Report a critical wrong fact at once, under line 1.
- Stop when the run matches the previous run: report it as stable and recommend no page change.
- After a content refresh, compare the owner's capture of citations taken at publish time with the current one. For each lost question, name the cause only when the captures show it; otherwise write that the cause is unknown and name one check that would show it.
- Compare with the previous run the owner supplies. Send no correction or outreach.

## Delayed outcomes

Name these outcomes as `not measured` unless the owner supplies data:

- Branded search and direct visits to the exposed page, in windows of 1 hour, 24 hours, and 7 days after exposure (heuristic defaults; match the window to the decision).
- A "How did you hear about us?" field with an AI option, and a follow-up question about the prompt the buyer used.

When the owner supplies outcome data, label each result as an observation, an association, or a causal result, and name the design that supports the label: holdout, matched comparison, interrupted time series, or pre/post.

Referral data may undercount AI-influenced visits. Group the AI assistant referrer domains present in the owner's data into one channel; check each assistant's current documentation for whether its visits carry a referrer, and read the channel as a lower bound unless that check shows otherwise.
