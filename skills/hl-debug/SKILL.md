---
name: hl-debug
description: "Investigate a bug by first building a fast feedback loop that shows the symptom, then running discriminating experiments, and report the supported hypotheses or the defect proven by toggling it. Fixes only when asked, behind a failing regression test. Use when something fails (including a named test the user asks you to explain), behaves unexpectedly, is flaky, or got slower and the cause is unknown. Not for fixing failing pull request checks (use `hl-ci-fix`)."
---
# Debug

Input: `[bug description or report path]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Explain the cause through the reproduction and the experiment that distinguishes it from alternatives. Keep failed attempts only when they limit the conclusion or next step.

Investigate the input; if empty, the latest bug discussion. No symptom: ask.

Safety:
- Until the user asks for a fix, never edit the user's working tree: no implementation or repository configuration changes. Put experiments in a permitted temporary directory, separate from original files. An environment-provided temporary path grants no extra access.
- Explicit approval first for shared-state writes, network side effects, signing, paid model runs, or destructive probes.
- Never copy credentials.
- Commands that move HEAD (for example `git bisect`) run only in a separate worktree or clone the user approved.

## Observe

Record:
- Symptom, expected behavior and the source of that expectation, revision and environment, reproduction steps.
- Actual command results. Status: reproduced, traced, or unable to reproduce.
- That the code you read is the code that runs: branch, build artifact, version, cache.

Keep three things apart: symptom (what is observed), trigger (what changed so it shows now), defect (the wrong code or state). Removing the trigger does not fix the defect.

Intermittent failure: report failures/attempts, conditions, and the attempt budget. Ten runs are a starting sample, not proof of determinism. A factor with no observed rate change is not cleared.

## Feedback loop

Before any hypothesis, build one command that shows the user's exact symptom, and run it. Try, in order: a failing test at the closest seam, a request to the running service, a CLI run diffed against known-good output, a headless browser script, a replayed captured payload, a throwaway harness, a fuzz or bisect script.

The loop is ready when it fails for the reported reason (it matches this error message or value, not any failure), gives the same result each run (or a measured failure rate), takes seconds, and needs no human. Tighten it until it does: pin time and seeds, sharpen the assertion, cut setup. Intermittent: raise the failure rate before you investigate.

No loop possible: say so, list what you tried, and ask for an environment, a captured artifact, or access. Do not hypothesize without a loop.

## Investigate

Before testing, rank the plausible, falsifiable hypotheses without padding their count, each as "if X, then changing Y makes the symptom disappear". Include the user's suspect and test it explicitly: clear it or keep it with evidence. Run the cheapest discriminating check first.

Pick the method the evidence supports:
- Known good and bad states plus a reliable pass/fail check: bisect along the axis that differs: commits, input, configuration, dependency versions, environment, or test order. First confirm both endpoints and that the check gives the same verdict on repeated runs. With `git bisect run`, exit 0 means good, 125 means untestable, any other code from 1 to 127 means bad. Prefer a direct check when cheaper or when the trace already names the cause. The culprit is a hypothesis until toggling only its relevant change flips the symptom and you can explain the mechanism.
- Test passes alone but fails in the suite: run it after each earlier test, or bisect the list of earlier tests, to find the polluter, then find the shared state it leaves (caches, globals, environment, files, time).
- A passing and a failing case: list every difference between them (caller, input, flags, environment, version); vary one at a time.
- Large failing input: minimize it, rerunning the loop after each cut, until every part is needed.
- Hidden state: prefer a debugger with a conditional breakpoint on the broken invariant (for example `balance < 0`), then walk up the frames to where the value first went wrong. Otherwise add logs in the scratch copy only, each for one hypothesis, tagged with one unique prefix such as `[DEBUG-a4f2]`. Slowdown: measure a baseline first, then bisect.
- Intermittent failure: repeated trials with one controlled factor; record seeds and timing where available.
- Several components: log what enters and leaves each boundary; the defect is in the first component whose output is wrong while its input is correct.
- Stack trace or deterministic path: trace inputs, state, and error propagation backward as `file:line` hops. The defect is at the first hop whose state breaks an invariant the rest of the path assumes. An expected call that never happens points to its caller.
- Agent orchestration: inspect actual registration, payload, dispatch and result status, and traces. A model's account of what it loaded or why it chose a tool is not telemetry. Load no skill the user did not invoke.

Two hypotheses fail at the same place: reread that code and recheck the assumptions before another attempt. Prerequisites missing: report blocked or switch method; never fabricate evidence.

## Conclude

Reader: the person who reported the bug, deciding whether to ask for a fix. They may not know this code. Use "possible cause", "reproduction command", and "change only the suspect line" instead of "hypothesis", "loop", and "toggle". Explain a scratch copy as an isolated copy, separate from the original files.

Keep only hypotheses that observations support. Consider that the expectation itself may be wrong. For each hypothesis, one numbered item: the possible cause as a bold plain sentence, then the evidence for and against and what it does not explain. Put the next check that would tell causes apart only in Next. In the report, no hypothesis count, forced why-chain, or confidence formula; do not assume one cause explains every symptom.

In the same scratch copy, run the reproduction command by itself before editing and confirm the reported symptom. Change only the suspected defect, then rerun that command under the same conditions. Show both observed results. A failing run from the original tree does not replace the scratch baseline; without both scratch results, use `Leading explanation`, not `Defect proven`.

When the request already asks for a fix ("fix it", "find and fix"), this report is not the answer: prove the suspected defect by the toggle, then go to Fix, change the code, and report as Fix says. Otherwise report in this shape:
- Line 1, bold: one plain sentence with the cause in everyday words. Put `file:line` inside the sentence, never first. It never starts with a label or the verdict word.
- Under line 1, plain sentences without labels: who else the defect reaches ("Every late return in production is charged too much."), and what is still uncertain when that limits the answer. How you reproduced it (the command and how often it fails) goes once, in the proof point.
- Shortest complete report: cut every sentence the reader would not miss. A point that needs no explanation is its bold sentence alone. The fix is stated in Next, not also in a point.
- Then numbered points, each a bold plain sentence with its decisive evidence:
  1. Where it goes wrong: name the traced files and functions, with `file:line` anchors from numbered reads. Use prose when it explains the cause; include a call tree when it adds understanding or the user requests it. A tree has verified nodes only, one hop per line, at most 8 lines of at most 80 characters. Annotate only hops that need it: the defect, a suspected hop, or an unknown edge.
  2. The proof: show both scratch-copy states and their actual reproduction results once, in prose or a `text` block. When the trigger differs from the defect, one point that names both: the trigger (what made it show up) and the defect (what is wrong).
  3. Only when true and useful: which test, type check, or assertion could have caught it earlier.
- `Verdict: <word>` on its own line just before `**Next:**`, one of:
  - `Defect proven`: changing only the defect in the scratch copy makes the symptom disappear.
  - `Leading explanation`: the evidence supports one cause; no toggle has proven it yet.
  - `Insufficient evidence`: a symptom is given, even a vague one, but no loop can be built, or no hypothesis fits. Use the blocked form below.
  - `Stopped`: the request names no symptom at all. Use the blocked form below.
- `**Next:**` the steps a person can do now, in order: the fix at `file:line`, and its regression test with the function that test calls. When no test can reach the defect without a large rewrite, say so plainly as a design problem. A decision for the user: one question, with the default marked.
- Blocked form, when no symptom is given or no loop can be built: line 1 says in plain words what is missing and why it blocks (for example `**I can't find the cause yet: no command I can run shows the bug.**`). Then one line on what was tried and the verdict line: `Insufficient evidence` when any symptom was given, even vague, else `Stopped`. `**Next:**` holds at most 3 numbered ways to unblock, the default marked `(default)`; they appear nowhere else. No call tree, no hypotheses.
- Reader rules: lead with the cause in everyday words, then the code name. When the user named a suspect (for example float rounding), line 1 says whether it is the cause. Gloss other technical words at first use (for example `generator`: a value that can be read only once). Spell out acronyms at first use. Give each number its unit and meaning (`30 instead of 27.0`, not `1 failure`). Name code, never people; no blame, no hype. No codes or tags such as `DEFECT` or `H1`.

