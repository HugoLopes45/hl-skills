<div align="center">

# hl-skills

### Build something worth shipping.

27 skills for your coding agent, from questioning an idea to debugging a failure to shaping a launch.

**[Get started](#get-started)** · [Find your next move](#find-your-next-move)

[![ci](https://github.com/HugoLopes45/hl-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/HugoLopes45/hl-skills/actions/workflows/ci.yml)
[![license](https://img.shields.io/badge/license-MIT-lightgrey)](./LICENSE)

</div>

## Don’t settle for “looks good.”

```text
Use hl-debug: this test passes alone but fails in the full suite.
Find the cause. Don’t change my code.
```

That’s the idea: ask for the work you actually need, not another confident answer.

## Find your next move

| You want to… | Reach for… |
|---|---|
| Turn “what if?” into something buildable | [hl-grill](./skills/hl-grill/SKILL.md) · [hl-spec](./skills/hl-spec/SKILL.md) |
| Raise the bar without growing the task | [hl-ambitious](./skills/hl-ambitious/SKILL.md) |
| Stop patching symptoms | [hl-debug](./skills/hl-debug/SKILL.md) |
| Build with proof, not hope | [hl-tdd](./skills/hl-tdd/SKILL.md) · [hl-verify](./skills/hl-verify/SKILL.md) |
| Cut the noise from a diff | [hl-deslop](./skills/hl-deslop/SKILL.md) · [hl-code-review](./skills/hl-code-review/SKILL.md) |
| Give your launch a story worth telling | [hl-launch-marketing](./skills/hl-launch-marketing/SKILL.md) |

**[Explore all 27 skills →](./skills/)**

## Get started

With Node.js 22.20+ and npm, run this in your project for Claude Code:

```bash
npx skills@1.7.2 add HugoLopes45/hl-skills --skill '*' --agent claude-code
```

Open a fresh Claude Code session. Pick a real bug. Start with `/hl-debug`.

<details>
<summary>Codex, OMP, and more ways to install</summary>

**Codex:** replace `--agent claude-code` with `--agent codex`, then invoke `$hl-debug` in a fresh session.

**Start small:** replace `--skill '*'` with `--skill hl-debug` to install just one.

**Use across projects:** add `--global` to install for your user.

**OMP on macOS or Linux:** install into the shared skills directory, then link into OMP:

```bash
npx skills@1.7.2 add HugoLopes45/hl-skills --global --skill '*' --agent codex
mkdir -p ~/.omp/agent/skills
ln -s ~/.agents/skills/hl-* ~/.omp/agent/skills/
```

Start a new OMP session and use `/skill:hl-debug`. Existing destinations are not overwritten; inspect them rather than forcing replacement.

For other agents and installer options, see the [skills CLI](https://github.com/vercel-labs/skills).

</details>

---

[Contribute](./CONTRIBUTING.md) · [Security](./SECURITY.md) · [MIT](./LICENSE)
