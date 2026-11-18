---
name: hl-deslop
description: "Remove AI-generated slop, hallucinations, and tautologies: style tells (narrating comments, defensive cruft on trusted paths, type escapes, needless nesting, one-call wrappers), dead weight (unused code, speculative generality, placeholder residue, reinvented helpers, production code only tests use), tests that guard no behavior (restating the implementation, unable to fail, duplicated), false claims (comments the code contradicts, phantom references, fabricated numbers, doc drift, error-message drift). On a change, edits only changed lines. On existing code (a named path outside the change, or --all), maps the code, double-checks each candidate with a tool, and proposes a plan before editing. The lint, including its complexity rule, must pass without weakening. --report lists findings without editing. Use when AI-written code was generated or accepted, before committing, when a diff smells generated, or when a file, module, or test suite feels bloated, brittle, or over-defended."
---
# Deslop

Input: `[path] [--base <ref>] [--staged] [--all] [--report]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Report meaningful removals and how behavior was checked. Keep public contracts, safety checks, accessibility, and unrelated edits intact; omit routine cleanup narration.

Remove the tells of AI-written content from a change, then make the rest read like the file it lives in. Three kinds:
- Noise: true but worthless (narration, ceremony, padding, tautologies: tests and checks that restate what something else already guarantees). Delete.
- Dead weight: code or prose that serves nothing (unused, unreachable, speculative, leftover). Delete.
- Lies: claims the artifact contradicts (stale comments, phantom references, invented numbers). Fix to match reality, delete, or flag when the lie may mark a live bug.

Default move: delete. Noise or dead weight qualifies only if removing it changes nothing a reader, the type checker, or the runtime relies on. A lie fix qualifies only if the truth is checkable in the repository and the fix states it.

## Gates

Every edit passes all five:
1. Behavior unchanged. If removal could change runtime behavior, it is not slop; leave it. A fix never adds behavior: no new fallbacks, defaults, or handling. The tests and the lint pass at least as well as before; never raise a lint threshold, add a disable pragma, skip a test, or loosen an expectation to make a check pass.
2. Code is the source of truth for prose about it. Never edit code to satisfy a comment or doc. Decide a comment-code disagreement on evidence:
   - Comment rot: an existing test or caller pins the code's behavior, or git history shows the comment predates a later code change. Fix or delete the prose.
   - Possible bug: nothing pins the behavior, and the comment is newer than the code or may record intent the code fails to implement. Flag it; edit neither side.
3. Diff only. Editable lines are the diff's added lines plus lines an in-scope edit mechanically forces (re-indenting after flattening a wrapping `if`). Never the rest of a hunk's context; never a whole function for one changed line. A fix that needs other lines is flagged, not applied. This limits edits, not reads: verifying a claim may need any file. In existing-code mode, editable lines are the plan items the user approved.
4. Unsure: flag, do not delete. A comment that might say why, a guard that might catch a real failure, a claim you cannot verify: keep it and list it for a human.
5. Double-checked: a reading of the code and, where the Double-check table requires one, an observed mechanical check agree. Name what already guarantees the removed item. The checks disagree, or a required mechanical check could not run: flag.

On prose, gate 1 means meaning unchanged, except that false meaning has no protection: correcting a wrong claim is the fix.

## Order

1. Before editing, run the typecheck, the lint, and the tests, found from the project's configuration, and record the results as the baseline. Report whether the lint enforces a complexity rule; the project has none: say so and add none.
2. Truth catalog first. Check every comment you plan to delete as noise against the code it describes: one that narrates and lies is a possible-bug flag; deleting it as style destroys the evidence.
3. Code catalog.
4. Double-check every candidate. Existing-code mode: map first, propose the plan, and stop (see Existing code).
5. Verify and report (see Output). Done means the lint exits 0. A function still above the complexity limit: delete only tautological branches inside the diff or the approved plan, never a branch a caller can reach; still above: report the function and its score, and leave the split to the user.

## Scope

The input sets what to scan. Default: every change between the merge base and the working tree (committed, staged, unstaged). Base: the merge base with the configured default branch or the verified target of `refs/remotes/origin/HEAD`; never assume `main` or `master`. None resolves: stop and ask for `--base <ref>`; never widen to the whole repository.
- `--base <ref>`: the diff base.
- `--staged`: staged changes only. The reply says in one line whether unstaged changes exist and that they were not reviewed.
- A path: only that file's or directory's changed lines.
- `--all`, or a named path with no changes: existing code, changed or not, in the named path or the whole repository. Find sources and tests from the build and test configuration; never assume directory names. This is the only mode that edits unchanged code, and only after the user approves a plan (see Existing code).

Out of scope even when the diff touches them:
- Generated files: a `@generated`, `Code generated by`, or `DO NOT EDIT` header, `linguist-generated` in `.gitattributes`, or the repository's build-output paths. A filename convention alone is a hint; verify it, and report when a file's status is a guess.
- Vendored code and lockfiles.
- Snapshots, fixtures, cassettes (`__snapshots__/`, `*.snap`, recorded HTTP): content must byte-match a captured value. Flag a tell against the source that produced it; never edit in place.
- String literals that are program output: error messages, log text, UI copy, payload fields. Tests, alert rules, and other services may match their exact bytes. Flag slop inside them; never edit.

Diff mode, and not a Git repository or no changes in scope: print `Nothing to deslop: clean tree or no changes in scope.` and stop.

## Code catalog

Match the literal syntax in the changed lines, apply the fix, honor the keep condition.

1. Narrating comments: a comment restating the line below (`// increment count` over `count++`, `# fetch the user` over `user = get_user()`); banner dividers (`// ---- helpers ----`); a docstring that only echoes the signature; chat voice (`// feel free to adjust this`, `// you can customize the threshold`, `// let's add a helper here`, `// sorry, this is a bit hacky`). Delete. Keep a comment that says why, records a non-obvious constraint, or links an issue.
2. Defensive cruft on trusted paths: `catch (e) { console.error(e); throw e }`; `if (!x) return` on a value the types guarantee non-null; `?? []`, `|| {}`, `?.` on values that cannot be nullish here; a null check one line after a non-null assignment; a `try` around a whole function when one call inside can raise (narrow it); a range check or conversion an earlier guard on the same path already guarantees. Delete, except:
   - Trace the value to its entry point. A value from `JSON.parse`, `fetch().json()`, an external SDK, an `any`/`unknown` cast, or a database row crossed an unpoliced boundary; its guard stays.
   - Security guards are never cruft: sanitization, escaping, path checks, and authorization depend on every caller in the repository.
   - A catch that logs context is deletable only when an upstream handler captures the same context.
   Keep any guard for a failure that can occur on this path.
