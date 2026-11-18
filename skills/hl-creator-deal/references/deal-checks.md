# Deal checks

Use only supplied evidence. Name each source, its date range, and its count.

## Fit checks

| Check | Supplied evidence | What it decides |
|---|---|---|
| Audience match | audience location, age or role, comment questions | whether the audience is the buyer |
| Post sample | post dates, count, format | what the sample can describe |
| Sponsored record | sponsored posts in the sample and their results | how promotions compare with the creator's other posts |
| Brand conflict | competitor or off-brand posts in the sample | whether a conflict blocks the deal |
| Unprompted mention | posts that name the category without a brief | whether the creator already fits |

## Channel and newsletter checks

Use for a paid post in a messaging channel or a sponsored newsletter issue. Use the channel's supplied history only.

1. **Reach.** Take the median views of posts at least a week old (heuristic default) and divide by the subscriber count. Compare the result with channels of the same size, topic, and language only when the user supplies that comparison with its source and scope.
2. **Activity.** From the supplied post dates, find the longest gap between posts. A gap over 30 days (heuristic default), or no post in the 30 days before the latest supplied date, is red flag 9.
3. **Ad load.** Count the ads per day among the supplied posts from the last 30 days (heuristic default). The owner's post competes with the other ads published that day, so the owner chooses a publish day with fewer ads.
4. **Ad contact.** If the supplied channel description names an ad contact who sells placements on other channels, ask whether those channels share the audience before the owner prices a bundle on combined views.
5. **Admin statistics.** Ask for the channel's own statistics for the last 30 days (heuristic default). A refusal is red flag 8.
6. **Cost per thousand past views.** Cost per thousand past views = supplied price ÷ median views from check 1 × 1,000. It describes past posts, not this placement.
7. **Repeat placement.** Read each earlier placement before the owner rebooks: its date, angle, clicks, and signups. Do not repeat an angle sent to the same list recently (heuristic default: 30 days).
8. **Newsletter clicks.** Count a click only when a supplied analytics session matches it; label the rest `unverified`.

## Red flags

A red flag is a question to answer before any offer. It is not proof of fraud.

1. A jump in followers or views that no post or campaign explains.
2. Comments that repeat across posts or ignore the post's topic.
3. A post's views, likes, or comments under half the median of posts with the same format in the sample (heuristic default; the owner may set another cut-off).
4. Audience location or language that differs from the creator's stated market.
5. A sponsored post in the sample without a disclosure label.
6. A product claim in the creator's posts that the supplied evidence cannot back.
7. Audience data with no source or no date.
8. A refusal to share the channel's own statistics.
9. A long silence in the channel's supplied post dates.

## Disclosure check

1. List each material connection: payment, free product, commission, gift, trip, discount, or a personal tie.
2. For each market where the audience sits and each platform in the deal, read the current official guidance in this session. Record its title, its URL, and the date you read it. If you cannot read it, write `unverified: <market or platform>`.
3. Compare the brief's wording and placement with that guidance. Check whether the disclosure sits in the post where a viewer sees it before engaging, whether a video says it aloud, whether the platform's paid-partnership label applies, and whether the rule covers free product.
4. Check the draft before go-live and the live post after it ships. Record the date and the link.
5. Give these questions to the owner's adviser. The skill does not answer them: who is liable, which wording counts, whether the brand must monitor posts, how cross-border and regulated categories apply, and the contract terms for disclosure, usage rights, and stop or rework.

## Payment options

| Option | Pays for | Needs before a number |
|---|---|---|
| Product only | the product, no fee | the product's cost and the owner's margin on it |
| Flat fee | one post or a fixed set of deliverables | the target cost per qualified outcome and the expected qualified outcomes |
| Commission on tracked sales | each tracked sale | the margin per sale after refunds, and tracking |
| Hybrid | a flat part plus commission | the inputs of both the flat fee and the commission |
| Performance share | a share of media spend or revenue behind the creator's posts, with an optional monthly minimum paid only when a set quota is met | the share rate, per-post spend or revenue reports, and usage rights in writing before the first post |

Formulas, with the owner's inputs only:
- Flat fee ceiling = target cost per qualified outcome × expected qualified outcomes. Take the expected qualified outcomes from the creator's supplied sponsored results or the owner's own test. With neither, write `[PLACEHOLDER: owner sets the fee]`.
- A commission per sale above the margin per sale after refunds loses money on each tracked sale.
- Performance share = owner's share rate × media spend behind the creator's posts (or × revenue, when revenue is the basis). The share adds to media cost, so the owner tests the rate against the target cost per qualified outcome. The skill proposes no rate.
- Usage rights are a separate line: name the window, the channels, and the fee. The owner sets the fee.

## Measurement plan

Set each item before go-live, for each creator:
1. One primary outcome: the owner's qualified outcome, with its definition and the window that counts it (`Default: none`).
2. Cost per qualified outcome: all deal costs, including the fee, product cost, and any other cost the owner supplies, divided by qualified outcomes, in the supplied currency.
3. Tracking: one unique code and one unique link or landing page per creator, created before go-live. Tag each link with UTM parameters (the `utm_*` tags in the link address) that name the creator and placement; the owner sets the naming pattern (`hl-tracking-plan` can propose one).
4. A "how did you hear about us?" question at signup or checkout. Its answers are self-reported; they do not show the post's effect.
5. A decision rule that the owner writes before launch (`Default: none`). The rule names which result leads to a one-off, a repeat, or a longer partnership. The owner applies it after the window.
6. Context only: reach, views, likes, and earned-media value. They never count as results.
7. Readout: give the export to `hl-reporting`. It labels credited counts as `attributed to` the creator.
