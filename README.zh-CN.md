# hl-skills

一组技能，为你的编程智能体在工程和增长两方面的每一项工作提供一套经过测试的方法。适用于 Claude Code、Codex、Cursor、Gemini CLI、GitHub Copilot、OpenCode、Pi，以及任何读取 `SKILL.md` 的智能体。

[![ci](https://github.com/HugoLopes45/hl-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/HugoLopes45/hl-skills/actions/workflows/ci.yml)
[![release](https://img.shields.io/github/v/release/HugoLopes45/hl-skills)](./CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-lightgrey)](./LICENSE)

[English](./README.md)。如果中英文内容不一致，以英文版为准。

你的智能体写得很快。它也可能靠猜、过早地附和你，并用它并不掌握的证据填补空白。每个技能都要求它拿出证据：文件和行号、测试运行、来源，或者在缺少证据的地方留下可见的占位符。

## 安装

```bash
npx skills add HugoLopes45/hl-skills
```

在你的项目中运行，然后按安装程序操作。需要 Node.js 22.20+ 和 npm。无需配置，无需服务器，无需 API 密钥。添加 `-g` 可用于本机上的每个项目，或用 `-s hl-debug -s hl-tdd` 选择技能。

然后打开一个新的智能体会话，并提出请求：

> Use hl-debug to find why this test fails only in the full suite.

## 技能

### 工程

| 领域 | 技能 | 示例 |
|---|---|---|
| 思考 | [hl-discover](./skills/hl-discover/SKILL.md) | `Use hl-discover to map this repo and show me where to start.` |
| 思考 | [hl-grill](./skills/hl-grill/SKILL.md) | `Use hl-grill to compare magic links and passwords for this app.` |
| 思考 | [hl-spec](./skills/hl-spec/SKILL.md) | `Use hl-spec to plan CSV exports with clear acceptance criteria.` |
| 思考 | [hl-challenge](./skills/hl-challenge/SKILL.md) | `Use hl-challenge to find the weak assumptions in this plan.` |
| 思考 | [hl-spike](./skills/hl-spike/SKILL.md) | `Use hl-spike to test whether SQLite can handle our write load.` |
| 思考 | [hl-adr](./skills/hl-adr/SKILL.md) | `Use hl-adr to record why we chose PostgreSQL and the cost of reversing it.` |
| 思考 | [hl-roast](./skills/hl-roast/SKILL.md) | `Use hl-roast to roast this landing page, savage level.` |
| 构建 | [hl-tdd](./skills/hl-tdd/SKILL.md) | `Use hl-tdd to reject expired invitations, test first.` |
| 构建 | [hl-tickets](./skills/hl-tickets/SKILL.md) | `Use hl-tickets to turn this feature plan into independently testable tickets.` |
| 构建 | [hl-ambitious](./skills/hl-ambitious/SKILL.md) | `Use hl-ambitious to make this task deeper without expanding its scope.` |
| 构建 | [hl-show-me](./skills/hl-show-me/SKILL.md) | `Use hl-show-me to draw how authentication works in this app.` |
| 构建 | [hl-explainer-video](./skills/hl-explainer-video/SKILL.md) （实验性） | `Use hl-explainer-video to make a short narrated video explaining CRDTs.` |
| 构建 | [hl-writing-for-agents](./skills/hl-writing-for-agents/SKILL.md) | `Use hl-writing-for-agents to make this prompt shorter without losing its requirements.` |
| 修复 | [hl-debug](./skills/hl-debug/SKILL.md) | `Use hl-debug to find why this test fails only in the full suite.` |
| 修复 | [hl-ci-fix](./skills/hl-ci-fix/SKILL.md) | `Use hl-ci-fix to fix the failing checks on this PR.` |
| 修复 | [hl-security-audit](./skills/hl-security-audit/SKILL.md) | `Use hl-security-audit to audit our password-reset flow for account-takeover risks.` |
| 修复 | [hl-improve](./skills/hl-improve/SKILL.md) | `Use hl-improve to prioritize what we should fix in this codebase.` |
| 修复 | [hl-lessons](./skills/hl-lessons/SKILL.md) | `Use hl-lessons to turn what we learned from this bug into a durable safeguard.` |
| 交付 | [hl-code-review](./skills/hl-code-review/SKILL.md) | `Use hl-code-review to review this branch for bugs and regressions.` |
| 交付 | [hl-receive-review](./skills/hl-receive-review/SKILL.md) | `Use hl-receive-review to evaluate these review comments before we make changes.` |
| 交付 | [hl-deslop](./skills/hl-deslop/SKILL.md) | `Use hl-deslop to remove unnecessary abstractions from this diff.` |
| 交付 | [hl-verify](./skills/hl-verify/SKILL.md) | `Use hl-verify to check this change against its acceptance criteria.` |
| 交付 | [hl-commit](./skills/hl-commit/SKILL.md) | `Use hl-commit to commit the staged changes.` |
| 交付 | [hl-split-pr](./skills/hl-split-pr/SKILL.md) | `Use hl-split-pr to plan smaller PRs from this oversized diff.` |
| 交付 | [hl-open-pr](./skills/hl-open-pr/SKILL.md) | `Use hl-open-pr to open a draft PR for this branch.` |
| 交付 | [hl-checkpoint](./skills/hl-checkpoint/SKILL.md) | `Use hl-checkpoint to prepare a handoff before I start a fresh session.` |
| 发布 | [hl-startup](./skills/hl-startup/SKILL.md) | `Use hl-startup to pressure-test this SaaS idea before I build it.` |
| 发布 | [hl-launch-marketing](./skills/hl-launch-marketing/SKILL.md) | `Use hl-launch-marketing to plan a two-week launch for this product.` |

### 增长与营销

| 领域 | 技能 | 示例 |
|---|---|---|
| 策略 | [hl-positioning](./skills/hl-positioning/SKILL.md) | `Use hl-positioning to state what this hot sauce should claim, from our five buyer interviews.` |
| 策略 | [hl-persona](./skills/hl-persona/SKILL.md) | `Use hl-persona to build buyer cards from these six interview notes, with no invented details.` |
| 策略 | [hl-competitor-analysis](./skills/hl-competitor-analysis/SKILL.md) | `Use hl-competitor-analysis to profile these two rivals from their dated captures.` |
| 策略 | [hl-pricing](./skills/hl-pricing/SKILL.md) | `Use hl-pricing to propose a plan structure and a test, from our buyer survey.` |
| 搜索 | [hl-seo-audit](./skills/hl-seo-audit/SKILL.md) | `Use hl-seo-audit to find why this page is blocked from search.` |
| 搜索 | [hl-keyword-research](./skills/hl-keyword-research/SKILL.md) | `Use hl-keyword-research to pick the next page to write from this Search Console export.` |
| 搜索 | [hl-content-brief](./skills/hl-content-brief/SKILL.md) | `Use hl-content-brief to brief a guide on how to chase a late invoice, for freelance designers in the United States.` |
| 搜索 | [hl-ai-search-visibility](./skills/hl-ai-search-visibility/SKILL.md) | `Use hl-ai-search-visibility to check whether ChatGPT, Perplexity, and Google AI answers can use this page.` |
| 搜索 | [hl-schema-markup](./skills/hl-schema-markup/SKILL.md) | `Use hl-schema-markup to check the JSON-LD on this product page against its visible price.` |
| 搜索 | [hl-internal-linking](./skills/hl-internal-linking/SKILL.md) | `Use hl-internal-linking to find orphan pages and broken targets in this links export.` |
| 文案 | [hl-copywriting](./skills/hl-copywriting/SKILL.md) | `Use hl-copywriting to rewrite this hero without invented proof.` |
| 文案 | [hl-article-writing](./skills/hl-article-writing/SKILL.md) | `Use hl-article-writing to turn this brief into a complete article for our publication, in the requested language. Keep every figure sourced.` |
| 文案 | [hl-de-ai-rewriting](./skills/hl-de-ai-rewriting/SKILL.md) | `Use hl-de-ai-rewriting to make this shipping notice clearer, keeping every date and fee.` |
| 文案 | [hl-email](./skills/hl-email/SKILL.md) | `Use hl-email to draft a renewal reminder from this brief, with placeholders for any offer we have not supplied.` |
| 文案 | [hl-email-sequence](./skills/hl-email-sequence/SKILL.md) | `Use hl-email-sequence to map a three-step welcome sequence from these recorded events.` |
| 转化 | [hl-page-cro-audit](./skills/hl-page-cro-audit/SKILL.md) | `Use hl-page-cro-audit to find what blocks booking on this clinic page, and label each hypothesis.` |
| 转化 | [hl-onboarding](./skills/hl-onboarding/SKILL.md) | `Use hl-onboarding to design the first-week flow for this fitness app from its step list.` |
| 转化 | [hl-ab-test-plan](./skills/hl-ab-test-plan/SKILL.md) | `Use hl-ab-test-plan to plan a test on this pricing toggle, with sizing from our baseline export.` |
| 渠道 | [hl-social](./skills/hl-social/SKILL.md) | `Use hl-social to draft two captions from this brief. Platform and market are in the brief.` |
| 渠道 | [hl-paid-ads](./skills/hl-paid-ads/SKILL.md) | `Use hl-paid-ads to write three search ad variants from this brief, with missing proof as placeholders.` |
| 渠道 | [hl-short-video](./skills/hl-short-video/SKILL.md) | `Use hl-short-video to turn this brief into a 30-second script for our chosen platform, with spoken lines, shots, on-screen text and rights checks.` |
| 分析 | [hl-tracking-plan](./skills/hl-tracking-plan/SKILL.md) | `Use hl-tracking-plan to plan the events behind this booking decision. Flag personal data.` |
| 分析 | [hl-reporting](./skills/hl-reporting/SKILL.md) | `Use hl-reporting to summarise this weekly export by channel. Name what is missing.` |

## 调用技能

| 智能体 | 项目文件夹 | 全局文件夹 | 调用技能 |
|---|---|---|---|
| [Claude Code](https://code.claude.com/docs/en/skills) | `.claude/skills/` | `~/.claude/skills/` | `/hl-debug` |
| [Codex](https://developers.openai.com/codex/skills) | `.agents/skills/` | `~/.agents/skills/` | `$hl-debug` or `/skills` |
| [Cursor](https://cursor.com/docs/skills) | `.agents/skills/` | `~/.agents/skills/` | `/hl-debug` in Agent chat |
| [Gemini CLI](https://geminicli.com/docs/cli/skills/) | `.agents/skills/` | `~/.agents/skills/` | by description |
| [GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) | `.agents/skills/` | `~/.agents/skills/` | `/hl-debug` |
| [OpenCode](https://opencode.ai/docs/skills/) | `.agents/skills/` | `~/.agents/skills/` | by description |
| [Pi](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md) | `.agents/skills/` | `~/.agents/skills/` | `/skill:hl-debug` |

当你的请求与某个技能匹配时，技能也会自行加载。安装后开启一个新会话。

## 更新和固定版本

```bash
npx skills list                                   # what is installed
npx skills update hl-debug hl-tdd                 # update these skills
npx skills remove -s hl-tdd                       # remove one skill
npx skills add HugoLopes45/hl-skills#v1.0.0       # every skill at v1.0.0
```

不带名称的 `npx skills update` 会更新该范围内来自所有来源的每个技能。发布遵循语义化版本；实验性技能可能在任何版本中变化。参见 [CHANGELOG.md](./CHANGELOG.md)。

## 局限

每个技能都在真实智能体上分别以使用和不使用该技能的方式进行测试。这些是 AI 指令，不是有保证的结果：请审查输出。技能以你的智能体的全部权限运行，因此安装前请先阅读技能。请按 [SECURITY.md](./SECURITY.md) 的说明报告漏洞（英文）。

## 参与贡献

阅读 [CONTRIBUTING.md](./CONTRIBUTING.md) 和 [STYLE.md](./STYLE.md)（英文）。采用 MIT 许可证，参见 [LICENSE](./LICENSE)。