3. Type escapes: `as any`, `: any`, `as unknown as T`, `@ts-ignore`, `@ts-expect-error`, `# type: ignore`, a bare `except:`, `.unwrap()` or `!` added to silence the checker. Replace with the real type or a handled error. Handled means failing the way the function already fails elsewhere, never a new silent default (`?? ({} as Config)` swaps a crash for wrong data). Cannot tell why the escape was needed: flag; do not guess. Keep only at a genuinely untyped boundary, with a comment saying so.
4. Needless nesting: `if (cond) { <rest of function> }` that inverts to `if (!cond) return;`; `else` after `return` or `throw`; arrow-shaped pyramids. Flatten with early returns. Keep nesting that maps to real branching.
5. Ceremony: `const result = f(); return result;`; a one-call wrapper used once (inline it only if its definition is in your changed lines; a pre-existing wrapper your diff made single-use is flagged, not edited); an `else` duplicating a fall-through; a literal restated where a constant exists; a rename or re-export that adds nothing. Cut. Keep an extraction that is reused or names a non-obvious step.
6. Idiom drift: new code disagrees with the file on quote style, import grouping, naming case, error handling, comment density, or test shape. Conform to the file, with two limits: never respell a name that is an interface (serialized field, database column, i18n key, URL parameter, public export; check for a schema, migration, or locale file first); the file's idiom never overrides the catalogs (a file that narrates every line does not license new narrating comments). The file wins even when the new style is better; raise the file's own style problem separately.
7. Dead weight the change added: an import, variable, parameter, or export the diff introduces and nothing uses; a helper never called; an unreachable branch; a feature flag or config key nothing reads; production code only tests use (reset hooks, test-only getters), deleted with those tests. Before deleting, search the identifier and its plain-string form across the repository (source, config, IaC, SQL, CI). Dynamic dispatch (`obj[name]`, `getattr`, DI registries, decorator self-registration) counts as use. An export reachable from the package's public entry point, or an environment or config key that infrastructure outside the repository may read, is flagged possibly-external, never deleted. Delete only on an empty search with none of these exceptions.
8. Speculative generality: a parameter every caller passes the same value; an `options` object with one shape ever constructed; an interface or base class with one implementation; a `mode` or `type` switch with one arm exercised. Inline the single case; for an exported or public signature, flag instead. Keep generality an existing caller uses or the task explicitly requested.
9. Placeholder residue:
   - Debug output (`console.log`, `print`, `dbg!`) and commented-out code the change added: delete, unless it is the program's designed stdout (a piped CLI, a `bin` entry, a test or doc asserting on the output).
   - Sample or demo blocks in production files: delete.
   - A stub body (`pass`, `throw new Error("not implemented")`, `// TODO: implement`) where working code was claimed: flag as incomplete; do not delete.
   - An exemplar literal on a live path (`"John Doe"`, `"foo@example.com"`, a `555-` phone number, lorem ipsum as a default, fallback, or seed): flag as a possible bug. Fine inside tests and fixtures.
