# 贡献指南

[English](./CONTRIBUTING.md)。如果中英文内容不一致，以英文版为准。

参与贡献即表示您同意遵守[行为准则](./CODE_OF_CONDUCT.zh-CN.md)。

## 工作流程

本地检查需要 Python 3、`pytest`、`ruff`、`ffmpeg` 和 `ffprobe`。缺少相应工具时会跳过媒体检查；被跳过的检查不能作为发布证据。安装还需要与所选 skills CLI 版本兼容的 Node.js 和 npm。

```bash
git clone git@github.com:HugoLopes45/hl-skills.git
cd hl-skills
git checkout -b feature/<short-name>
# 添加或编辑技能
python3 scripts/validate.py
ruff check --select C901 .
python3 -m unittest discover scripts
python3 -m unittest discover evals
npx skills add . --list            # 检查 CLI 能否找到该技能
git commit -m "feat: add <skill>"
gh pr create
```

变更通过针对 `main` 的拉取请求提交。拉取请求采用 squash 合并，因此拉取请求的标题会成为 `main` 上的提交。标题必须遵循 Conventional Commits，例如 `feat(hl-tdd): add --watch`。CI 会检查标题格式。

## 版本与发布

发布遵循语义化版本。提交类型决定下一个版本号：

| 变更 | 提交 | 版本 |
|---|---|---|
| 重命名或删除技能，或更改技能的调用方式 | `feat!:` 或 `BREAKING CHANGE:` 页脚 | major |
| 新技能、新模式或新参数 | `feat:` | minor |
| 修复错误或不清晰的行为 | `fix:` | patch |
| `docs:`、`refactor:`、`test:`、`ci:`、`chore:` | | 单独提交不发布版本 |

描述以“Experimental: behavior and inputs may change in any release.”结尾的技能不在上表范围内。其变更使用 `feat:` 或 `fix:`，绝不产生 major 版本。移除该标记后，技能即转为稳定版。

[release-please](https://github.com/googleapis/release-please) 会在 `main` 上保持一个发布拉取请求处于打开状态。它汇总版本号的变更和 `CHANGELOG.md` 条目。合并该拉取请求后，会打上 `vX.Y.Z` 标签并发布 GitHub release。如需指定版本，请在提交中添加 `Release-As: X.Y.Z` 页脚。

## 目录结构

```
skills/<name>/SKILL.md          一个技能
skills/<name>/references/       技能按需加载的长篇材料
scripts/validate.py             格式与链接检查，由 CI 运行
scripts/test_validate.py        validate.py 的测试
evals/                          行为评测及其检查，参见 evals/README.zh-CN.md
STYLE.md                        技能的编写方式，参见 STYLE.zh-CN.md
```

## 添加技能

1. 确认没有现有技能已经完成该工作。新技能必须比现有技能更精准。
2. 创建 `skills/<name>/SKILL.md`：

   ```yaml
   ---
   name: <name>            # hl- 前缀，小写，使用连字符，与目录名相同
   description: "<What it does>. Use when <trigger>."
   ---
   ```

3. 按 [STYLE.zh-CN.md](./STYLE.zh-CN.md) 编写正文：仅使用英文，与宿主无关，少于 500 行，长篇材料放入 `references/`。技能正文保持英文，不翻译为中文。
4. 将技能添加到 `README.md` 中对应的表格。
5. 运行 `python3 scripts/validate.py` 并修复所有错误。CI 会运行相同的检查，并使用 `skills` CLI 安装每个技能。

`hl-writing-for-agents --skill` 模式会逐步完成这些步骤。

## 规则

- 一个目录对应一个技能。不允许嵌套技能。
- 仅使用英文。
- 不包含机密信息、个人绝对路径或内部主机名。
- 不点名具体的人。编码的是方法，而不是某个人。
- 描述即触发条件。描述模糊会导致技能永远不被加载，或在错误的时机加载。
- 具有副作用的技能（提交、推送、创建 issue）须写明“Use only when the user explicitly asks”。
- 删除或重命名技能会破坏现有安装。请将其标记为破坏性变更，并在拉取请求描述中说明。

## 评审

提交拉取请求前，可使用本仓库中的这些技能：`hl-code-review`、`hl-deslop`、`hl-verify`；当差异超过约 200 行或混合了多个关注点时，使用 `hl-split-pr`。
