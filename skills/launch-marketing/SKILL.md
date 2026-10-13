---
name: launch-marketing
description: "Produce marketing artifacts for a solo or small-team software product: positioning block, paste-ready landing copy, 14-day launch plan, ranked channel experiments, 30-day content engine. Produces the artifact, not advice. Also prices the product and designs the offer and unit economics. Use when the user asks how to market, launch, position, or price a product."
---
# Launch Marketing

Input: `[product + stage] [--mode position|landing|launch|channels|content|pricing|offer] [--depth quick|deep]`

Marketing execution for a one-person SaaS: no budget, no brand, no team; distribution comes from sharp positioning, founder-led channels, and compounding content. Every mode ends in an artifact shippable today, not a strategy deck.

Needs a product (even hypothetical) and a stage. Neither in args nor conversation → ask for the one-line product and stage (pre-launch, launched, flat MRR), then run. One clarifying question max.

## Principles

- Positioning before promotion: traffic to an unclear promise converts at zero.
- One channel done daily beats five done weekly.
- Sell the after-state, not the feature list.
- Pre-launch: ten warm DMs beat one blog post; do things that don't scale first.
- Show, don't claim: demo GIF, real numbers, build-in-public receipts.

## Modes

`pricing` follows [references/pricing.md](references/pricing.md); `offer` follows [references/offer.md](references/offer.md), whose own modes are picked by the question.

### position (default)

1. Extract buyer, painful event, current alternative, unique mechanism from what's given.
2. Write the positioning block: for-statement ("For [buyer] who [pain], [product] is the [category] that [outcome], unlike [alternative], it [mechanism]"), a one-liner ≤10 words, three ranked proof points.
3. Stress it: would the named buyer recognize themselves in five seconds? Could the incumbent paste this on their own site? Interchangeable → sharpen the mechanism, rewrite once.

Lead with a verdict line: the one-liner plus the venue to test it in this week.

### landing

Paste-ready landing copy, section by section: hero (headline ≤8 words, subhead, one CTA), pain mirror (three bullets in the buyer's words), how-it-works (three steps), proof, pricing framing, FAQ (five real objections), final CTA. Designer notes only where copy alone can't carry the section. Lead with the hero headline and its CTA. Never invent testimonials, logos, or metrics; label placeholders and pair with the plan to earn the real thing.

### launch

14-day plan around one primary venue (Product Hunt, HN Show, a specific subreddit, a niche community), picked for where the buyer is, reason stated. Pre-launch week: asset list, ten warm DMs, teaser. Launch day, hour by hour: post copy written out, first-comment copy, reply cadence. Post week: follow-ups, turning replies into onboarding. Every day carries an action and a done-when, in a table: day, action, done when; full copy goes below it. Include the venue's house rules that get posts killed: self-promotion ratios, flair, timing; label a rule's number public, with where to confirm it, or estimate. Lead with the venue and the launch date.

### channels

Rank the three best acquisition channels for this product, buyer, and founder from: cold outreach, SEO, programmatic SEO, content/build-in-public, communities, marketplaces and integrations, partnerships, paid (rarely right for solo). Lead with the commitment: one primary plus one compounding channel, and what not to do. Then a ranked table: channel, hours per week, kill signal; under it, one block per channel: why this buyer is there, a first experiment runnable in a week. Channel economics belong to the `offer` mode; this mode picks venues and experiments.

### content

30-day content engine for one channel: pillar topics derived from buyer pains (not keywords first), twelve post/article prompts with hooks, a repurposing chain (article → thread → newsletter), weekly time budget ≤4 hours. Lead with the channel and the pillar topics. When the channel is SEO: keyword intent tiers, one programmatic pattern if the product's data supports it, and an honest timeline in months, not days.

## Output rules

- `--depth quick` ≤300 words, position and channels only: the lead line, then the artifact itself (position: for-statement, one-liner, three proof points; channels: the ranked table, with each channel's first experiment in its row and no blocks below), one line per item. The extraction and stress test stay internal; report only a rewrite they forced. landing, launch, content are artifacts and always ship complete. deep: full artifact, no padding.
- Buyer's words over marketing-speak: pull phrases from reviews/threads the user provided; invented voice is labeled as such.
- Every number labeled measured, public, or estimate.

## Anti-patterns (don't do these)

- "Post consistently on all platforms": generic advice is a failure state; every recommendation names a venue and a first action.
- Fabricated social proof, anywhere, ever.
- A launch plan that ignores the venue's self-promo rules.
- Positioning the incumbent could run unchanged.
- Ship scope or kill decisions answered here instead of `startup ship` or `startup kill`.
