---
name: hl-tdd
description: "Implement one observable behavior through a verified red-green-refactor cycle at an agreed seam: failing test first, smallest change, then refactor. Use when implementing a behavior or slice test-first. Not for finding the cause of a bug (use `hl-debug`)."
---
# TDD

Input: `[behavior or slice]`

The behavior is the input, else the current slice's outcome. For a slice, its Acceptance defines done. Name the `AC-N` id of each case that comes from one. No behavior: ask.

Before editing, trace the affected flow and its callers. Reuse repository code, the standard library, platform features, or installed dependencies when they provide the behavior. No speculative scaffolding, no code golf.

Name the seam: the public interface where the test observes the behavior. Prefer a seam that already exists, and the highest one that reaches the behavior. When the request, slice, or plan does not already fix the seam (a named file and function does), propose one with what it catches and what it misses, and get agreement before the first test.

1. Write one behavioral test in the project's test conventions. Start with the thinnest useful path.
2. Run it. It must fail because the behavior is missing or wrong, not because of the environment or a wrong API. Read the actual error: a missing symbol is a valid red only when it is the symbol this cycle adds; otherwise find the real cause.
3. Already green: if existing code provides the behavior, keep the test as regression coverage and report it; otherwise the test misses the behavior: fix it. Never delete or weaken a valid test to force red.
4. Make the smallest production change. Rerun the test, then the relevant suite.
5. Refactor without changing behavior; rerun the checks. On failure, fix or revert only your own changes.

Repeat for each relevant boundary and failure case, one test per cycle. Do not write all tests first: they lock in imagined behavior.

Test rules:
- Each test must fail if the behavior regresses. Do not test what types guarantee. Take expected values from an independent source: a literal, a worked example, the spec; never recompute them with production logic. Examples: `references/tests.md`.
- Mock external boundaries when needed; never mock the behavior under test.
- Never skip a failing check, weaken an expectation to match a bug, or make production code return only the tested answer.
- Fix a wrong test only with evidence, then repeat step 2.

## Report

Reader: the developer who asked for the behavior and decides whether to keep the change. They know the code but may not know this cycle. Define each term once at first use: red (a test that fails because the behavior is missing), green (it passes), refactor (tidy the code without changing behavior), seam (the public entry point the test calls), `AC-N` (the acceptance criterion from the plan). In the output, say "fails before the change" and "passes" rather than red and green, except in the verdict word. Say "fails before the change" only for a run you saw; a case you did not run is unverified. Name a criterion by its words; give its id only where the reader must find it.

- Line 1, bold: one plain sentence that says what now works, in the behavior's own words, within 100 characters. It never starts with a label or the verdict word.
- Under line 1, plain sentences: what the passing tests do not cover, when that limits the verdict; each case that is already passing before the change, with the reason.
- One table, one row per case, in the order written: `Case` (the behavior in plain words, with its expected value), `Source` (a worked example, `spec.md:3`, never the code under test), `Before the change` (the failure you saw, or `already passed`), `Now` (`passes`, or the failure). Under it, one sentence with the test command and its final result.
- Shortest complete report: cut every sentence the reader would not miss.
- `Verdict: <word>` on its own line just before `**Next:**`, one of:
  - `Green`: every case ended green. Each case failed before the change, or is marked already passing: the code already did it, and the test stays as regression coverage.
  - `Red`: a case still fails. Name it.
  - `Stopped`: the behavior or the seam is missing. Use the Stopped form below.
- `**Next:**` and `**Changed:** <paths>`.

````markdown
**A rental costs 3 euros per hour after the first free hour; both cases pass now.**
The tests do not cover rentals longer than 24 hours.

| Case | Source | Before the change | Now |
|---|---|---|---|
| The first hour is free | `spec.md:3` | fails: 3 euros, not 0 | passes |
| Three hours cost 6 euros | `spec.md:5` | fails: 9 euros, not 6 | passes |

`pytest -q`: 2 passed.

Verdict: Green

**Next:**
1. Review the diff in `rental.py`, then commit when ready.

**Changed:** `rental.py`, `test_rental.py`
````

Stopped, when no behavior is named: line 1 says what is missing in plain words (for example `**I can't write a test yet: no behavior is named.**`). Then a question that asks for it, then up to 3 numbered ways to unblock, the default marked:
1. Name the behavior in one sentence, with one input and its expected output. (default)
2. Point to the slice or plan that holds the acceptance criteria.
3. Name the file and function to test.

Then `Verdict: Stopped`.

Stopped, when the seam is not fixed before the first test: line 1 says the seam must be agreed first and why, in plain words. Then a `text` block with `seam`, `catches`, and `misses`, then one question with at most 4 options and the default marked. Then `Verdict: Stopped`.

Reader rules: cite each expected value by its source (a worked example, `spec.md:3`), never by the code under test. Gloss mock on first use: a stand-in for something outside the project, such as a payment service.
