---
name: hl-launch-marketing
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

Open the reply with the one-liner and the venue to test it in this week.

### landing

Paste-ready landing copy, section by section: hero (headline ≤8 words, subhead, one CTA), pain mirror (three bullets in the buyer's words), how-it-works (three steps), proof, pricing framing, FAQ (five real objections), final CTA. Designer notes only where copy alone can't carry the section. Lead with the hero headline and its CTA. Never invent testimonials, logos, or metrics; label placeholders and pair with the plan to earn the real thing.

### launch

14-day plan around one primary venue (Product Hunt, HN Show, a specific subreddit, a niche community), picked for where the buyer is, reason stated. Pre-launch week: asset list, ten warm DMs, teaser. Launch day, hour by hour: post copy written out, first-comment copy, reply cadence. Post week: follow-ups, turning replies into onboarding. Every day carries an action and a done-when, in a table: day, action, done when; full copy goes below it. Include the venue's house rules that get posts killed: self-promotion ratios, flair, timing; label a rule's number public, with where to confirm it, or estimate. Lead with the venue and the launch date.

### channels

Rank the three best acquisition channels for this product, buyer, and founder from: cold outreach, SEO, programmatic SEO, content/build-in-public, communities, marketplaces and integrations, partnerships, paid (rarely right for solo). Lead with the commitment: one primary plus one compounding channel, and what not to do. Then a ranked table: channel, hours per week, kill signal; under it, one block per channel: why this buyer is there, a first experiment runnable in a week. Channel economics belong to the `offer` mode; this mode picks venues and experiments.

### content

30-day content engine for one channel: pillar topics derived from buyer pains (not keywords first), twelve post/article prompts with hooks, a repurposing chain (article → thread → newsletter), weekly time budget ≤4 hours. Lead with the channel and the pillar topics. When the channel is SEO: keyword intent tiers, one programmatic pattern if the product's data supports it, and an honest timeline in months, not days.

## Output

Reader: a solo founder who must act this week: publish a post, change a price, or pick a channel. The decision served: what to do next and where.

Line 1, bold: one plain sentence, under 100 characters, that answers the founder's question with the decision in it. Never opens with a label, verdict word, or number.

The verdict line sits just before `**Next:**`, per mode:
- position: `Sharp` (the stress test passed) or `Rewritten` (the first draft failed; the rewrite follows).
- channels: `Commit` (one primary channel plus one compounding channel).
- launch: `Launch` (the venue and launch date).
- landing: `Draft` (copy complete; proof left as placeholders).
- content: `Plan` (the channel and pillar topics).
- pricing: `Charge <amount>`, `Wrong segment`, or `Do not build`.
- offer: `Strong`, `Not yet, fix <term>`, or `Wrong buyer`.
- economics: `Hold` (a number is under its threshold) or `Scale`. Line 1 names the number that hurts most, for example `**Each customer costs $120 and returns $80, so do not scale ads yet.**`
- constraint: `Optimize` or `Push volume`.

Under line 1, plain sentences, one each, only when they apply: the input that blocks the first action, and each detail you did not get, with the default you chose (for example "I assumed you post from your personal profile, not a company page."). For a minor gap, pick a safe default and say so; ask only when the gap blocks the work.

Body by mode, numbered points unless the view says otherwise:
- position: the for-statement in a fence with `[PLACEHOLDER]` slots, then the one-liner as a bold sentence, then up to three proof points, one sentence each, numbered.
- channels: table of up to 5 channels: channel, hours a week, kill signal (the sign to stop). Under it, one numbered point per channel: its first experiment, runnable in a week.
- launch: table of day, action, done when for the 14 days. Hour-by-hour launch-day table. Post copy and first-comment copy in fences with `[PLACEHOLDER]` slots, after the tables.
- content: 12 numbered prompts with hooks. The repurposing chain as a `text` flow: article -> thread -> newsletter.
- pricing: the calculation, one step per line in a `text` fence of at most 8 lines: item, amount, basis (`your figure, not measured`, `public`, or `estimate`). Then the verdict.
- offer: one numbered point per step, in plain words: the outcome the buyer wants, proof it works, time to first win, effort for the buyer, bonuses, price and what it is compared with, the buyer. Each bold sentence names the problem, or says the step is fine.
- economics: table of metric, value, basis, up to 5 rows: cost to win a customer (CAC), lifetime profit per customer (LTV), payback, gross margin, runway. Warning lines under it, as plain sentences.
- landing, launch, and content are artifacts: they ship complete. `quick` depth (position and channels only) is at most 300 words in total, gate lines and `**Next:**` included; cut prose before table rows; `deep` is the full artifact with no padding.

End with `**Next:**`, one step per line: the post to publish, the message to send, the number to measure. A check or fix needed before a step goes in that step, not above the verdict: a venue rule that gets posts removed, a placeholder to replace before posting.

Stopped: line 1 says in plain words what is missing and why it blocks. Then `Verdict: Stopped`. `**Next:**` holds up to 3 numbered ways to unblock, default marked, listed nowhere else. Example Next:
1. Which product, in one line, and at what stage: pre-launch, launched, or flat revenue? (default)
2. Name the venue you already use, if any.

Reader rules:
- Define once: CTA (the button or link readers press), DM (direct message), CAC (cost to win one paying customer), LTV (profit one customer brings over their time), churn (share of customers who cancel each month), payback (months until a customer's profit covers their win cost), SEO (free search traffic).
- Buyer's words over marketing-speak: pull phrases from reviews or threads the user gave. Label invented voice as invented.
- Label every number `your figure, not measured` (a figure the user gave), `public` (with where to confirm it), or `estimate`. Never call a figure measured unless someone measured it. In tables, put the label in the basis column, not on each row's prose.
- Never invent testimonials, logos, badges, or metrics. Use `[PLACEHOLDER]` and say what real proof replaces it.
- No hype, no blame. Use the output words, not the method's labels: "the outcome the buyer wants", not "dream outcome".

Example (position, depth quick):

````markdown
**The first draft fit any kitchen app; the rewrite names the pan. Test it in a baking forum.**
I have not tested whether bakers scale by pan size: ask five bakers before building more.

Rewrite of the positioning statement:

```text
For home bakers who halve, double, or convert recipes by hand, BakeScale is the recipe
scaler that resizes ingredients to your real pan, unlike apps that only multiply amounts.
```

1. **Scaling follows your pan, not a multiplier.** Ingredients change to fit a 20 cm round.
2. **The recipe prints as one sheet for the cupboard.** Keep it next to the tin.
3. **The converted list works offline.** It survives a bad signal in the kitchen.

Verdict: Rewritten

**Next:**
1. Post a question in the forum: "How do you scale a recipe to a different pan?" No link.
2. Write the answers down; reuse the exact words in the next draft.
````

## Anti-patterns (don't do these)

- "Post consistently on all platforms": generic advice is a failure state; every recommendation names a venue and a first action.
- Fabricated social proof, anywhere, ever.
- A launch plan that ignores the venue's self-promo rules.
- Positioning the incumbent could run unchanged.
- Ship scope or kill decisions answered here instead of `hl-startup ship` or `hl-startup kill`.