10. Reinvented wheel: the diff hand-rolls what the repository's utilities, the standard library, or an installed dependency already provides (`deepEqual`, `debounce`, `retry`, `chunk`/`groupBy`, a date formatter, a UUID). Search for an equivalent before accepting new logic with a classic shape. Replace call sites and delete the copy only when the contracts verifiably match, edge cases included; unsure or deliberately different: flag. Keep a reimplementation whose difference is documented and load-bearing.

11. Tests that guard no behavior. Rewrite a test that also covers behavior callers rely on: assert what a caller observes through the public interface, with the expected value from an independent source (a literal, a worked example, the spec; never production logic). Delete the rest:
   - It restates the implementation: a constant equals its literal, or the expected value is computed with the same logic as the code.
   - It cannot fail: it tests the platform or framework, asserts what the types guarantee, or mocks the unit under test and asserts what the mock returns.
   - It depends on the past: it asserts that removed code stays gone.
   - It depends on the implementation: private state, call order, call counts, which helper ran.
   - It copies another test: every regression that fails one also fails the other. Keep the clearer test at the public entry point.
   Keep a test of absence that is required behavior (a removed endpoint must return 404, a secret must stay out of logs), of untrusted-input validation, of a fixed bug, or at another level that catches a different failure. Snapshots and fixtures stay out of scope.

Backstop: anything written for no one that loses nothing when cut is slop; apply the gates and cut it.

## Truth catalog

Check every claim in the changed lines that names something checkable: a symbol against the repository, a link against its target, a described behavior against the code. Verify by search or by reading the target, never from memory. A checkable claim you did not check is unfinished work.

1. Comment-code contradiction: the comment says it returns null on error, the code throws; the doc says default 10, the code says 30; a `@param` or `:param:` for a renamed or removed argument; a docstring describing steps the body does not take; a comment copied from elsewhere. Decide with gate 2. For comment rot, fix the prose, or delete it if the corrected version says nothing.
2. Phantom references: names that resolve to nothing. Resolve each:
   - An added `import` or `require` that does not resolve: possible bug, never a silent deletion.
   - A function, file, or module a comment mentions that is not in the repository.
   - An environment variable or config key nothing reads (the exceptions of code item 7 apply).
   - A CLI flag the parser does not define.
   - A relative link, heading anchor, or README badge with no live target.
   - A dependency method or option absent from the version pinned in the lockfile.
   A near match exists: fix to the real name. Nothing exists: delete the reference; for a live call or import, flag.
