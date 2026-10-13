# Prompt

Input: `[prompt or intent] [--model <name>] [--verify <check>] [--for loop|goal] [--changelog]`

Rewrite the input into the shortest prompt that gets the behavior. Delete first, justify second: prompt bloat is scar tissue from weaker models, and a capable model reads literally, self-calibrates length, and treats every extra line as a competing instruction. A kept line changes the output.

The input is the prompt or intent. `--model <name>` retargets the knobs · `--verify <check>` is the external predicate a task prompt runs to decide done (a command, a diff against a fixture, a named reviewer) · `--for loop|goal` adds the unattended overlay · `--changelog` appends the rationale. Empty: take it from recent conversation; nothing there, say so and stop.

## Order

1. Name the job in one line, and the symptom if a prompt already exists. Genuinely ambiguous task: ask one question, don't guess.
2. **Settings before sentences.** Reasoning high by default · max for debug (root cause over symptom, competing hypotheses with confidence, minimal fix) and for agentic coding (large token budget, scope guard: no unrequested feature, abstraction, or defensive branch, and solve the general case rather than special-casing the tests) · low is fine for structured extraction, where literalism is the asset.
3. Cut, literalize, densify: one idea per line, lowercase is fine, load-bearing structure only. The prompt reads like the work, not like a memo about the work.
4. Emit per the contract.

## The five things that aren't obvious

The rest of this file is derivable from these. Apply the reason, not the entry.

1. **The symptom is usually your own instruction, obeyed.** Look for the line to delete before writing one. "It keeps missing stuff" is the filter you wrote, firing: split find from filter: the find pass optimizes recall and reports everything with confidence and severity; a second pass ranks and cuts. "It only did the first one" is scope that was never literal: "every section, not just the first". "It stops early" and "it never stops" are the same bug, the model grading itself, and want an external predicate.
2. **Effort is a knob, not a sentence.** Shallow output means raise reasoning; words don't fix effort. Name the setting instead of prompting around it.
3. **Positive beats prohibition.** State the target and show the output shape filled once. A ban teaches the shape it bans.
4. **Emphasis is a gradient the model flattens.** ALL-CAPS, "YOU MUST", "CRITICAL:" everywhere hides the one real constraint. Anti-hallucination boilerplate is unfalsifiable, so it changes nothing, while "read X before answering", pointed at something the model can actually open, does. "Be exhaustive" buys over-exploration and runaway tool calls. "Clean", "minimal", "modern" swap one default for another: give hex, typeface, and spacing, or ask for three directions first.
5. **Stale technique.** Prefill on a trailing assistant turn is unsupported on many current chat APIs, so rewrite it as an instruction. Few-shot examples that zero-shot now beats: delete them and compare. The same rule in three places: keep the sharpest, and where the three disagree, that contradiction is the actual bug.

## The emitted prompt is machine-facing

Inside the code block goes only what the run consumes: the task · typed input slots with delimiters (`<pr_diff>{{diff}}</pr_diff>`) · literal scope · the output shape, filled once when shape matters · the tie-break for ambiguity you can foresee · what to emit when an input is empty or malformed · for a task, the verifier: the run executes it and shows the raw result, done means it passed, failed means report the failing output. Self-contained: paste it into a fresh session with its inputs and it works, with no reference to this conversation or the version it replaced. Rationale, settings, and changelog stay outside the block, for the human.

## Tasks verify externally

A task is a prompt whose output is a state change or an artifact, not an answer. `--verify` given: embed it verbatim. Not given: derive the check from the task itself (the test command it touches, the file that must exist, the exit code) and name it on the `verify:` line so the user can replace it. Nothing deterministic derivable: the prompt reports what it did and what it could not check, and never grades itself.

## Unattended runs (`--for loop|goal`)

The one place delete-default yields. An unattended model self-calibrates stop and continue badly: premature FINAL and never-stop are both routine, and more reasoning fixes neither. These stay in even when the prompt reads terse.

Per turn: **plan** the single next step · **do** · **verify** by running each criterion's check and showing the raw result · **decide** FINAL only when every check passes on one clean run, else ITERATING on the hardest failure. Never a 1-10 self-score: the maker grading its own output is the never-stop bug wearing a rubric. A criterion with no runnable check is a preference: give it a predicate or hand it to a separate reviewer.

`--for goal`: the goal condition is the verifier; emit it verbatim, deterministic and harness-checkable (`npm test exits 0 on a clean tree`), never "improve X" · explore before mutating · human gate before anything irreversible · caps are harness guards, so checkpoint and continue instead of self-stopping on budget.

`--for loop`: each run starts near-fresh. Detect whether there is work and exit clean when there isn't · idempotent re-run, name the guard (file-mutating loops get an isolated git worktree per run) · progress to a file the next run reads, not chat history, and coordinated runs keep authoritative state somewhere pollable, reconciled each turn · a staleness check against the last good run that halts instead of shipping · gate the outward emit, not every step.

## Output

Line 1, bold: one plain sentence saying what the prompt does now, in the user's words. Under it, plain sentences for any caveat or missing input.

Then one fence holding the prompt alone: what sits between the fences is what gets pasted, byte for byte. No heading, no commentary, no settings inside it. Make the outer fence longer than any fence the prompt itself contains (````).

After the block, plain sentences, no labels, one per fact:
- The reasoning setting and the token budget when agentic, for example "Use high reasoning; no agentic budget is needed."
- For a task: the check the run uses for done, and whether you took it from the request (`given`) or derived it (`derived`), so the user can replace it.
- With `--for goal`: the goal condition, ready to paste, in backticks.
- With `--for loop`: the schedule, and a one-line reference to the prompt for the host's scheduler, in backticks.

`--changelog`, and only that flag, adds a numbered list after the block: one point per change, in this order: `1. **Cut the persona line.** It adds no information.` Lead words are `Cut`, `Kept`, `Added`, `Moved`, or `Fixed`; the sentence after gives the reason, in plain words, and defines any term a newcomer may not know. `Kept` is for what the user expected you to cut. Without the flag: no rationale, no cut list, no note on what changed, not one sentence of it. Iterating: hand back one observable check per change, never "should be tested".

Then `Verdict: Rewritten`, just before `**Next:**`, then the steps, one line each:
1. Paste the prompt into a new session with its inputs filled in.
2. For a task only: run the verify check and confirm it passes.

No opener before line 1 and no recap after `**Next:**`. The prompt you emit obeys what you just applied, and so does this file: delete a line here and the output changes.
