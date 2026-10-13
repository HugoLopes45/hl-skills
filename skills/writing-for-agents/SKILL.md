---
name: writing-for-agents
description: "Write text an agent executes. By default, rewrite a raw intent, a prompt, a system prompt, or an AGENTS.md or other instruction-file snippet into the shortest text that gets the behavior, for any capable LLM; --for loop|goal tunes a prompt that runs unattended; --verify <check> gives a task prompt its done predicate. --skill writes or reviews an agent skill (SKILL.md): one job, a description that triggers at the right time, an output a person can skim, a lean body, and checks before it ships. Use when handed a prompt or instruction-file snippet to tune, tighten, de-cruft, or port to another model, even when the word \"prompt\" is never said; when a prompt misbehaves (misses items, answers shallowly, stops early, never stops, ignores the format) or is bloated with ALL-CAPS and boilerplate; or when the user wants to create, draft, or improve a skill."
---
# Writing for Agents

Input: `[text, intent, or path] [--skill] [mode options]`

With `--skill`, or when the input is a skill or a request to create one, follow [references/skill-file.md](references/skill-file.md). Otherwise follow [references/prompt.md](references/prompt.md).
