---
name: hl-launch-marketing
description: "Produce launch artifacts for a solo or small-team software product: 14-day launch plan, ranked channel experiments, 30-day content engine, and an offer and unit-economics check. Produces the artifact, not advice. Its position, landing, and pricing modes serve a launch when named with --mode. Use when the user asks how to market or launch a product, which channels to use, or what to post. Not for a standalone positioning canvas (hl-positioning), price structure (hl-pricing), or landing page copy (hl-copywriting)."
---
# Launch Marketing

Input: `[product + stage] [--mode position|landing|launch|channels|content|pricing|offer] [--depth quick|deep]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Deliver requested copy, calculations, and schedules in full. Separate supplied figures, checked sources, unverified claims, and proposed targets; keep publishing prerequisites in Next.

Default to a solo software founder with limited time and budget unless the input says otherwise. Treat channel and positioning choices as hypotheses to test. Every mode delivers the requested artifact, not a strategy deck; a draft with placeholders is not ready to publish. Do not publish, send outreach, buy ads, or change billing without action-specific approval.

Needs a product (even hypothetical) and a stage. Neither in args nor conversation → ask for the one-line product and stage (pre-launch, launched, flat MRR), then run. One clarifying question max.

## Principles

- Clarify the buyer and promise before proposing promotion.
- Start with a channel the founder can sustain; compare outcomes before expanding.
- Describe the buyer's outcome, not just the feature list.
- Propose a small outreach test where access and consent permit it; when consent cannot be confirmed, stage the outreach for the owner, mark it `consent unconfirmed` in Next, and do not send it.
- Before a physical or stunt play, check that it fits the buyer, gives something rather than pitching, and has a target list and deal size that cover its cost. Test it on a few targets before scaling.
- Use actual demos and supported figures; missing proof stays a placeholder.
- Before the artifact, compare each candidate factual sentence with its exact supporting source passage. Record the approved final wording, placeholder, or omission; check the subject, effects, and timing.
- Assemble factual copy verbatim from approved wording or placeholders, including headings and calls to action. New factual wording returns to the comparison before inclusion. Report specific comparisons and remaining limits, not blanket certification; a confirmation request in Next does not qualify finished copy.

Claim-construction example, not product facts:

| Exact source passage | Approved final wording | Still unknown |
|---|---|---|
| DeskNote reads Markdown files. | Read Markdown files with DeskNote. | Format limits and setup; not "every file" or "no setup". |
| CTA: Join the launch list. | Join the launch list. `[PLACEHOLDER: signup URL]` | Email frequency, delivery date, and launch-day promises. |
| DeskNote exports a text summary. | Export a text summary. | Other file writes; exporting does not establish "the only file it writes". |
| Founder note: repeated labels are easy to miss. | Repeated labels are easy to miss. | Detection timing; not "found only after sending". |

## Modes

`pricing` follows [references/pricing.md](references/pricing.md); `offer` follows [references/offer.md](references/offer.md), whose own modes are picked by the question.

Read [references/lead-magnet.md](references/lead-magnet.md) when `offer` `acquire` builds a lead magnet: formats, gates, quizzes, calculators, checkers, and audits. Report the lead magnet under the `acquire` verdict, `Commit`.

Before writing a headline, one-liner, landing section, or post, read [references/calibration.md](references/calibration.md) and check each dimension.

### position (default)

1. Extract buyer, painful event, current alternative, unique mechanism from what's given.
2. Write the positioning block: for-statement ("For [buyer] who [pain], [product] is the [category] that [outcome], unlike [alternative], it [mechanism]"), a concise one-liner, ranked proof points supported by the input or checked sources.
3. Stress it: would the named buyer recognize themselves in five seconds? Could the incumbent paste this on their own site? Interchangeable → sharpen the mechanism, rewrite once.

Open the reply with the one-liner; Next owns the venue and validation action for this week.

### landing

Complete landing draft, section by section: hero (concise headline, subhead, one CTA), pain mirror (three bullets in the buyer's words), how-it-works (three steps), proof, pricing framing, FAQ (five real objections), final CTA. Designer notes only where copy alone can't carry the section. The page itself starts with the hero headline and its CTA. Never invent testimonials, logos, or metrics; label placeholders and pair with the plan to earn the real thing. Quote a customer only with their permission, the original date, and the source.

### launch

Before the plan, run the pre-launch checks in `references/launch-readiness.md`, and name the current phase and the next one. The 14-day plan below applies only when the next phase is Full launch; that file sets the other cases. Build the plan around one primary venue (Product Hunt, HN Show, a specific subreddit, a niche community), picked for where the buyer is, reason stated. List the venue's cons from a checked source; if you did not check them, mark them unverified; choose the venue only if the cons are acceptable. Pre-launch week: asset list, ten warm DMs, teaser. With partners or affiliates, give all of them one shared date, one asset set, and one real, checkable reason for their audience to act now. Launch day, hour by hour: post copy written out, first-comment copy, reply cadence; route each complaint to the owner at once. Post week: follow-ups, turning replies into onboarding, and the post-launch steps in `references/launch-readiness.md`. Every day carries an action and a done-when, in a table: day, action, done when; full copy goes below it. Include the venue's house rules that get posts killed: self-promotion ratios, flair, timing; cite the current rule and source when checked; otherwise mark it unverified and make checking it a prerequisite. Never estimate a venue's rules. Lead with the venue and the launch date.

Updates to a live product follow `references/release-updates.md`. A site launch, redesign, or migration runs `references/site-launch-qa.md` before the switch.

### channels

Rank the acquisition channels that fit this product, buyer, and founder from: cold outreach, SEO, programmatic SEO, content/build-in-public, communities, free tools, directory listings, marketplaces and integrations, partnerships, paid (rarely right for solo). Lead with the commitment: one primary plus one compounding channel, and what not to do. Then a ranked table: channel, hours per week, kill signal; under it, one block per channel: why this buyer is there, a first experiment runnable in a week. Channel economics belong to the `offer` mode; this mode picks venues and experiments.

Tag each channel as owned (an audience you control: a list, a community, the product), rented (a platform's audience you can lose: a social feed, a directory), or borrowed (another owner's audience: a partner's newsletter, a guest post). Rented and borrowed reach must move people to an owned channel, such as a list, a community, or the product. Do not spread effort across platforms without one primary channel and a repurposing plan. Before counting on a third-party platform for search traffic, check the search engine's current guidance on that platform. If you cannot check, mark it unverified and make the check a prerequisite in Next.

Pick channels by stage, budget, and timeline. State why each chosen channel fits, and name each skipped channel with its reason. Tell the founder to check each channel's kill signal during its first experiment and stop the channel when it fires. A flat result, or rising effort with flat output, is a kill signal. Add an acquisition channel only after the supplied retention records are read and the problems they show are addressed; without such records, write that check into Next. Rank a paid placement, such as a sponsorship or ads, only with a dated rate and an audience source. Before a giveaway or contest, check the platform's current promotion rules and the local contest law. If you cannot check, mark it unverified and make the check a prerequisite in Next.

Read `references/channel-playbooks.md` for community, partner, and free-tool channels, and `references/directory-listings.md` before any directory or integration listing.

### content

30-day content engine for one channel: pillar topics derived from buyer pains (not keywords first), twelve post/article prompts with hooks, a repurposing chain (article → thread → newsletter), weekly time budget ≤4 hours (heuristic default). Lead with the channel and the pillar topics. Original data posts use only product data the owner supplies, with its export date and scope. A free template is content too: name its job and the product step it leads to. When the channel is SEO: keyword intent tiers, one programmatic pattern if the product's data supports it, and an honest timeline in months, not days.

## Output

Reader: a solo founder who must act this week: publish a post, change a price, or pick a channel. The decision served: what to do next and where.

Line 1, bold: one plain sentence, that answers the founder's question with the decision in it. Never opens with a label, verdict word, or number.

The verdict line sits just before `**Next:**`, per mode:
- position: `Sharp` (the stress test passed) or `Rewritten` (the first draft failed; the rewrite follows).
- channels: `Commit` (one primary channel plus one compounding channel).
- launch: `Launch` (the venue and launch date); `Not yet, fix <open criterion>` when the next phase is not Full launch; `Plan` (the after-launch checks) when the product is already at Full launch.
- landing: `Draft` (copy complete; unsupported claims left as placeholders).
- content: `Plan` (the channel and pillar topics).
- pricing: `Charge <amount>`, `Wrong segment`, or `Do not build`.
- tiers: `Plan` (the tier table).
- monetize: `Charge <amount>` (the feature's price and model).
- offer: `Strong`, `Not yet, fix <term>`, or `Wrong buyer`.
- acquire: `Commit` (one channel and its attempt target).
- economics: `Hold` (a number is past its threshold) or `Scale`.
- constraint: `Optimize` or `Push volume`.

Under line 1, plain sentences, one each, only when they apply: the input that blocks the first action, and each detail you did not get, with the default you chose (for example "I assumed you post from your personal profile, not a company page."). For a minor gap, pick a safe default and say so; ask only when the gap blocks the work.

Body by mode, numbered points unless the view says otherwise:
- position: the for-statement in a fence with `[PLACEHOLDER]` slots, then the supported proof points in a numbered list, with the evidence and limits needed to check them. The one-liner is the opening, not repeated here.
- channels: compare the channels that fit the goal and constraints: channel, hours a week, kill signal (the sign to stop). Use a table for short cells; otherwise numbered items. Under it, one numbered point per channel, starting with its tag (owned, rented, or borrowed): its first experiment, runnable in a week.
- launch: when the next phase is Full launch, a table of day, action, done when for the 14 days, an hour-by-hour launch-day table, then post copy and first-comment copy in fences with `[PLACEHOLDER]` slots. Before Full launch, give the current phase's open criteria from `references/launch-readiness.md`. Already at Full launch: give the after-launch checks.
- content: 12 numbered prompts with hooks. The repurposing chain as a `text` flow: article -> thread -> newsletter.
- pricing: the complete calculation, one step per line in a `text` fence: item, amount, basis (`your figure, not measured`, `checked source`, `unverified`, or `estimate from stated assumptions`). Then the verdict.
- offer: first apply the buyer/outcome gate in `references/offer.md`. If either is missing or vague, report that gap and `Verdict: Not yet, fix the buyer and outcome` (name only the missing term when one is known). Do not enumerate downstream dimensions after this gate stops the analysis. Put the missing decision and its validation in Next. If the gate passes, report the supported dimensions in plain words: outcome, proof, time to first win, buyer effort, bonuses, guarantee, scarcity, name, price comparison, and buyer. Each bold sentence names the problem, or says the step is fine. Complete requested copy still ships, with explicit `[PLACEHOLDER]` slots for unsupported content.
- economics: table of metric, value, basis. Warning lines under it, as plain sentences.
- landing and content are artifacts: they ship complete. A launch artifact is complete for the phase selected above; do not draft a public launch before the phase gate permits it. `quick` depth (position and channels only) keeps the decision, its basis, and the first experiment. `deep` explains the tradeoffs. Neither drops a warning or shortens a required artifact.

End with `**Next:**`, one step per line: the post to publish, the message to send, the number to measure. A check or fix needed before a step goes in that step, not above the verdict: a venue rule that gets posts removed, a placeholder to replace before posting.

Stopped: line 1 says in plain words what is missing and why it blocks. Then `Verdict: Stopped`. `**Next:**` holds up to 3 numbered ways to unblock, default marked, listed nowhere else. Example Next:
1. Which product, in one line, and at what stage: pre-launch, launched, or flat revenue? (default)
2. Name the venue you already use, if any.

Reader rules:
- Define once: CTA (the button or link readers press), DM (direct message), CAC (cost to win one paying customer), LTV (profit one customer brings over their time), churn (share of customers who cancel each month), payback (months until a customer's profit covers their win cost), SEO (free search traffic).
- Buyer's words over marketing-speak: pull phrases from reviews or threads the user gave. Label invented voice as invented.
- Label figures by their basis: supplied, measured with its method, checked source, unverified, or estimated from stated assumptions. A public page is not checked evidence until read. In tables, put this in the basis column; do not repeat it in prose.
- Never invent testimonials, logos, badges, or metrics. Use `[PLACEHOLDER]` and say what real proof replaces it.
- No hype, no blame. Use the output words, not the method's labels: "the outcome the buyer wants", not "dream outcome".

Example (position, depth quick). Supplied example facts: BakeScale adjusts ingredients by pan size, prints one sheet, and keeps converted lists offline. Buyer validation is absent:

````markdown
**BakeScale adjusts ingredients to the chosen pan size.**
I have not tested whether bakers scale by pan size.

| Exact source passage | Approved final wording |
|---|---|
| BakeScale adjusts ingredients by pan size | For [PLACEHOLDER: validated buyer and painful event], BakeScale adjusts ingredients to the chosen pan size, unlike [PLACEHOLDER: checked alternative and its difference]. |
| adjusts ingredients by pan size | Ingredients scale to the chosen pan size. |
| prints one sheet | BakeScale prints one sheet. |
| keeps converted lists offline | Converted lists stay offline. |

Rewrite of the positioning statement:

```text
For [PLACEHOLDER: validated buyer and painful event], BakeScale adjusts ingredients to the chosen pan size, unlike [PLACEHOLDER: checked alternative and its difference].
```

1. **Ingredients scale to the chosen pan size.**
2. **BakeScale prints one sheet.**
3. **Converted lists stay offline.**

Verdict: Rewritten

**Next:**
1. Before building more, ask in the baking forum: "How do you scale a recipe to a different pan?" No link.
2. Write the answers down; reuse the exact words in the next draft.
````

## Anti-patterns (don't do these)

- "Post consistently on all platforms": generic advice is a failure state; every recommendation names a venue and a first action.
- Fabricated social proof, anywhere, ever.
- A launch plan that ignores the venue's self-promo rules.
- Positioning the incumbent could run unchanged.
- Ship scope or kill decisions answered here instead of `hl-startup ship` or `hl-startup kill`.
