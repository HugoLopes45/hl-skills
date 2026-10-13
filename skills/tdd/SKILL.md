---
name: tdd
description: "Implement one observable behavior through a verified red-green-refactor cycle at an agreed seam: failing test first, smallest change, then refactor. Use when implementing a behavior or slice test-first. Not for finding the cause of a bug (use `debug`)."
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

First line: the behavior, and whether every case ended green. Then a table: case, step (red, already green, green, refactor), command, observed result. Passing tests prove only the behavior they cover.
