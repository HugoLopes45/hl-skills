# hl-skills：让你的编程智能体拿出证据的 Agent Skills

**别再只听智能体的一面之词。**

hl-skills 是一套免费、开源的 Agent Skills，包含 50 多个技能，适用于 Claude Code、Codex、Cursor、Gemini CLI、GitHub Copilot、OpenCode、Pi，以及任何读取 `SKILL.md` 的智能体。每个技能为你的智能体在工程或增长中的一项工作提供一套经过测试的方法：调试、代码审查、安全、需求规格、SEO、文案、定价等。

[![ci](https://github.com/HugoLopes45/hl-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/HugoLopes45/hl-skills/actions/workflows/ci.yml)
[![release](https://img.shields.io/github/v/release/HugoLopes45/hl-skills)](./CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-lightgrey)](./LICENSE)

[English](./README.md)。如果中英文内容不一致，以英文版为准。

[带来的变化](#带来的变化) · [安装](#安装) · [工程技能](#工程技能) · [增长技能](#增长技能) · [常见问题](#常见问题)

你的智能体写得很快。它也可能靠猜、过早地附和你，并用它并不掌握的证据填补空白。有了 hl-skills，它会拿出证据：文件和行号、它运行的命令及结果、来源，或者在缺少证据的地方留下可见的占位符。

## 带来的变化

| 单独使用时，智能体可能 | 使用 hl-skills 后，它必须 | 技能 |
|---|---|---|
| 什么都没运行就说“完成了” | 根据真实命令结果，把每项需求报告为通过、失败、未验证或受阻 | [hl-verify](./skills/hl-verify/SKILL.md) |
| 修复一个从未复现的缺陷 | 先复现症状，再只在一个失败的回归测试保护下修复 | [hl-debug](./skills/hl-debug/SKILL.md) |
| 为了让你满意而批准你的计划 | 给出继续、先修复或停止的结论，并在存在时指出更小的版本 | [hl-challenge](./skills/hl-challenge/SKILL.md) |
| 接受每一条审查意见 | 对照代码，为每条意见决定同意、推迟、反对或澄清 | [hl-receive-review](./skills/hl-receive-review/SKILL.md) |
| 在落地页里填入你从未提供的证据 | 写下 `[PLACEHOLDER: proof needed]`，并说明替换它所需的证据 | [hl-copywriting](./skills/hl-copywriting/SKILL.md) |
| 陈述它从未核实的事实 | 让每个结论都基于你的证据或它观察到的结果，并以结论判定收尾 | 每个技能 |

## 安装

一条命令。无需配置，无需服务器，无需 API 密钥。

```bash
npx skills add HugoLopes45/hl-skills
```

在你的项目中运行，然后按安装程序操作。需要 Node.js 22.20+ 和 npm。添加 `-g` 可用于本机上的每个项目，或用 `-s hl-debug -s hl-tdd` 选择技能。

然后打开一个新的智能体会话，试试下面任意一条：

> Use hl-roast to roast this README, savage level.
>
> Use hl-debug to find why this test fails only in the full suite.
>
> Use hl-challenge to find the weak assumptions in this plan.

### 调用技能

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

## 工程技能

从第一个想法到合并的拉取请求。找到你所处的阶段，然后复制提示词。

[写代码之前](#写代码之前) · [构建之中](#构建之中) · [出问题时](#出问题时) · [合并之前](#合并之前) · [发布之前](#发布之前)

### 写代码之前

*你有一个想法、一个粗略的计划，或者一个还不熟悉的代码库。*

| 技能 | 你得到 | 试试这条提示词 |
|---|---|---|
| [hl-discover](./skills/hl-discover/SKILL.md) | 陌生代码库的地图：技术栈、命令、从哪里开始 | `Use hl-discover to map this repo and show me where to start.` |
| [hl-grill](./skills/hl-grill/SKILL.md) | 真正不同的方案对比，再追问直到计划清晰 | `Use hl-grill to compare magic links and passwords for this app.` |
| [hl-spec](./skills/hl-spec/SKILL.md) | 一份带可测试验收标准的功能计划 | `Use hl-spec to plan CSV exports with clear acceptance criteria.` |
| [hl-challenge](./skills/hl-challenge/SKILL.md) | 对计划的结论：继续、先修复或停止 | `Use hl-challenge to find the weak assumptions in this plan.` |
| [hl-spike](./skills/hl-spike/SKILL.md) | 一次限时实验，结论为继续、转向或无定论 | `Use hl-spike to test whether SQLite can handle our write load.` |
| [hl-adr](./skills/hl-adr/SKILL.md) | 一份记录选项和撤销成本的决策记录 | `Use hl-adr to record why we chose PostgreSQL and the cost of reversing it.` |
| [hl-roast](./skills/hl-roast/SKILL.md) | 一次有趣又诚实的吐槽，每个笑点都指向真实缺陷 | `Use hl-roast to roast this landing page, savage level.` |

### 构建之中

*你知道要做什么了。现在测试先行，小步构建。*

| 技能 | 你得到 | 试试这条提示词 |
|---|---|---|
| [hl-tdd](./skills/hl-tdd/SKILL.md) | 按红、绿、重构实现一个行为，先写失败的测试 | `Use hl-tdd to reject expired invitations, test first.` |
| [hl-tickets](./skills/hl-tickets/SKILL.md) | 细粒度切片，每片一个拉取请求，输出为文件或 GitHub issue | `Use hl-tickets to turn this feature plan into independently testable tickets.` |
| [hl-ambitious](./skills/hl-ambitious/SKILL.md) | 更高的任务标准，范围不变 | `Use hl-ambitious to make this task deeper without expanding its scope.` |
| [hl-show-me](./skills/hl-show-me/SKILL.md) | 用图回答：图示、树、表格或时间线 | `Use hl-show-me to draw how authentication works in this app.` |
| [hl-explainer-video](./skills/hl-explainer-video/SKILL.md) （实验性） | 一个主题的简短配音讲解视频 | `Use hl-explainer-video to make a short narrated video explaining CRDTs.` |
| [hl-writing-for-agents](./skills/hl-writing-for-agents/SKILL.md) | 为智能体执行而写的提示词和指令 | `Use hl-writing-for-agents to make this prompt shorter without losing its requirements.` |

### 出问题时

*测试失败、CI 变红，或者某处看起来不安全。*

| 技能 | 你得到 | 试试这条提示词 |
|---|---|---|
| [hl-debug](./skills/hl-debug/SKILL.md) | 缺陷的已证实原因，来自一个能复现症状的循环 | `Use hl-debug to find why this test fails only in the full suite.` |
| [hl-ci-fix](./skills/hl-ci-fix/SKILL.md) | 修好失败的 PR 检查，且不削弱测试或 CI | `Use hl-ci-fix to fix the failing checks on this PR.` |
| [hl-security-audit](./skills/hl-security-audit/SKILL.md) | 一份从源码追踪、按优先级排序的安全报告 | `Use hl-security-audit to audit our password-reset flow for account-takeover risks.` |
| [hl-reverse-engineering](./skills/hl-reverse-engineering/SKILL.md) | 从可引用的证据出发，弄清已发布的应用、二进制文件、软件包或扩展如何工作、改了什么、是否应保留 | `Use hl-reverse-engineering to tell me if this ad blocker .crx is safe to keep.` |
| [hl-pentest](./skills/hl-pentest/SKILL.md) | 经授权、有边界、带观察证据的渗透测试 | `Use hl-pentest to plan paranoid tests for this staging API. Do not contact it yet.` |
| [hl-security-fix](./skills/hl-security-fix/SKILL.md) | 从根源修复漏洞，再复测攻击和绕过方式 | `Use hl-security-fix to close this cross-tenant export flaw and verify the fix.` |
| [hl-improve](./skills/hl-improve/SKILL.md) | 交给另一个智能体执行的优先级修复计划，从不修改源码 | `Use hl-improve to prioritize what we should fix in this codebase.` |
| [hl-lessons](./skills/hl-lessons/SKILL.md) | 针对错误的最低成本持久修复：一项检查或一条规则 | `Use hl-lessons to turn what we learned from this bug into a durable safeguard.` |

三个安全技能都默认使用 paranoid 验证。这只增加审查强度，不扩大权限或范围。审计只审查源码；渗透测试需要明确的主动测试授权；安全修复需要修复请求。

### 合并之前

*代码能跑了。现在证明它、清理它、交付它。*

| 技能 | 你得到 | 试试这条提示词 |
|---|---|---|
| [hl-code-review](./skills/hl-code-review/SKILL.md) | 带位置、触发条件、后果和证据的审查发现 | `Use hl-code-review to review this branch for bugs and regressions.` |
| [hl-receive-review](./skills/hl-receive-review/SKILL.md) | 对每条意见给出同意、推迟、反对或澄清 | `Use hl-receive-review to evaluate these review comments before we make changes.` |
| [hl-deslop](./skills/hl-deslop/SKILL.md) | 从变更中移除 AI 垃圾代码和同义反复，或为现有代码提出清理计划 | `Use hl-deslop to remove unnecessary abstractions from this diff.` |
| [hl-verify](./skills/hl-verify/SKILL.md) | 每项需求的通过、失败、未验证或受阻 | `Use hl-verify to check this change against its acceptance criteria.` |
| [hl-commit](./skills/hl-commit/SKILL.md) | 基于已暂存变更的提交信息 | `Use hl-commit to commit the staged changes.` |
| [hl-split-pr](./skills/hl-split-pr/SKILL.md) | 把大 diff 拆成有序、可审查的拉取请求 | `Use hl-split-pr to plan smaller PRs from this oversized diff.` |
| [hl-open-pr](./skills/hl-open-pr/SKILL.md) | 带验证、风险和恢复说明的草稿拉取请求 | `Use hl-open-pr to open a draft PR for this branch.` |
| [hl-checkpoint](./skills/hl-checkpoint/SKILL.md) | 清空上下文前保存决策、证据和下一步 | `Use hl-checkpoint to prepare a handoff before I start a fresh session.` |

### 发布之前

*产品已经成形。先检验想法，再规划发布。*

| 技能 | 你得到 | 试试这条提示词 |
|---|---|---|
| [hl-startup](./skills/hl-startup/SKILL.md) | 把一个想法从零推进到保留或放弃的结论 | `Use hl-startup to pressure-test this SaaS idea before I build it.` |
| [hl-launch-marketing](./skills/hl-launch-marketing/SKILL.md) | 14 天发布计划、渠道实验和内容引擎 | `Use hl-launch-marketing to plan a two-week launch for this product.` |

## 增长技能

从你主张什么到你衡量什么。每个技能都基于你提供的材料：简报、访谈、导出数据和页面。

[想清楚要主张什么](#想清楚要主张什么) · [被找到](#被找到) · [写好文字](#写好文字) · [把访客变成用户](#把访客变成用户) · [触达用户](#触达用户) · [衡量结果](#衡量结果)

### 想清楚要主张什么

*决定你卖什么、卖给谁、和谁竞争、定什么价。*

| 技能 | 你得到 | 试试这条提示词 |
|---|---|---|
| [hl-positioning](./skills/hl-positioning/SKILL.md) | 基于买家证据的定位陈述 | `Use hl-positioning to state what this hot sauce should claim, from our five buyer interviews.` |
| [hl-persona](./skills/hl-persona/SKILL.md) | 来自访谈、评论和工单的用户画像，不含任何编造 | `Use hl-persona to build buyer cards from these six interview notes, with no invented details.` |
| [hl-competitor-analysis](./skills/hl-competitor-analysis/SKILL.md) | 注明日期的竞品档案，事实与推测分开 | `Use hl-competitor-analysis to profile these two rivals from their dated captures.` |
| [hl-pricing](./skills/hl-pricing/SKILL.md) | 价格结构、价格区间，以及面向新买家的测试 | `Use hl-pricing to propose a plan structure and a test, from our buyer survey.` |
| [hl-win-loss](./skills/hl-win-loss/SKILL.md) | 赢单和丢单的原因，按买家原话编码并计数 | `Use hl-win-loss to read why we lose to a rival from these deal records.` |
| [hl-marketing-plan](./skills/hl-marketing-plan/SKILL.md) | 周期营销计划：至多三个押注，按漏斗阶段的行动，停止标准 | `Use hl-marketing-plan to plan next quarter's bets.` |

### 被找到

*找出阻碍你的页面出现在搜索和 AI 回答中的问题，再决定下一篇写什么。*

| 技能 | 你得到 | 试试这条提示词 |
|---|---|---|
| [hl-seo-audit](./skills/hl-seo-audit/SKILL.md) | 搜索审核、网站结构、迁移检查和排名诊断 | `Use hl-seo-audit to find why this page is blocked from search.` |
| [hl-keyword-research](./skills/hl-keyword-research/SKILL.md) | 来自买家用语和 Search Console 的关键词和主题集群 | `Use hl-keyword-research to pick the next page to write from this Search Console export.` |
| [hl-content-brief](./skills/hl-content-brief/SKILL.md) | 一份页面简报：查询、意图、答案、大纲和待引用的事实 | `Use hl-content-brief to brief a guide on how to chase a late invoice, for freelance designers in the United States.` |
| [hl-ai-search-visibility](./skills/hl-ai-search-visibility/SKILL.md) | 页面能否在 AI 回答中被找到和引用 | `Use hl-ai-search-visibility to check whether ChatGPT, Perplexity, and Google AI answers can use this page.` |
| [hl-schema-markup](./skills/hl-schema-markup/SKILL.md) | 对照页面可见内容检查结构化数据 | `Use hl-schema-markup to check the JSON-LD on this product page against its visible price.` |
| [hl-internal-linking](./skills/hl-internal-linking/SKILL.md) | 孤立页面，以及指向失效、重定向或 noindex 页面的链接 | `Use hl-internal-linking to find orphan pages and broken targets in this links export.` |
| [hl-link-building](./skills/hl-link-building/SKILL.md) | 外链计划：目标页面、链接站点、外联草稿与检查 | `Use hl-link-building to plan which sites should link to our buyer guide.` |
| [hl-local-visibility](./skills/hl-local-visibility/SKILL.md) | 本地列表、评价与线索回复的排序修复清单 | `Use hl-local-visibility to audit how my business shows in local search.` |
| [hl-app-store-listing](./skills/hl-app-store-listing/SKILL.md) | 审核或起草应用商店列表字段，依据商店现行规则核对 | `Use hl-app-store-listing to rewrite my app store title and keywords.` |

### 写好文字

*基于你的简报写页面、文章和邮件，保留每一个事实。*

| 技能 | 你得到 | 试试这条提示词 |
|---|---|---|
| [hl-copywriting](./skills/hl-copywriting/SKILL.md) | 基于已提供事实的网站与产品文案、标语和界面微文案 | `Use hl-copywriting to rewrite this hero without invented proof.` |
| [hl-article-writing](./skills/hl-article-writing/SKILL.md) | 基于你的简报和来源的解释性文章 | `Use hl-article-writing to turn this brief into a complete article for our publication, in the requested language. Keep every figure sourced.` |
| [hl-de-ai-rewriting](./skills/hl-de-ai-rewriting/SKILL.md) | 更直白的文字，保留每个主张、数字和名称 | `Use hl-de-ai-rewriting to make this shipping notice clearer, keeping every date and fee.` |
| [hl-email](./skills/hl-email/SKILL.md) | 一封邮件、媒体推介、更正或回复，围绕一个行动 | `Use hl-email to draft a renewal reminder from this brief, with placeholders for any offer we have not supplied.` |
| [hl-email-sequence](./skills/hl-email-sequence/SKILL.md) | 生命周期和外联邮件序列：触发条件、时机、跳过规则和退出条件 | `Use hl-email-sequence to map a three-step welcome sequence from these recorded events.` |

### 把访客变成用户

*找出阻碍访客的因素，再规划能给出答案的测试。*

| 技能 | 你得到 | 试试这条提示词 |
|---|---|---|
| [hl-page-cro-audit](./skills/hl-page-cro-audit/SKILL.md) | 访客与页面主要行动之间的障碍 | `Use hl-page-cro-audit to find what blocks booking on this clinic page, and label each hypothesis.` |
| [hl-onboarding](./skills/hl-onboarding/SKILL.md) | 从首次运行到首次获得价值的最短路径 | `Use hl-onboarding to design the first-week flow for this fitness app from its step list.` |
| [hl-lead-lifecycle](./skills/hl-lead-lifecycle/SKILL.md) | 线索阶段、资格判定、分配，以及向销售的交接 | `Use hl-lead-lifecycle to write the stages and handoff rules from my won and lost leads.` |
| [hl-churn-prevention](./skills/hl-churn-prevention/SKILL.md) | 自愿与非自愿流失的拆分、含一次挽留优惠的取消流程，以及扣款失败的挽回规则 | `Use hl-churn-prevention to plan a cancel flow from our cancellation export.` |
| [hl-ab-test-plan](./skills/hl-ab-test-plan/SKILL.md) | 一次 A/B 测试，含指标和基于你的基线的样本量 | `Use hl-ab-test-plan to plan a test on this pricing toggle, with sizing from our baseline export.` |

### 触达用户

*社交帖子、广告和短视频，按你简报中的平台撰写。*

| 技能 | 你得到 | 试试这条提示词 |
|---|---|---|
| [hl-social](./skills/hl-social/SKILL.md) | 适合简报中平台的帖子、轮播图、评论和回复 | `Use hl-social to draft two captions from this brief. Platform and market are in the brief.` |
| [hl-paid-ads](./skills/hl-paid-ads/SKILL.md) | 适用于任何广告平台、市场和货币的广告文案 | `Use hl-paid-ads to write three search ad variants from this brief, with missing proof as placeholders.` |
| [hl-short-video](./skills/hl-short-video/SKILL.md) | 含台词、镜头和屏幕文字的短视频脚本 | `Use hl-short-video to turn this brief into a 30-second script for our chosen platform, with spoken lines, shots, on-screen text and rights checks.` |
| [hl-referral-program](./skills/hl-referral-program/SKILL.md) | 不超过成本上限的推荐奖励，含规则和衡量方案 | `Use hl-referral-program to design a referral reward that stays under our acquisition target.` |
| [hl-creator-deal](./skills/hl-creator-deal/SKILL.md) | 达人匹配度、付费试用合作、简报、合作条款和衡量方案 | `Use hl-creator-deal to evaluate this creator's fit and brief a sponsored post.` |
| [hl-event-plan](./skills/hl-event-plan/SKILL.md) | 单场活动的办、试办、调整或放弃决定，含活动流程和复盘口径 | `Use hl-event-plan to decide whether this workshop is worth its budget.` |
| [hl-public-relations](./skills/hl-public-relations/SKILL.md) | 媒体计划、推介信、新闻稿、回应评论和危机临时声明 | `Use hl-public-relations to plan press coverage for our product launch.` |
| [hl-text-messaging](./skills/hl-text-messaging/SKILL.md) | 选择加入的短信方案：同意证明、流程规格、退订规则、顾问问题 | `Use hl-text-messaging to plan the restock text flow and its opt-in form.` |
| [hl-prospecting](./skills/hl-prospecting/SKILL.md) | 根据提供的记录生成带来源的潜客名单和外联方案 | `Use hl-prospecting to build a sourced prospect list of independent bakeries in our town.` |
| [hl-sales-enablement](./skills/hl-sales-enablement/SKILL.md) | 基于已提供证据的销售资料，每项主张标注来源 | `Use hl-sales-enablement to draft a one-pager for a champion.` |

### 衡量结果

*发布前规划事件，发布后读懂数字。*

| 技能 | 你得到 | 试试这条提示词 |
|---|---|---|
| [hl-tracking-plan](./skills/hl-tracking-plan/SKILL.md) | 围绕一个决策的事件、指标、负责人和隐私检查 | `Use hl-tracking-plan to plan the events behind this booking decision. Flag personal data.` |
| [hl-reporting](./skills/hl-reporting/SKILL.md) | 基于你的导出数据的绩效报告，并指出缺口 | `Use hl-reporting to summarise this weekly export by channel. Name what is missing.` |

## 更新和固定版本

```bash
npx skills list                                   # what is installed
npx skills update hl-debug hl-tdd                 # update these skills
npx skills remove -s hl-tdd                       # remove one skill
npx skills add HugoLopes45/hl-skills#v1.0.0       # every skill at v1.0.0
```

不带名称的 `npx skills update` 会更新该范围内来自所有来源的每个技能。发布遵循语义化版本；实验性技能可能在任何版本中变化。参见 [CHANGELOG.md](./CHANGELOG.md)。

## 常见问题

### 什么是 Agent Skill？

Agent Skill 是一个包含 `SKILL.md` 文件的文件夹。当你调用该技能，或你的请求与技能描述匹配时，智能体会加载它。每个技能都是可读的文本，因此你可以在安装前先阅读它。

### hl-skills 支持哪些智能体？

Claude Code、Codex、Cursor、Gemini CLI、GitHub Copilot CLI、OpenCode、Pi，以及任何读取 `SKILL.md` 的智能体。各智能体的文件夹和调用命令见[调用技能](#调用技能)。

### hl-skills 免费吗？

免费。hl-skills 采用 MIT 许可证，无需账号、服务器或 API 密钥。

### 技能和提示词有什么不同？

提示词只要求一个结果。技能为你的智能体提供一套完整的方法：何时使用、步骤、证据规则、何时停止，以及一份以结论判定收尾的报告。

## 局限

结构检查已通过；智能体输出评估尚未完成。这些是 AI 指令，不是有保证的结果：请审查输出。技能以你的智能体的全部权限运行，因此安装前请先阅读技能。请按 [SECURITY.md](./SECURITY.md) 的说明报告漏洞（英文）。

## 参与贡献

阅读 [CONTRIBUTING.md](./CONTRIBUTING.md) 和 [STYLE.md](./STYLE.md)（英文）。采用 MIT 许可证，参见 [LICENSE](./LICENSE)。
