# hl-skills

Skills that give your coding agent a tested method for one job each, in engineering and in growth. For Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode, Pi, and any agent that reads `SKILL.md`.

[![ci](https://github.com/HugoLopes45/hl-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/HugoLopes45/hl-skills/actions/workflows/ci.yml)
[![release](https://img.shields.io/github/v/release/HugoLopes45/hl-skills)](./CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-lightgrey)](./LICENSE)

[简体中文](./README.zh-CN.md)

Your agent writes fast. It can also guess, agree with you too soon, and fill a gap with proof it does not have. Each skill makes it show the evidence: the file and line, the test run, the source, or a visible placeholder where proof is missing.

## Install

```bash
npx skills add HugoLopes45/hl-skills
```

Run it in your project and follow the installer. Requires Node.js 22.20+ and npm. No config, no server, no API key. Add `-g` for every project on this machine, or pick skills with `-s hl-debug -s hl-tdd`.

Then open a fresh agent session and ask:

> Use hl-debug to find why this test fails only in the full suite.

## Skills

### Engineering

| Area | Skill | Example |
|---|---|---|
| Think | [hl-discover](./skills/hl-discover/SKILL.md) | `Use hl-discover to map this repo and show me where to start.` |
| Think | [hl-grill](./skills/hl-grill/SKILL.md) | `Use hl-grill to compare magic links and passwords for this app.` |
| Think | [hl-spec](./skills/hl-spec/SKILL.md) | `Use hl-spec to plan CSV exports with clear acceptance criteria.` |
| Think | [hl-challenge](./skills/hl-challenge/SKILL.md) | `Use hl-challenge to find the weak assumptions in this plan.` |
| Think | [hl-spike](./skills/hl-spike/SKILL.md) | `Use hl-spike to test whether SQLite can handle our write load.` |
| Think | [hl-adr](./skills/hl-adr/SKILL.md) | `Use hl-adr to record why we chose PostgreSQL and the cost of reversing it.` |
| Think | [hl-roast](./skills/hl-roast/SKILL.md) | `Use hl-roast to roast this landing page, savage level.` |
| Build | [hl-tdd](./skills/hl-tdd/SKILL.md) | `Use hl-tdd to reject expired invitations, test first.` |
| Build | [hl-tickets](./skills/hl-tickets/SKILL.md) | `Use hl-tickets to turn this feature plan into independently testable tickets.` |
| Build | [hl-ambitious](./skills/hl-ambitious/SKILL.md) | `Use hl-ambitious to make this task deeper without expanding its scope.` |
| Build | [hl-show-me](./skills/hl-show-me/SKILL.md) | `Use hl-show-me to draw how authentication works in this app.` |
| Build | [hl-explainer-video](./skills/hl-explainer-video/SKILL.md) (experimental) | `Use hl-explainer-video to make a short narrated video explaining CRDTs.` |
| Build | [hl-writing-for-agents](./skills/hl-writing-for-agents/SKILL.md) | `Use hl-writing-for-agents to make this prompt shorter without losing its requirements.` |
| Fix | [hl-debug](./skills/hl-debug/SKILL.md) | `Use hl-debug to find why this test fails only in the full suite.` |
| Fix | [hl-ci-fix](./skills/hl-ci-fix/SKILL.md) | `Use hl-ci-fix to fix the failing checks on this PR.` |
| Fix | [hl-security-audit](./skills/hl-security-audit/SKILL.md) | `Use hl-security-audit to audit our password-reset flow for account-takeover risks.` |
| Fix | [hl-improve](./skills/hl-improve/SKILL.md) | `Use hl-improve to prioritize what we should fix in this codebase.` |
| Fix | [hl-lessons](./skills/hl-lessons/SKILL.md) | `Use hl-lessons to turn what we learned from this bug into a durable safeguard.` |
| Ship | [hl-code-review](./skills/hl-code-review/SKILL.md) | `Use hl-code-review to review this branch for bugs and regressions.` |
| Ship | [hl-receive-review](./skills/hl-receive-review/SKILL.md) | `Use hl-receive-review to evaluate these review comments before we make changes.` |
| Ship | [hl-deslop](./skills/hl-deslop/SKILL.md) | `Use hl-deslop to remove unnecessary abstractions from this diff.` |
| Ship | [hl-verify](./skills/hl-verify/SKILL.md) | `Use hl-verify to check this change against its acceptance criteria.` |
| Ship | [hl-commit](./skills/hl-commit/SKILL.md) | `Use hl-commit to commit the staged changes.` |
| Ship | [hl-split-pr](./skills/hl-split-pr/SKILL.md) | `Use hl-split-pr to plan smaller PRs from this oversized diff.` |
| Ship | [hl-open-pr](./skills/hl-open-pr/SKILL.md) | `Use hl-open-pr to open a draft PR for this branch.` |
| Ship | [hl-checkpoint](./skills/hl-checkpoint/SKILL.md) | `Use hl-checkpoint to prepare a handoff before I start a fresh session.` |
| Launch | [hl-startup](./skills/hl-startup/SKILL.md) | `Use hl-startup to pressure-test this SaaS idea before I build it.` |
| Launch | [hl-launch-marketing](./skills/hl-launch-marketing/SKILL.md) | `Use hl-launch-marketing to plan a two-week launch for this product.` |

### Growth and marketing

| Area | Skill | Example |
|---|---|---|
| Strategy | [hl-positioning](./skills/hl-positioning/SKILL.md) | `Use hl-positioning to state what this hot sauce should claim, from our five buyer interviews.` |
| Strategy | [hl-persona](./skills/hl-persona/SKILL.md) | `Use hl-persona to build buyer cards from these six interview notes, with no invented details.` |
| Strategy | [hl-competitor-analysis](./skills/hl-competitor-analysis/SKILL.md) | `Use hl-competitor-analysis to profile these two rivals from their dated captures.` |
| Strategy | [hl-pricing](./skills/hl-pricing/SKILL.md) | `Use hl-pricing to propose a plan structure and a test, from our buyer survey.` |
| Search | [hl-seo-audit](./skills/hl-seo-audit/SKILL.md) | `Use hl-seo-audit to find why this page is blocked from search.` |
| Search | [hl-keyword-research](./skills/hl-keyword-research/SKILL.md) | `Use hl-keyword-research to pick the next page to write from this Search Console export.` |
| Search | [hl-content-brief](./skills/hl-content-brief/SKILL.md) | `Use hl-content-brief to brief a guide on how to chase a late invoice, for freelance designers in the United States.` |
| Search | [hl-ai-search-visibility](./skills/hl-ai-search-visibility/SKILL.md) | `Use hl-ai-search-visibility to check whether ChatGPT, Perplexity, and Google AI answers can use this page.` |
| Search | [hl-schema-markup](./skills/hl-schema-markup/SKILL.md) | `Use hl-schema-markup to check the JSON-LD on this product page against its visible price.` |
| Search | [hl-internal-linking](./skills/hl-internal-linking/SKILL.md) | `Use hl-internal-linking to find orphan pages and broken targets in this links export.` |
| Copy | [hl-copywriting](./skills/hl-copywriting/SKILL.md) | `Use hl-copywriting to rewrite this hero without invented proof.` |
| Copy | [hl-article-writing](./skills/hl-article-writing/SKILL.md) | `Use hl-article-writing to turn this brief into a complete article for our publication, in the requested language. Keep every figure sourced.` |
| Copy | [hl-de-ai-rewriting](./skills/hl-de-ai-rewriting/SKILL.md) | `Use hl-de-ai-rewriting to make this shipping notice clearer, keeping every date and fee.` |
| Copy | [hl-email](./skills/hl-email/SKILL.md) | `Use hl-email to draft a renewal reminder from this brief, with placeholders for any offer we have not supplied.` |
| Copy | [hl-email-sequence](./skills/hl-email-sequence/SKILL.md) | `Use hl-email-sequence to map a three-step welcome sequence from these recorded events.` |
| Conversion | [hl-page-cro-audit](./skills/hl-page-cro-audit/SKILL.md) | `Use hl-page-cro-audit to find what blocks booking on this clinic page, and label each hypothesis.` |
| Conversion | [hl-onboarding](./skills/hl-onboarding/SKILL.md) | `Use hl-onboarding to design the first-week flow for this fitness app from its step list.` |
| Conversion | [hl-ab-test-plan](./skills/hl-ab-test-plan/SKILL.md) | `Use hl-ab-test-plan to plan a test on this pricing toggle, with sizing from our baseline export.` |
| Channels | [hl-social](./skills/hl-social/SKILL.md) | `Use hl-social to draft two captions from this brief. Platform and market are in the brief.` |
| Channels | [hl-paid-ads](./skills/hl-paid-ads/SKILL.md) | `Use hl-paid-ads to write three search ad variants from this brief, with missing proof as placeholders.` |
| Channels | [hl-short-video](./skills/hl-short-video/SKILL.md) | `Use hl-short-video to turn this brief into a 30-second script for our chosen platform, with spoken lines, shots, on-screen text and rights checks.` |
| Analytics | [hl-tracking-plan](./skills/hl-tracking-plan/SKILL.md) | `Use hl-tracking-plan to plan the events behind this booking decision. Flag personal data.` |
| Analytics | [hl-reporting](./skills/hl-reporting/SKILL.md) | `Use hl-reporting to summarise this weekly export by channel. Name what is missing.` |

## Call a skill

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

## Update and pin

```bash
npx skills list                                   # what is installed
npx skills update hl-debug hl-tdd                 # update these skills
npx skills remove -s hl-tdd                       # remove one skill
npx skills add HugoLopes45/hl-skills#v1.0.0       # every skill at v1.0.0
```

`npx skills update` without names updates every skill in that scope, from every source. Releases follow semantic versioning; experimental skills may change in any release. See [CHANGELOG.md](./CHANGELOG.md).

## Limits

Each skill is tested against a real agent, with and without the skill. These are AI instructions, not guaranteed results: review the output. Skills run with your agent's full permissions, so read a skill before you install it. Report vulnerabilities as [SECURITY.md](./SECURITY.md) describes.

## Contribute

Read [CONTRIBUTING.md](./CONTRIBUTING.md) and [STYLE.md](./STYLE.md). MIT licensed, see [LICENSE](./LICENSE).
