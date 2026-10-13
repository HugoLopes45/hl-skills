---
name: hl-spike
description: "Run a time-boxed technical spike: define a testable hypothesis and budget, run the fewest discriminating experiments, and conclude proceed, pivot, or inconclusive. Use when a technical unknown blocks a decision."
---
# Spike

Input: `[topic]`

Use the input as the topic. Establish a testable hypothesis, pass and fail criteria, scope, and a time and resource budget before experiments. Ask for missing decisions one at a time; do not proceed on an undefined hypothesis. Until one is set, ask and give no PROCEED, PIVOT, or INCONCLUSIVE verdict.

Choose the fewest experiments that distinguish the outcomes, at most four per spike. For each, state what it measures and the command or observation. This skill does not authorize live, paid, destructive, or repository-changing experiments. Request approval where needed. Without approval, do not contact a production system in any way, not even a name lookup or a reachability check.

Run safe, available experiments. Record actual output and elapsed time; label unavailable experiments human-run or blocked. Missing evidence is inconclusive, not failure or success.

## Report

Reader: the person who decides whether to adopt the approach, change it, or wait. They are not a specialist in this technology. Define each term at first use: hypothesis (the claim the spike tests), budget (the time allowed), pass and fail criteria (the numbers that decide the verdict). Spell out acronyms at first use.

- Line 1, bold: one plain sentence with the answer and its measured number, within 100 characters, for example `**Yes: 200,000 rows go into the database in 0.14 seconds, under the 2-second limit.**` It never starts with a label or the verdict word.
- Under line 1, plain sentences: each blocker or precondition, for example `The live database test needs your approval, so I did not run it.`; where the experiments ran and whether scratch files remain, when that matters to the result.
- The test, in one plain sentence: what was tested, the pass number, and the time allowed and used, with units.
- Shortest complete report: cut every sentence the reader would not miss, and state each fact once.
- Then the experiments, as a numbered list. Each item is a bold sentence with the result and its unit, then the method (command or observation, in backticks), then its status in words: `I ran this`, `I did not run this: <reason>`, or `a person must run this`.
- Then what the result does not cover, in plain sentences, and what was raised but not tested, one line each.
- `Verdict: <word>` on its own line just before `**Next:**`, one of:
  - `Proceed`: the measured result meets the pass criterion.
  - `Pivot`: the measured result misses the pass criterion; choose another approach.
  - `Inconclusive`: evidence is missing or no experiment could run. It is neither a pass nor a fail.
  - `Stopped`: no hypothesis is set yet. Use the Stopped form below.
- `**Next:**` the steps a person can do now, in order.

````markdown
**Yes: Pillow makes a 1080p thumbnail in 38 ms, under the 100 ms limit.**
I tested whether Pillow resizes a 1920x1080 photo in under 100 ms, in 4 of the 15 minutes allowed.

1. **A thumbnail takes 38 ms on this laptop.**
   `python3 bench.py --n 50`: median 38 ms, slowest 61 ms. I ran this.
2. **The server is unmeasured.** It needs access I do not have, so a person must run it.

The result covers this laptop and the sample photos only. Memory use per thumbnail is not tested yet.

Verdict: Proceed

**Next:**
1. Measure 200 real photos on the server before choosing Pillow.
````

Stopped, when no hypothesis is set: line 1 says what is missing and why the spike cannot start, for example `**I can't start the spike yet: no pass or fail number is set.**`. Then a question that asks for them, then up to 3 numbered ways to unblock, the default marked:
1. Restate the question as pass and fail numbers, for example "under 2 s" (default).
2. Name the topic and the time budget, and the skill proposes the hypothesis.
3. Point to a README that states the question.

Then `Verdict: Stopped`.

No file deliverable unless requested. No `**Changed:**` line: this skill does not write to the project.
