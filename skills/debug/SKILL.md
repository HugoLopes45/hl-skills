---
name: debug
description: "Investigate a bug by first building a fast feedback loop that shows the symptom, then running discriminating experiments, and report the supported hypotheses or the defect proven by toggling it. Fixes only when asked, behind a failing regression test. Use when something fails, behaves unexpectedly, is flaky, or got slower and the cause is unknown. Not for fixing failing pull request checks (use `ci-fix`)."
---
# Debug

Input: `[bug description or report path]`

Investigate the input; if empty, the latest bug discussion. No symptom: ask.

Safety:
- Until the user asks for a fix, never edit the user's working tree: no implementation or repository configuration changes. Repros and experiments go in a temporary directory or scratch copy.
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

Before testing, rank the falsifiable hypotheses (usually 2 to 5), each as "if X, then changing Y makes the symptom disappear". Include the user's suspect and test it explicitly: clear it or keep it with evidence. Run the cheapest discriminating check first.

Pick the method the evidence supports:
- Known good and bad states plus a reliable pass/fail check: bisect along the axis that differs: commits, input, configuration, dependency versions, environment, or test order. First confirm both endpoints and that the check gives the same verdict on repeated runs. With `git bisect run`, exit 0 means good, 125 means untestable, any other code from 1 to 127 means bad. Skip bisect for fewer than 5 candidates or when the trace already names the cause. The culprit is a hypothesis until toggling only its relevant change flips the symptom and you can explain the mechanism.
- Test passes alone but fails in the suite: run it after each earlier test, or bisect the list of earlier tests, to find the polluter, then find the shared state it leaves (caches, globals, environment, files, time).
- A passing and a failing case: list every difference between them (caller, input, flags, environment, version); vary one at a time.
- Large failing input: minimize it, rerunning the loop after each cut, until every part is needed.
- Hidden state: prefer a debugger with a conditional breakpoint on the broken invariant (for example `balance < 0`), then walk up the frames to where the value first went wrong. Otherwise add logs in the scratch copy only, each for one hypothesis, tagged with one unique prefix such as `[DEBUG-a4f2]`. Slowdown: measure a baseline first, then bisect.
- Intermittent failure: repeated trials with one controlled factor; record seeds and timing where available.
- Several components: log what enters and leaves each boundary; the defect is in the first component whose output is wrong while its input is correct.
- Stack trace or deterministic path: trace inputs, state, and error propagation backward as `file:line` hops. The defect is at the first hop whose state breaks an invariant the rest of the path assumes. An expected call that never happens points to its caller.
- Agent orchestration: inspect actual registration, payload, dispatch and result status, and traces. A model's account of what it loaded or why it chose a tool is not telemetry. Load no skill the user did not invoke.

Two hypotheses fail at the same place: stop and reread the code there; your model of it is wrong. Prerequisites missing: report blocked or switch method; never fabricate evidence.

## Conclude

Keep only hypotheses that observations support. Consider that the expectation itself may be wrong. For each hypothesis, one block, one field per line: hypothesis, evidence for, evidence against, unexplained symptoms, next discriminating check. In the report, no hypothesis count, forced why-chain, or confidence formula; do not assume one cause explains every symptom.

A defect is proven only when, in a scratch copy, the symptom is present with it and absent with only the defect toggled, both runs shown. Anything less stays a hypothesis.

Report, status first: the proven defect, the leading supported explanation, or insufficient evidence. When a path was traced, show it as a call tree with `file:line` per hop: verified nodes only, unknown edges marked unknown, and the proven defect hop marked, or the suspected hop labeled hypothesis. Read every file on the path with numbered output (for example `cat -n`) and take each line number from it, never from counting. Then the loop command, the hypothesis blocks, checks actually run, remaining uncertainty, who else the defect reaches (production, other callers, or only tests), likely change scope, proposed fix direction, and what would have caught the defect earlier (test, type, assertion, lint). For a proven defect, name the regression test and the seam it uses; when no seam reaches the defect, report that as an architecture finding.

Structured handoff, when needed: append YAML with `symptom`, `revision`, `methods`, `repro_status`, `repro_rate`, `hypotheses` with evidence, `unresolved_checks`, `next_action`, `blast_radius`. Never mark an unverified hypothesis as cleared for an automatic fix.

## Fix

Fix only when the user asked for a fix or approves one after the report; otherwise stop at the report. No proven defect: report and do not fix. Fix the proven defect, not the trigger or the symptom:
1. Write the regression test at the seam that reaches the defect. Run it and see it fail for the reported reason.
2. Make the smallest change at the defect.
3. Rerun the regression test, the original loop, and the related suite. Show the results.
4. Search the working tree for your debug prefix; none may remain.

Report as in Conclude, status first (for example `Status: defect proven and fixed`), then the change and the test results.

After three failed fixes, stop and question the design with the user before a fourth.