````markdown
**Late returns are charged from the loan start, not the due date, so fines are too high.**
Every late return in production is charged too much.

1. **The fine counts the loan period as late.**
   Fines are $0.25 a day after the due date (day 14), so 6 late days should cost $1.50.
   `test_fine_counts_from_due_date` at `test_fines.py:22` calls `fine()` at `fines.py:9`.
   At `fines.py:12`, it counts from day 0 and charges 20 days, $5.00.

2. **Counting from the due date fixes the result.**
   In the same permitted scratch copy, `pytest test_fines.py -q` ran before any edit, then after changing only the suspect line:
   ```text
   unchanged copy counts from loan start   1 failed, 3 passed
   only change    counts from due date     4 passed
   ```

3. **The existing suite had no test for a return after the due date**, so it missed this defect.

Verdict: Defect proven

**Next:**
1. Add the test `test_fine_counts_from_due_date`; it calls `fine()` directly.
2. Change `fines.py:12` to count from `loan.due`, then rerun the test.
````

Structured handoff, when needed: append YAML with `symptom`, `revision`, `methods`, `repro_status`, `repro_rate`, `hypotheses` with evidence, `unresolved_checks`, `next_action`, `blast_radius`. Never mark an unverified hypothesis as cleared for an automatic fix.

## Fix

Fix only when the user asked for a fix or approves one after the report; otherwise stop at the report. No proven defect: report and do not fix. Fix the proven defect, not the trigger or the symptom:
1. Write the regression test through the closest function that reaches the defect. Run it and see it fail for the reported reason.
2. Make the smallest change at the defect.
3. Rerun the regression test, the original loop, and the related suite. Show the results.
4. Search the working tree for your debug prefix; none may remain.

Report as in Conclude; line 1 is a plain sentence that says the defect is fixed and what it was. Preserve the traced file/function anchors, reproduction command and results, trigger/defect distinction, actual regression-before/after results, and separate scratch-copy proof. Prose may carry this evidence; use a call tree, `diff`, or proof view only when it adds understanding or the user requests it. Illustrations stay within 8 lines of 80 characters; requested code and artifacts remain complete. Never describe an ordinary before/after edit as an unobserved scratch-copy toggle. End with `Verdict: Defect proven (fixed)`, `**Next:**`, and `**Changed:** <paths>`.

After three failed fixes, stop and question the design with the user before a fourth.
