---
name: hl-writing-for-agents
description: "Write text an agent executes. By default, rewrite a raw intent, a prompt, a system prompt, or an AGENTS.md or other instruction-file snippet into the shortest text that gets the behavior, for any capable LLM; --for loop|goal tunes a prompt that runs unattended; --verify <check> gives a task prompt its done predicate. --skill writes or reviews an agent skill (SKILL.md): one job, a description that triggers at the right time, an output a person can skim, a lean body, and checks before it ships. Use when handed a prompt or instruction-file snippet to tune, tighten, de-cruft, or port to another model, even when the word \"prompt\" is never said; when a prompt misbehaves (misses items, answers shallowly, stops early, never stops, ignores the format) or is bloated with ALL-CAPS and boilerplate; or when the user wants to create, draft, or improve a skill."
---
# Writing for Agents

Input: `[text, intent, or path] [--skill] [mode options]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Deliver the complete prompt or skill. Distinguish static checks, expected examples, and observed runs; keep host capabilities and limits explicit.

With `--skill`, or when the input is a skill or a request to create one, follow [references/skill-file.md](references/skill-file.md). Otherwise follow [references/prompt.md](references/prompt.md).

## Output

Reader: someone who asked for a prompt or a skill, and will paste or save the result. The decision: use the result, or supply what is missing.

- Line 1, bold: one plain sentence that answers the request, in the user's words.
- Under line 1: plain sentences for anything that limits the result, such as a prompt you did not run.
- Prompt mode: the rest follows the Output section of [references/prompt.md](references/prompt.md). The prompt in its fence is the artifact, shown whole.
- Skill mode: the check table in [references/skill-file.md](references/skill-file.md).
- `Verdict: <word>` on its own line just before `**Next:**`, one fixed word:
  - `Rewritten`: prompt mode; the prompt is ready to paste.
  - `Written`: skill mode; the skill file is saved.
  - `Covered, use <skill>`: skill mode; an existing skill already does the job, so no file is written.
  - `Stopped`: input is missing. See below.
- `**Next:**` holds the steps a person takes now, in order.
- `**Changed:** <path>` in skill mode: the saved file, or `none`.
- Missing input: line 1 says what is missing and why it blocks; then `Verdict: Stopped`; then `**Next:**` with up to 2 numbered ways out, the default first, listed nowhere else. Prompt mode: `**I need the prompt before I can tune it.**`, then in Next: 1. Paste the prompt or give its path (default). 2. Describe the task in one sentence.
- Human-facing prose: when `verifier` is used, define it once as the check that proves the task is done. Do not introduce it in missing-input replies.

The example below fixes the shape of a skill-mode reply, not its content.

````markdown
**I wrote a skill that finds broken links in a draft release note.**
I did not run it in a live session. The row marked expected is not observed.

| Check | Input | Result |
|---|---|---|
| Name matches the folder | frontmatter | passed |
| Description says `Use when` | frontmatter | passed |
| No host-only tool names | grep for them | passed |
| Note with no links | a sample draft | expected: written, not run |

Verdict: Written

**Next:**
1. Start a new session so your agent app loads the skill.
2. Run `hl-code-review` on `skills/release-notes-links/SKILL.md` before it ships.

**Changed:** `skills/release-notes-links/SKILL.md`
````
