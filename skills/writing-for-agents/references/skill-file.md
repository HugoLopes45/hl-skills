# Skill

Input: `--skill [what the skill should do | path to an existing SKILL.md]`

Turn an intent into a skill that an agent runs well. The artifact is a file the model executes: write it like the work, not a memo about the work.

The input is the intent or the skill to review. No input: take the intent from the recent conversation; nothing there, say so and stop.

## Every run

1. State the one job in a sentence. Search the target skill collection for overlap by name, description, and topic. An existing skill covers it and the new one is not sharper: stop, do not add it. Never rewrite the existing skill unless the user passed its path. This gate comes before any drafting.
2. Design the output contract before the steps that produce it.
3. Draft the description. It is the trigger, so it is the hardest line to get right.
4. Write the body.
5. Place it, verify it statically, and check its output.

## Format

- Path `<skills dir>/<name>/SKILL.md`. `name` is 1-64 characters of lowercase letters, digits, and single hyphens, equal to the directory name.
- Frontmatter holds `name` and `description` (max 1024 characters). Add `license`, `compatibility`, `metadata`, or `allowed-tools` only when needed. Host-specific fields work only on that host; prefer body text for rules every host must follow.
- Keep `SKILL.md` short. Long tables, catalogs, examples, and subagent prompts go in `references/<topic>.md`; link each one from the step that needs it. Scripts go in `scripts/`.

## Output contract

Write into the skill what the user receives: its first line, its sections in order, and the view for each part.

- First line: the answer, verdict, or blocker. Then evidence and implications; the next action last, when there is one. Blockers and risks stay above the details.
- Pick the view by content: a table for items with the same fields (at most 5 columns, short cells), a call tree for a flow (only nodes read or run), a file tree for layout, a timeline for events, pseudocode for logic, types and signatures for a contract, a `diff` for a change to an existing structure. Mermaid only where it renders. A view only where it beats a sentence.
- Prose in loose ASD-STE100: short sentences, one meaning per word, active voice. Verified facts, inferences, and unknowns visibly apart. Omit empty sections. No preamble or recap.
- Deliver the artifact, not instructions to make it.
- Agent-facing formats (subagent records, handoff briefs, plans for another agent, emitted prompts, commit messages, tracker tickets) stay exact; these rules do not apply to them.

## The description is the trigger

Hosts see only the name and description when they decide to load a skill. Lead with what the skill does, then `Use when ...` with the concrete situations, one per branch. A description keyed on a common word (`code`, `test`, `skill`) loads too often; name the specific situation instead.

- Weak: `A skill for working with database queries and related tasks.`
- Sharp: `Review a SQL migration for lock risk, missing indexes, and unsafe defaults. Use before applying a schema change to production.`

A skill with side effects or cost (commit, push, deploy, external writes, paid services) says `Use only when the user explicitly asks` and acts only on that request.

## Body

- First line is the job. Then the input contract, the steps, and the output contract.
- State the target, not the banned behavior: "report every finding" beats "don't filter".
- Each step has a checkable end. A fuzzy end invites an early stop; make it checkable or split it off.
- Host-neutral: no host tool names, slash syntax, or argument variables such as `$ARGUMENTS`. When a step needs a capability some hosts lack (subagents, web access), say what to do without it.
- No named people and no voice imitation; encode the method.
- Never load another skill; name one only as a suggestion in the output.
- Cut filler, ALL-CAPS emphasis, ceremony, and generic anti-hallucination boilerplate. Every line must change the output; delete a line that does not.

Inside a repository with its own style guide (for example `STYLE.md`), that guide wins.

## Before done

- Frontmatter parses as YAML; `name` equals the directory name; the description contains the exact words `Use when`.
- Every `references/` link resolves.
- The repository's validator passes when it has one (in this collection: `python3 scripts/validate.py`).
- Output check: follow the draft on two or three representative inputs, one of them an edge case. A run that is unsafe or impossible here: write the expected output and label it expected. Each human-facing output passes only when the first line answers the request, each view beats the prose it replaces, facts and assumptions are apart, nothing can be cut without losing meaning, and the user can act on it without rework. An agent-facing output passes when it matches its format exactly. A failure means fixing the skill, not the sample.
- A host may need a new session to load a new skill. You cannot observe that in this turn, so do not claim it.

Return, first line, with no preamble before it: the skill's path, or the existing skill that already covers the job. Then a table: check, input (output checks only), result: passed, expected (written, not run), or failed with the checks it failed. Suggest a `code-review` of the new file before it ships.
