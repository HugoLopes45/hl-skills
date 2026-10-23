# Skill

Input: `--skill [what the skill should do | path to an existing SKILL.md]`

Turn an intent into a skill that an agent runs well. The artifact is a file the model executes: write it like the work, not a memo about the work.

The input is the intent or the skill to review. No input: take the intent from the recent conversation; nothing there, say so and stop.

## Every run

1. State the one job in a sentence. Search the target skill collection for overlap by name, description, and topic. An existing skill covers it and the new one is not sharper: stop, do not add it. Revise an existing skill only when the user targeted it by name, path, or an explicit collection-wide request. This gate comes before any drafting.
2. Design the output contract before the steps that produce it.
3. Draft the description. It is the trigger, so it is the hardest line to get right.
4. Write the body.
5. Place it, verify it statically, and check its output.

## Format

- Path `<skills dir>/<name>/SKILL.md`. `name` is 1-64 characters of lowercase letters, digits, and single hyphens, equal to the directory name.
- Frontmatter holds `name` and `description` (max 1024 characters). Add `license`, `compatibility`, `metadata`, or `allowed-tools` only when needed. Host-specific fields work only on that host; prefer body text for rules every host must follow.
- Keep `SKILL.md` short. Long tables, catalogs, examples, and subagent prompts go in `references/<topic>.md`; link each one from the step that needs it. Scripts go in `scripts/`.

## Output contract

Write into the skill what the user receives: who reads it and when, the decision it serves, its line 1 and `Verdict:` line with the fixed verdict words, its sections in order, the view for each part, and one rendered example.

- The reader is smart but new to the domain. Line 1 and the next steps alone must tell them what happened, whether to worry, and what to do. Effect in everyday words first, then the technical name; define each term or acronym at first use; every number with its unit and meaning; each next step something a person can do now.

- Line 1: bold, one plain sentence with the answer, never a label. Then blockers and risks as plain sentences, then numbered points, then `Verdict: <word>` with the skill's fixed verdict words on its own line, and the next action last in `**Next:**`.
- Pick the view by content: a table for items with the same fields (at most 5 columns, short cells), a call tree for a flow (only nodes read or run), a file tree for layout, a timeline for events, pseudocode for logic, types and signatures for a contract, a `diff` for a change to an existing structure. Mermaid only where it renders. A view only where it beats a sentence. ASCII illustrations stay within 8 lines of 80 characters; requested code and artifacts remain complete.
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
- Cut filler, ceremony, and duplicate rules. Preserve checkable grounding, safety, permissions, and failure behavior; shorten wording without deleting those constraints.

Inside a repository with its own style guide (for example `STYLE.md`), that guide wins.

## Before done

- Frontmatter parses as YAML; `name` equals the directory name; the description has a concrete `Use when` or `Use only when` trigger.
- Every `references/` link resolves.
- The repository's validator passes when it has one (in this collection: `python3 scripts/validate.py`).
- Output check: follow the draft on two or three representative inputs, one of them an edge case. A run that is unsafe or impossible here: write the expected output and label it expected. Each human-facing output passes only when line 1 answers the request in words a newcomer understands, the `Verdict:` line sits just before `**Next:**`, no code needs a legend, each view beats the prose it replaces, facts and assumptions are apart, nothing can be cut without losing meaning, and the user can act on it without rework. An agent-facing output passes when it matches its format exactly. A failure means fixing the skill, not the sample.
- A host may need a new session to load a new skill. You cannot observe that in this turn, so do not claim it.

Return, with no preamble: line 1, bold, one plain sentence. For a written skill: what it does, in plain words. For a covered job: the existing skill and what it already does. Then explain each caveat that limits the verdict, such as a skill not run in a live session; say which rows are expected, not observed. Then the checks: a table of up to 5 checks with the fields check, input (the sample used, output checks only), and result: `passed`, `expected: written, not run`, or `failed: <reason>`. More than 5 checks: a numbered list, one check per point, with its result. Then `Verdict: Written`, or `Verdict: Covered, use <skill>`, just before `**Next:**`. `**Next:**`: start a new session so your agent app loads the skill, and run `hl-code-review` on the new file before it ships. For a covered job, `**Next:**` names the existing skill to use. Then `**Changed:** <path>` for a written skill, or `**Changed:** none`.
