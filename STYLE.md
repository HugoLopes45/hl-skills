# Skill style guide

Every skill in this repository follows this guide. Write the smallest thing a copy of you could regenerate it from. Compress language, not the investigation or delivered behavior.

## Format

One skill is one directory, `skills/<name>/SKILL.md`. Frontmatter holds `name` (equal to the directory name) and `description`; add `license`, `compatibility`, or `metadata` only when needed. Long tables, catalogs, and prompts for subagents go in `references/` next to `SKILL.md`.

English only. Host-neutral: no host-specific tool names, slash-command syntax, argument variables such as `$ARGUMENTS`, or config paths. Name other skills in backticks (`code-review`). When a step needs a capability some hosts lack (subagents, web access), say what to do without it.

No named people. A skill encodes a method, not an imitation of someone's voice or opinions.

## Prose

Use imperative rules, short sentences, clear fragments, and one term per concept. Delete filler, routine tool narration, decorative sections, and duplicate summaries. No invented shorthand or broken grammar for its own sake.

Preserve negation, conditions, causality, and step order. Keep literal code, commands, paths, identifiers, numbers, units, versions, and quoted errors exact. Preserve frontmatter, input syntax, permissions, and output contracts unless the change explicitly targets them.

Merge overlapping rules; retain reinforcement for critical constraints and examples that distinguish behavior. Clarity wins: warnings, approvals, and ambiguous sequences need complete wording. Honor requested depth and format. Human-facing artifacts use complete sentences, not compressed fragments.

## Output

A person skims what a skill returns. Design the output before the steps: what the user receives, its first line, and the view for each part. Show the shape; use prose only for what has no shape. Each skill names the views its output uses.

- First line: the answer (verdict, result, or blocker). Then evidence and implications; the next action last, when there is one. Blockers, risks, and caveats stay above the details.
- A view only where it beats a sentence; a one-line answer needs no diagram. One view per point, next to the one or two sentences it supports:

| Content | View |
|---|---|
| Items with the same fields (findings, claims, options, checks) | Table: at most 5 columns, short cells; a heading per group instead of a repeated column |
| Items with long fields | One block per item, one field per line |
| Runtime or failure flow | Call tree, `file:line` per node; only nodes you read or ran, unknown edges marked unknown |
| Layout, ownership, scope of a change | Shallow file tree, one responsibility per entry |
| Events in order | Timeline, one `time or step - event` line each |
| Logic or an algorithm | Pseudocode |
| A contract before the code exists | Types and signatures |
| A change to an existing structure | `diff` of that structure (tree, call tree, pseudocode, or code) |
| Interactions or state transitions | Mermaid sequence or state diagram where it renders (a pull request, a Markdown page on a forge, an HTML page that loads Mermaid); elsewhere a call tree or `state --event--> state` lines |
| A UI, a layout, or a numeric trend | One focused HTML page |
| A concept the reader must step through or vary | An interactive HTML page: step-through, a slider per parameter, or animation |

- Prefer text views: they read the same in a terminal and on a rendered page.
- Prose follows ASD-STE100 loosely: procedure sentences up to 20 words, descriptive up to 25; one meaning per word; active voice; articles kept. Replace jargon, or define it once.
- A long explanation: offer an interactive HTML page; a video only on explicit request (`explainer-video`).
- Keep verified facts, inferences, and unknowns visibly apart: a status column or a label.
- Deliver the requested artifact (file, table, diagram, code) within the skill's permissions, not instructions to make it.
- Quote only the log lines that prove a point; raw logs are never the result.
- Omit empty sections; write "none" only where absence is the answer (no findings, no blockers).
- No preamble, recap, or closing summary.
- Agent-facing formats (subagent records, handoff briefs, plans for another agent, emitted prompts, commit messages, tracker tickets) stay exact; these rules do not apply to them.

Before a skill ships, check its output on representative inputs, as `writing-for-agents --skill` describes.

## Implementation workflows

YAGNI: deletion before addition. Build the smallest correct version; challenge the remaining requirements in the same reply. Label unfinished scope.

Understand the request, affected flow, and callers first. Prefer existing behavior, repository code, standard library, native platform, installed dependency, then minimal new code. Never weaken validation, data-loss handling, security, accessibility, or edge-case correctness to reduce size.

Delete tautological code and tests. Remove checks already guaranteed by types or earlier guards on the same path. Comments explain why, never restate code.

## Evidence and scope

Missing evidence means unknown, not success. Label proposed criteria and expected output as not observed. Name blockers and checks not run. No output-length, finding, or test-count quota proves quality or savings.

The description is the trigger: state what the skill does, then `Use when ...`. Hosts may load a skill whenever its description matches the request. A skill with side effects (commit, push, pull request, CI changes) says `Use only when the user explicitly asks` in its description and acts only on that request. A skill never loads another skill on its own; it may name one as a suggestion.
