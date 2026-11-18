# hl-skills: Agent Skills that make your coding agent show its work

**Stop taking your agent's word for it.**

hl-skills is a free, open-source collection of more than 50 Agent Skills for Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode, Pi, and any agent that reads `SKILL.md`. Each skill gives your agent a tested method for one job, in engineering and in growth: debugging, code review, security, specs, SEO, copywriting, pricing, and more.

[![ci](https://github.com/HugoLopes45/hl-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/HugoLopes45/hl-skills/actions/workflows/ci.yml)
[![release](https://img.shields.io/github/v/release/HugoLopes45/hl-skills)](./CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-lightgrey)](./LICENSE)

[简体中文](./README.zh-CN.md) · [What changes](#what-changes) · [Install](#install) · [Engineering skills](#engineering-skills) · [Growth skills](#growth-skills) · [FAQ](#faq)

Your agent writes fast. It can also guess, agree with you too soon, and fill a gap with proof it does not have. With hl-skills, it shows its work: the file and line, the command it ran and its result, the source, or a visible placeholder where proof is missing.

## What changes

| Your agent alone can | With hl-skills, it must | Skill |
|---|---|---|
| Say "done" without running anything | Report each requirement as passed, failed, unverified, or blocked, from real command results | [hl-verify](./skills/hl-verify/SKILL.md) |
| Patch a bug it never reproduced | Show the symptom first, then fix only behind a failing regression test | [hl-debug](./skills/hl-debug/SKILL.md) |
| Approve your plan to keep you happy | Return proceed, fix first, or stop, and name the smaller version if one exists | [hl-challenge](./skills/hl-challenge/SKILL.md) |
| Accept every review comment | Decide agree, defer, disagree, or clarify for each comment, against the code | [hl-receive-review](./skills/hl-receive-review/SKILL.md) |
| Fill a landing page with proof you never gave it | Write `[PLACEHOLDER: proof needed]` and name the proof that replaces it | [hl-copywriting](./skills/hl-copywriting/SKILL.md) |
| State facts it never checked | Ground each claim in your evidence or in results it observed, and end with a verdict | Every skill |

## Install

One command. No config, no server, no API key.

```bash
npx skills add HugoLopes45/hl-skills
```

Run it in your project and follow the installer. Requires Node.js 22.20+ and npm. Add `-g` for every project on this machine, or pick skills with `-s hl-debug -s hl-tdd`.

Then open a fresh agent session and try one of these:

> Use hl-roast to roast this README, savage level.
>
> Use hl-debug to find why this test fails only in the full suite.
>
> Use hl-challenge to find the weak assumptions in this plan.

### Call a skill

| Agent | Project folder | Global folder | Call a skill |
|---|---|---|---|
| [Claude Code](https://code.claude.com/docs/en/skills) | `.claude/skills/` | `~/.claude/skills/` | `/hl-debug` |
| [Codex](https://developers.openai.com/codex/skills) | `.agents/skills/` | `~/.agents/skills/` | `$hl-debug` or `/skills` |
| [Cursor](https://cursor.com/docs/skills) | `.agents/skills/` | `~/.agents/skills/` | `/hl-debug` in Agent chat |
| [Gemini CLI](https://geminicli.com/docs/cli/skills/) | `.agents/skills/` | `~/.agents/skills/` | by description |
| [GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) | `.agents/skills/` | `~/.agents/skills/` | `/hl-debug` |
| [OpenCode](https://opencode.ai/docs/skills/) | `.agents/skills/` | `~/.agents/skills/` | by description |
| [Pi](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md) | `.agents/skills/` | `~/.agents/skills/` | `/skill:hl-debug` |

Skills also load by themselves when your request matches one. Start a new session after you install.

## Engineering skills

From the first idea to the merged pull request. Find your moment, then copy the prompt.

[Before you code](#before-you-code) · [While you build](#while-you-build) · [When it breaks](#when-it-breaks) · [Before you merge](#before-you-merge) · [Before you launch](#before-you-launch)

### Before you code

*You have an idea, a loose plan, or a repository you do not know yet.*

| Skill | You get | Try this prompt |
|---|---|---|
| [hl-discover](./skills/hl-discover/SKILL.md) | A map of an unfamiliar repo: stack, commands, where to start | `Use hl-discover to map this repo and show me where to start.` |
| [hl-grill](./skills/hl-grill/SKILL.md) | Real options compared, then questions until the plan is clear | `Use hl-grill to compare magic links and passwords for this app.` |
| [hl-spec](./skills/hl-spec/SKILL.md) | A feature plan with acceptance criteria you can test | `Use hl-spec to plan CSV exports with clear acceptance criteria.` |
| [hl-challenge](./skills/hl-challenge/SKILL.md) | A verdict on your plan: proceed, fix first, or stop | `Use hl-challenge to find the weak assumptions in this plan.` |
| [hl-spike](./skills/hl-spike/SKILL.md) | A time-boxed experiment that ends in proceed, pivot, or inconclusive | `Use hl-spike to test whether SQLite can handle our write load.` |
| [hl-adr](./skills/hl-adr/SKILL.md) | A decision record with the options and the cost of reversal | `Use hl-adr to record why we chose PostgreSQL and the cost of reversing it.` |
| [hl-roast](./skills/hl-roast/SKILL.md) | A funny, honest teardown where every joke points at a real flaw | `Use hl-roast to roast this landing page, savage level.` |

### While you build

*You know what to build. Now build it test first, in small steps.*

| Skill | You get | Try this prompt |
|---|---|---|
| [hl-tdd](./skills/hl-tdd/SKILL.md) | One behavior built red, green, refactor, failing test first | `Use hl-tdd to reject expired invitations, test first.` |
| [hl-tickets](./skills/hl-tickets/SKILL.md) | Thin slices, one pull request each, as files or GitHub issues | `Use hl-tickets to turn this feature plan into independently testable tickets.` |
| [hl-ambitious](./skills/hl-ambitious/SKILL.md) | A higher standard for the task, with the same scope | `Use hl-ambitious to make this task deeper without expanding its scope.` |
| [hl-show-me](./skills/hl-show-me/SKILL.md) | The answer as a picture: diagram, tree, table, or timeline | `Use hl-show-me to draw how authentication works in this app.` |
| [hl-explainer-video](./skills/hl-explainer-video/SKILL.md) (experimental) | A short narrated explainer video on one topic | `Use hl-explainer-video to make a short narrated video explaining CRDTs.` |
| [hl-writing-for-agents](./skills/hl-writing-for-agents/SKILL.md) | Prompts and instructions written for an agent to execute | `Use hl-writing-for-agents to make this prompt shorter without losing its requirements.` |

### When it breaks

*A test fails, CI is red, or something looks unsafe.*

| Skill | You get | Try this prompt |
|---|---|---|
| [hl-debug](./skills/hl-debug/SKILL.md) | The proven cause of a bug, from a loop that shows the symptom | `Use hl-debug to find why this test fails only in the full suite.` |
| [hl-ci-fix](./skills/hl-ci-fix/SKILL.md) | Failing PR checks fixed, without weakening tests or CI | `Use hl-ci-fix to fix the failing checks on this PR.` |
| [hl-security-audit](./skills/hl-security-audit/SKILL.md) | A prioritized security report, traced from the source | `Use hl-security-audit to audit our password-reset flow for account-takeover risks.` |
| [hl-reverse-engineering](./skills/hl-reverse-engineering/SKILL.md) | How a shipped app, binary, package or extension really works, what changed, or whether to keep it, from cited evidence | `Use hl-reverse-engineering to tell me if this ad blocker .crx is safe to keep.` |
| [hl-pentest](./skills/hl-pentest/SKILL.md) | Authorized, bounded penetration tests with observed evidence | `Use hl-pentest to plan paranoid tests for this staging API. Do not contact it yet.` |
| [hl-security-fix](./skills/hl-security-fix/SKILL.md) | A vulnerability fixed at its root, then attacks and bypasses retested | `Use hl-security-fix to close this cross-tenant export flaw and verify the fix.` |
| [hl-improve](./skills/hl-improve/SKILL.md) | Prioritized fix plans for another agent; never edits source code | `Use hl-improve to prioritize what we should fix in this codebase.` |
| [hl-lessons](./skills/hl-lessons/SKILL.md) | The cheapest durable fix for a mistake: a check or a rule | `Use hl-lessons to turn what we learned from this bug into a durable safeguard.` |

All three security skills use paranoid verification by default. This increases scrutiny, not permission or scope. Audit reviews source; pentest requires explicit active-test permission; security-fix requires a repair request.

### Before you merge

*The code works. Now prove it, clean it, and ship it.*

| Skill | You get | Try this prompt |
|---|---|---|
| [hl-code-review](./skills/hl-code-review/SKILL.md) | Findings with location, trigger, consequence, and evidence | `Use hl-code-review to review this branch for bugs and regressions.` |
| [hl-receive-review](./skills/hl-receive-review/SKILL.md) | Agree, defer, disagree, or clarify, for each comment | `Use hl-receive-review to evaluate these review comments before we make changes.` |
| [hl-deslop](./skills/hl-deslop/SKILL.md) | AI slop and tautologies removed from a change, or a cleanup plan for existing code | `Use hl-deslop to remove unnecessary abstractions from this diff.` |
| [hl-verify](./skills/hl-verify/SKILL.md) | Passed, failed, unverified, or blocked, for each requirement | `Use hl-verify to check this change against its acceptance criteria.` |
| [hl-commit](./skills/hl-commit/SKILL.md) | A commit message grounded in the staged changes | `Use hl-commit to commit the staged changes.` |
| [hl-split-pr](./skills/hl-split-pr/SKILL.md) | A large diff split into ordered, reviewable pull requests | `Use hl-split-pr to plan smaller PRs from this oversized diff.` |
| [hl-open-pr](./skills/hl-open-pr/SKILL.md) | A draft pull request with verification, risk, and recovery notes | `Use hl-open-pr to open a draft PR for this branch.` |
| [hl-checkpoint](./skills/hl-checkpoint/SKILL.md) | Decisions, evidence, and next step saved before you clear the context | `Use hl-checkpoint to prepare a handoff before I start a fresh session.` |

### Before you launch

*The product is real. Test the idea, then plan the launch.*

| Skill | You get | Try this prompt |
|---|---|---|
| [hl-startup](./skills/hl-startup/SKILL.md) | An idea taken from nothing to keep or kill | `Use hl-startup to pressure-test this SaaS idea before I build it.` |
| [hl-launch-marketing](./skills/hl-launch-marketing/SKILL.md) | A 14-day launch plan, channel experiments, and a content engine | `Use hl-launch-marketing to plan a two-week launch for this product.` |

## Growth skills

From what you claim to what you measure. Each skill works from what you supply: briefs, interviews, exports, and pages.

[Know what to claim](#know-what-to-claim) · [Get found](#get-found) · [Write the words](#write-the-words) · [Turn visitors into users](#turn-visitors-into-users) · [Reach people](#reach-people) · [Measure what happened](#measure-what-happened)

### Know what to claim

*Decide what you sell, to whom, against whom, and at what price.*

| Skill | You get | Try this prompt |
|---|---|---|
| [hl-positioning](./skills/hl-positioning/SKILL.md) | A positioning statement built from buyer evidence | `Use hl-positioning to state what this hot sauce should claim, from our five buyer interviews.` |
| [hl-persona](./skills/hl-persona/SKILL.md) | Personas from interviews, reviews, and tickets, with nothing invented | `Use hl-persona to build buyer cards from these six interview notes, with no invented details.` |
| [hl-competitor-analysis](./skills/hl-competitor-analysis/SKILL.md) | Dated competitor profiles, with facts kept apart from guesses | `Use hl-competitor-analysis to profile these two rivals from their dated captures.` |
| [hl-pricing](./skills/hl-pricing/SKILL.md) | A price structure, a price range, and a test on new buyers | `Use hl-pricing to propose a plan structure and a test, from our buyer survey.` |
| [hl-win-loss](./skills/hl-win-loss/SKILL.md) | Why deals are won and lost, coded from buyers' words and counted | `Use hl-win-loss to read why we lose to a rival from these deal records.` |
| [hl-marketing-plan](./skills/hl-marketing-plan/SKILL.md) | A period plan: three bets at most, moves by funnel stage, stop criteria | `Use hl-marketing-plan to plan next quarter's bets.` |

### Get found

*Find what blocks your pages in search and in AI answers, then pick what to write next.*

| Skill | You get | Try this prompt |
|---|---|---|
| [hl-seo-audit](./skills/hl-seo-audit/SKILL.md) | Search audit, site structure, migration checks, and ranking diagnosis | `Use hl-seo-audit to find why this page is blocked from search.` |
| [hl-keyword-research](./skills/hl-keyword-research/SKILL.md) | Keywords and topic clusters from buyer words and Search Console | `Use hl-keyword-research to pick the next page to write from this Search Console export.` |
| [hl-content-brief](./skills/hl-content-brief/SKILL.md) | One page brief: query, intent, answer, outline, and facts to source | `Use hl-content-brief to brief a guide on how to chase a late invoice, for freelance designers in the United States.` |
| [hl-ai-search-visibility](./skills/hl-ai-search-visibility/SKILL.md) | Whether a page can be found and quoted in AI answers | `Use hl-ai-search-visibility to check whether ChatGPT, Perplexity, and Google AI answers can use this page.` |
| [hl-schema-markup](./skills/hl-schema-markup/SKILL.md) | Structured data checked against what the page shows | `Use hl-schema-markup to check the JSON-LD on this product page against its visible price.` |
| [hl-internal-linking](./skills/hl-internal-linking/SKILL.md) | Orphan pages and links to broken, redirected, or noindex pages | `Use hl-internal-linking to find orphan pages and broken targets in this links export.` |
| [hl-link-building](./skills/hl-link-building/SKILL.md) | Link plan: target pages, linking sites, outreach drafts, checks | `Use hl-link-building to plan which sites should link to our buyer guide.` |
| [hl-local-visibility](./skills/hl-local-visibility/SKILL.md) | Local listing, review, and lead-reply readout with ordered fixes | `Use hl-local-visibility to audit how my business shows in local search.` |
| [hl-app-store-listing](./skills/hl-app-store-listing/SKILL.md) | Audit or draft store listing fields, checked against store rules | `Use hl-app-store-listing to rewrite my app store title and keywords.` |

### Write the words

*Pages, articles, and emails from your brief, with every fact kept.*

| Skill | You get | Try this prompt |
|---|---|---|
| [hl-copywriting](./skills/hl-copywriting/SKILL.md) | Website and product copy, taglines, and interface microcopy from supplied facts | `Use hl-copywriting to rewrite this hero without invented proof.` |
| [hl-article-writing](./skills/hl-article-writing/SKILL.md) | Explanatory articles from your brief and sources | `Use hl-article-writing to turn this brief into a complete article for our publication, in the requested language. Keep every figure sourced.` |
| [hl-de-ai-rewriting](./skills/hl-de-ai-rewriting/SKILL.md) | Plainer prose that keeps every claim, number, and name | `Use hl-de-ai-rewriting to make this shipping notice clearer, keeping every date and fee.` |
| [hl-email](./skills/hl-email/SKILL.md) | One email, journalist pitch, correction, or reply with one action | `Use hl-email to draft a renewal reminder from this brief, with placeholders for any offer we have not supplied.` |
| [hl-email-sequence](./skills/hl-email-sequence/SKILL.md) | Lifecycle and outreach sequence maps: triggers, timing, skip rules, and exits | `Use hl-email-sequence to map a three-step welcome sequence from these recorded events.` |

### Turn visitors into users

*Find what stops a visitor, then plan the test that settles it.*

| Skill | You get | Try this prompt |
|---|---|---|
| [hl-page-cro-audit](./skills/hl-page-cro-audit/SKILL.md) | The barriers between a visitor and the page's main action | `Use hl-page-cro-audit to find what blocks booking on this clinic page, and label each hypothesis.` |
| [hl-onboarding](./skills/hl-onboarding/SKILL.md) | The shortest path from first run to first value | `Use hl-onboarding to design the first-week flow for this fitness app from its step list.` |
| [hl-lead-lifecycle](./skills/hl-lead-lifecycle/SKILL.md) | Lead stages, qualification, routing, and the handoff to sales | `Use hl-lead-lifecycle to write the stages and handoff rules from my won and lost leads.` |
| [hl-churn-prevention](./skills/hl-churn-prevention/SKILL.md) | Voluntary and involuntary churn split, a cancel flow with one save offer, and failed-payment recovery | `Use hl-churn-prevention to plan a cancel flow from our cancellation export.` |
| [hl-ab-test-plan](./skills/hl-ab-test-plan/SKILL.md) | One A/B test with metrics and a sample size from your baseline | `Use hl-ab-test-plan to plan a test on this pricing toggle, with sizing from our baseline export.` |

### Reach people

*Social posts, ads, and short videos, written for the platform in your brief.*

| Skill | You get | Try this prompt |
|---|---|---|
| [hl-social](./skills/hl-social/SKILL.md) | Posts, carousels, comments, and replies for the platform in your brief | `Use hl-social to draft two captions from this brief. Platform and market are in the brief.` |
| [hl-paid-ads](./skills/hl-paid-ads/SKILL.md) | Ad copy for any ad platform, market, and currency | `Use hl-paid-ads to write three search ad variants from this brief, with missing proof as placeholders.` |
| [hl-short-video](./skills/hl-short-video/SKILL.md) | Short-video scripts with lines, shots, and on-screen text | `Use hl-short-video to turn this brief into a 30-second script for our chosen platform, with spoken lines, shots, on-screen text and rights checks.` |
| [hl-referral-program](./skills/hl-referral-program/SKILL.md) | A referral reward under your cost ceiling, with rules and measurement | `Use hl-referral-program to design a referral reward that stays under our acquisition target.` |
| [hl-creator-deal](./skills/hl-creator-deal/SKILL.md) | Creator fit, paid trials, briefs, deal terms, and measurement | `Use hl-creator-deal to evaluate this creator's fit and brief a sponsored post.` |
| [hl-event-plan](./skills/hl-event-plan/SKILL.md) | A go, pilot, redesign, or pass decision on one event, with run of show and readout | `Use hl-event-plan to decide whether this workshop is worth its budget.` |
| [hl-public-relations](./skills/hl-public-relations/SKILL.md) | Press plan, pitch, release, reactive comment and crisis holding statement | `Use hl-public-relations to plan press coverage for our product launch.` |
| [hl-text-messaging](./skills/hl-text-messaging/SKILL.md) | Opt-in text program plan: consent proof, flow spec, opt-out rules, adviser questions | `Use hl-text-messaging to plan the restock text flow and its opt-in form.` |
| [hl-prospecting](./skills/hl-prospecting/SKILL.md) | A sourced prospect list and outbound plan from supplied records | `Use hl-prospecting to build a sourced prospect list of independent bakeries in our town.` |
| [hl-sales-enablement](./skills/hl-sales-enablement/SKILL.md) | Sales collateral from supplied proof, every claim source-tagged | `Use hl-sales-enablement to draft a one-pager for a champion.` |

### Measure what happened

*Plan the events before launch, then read the numbers after.*

| Skill | You get | Try this prompt |
|---|---|---|
| [hl-tracking-plan](./skills/hl-tracking-plan/SKILL.md) | Events, metrics, owners, and privacy checks tied to one decision | `Use hl-tracking-plan to plan the events behind this booking decision. Flag personal data.` |
| [hl-reporting](./skills/hl-reporting/SKILL.md) | A performance report from your exports, with gaps named | `Use hl-reporting to summarise this weekly export by channel. Name what is missing.` |

## Update and pin

```bash
npx skills list                                   # what is installed
npx skills update hl-debug hl-tdd                 # update these skills
npx skills remove -s hl-tdd                       # remove one skill
npx skills add HugoLopes45/hl-skills#v1.0.0       # every skill at v1.0.0
```

`npx skills update` without names updates every skill in that scope, from every source. Releases follow semantic versioning; experimental skills may change in any release. See [CHANGELOG.md](./CHANGELOG.md).

## FAQ

### What is an Agent Skill?

An Agent Skill is a folder with a `SKILL.md` file. Your agent loads it when you call the skill, or when your request matches the skill's description. Each skill is readable text, so you can read it before you install it.

### Which agents does hl-skills work with?

Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot CLI, OpenCode, Pi, and any agent that reads `SKILL.md`. See [Call a skill](#call-a-skill) for the folder and the command of each agent.

### Is hl-skills free?

Yes. hl-skills is MIT licensed. It needs no account, no server, and no API key.

### How is a skill different from a prompt?

A prompt asks for one result. A skill gives your agent a full method: when to use it, the steps, the evidence rules, when to stop, and a report that ends with a verdict.

## Limits

Structural checks pass; agent-output evaluations are incomplete. These are AI instructions, not guaranteed results: review the output. Skills run with your agent's full permissions, so read a skill before you install it. Report vulnerabilities as [SECURITY.md](./SECURITY.md) describes.

## Contribute

Read [CONTRIBUTING.md](./CONTRIBUTING.md) and [STYLE.md](./STYLE.md). MIT licensed, see [LICENSE](./LICENSE).