3. Fabricated specificity: concrete-sounding facts with no source (benchmark numbers, "40% faster", version or date stamps, spec or RFC citations, quotes). Checkable in the repository: check and fix. Checkable only externally: flag; do not delete what might be true.
4. Doc drift: README, docs, or changelog lines in the diff that document flags, endpoints, signatures, defaults, or behavior the code does not match. The code wins only when its behavior predates this diff. If the code also changed in this diff (doc said 5, old code said 5, new code says 3), the change may be a regression: flag as a possible bug; do not rewrite the doc to match unverified new code.
5. Error-message drift: a thrown or logged message describing a different failure than its condition (a timeout catch whose message says `invalid input`). The message is program output that may be matched elsewhere, and the mismatch often marks a mis-structured catch: flag as a possible bug; never rewrite it silently.

## Existing code

Unchanged code may be needed for reasons no one remembers: map it, double-check every candidate, and propose a plan before any edit. Here both catalogs apply to every line in scope, not only to what a change added: read "changed lines" and "the change added" in them as "in scope", and the diff-only limits of code items 5 and 7 do not apply.

Map: each symbol in scope with its callers, each test with the code and behavior it reaches, and the project's entry points. Use the most precise inspection available, and say which you used:
1. Semantic: a language server or code index (references, call hierarchy, implementations, diagnostics), the compiler or type checker.
2. Measured: the project's coverage tool, per test when it supports it; its mutation-testing tool; its dead-code or unused-export finder; its complexity report.
3. Text search, last: each name and its plain-string form. It misses dynamic dispatch and generated callers.

A large scope: map one module at a time. Split modules across parallel agents only when the environment provides them and the user's instructions allow delegation; merge their maps before classifying anything shared. A useful tool is missing: do not install it or add configuration. Work with what exists, and name the tool and what it would prove in `**Next:**`; adding it is the user's decision.

Run every mechanical check in a disposable copy of the project outside the workspace. No copy can be made (a sandbox blocks it): say so, plan only items whose checks need no copy (reading only, or reference searches), and flag the rest. The typecheck, lint, or tests cannot run: report as `--report` does and say why. Apply the whole plan in the copy and run the typecheck, the lint, and the tests; a failure removes the items that caused it from the plan. Propose the plan and stop. Apply only the items the user approves, in the request ("apply it without asking") or in a later message. A file changed since the plan: double-check its items again first.

## Double-check

Tool results are leads, not proof. Each candidate needs a reading and the mechanical check its row names, both observed. A deliberate break of code always runs in a disposable copy outside the workspace. Other checks run in the workspace in diff mode, which reverts an edit whose check fails, and in the copy in existing-code mode.

| Candidate | Reading | Mechanical check |
|---|---|---|
| Unused or forwarding code | Read each caller | Semantic references and text search agree |
| Guaranteed check | Read the guarantor on the same path | Removed: typecheck and tests pass |
| Test that cannot fail | Read what it asserts | Break the code it claims to guard: it still passes |
| Test that restates the code | Read what it restates | Change the restated value: a behavior test also fails |
| Copy of another test | Read both | Each break that fails it also fails the kept test |
| Comment that restates its line | Read the comment and the line | None needed: the line is the guarantor |
| Truth fix | Read the target it names | None needed: the target is the guarantor |
| Any other code edit | Read the edited code | Typecheck, lint, and tests pass after it |

A restating test whose change no behavior test catches is the only guard of that value: rewrite it against behavior, or flag it. A rewrite is proven when it fails on a break of the behavior it guards and passes once the code is restored.

## Output

Reader: the developer about to commit the change, or, for a plan, the owner of the code. Decision: commit the cleaned change, or first settle the possible bugs and flagged items; for a plan, approve all items, some, or none. Terms: a leftover is a sign that text or code was written without care (for example, a comment that restates the line below it); a baseline is the test result before any edit; a phantom reference is a name that points at nothing.

Line 1, bold, one plain sentence: what changed, and whether a possible bug was identified in the reviewed changes. Scope any absence claim to those changes; it is not a claim about all possible bugs. Never open with a verdict word.

