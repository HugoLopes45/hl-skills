# Lenses

Input: `--lens [<lens>] | --panel [--mode <mode>] [--depth quick|deep] [target]`

A lens is a fixed method: it changes what you check and report, not your tone.

## Pick

- `--lens <lens>`: that lens. `--lens` alone: pick one. `--panel`: run a panel.
- `--mode`: a mode of the lens. Default: the mode marked `(default)` in the lens file.
- `--depth quick` (default): under 300 words: the first two lines, then one numbered list of at most five items, at most 30 words each, with no nested lists or code; the smaller version, if any, is one of the five. This replaces the mode's sections, tables, and views. `--depth deep`: the mode's sections, as long as the target needs, no padding.
- The rest is the target: a path or pasted text; if empty, the most recent work in the conversation. No target: ask and stop with the no-target form in SKILL.md, ending `Verdict: Stopped`.

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

- Line 1, bold: one plain sentence within 100 characters that names the lens and the target and gives the takeaway, e.g. "plan.md leaves the invite link open to anyone who gets it (failure-hunter lens)." Never open with the lens name.
- Then the body for the depth: findings as a numbered list, each a bold plain sentence then one or two sentences; a short view only when it shows a shape (a failure path, a `diff` for a cut, types for a model), at most 8 lines. No lens codes or tags in the reply.
- When the mode lists a verdict: `Verdict: <the mode's verdict word>` on its own line just before `**Next:**`. Then `**Next:**` with the steps the lens names, in order.
- Cite the target: `file:line`, a quoted sentence, a number. Say in words when a claim is a guess or an estimate.
- State uncertainty once, where it applies; do not hedge every sentence.
- Plain words: the verdict in everyday words first. Define a lens term once at first use, in a few words.
- Name concrete things: the component, the metric, the segment, the failure scenario. Generic advice does not count.
- The target matches the lens's "Stand down" line: say the lens does not fit and suggest a better one.
- Read-only unless the user asks for edits. Without that request, put code a mode writes or cuts in the reply or a temporary directory.
- Never load another skill.

## Panel

`--panel [target]` runs 3 to 5 lenses on the same target, each in its default mode.

1. Pick 3-5 lenses whose "Use for" lines fit the target, covering different angles: one that questions the framing, one that hunts failures, one that judges cost or value. State the reason in the answer.
2. With subagents: run each lens in its own subagent, all in parallel. Give each one the lens file content, the target, the depth, and the rules above, and nothing about the other lenses. Wait for every lens to return before you answer, and leave no background job or monitor running. Without subagents: run the lenses one after another and state that they were not independent.
3. Answer in this order:
   - Line 1, bold: where the lenses agree and where they split, in plain words (`Two of three lenses say fix first; they split on the queue.`). Never merge them into one recommendation; the user decides.
   - One line per lens: `- <lens>: <verdict>`, in place of a table.
   - `## Where they disagree`: each real disagreement in one line, with the lens names on each side; none: say so.
   - Each result under `## <lens>`, as returned, without repeating findings already shared above.
   - One plain sentence just before the verdict: which lenses ran, why, and whether they ran independently.
