# Lenses

Input: `--lens [<lens>] | --panel [--mode <mode>] [--depth quick|deep] [target]`

A lens is a fixed method: it changes what you check and report, not your tone.

## Pick

- `--lens <lens>`: that lens. `--lens` alone: pick one. `--panel`: run a panel.
- `--mode`: a mode of the lens. Default: the mode marked `(default)` in the lens file.
- `--depth quick` (default): under 300 words: the first two lines, then one numbered list of at most five items, at most 30 words each, with no nested lists or code; the smaller version, if any, is one of the five. This replaces the mode's sections, tables, and views. `--depth deep`: the mode's sections, as long as the target needs, no padding.
- The rest is the target: a path or pasted text; if empty, the most recent work in the conversation. No target: ask and stop.

`--lens` with no name: pick the one whose "Use for" line best fits the target, and add your pick's reason to the first line.

| Lens | Use for | File |
|---|---|---|
| `minimalist` | Cut code, layers, and dependencies to what correctness needs | [minimalist.md](minimalist.md) |
| `failure-hunter` | Hidden state, boundaries, and failures that appear only in production | [failure-hunter.md](failure-hunter.md) |
| `data-model` | Untangle braided concerns; values versus mutable places; data-first design | [data-model.md](data-model.md) |
| `distributed` | Partitions, clocks, retries, idempotence, consistency claims | [distributed.md](distributed.md) |
| `operability` | Instrumentation, runbooks, on-call readiness | [operability.md](operability.md) |
| `boring-stack` | Stack choice, monolith versus services, dependency cost | [boring-stack.md](boring-stack.md) |
| `agent-tooling` | Agent setups: skills, hooks, subagents, tool servers, instruction files | [agent-tooling.md](agent-tooling.md) |
| `teacher` | Explain a concept from the ground up with a worked example | [teacher.md](teacher.md) |
| `discovery` | Should we build this: outcome, evidence, riskiest assumption | [discovery.md](discovery.md) |

Read only the chosen lens file, then follow it within the depth's format.

## Rules for every lens

- First line: the parsed lens, mode, depth, and target.
- Second line: the mode's verdict or takeaway, wherever the mode file lists it; a mode with neither gets a one-line answer. Then the body for the depth; do not repeat the verdict.
- Show shapes as views, not paragraphs: a call tree for a failure path, a `diff` for a cut, types and signatures for a model, pseudocode for an algorithm, a table for a comparison.
- Cite the target: `file:line`, a quoted sentence, a number. Label any claim you cannot cite `assumption` or `estimate`.
- State uncertainty once, where it applies; do not hedge every sentence.
- Name concrete things: the component, the metric, the segment, the failure scenario. Generic advice does not count.
- The target matches the lens's "Stand down" line: say the lens does not fit and suggest a better one.
- Read-only unless the user asks for edits. Without that request, put code a mode writes or cuts in the reply or a temporary directory.
- Never load another skill.

## Panel

`--panel [target]` runs 3 to 5 lenses on the same target, each in its default mode.

1. Pick 3-5 lenses whose "Use for" lines fit the target, covering different angles: one that questions the framing, one that hunts failures, one that judges cost or value. Print `Panel: <lens>, <lens>, ...: <one-line reason>`.
2. With subagents: run each lens in its own subagent, all in parallel. Give each one the lens file content, the target, the depth, and the rules above, and nothing about the other lenses. Wait for every lens to return before you answer, and leave no background job or monitor running. Without subagents: run the lenses one after another and state that they were not independent.
3. Print a table: lens, verdict. Then each result under `## <lens>`, as returned.
4. End with `## Where they disagree`: each real disagreement in one line, with the lens names on each side; none: say so. Never merge the lenses into one recommendation; the user decides.