Under line 1, plain sentences:
- The test result before and after, as a sentence: "I ran the tests before and after: 6 pass both times." Give the reason when a check did not run or did not pass. A failure in both runs is pre-existing: name it, and do not block on it. A new failure: revert the edit that caused it, since that edit was not slop removal. Compare failure sets, not raw counts.
- No baseline: say so and claim nothing about build health. A prose-only change: say no tests apply, and that you spot-checked the links.
- The typecheck, only when the repository has none: "The repository has no typecheck."
- The lint before and after, with its command and exit code, and whether it enforces a complexity rule. It still fails: quote the failing lines verbatim.
- Existing-code mode: which inspection built the map, and the result of the whole plan in the disposable copy.
- Staged mode only: one line saying whether unstaged changes exist and that they were not reviewed.

Then the body, as one numbered list for multiple points, or plain sentences for one simple edit, in this order:
- Possible bugs first: a comment that may record unimplemented intent, a stub presented as done, an import or call to a phantom symbol, an exemplar literal on a live path, doc drift that may be a regression, error-message drift. Each is a bold plain sentence that starts "This is a possible bug in <name>", then what it does, then that neither side was edited.
- Each edit: a bold plain sentence that names the removed item and its `file:line`, then the evidence for why it was safe, including any uncertainty. Show a `diff` view of the removed lines when it helps. Line numbers are post-edit positions.
- Each truth fix, when a comment or name was corrected to match the code: say what it said and what the code does.
- Untouched items only when they carry meaningful risk or explain the review boundary: name the item and why it was not touched, for example a possibly external export or program output. Omit unrelated old-slop inventories.

Report mode (`--report`): the same evidence and scope, with suggested fixes in Next and no edits.

Existing-code plan: line 1 says how many items you propose to delete, rewrite, and leave to the user, and whether any behavior protection would be lost. Body: items needing the user's decision first, then deletions, then rewrites, safest first within each group. Each item names the action, the item, and its `file:line`, what already guarantees it, and both checks with their observed results.

The reply ends with `Verdict: <word>` on its own line just before `**Next:**`:
- `Cleaned`: edits made and the lint exits 0.
- `Cleaned, lint fails`: edits made; the lint still fails for a reason cleanup cannot fix.
- `Planned`: existing-code plan proposed; nothing edited. Nothing qualifies: an empty plan, and line 1 names what you checked.
- `Reported`: `--report` run, or the baseline could not run in existing-code mode; nothing edited.
- `Stopped`: no base to compare with. Line 1 names the missing base. `**Next:**` then holds at most 3 numbered ways to unblock, default marked, such as `--base <ref>`.

With nothing in scope, print exactly: `Nothing to deslop: clean tree or no changes in scope.`

`**Next:**` holds each step, in order: for a plan, the approval question first (all items, some by number, or none); review each possible bug; each function still above the complexity limit; each missing tool; then commit. A staged run whose edits are unstaged says so, and `git add <path>` stages the cleanup.

Reader rules: no blame of the author; "the comment restates the code" is enough. Name each leftover once. Say "the test cannot fail", not "tautological"; "a stand-in object", not "mock"; "how many paths the function has" the first time you say "complexity". No hype, and no claim that the cleanup proves quality.

````markdown
**Removed 3 leftovers from 2 files; possible bugs remain in the reviewed changes.**
I ran the tests before and after: 6 pass both times. `ruff check .` exited 0 before and after; it limits each function to 10 paths. The repository has no typecheck.

1. **This is a possible bug in `scale_servings()` (scale.py:21): it returns 1 for 0 servings, but its comment says 0.**
   I changed neither side.

2. **This is a possible bug in `units.py:30`: the example name may be a live fallback, not test data.**
   I did not touch it.

3. **Removed `import math` from scale.py (line 4): nothing in the file reads it.**

4. **Removed `# multiply the amount by the factor` from scale.py (line 9): it restated the next line.**

5. **Removed a debug print from units.py (line 7): no caller reads stdout.**

Verdict: Cleaned

**Next:**
1. Decide what `scale_servings(0)` should return, then fix the code or the comment.
2. Decide whether the fallback at `units.py:30` is intended; it was not changed.
3. Run `git add scale.py units.py` after resolving those decisions; the cleanup is unstaged until then.

**Changed:** `scale.py`, `units.py`
````

