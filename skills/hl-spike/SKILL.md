---
name: hl-spike
description: "Run a time-boxed technical spike: define a testable hypothesis and budget, run the fewest discriminating experiments, and conclude proceed, pivot, or inconclusive. Use when a technical unknown blocks a decision."
---
# Spike

Input: `[topic]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Report the deciding observation and criterion with their method and limits. Keep missing evidence explicit; omit routine experiment narration.

Use the input as the topic. Establish a testable hypothesis, pass and fail criteria, scope, and a time and resource budget before experiments. Ask for missing decisions one at a time; do not proceed on an undefined hypothesis. Until one is set, ask and give no PROCEED, PIVOT, or INCONCLUSIVE verdict.

Choose the fewest experiments that distinguish the outcomes. Do not omit an experiment needed to resolve the hypothesis. For each, state what it measures and the command or observation. This skill does not authorize live, paid, destructive, or repository-changing experiments. Request approval where needed. Without approval, do not contact a production system in any way, not even a name lookup or a reachability check.

Run each approved experiment command by itself. Take exit status from the tool result, not an appended status-printing command.

Run safe, available experiments. Record actual output and elapsed time; label unavailable experiments human-run or blocked. Missing evidence is inconclusive, not failure or success.

## Report

Reader: the person who decides whether to adopt the approach, change it, or wait. They are not a specialist in this technology. Define each term at first use: hypothesis (the claim the spike tests), budget (the time allowed), pass and fail criteria (the observable conditions that decide the verdict). Spell out acronyms at first use.

- Line 1, bold: one plain sentence with the observed answer and its deciding criterion; include a number when the criterion is quantitative, for example `**Yes: 200,000 rows go into the database in 0.14 seconds, under the 2-second limit.**` It never starts with a label or the verdict word.
- Under line 1, plain sentences: each blocker or precondition, for example `The live database test needs your approval, so I did not run it.`; where the experiments ran and whether scratch files remain, when that matters to the result.
- Present the deciding observation and criterion once in the answer. Attach the method, repeat count, observed spread, and measurement boundaries to that result without repeating it. Report the investigation time allowed and used when it limits the conclusion.
- One experiment may use prose; multiple experiments may use numbered points with their actual results and units. State whether each ran and why any did not. Commands identify methods, not instructions for the reader; human-run checks belong only in Next.
- Preserve hardware and data scope, excluded work, what was raised but not tested, and uncertainty. Do not treat a sample as representative performance.
- `Verdict: <word>` on its own line just before `**Next:**`, one of:
  - `Proceed`: the measured result meets the pass criterion.
  - `Pivot`: the observed result meets the agreed fail criterion; choose another approach.
  - `Inconclusive`: evidence is missing, no experiment could run, or the result meets neither agreed criterion. It is neither a pass nor a fail.
  - `Stopped`: no hypothesis is set yet. Use the Stopped form below.
- `**Next:**` the steps a person can do now, in order.

````markdown
**Yes: Pillow makes a 1080p thumbnail in a median 38 ms, under the 100 ms limit.**
I ran `python3 bench.py --n 50` only on this laptop, using only the 1920x1080 sample photos; `--n` sets the resize trial count. The median is the middle timing; the slowest result was 61 ms.
The spike used 4 of the 15 minutes allowed. The server was not measured because I lack access.

Memory use per thumbnail is not tested yet.

Verdict: Proceed

**Next:**
1. Measure 200 real photos on the server before choosing Pillow.
````

Stopped, when no hypothesis is set: line 1 says what is missing and why the spike cannot start, for example `**I can't start the spike yet: no observable pass or fail condition is set.**`. Then `Verdict: Stopped`. Put the missing-decision question only in `**Next:**`, which holds up to 3 numbered ways to unblock, the default marked; they appear nowhere else:
1. Restate the question as observable pass and fail conditions, for example "under 2 s" (default).
2. Name the topic and the time budget, and the skill proposes the hypothesis.
3. Point to a README that states the question.

No file deliverable unless requested. No `**Changed:**` line: this skill does not write to the project.
