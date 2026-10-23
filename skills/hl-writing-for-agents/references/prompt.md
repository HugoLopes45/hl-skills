# Prompt

Input: `[prompt or intent] [--model <name>] [--verify <check>] [--for loop|goal] [--changelog]`

Rewrite the input into the shortest prompt that gets the behavior. Delete repetition, preserve operational constraints, and check whether each remaining instruction changes the intended output.

The input is the prompt or intent. `--model <name>` retargets the knobs · `--verify <check>` is the external predicate a task prompt runs to decide done (a command, a diff against a fixture, a named reviewer) · `--for loop|goal` adds the unattended overlay · `--changelog` appends the rationale. Empty: take it from recent conversation; nothing there, say so and stop.

## Order

1. Name the job in one line, and the symptom if a prompt already exists. Genuinely ambiguous task: ask one question, don't guess.
2. **Check supported settings.** Use the host's documented controls when available. Do not assume a reasoning setting or larger budget fixes the symptom; compare results before recommending a change.
3. Cut, literalize, densify: one idea per line, lowercase is fine, load-bearing structure only. The prompt reads like the work, not like a memo about the work.
4. Emit per the contract.

## The five things that aren't obvious

The rest of this file is derivable from these. Apply the reason, not the entry.

1. **Test the instruction against the symptom.** Look for a conflicting or unnecessary line before adding one. Consider separating candidate discovery from filtering, making scope explicit, or adding an observable stop condition. Check which change addresses the symptom; do not assume the cause.
2. **Separate settings from instructions.** Name only controls the target host supports. Preserve the task's evidence and scope requirements regardless of settings.
3. **Show the target.** Use a filled example when shape matters. Keep explicit prohibitions needed for safety, permissions, or correctness.
4. **Make constraints concrete.** Reserve emphasis for critical rules. Prefer checkable grounding such as "read X before answering". Specify coverage and stop conditions instead of "be exhaustive". Replace vague design words with supplied colors, type, and spacing; ask when the missing choice matters.
5. **Check compatibility.** Verify techniques and settings against the target API's current documentation. Keep examples that clarify behavior; compare before removing them. Merge duplicate rules and resolve contradictions.

## The emitted prompt is machine-facing

Inside the code block goes only what the run consumes: the task · typed input slots with delimiters (`<pr_diff>{{diff}}</pr_diff>`) · literal scope · the output shape, filled once when shape matters · the tie-break for ambiguity you can foresee · what to emit when an input is empty or malformed · for a task, the verifier: the run executes it and shows the raw result, done means it passed, failed means report the failing output. Self-contained: paste it into a fresh session with its inputs and it works, with no reference to this conversation or the version it replaced. Rationale, settings, and changelog stay outside the block, for the human.

## Tasks verify externally

A task is a prompt whose output is a state change or an artifact, not an answer. `--verify` given: embed it verbatim. Not given: derive the check from the task itself (the test command it touches, the file that must exist, the exit code) and name it on the `verify:` line so the user can replace it. Nothing deterministic derivable: the prompt reports what it did and what it could not check, and never grades itself.

## Unattended runs (`--for loop|goal`)

Unattended runs need an observable stop condition, permission boundaries, and a checkpoint. Preserve these when shortening the prompt.

Per turn: **plan** the single next step · **do** · **verify** by running each criterion's check and showing the raw result · **decide** FINAL only when every check passes on one clean run, else ITERATING on the hardest failure. Never a 1-10 self-score: the maker grading its own output is the never-stop bug wearing a rubric. A criterion with no runnable check is a preference: give it a predicate or hand it to a separate reviewer.

`--for goal`: the goal condition is the verifier; emit it verbatim, deterministic and harness-checkable (`npm test exits 0 on a clean tree`), never "improve X" · explore before mutating · human gate before anything irreversible · respect runtime, spending, and tool limits; checkpoint before a limit when possible, and never exceed it without approval.

`--for loop`: each run starts near-fresh. Detect whether there is work and exit clean when there isn't · idempotent re-run, name the guard (file-mutating loops get an isolated git worktree per run) · progress to a file the next run reads, not chat history, and coordinated runs use the host's existing durable state and coordination · a staleness check against the last good run that halts instead of shipping · gate the outward emit, not every step.

## Output

Line 1, bold: one plain sentence saying what the prompt does now, in the user's words. Under it, plain sentences for any caveat or missing input.

Then one fence holding the prompt alone: what sits between the fences is what gets pasted, byte for byte. No heading, no commentary, no settings inside it. Make the outer fence longer than any fence the prompt itself contains (````).

After the block, plain sentences, no labels, one per fact:
- The documented reasoning setting and any approved token budget, when applicable, for example "The intended setting is high reasoning; no agentic budget is needed."
- For a task: whether the artifact's check came from the request (`given`) or was derived (`derived`), and any limit on what it proves. Define verifier only when the term is used.
- With `--for goal`: any limitation on checking the artifact's goal condition, without repeating the condition.
- With `--for loop`: the intended schedule and the prompt's location. Keep scheduler setup instructions only in Next.

`--changelog`, and only that flag, adds a numbered list after the block: one point per change, in this order: `1. **Cut the persona line.** It adds no information.` Lead words are `Cut`, `Kept`, `Added`, `Moved`, or `Fixed`; the sentence after gives the reason, in plain words, and defines any term a newcomer may not know. `Kept` is for what the user expected you to cut. Without the flag: no rationale, no cut list, no note on what changed, not one sentence of it. Iterating: hand back one observable check per change, never "should be tested".

Then `Verdict: Rewritten`, just before `**Next:**`, then the steps, one line each:
1. Set any supported, approved settings, then paste the complete prompt into a new session with its inputs filled in. For an unattended loop, use the stated schedule and prompt location in the host's scheduler.
2. For a task only: run the artifact's verify check and confirm it passes; if the check was derived, confirm it matches the intended outcome first.

No opener before line 1 and no recap after `**Next:**`. The prompt you emit obeys what you just applied, and so does this file: delete a line here and the output changes.
