---
name: hl-deslop
description: "Remove AI-generated slop and hallucinations from a change: style tells (narrating comments, defensive cruft on trusted paths, type escapes, needless nesting, one-call wrappers), dead weight (unused code, speculative generality, placeholder residue, reinvented helpers), false claims (comments the code contradicts, phantom references, fabricated numbers, doc drift, error-message drift), and AI prose tells in Markdown, docs, and comments in any language. Edits only changed lines by default; naming a path opts that file in. --report lists findings without editing. Use when AI-written code was generated or accepted, before committing, when a diff smells generated, or on a pull request that is technically correct but over-explained, over-defended, or confidently wrong."
---
# Deslop

Input: `[path] [--base <ref>] [--staged] [--report]`

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
- Noise: true but worthless (narration, ceremony, padding). Delete.
- Dead weight: code or prose that serves nothing (unused, unreachable, speculative, leftover). Delete.
- Lies: claims the artifact contradicts (stale comments, phantom references, invented numbers). Fix to match reality, delete, or flag when the lie may mark a live bug.

Default move: delete. Noise or dead weight qualifies only if removing it changes nothing a reader, the type checker, or the runtime relies on. A lie fix qualifies only if the truth is checkable in the repository and the fix states it.

## Gates

Every edit passes all four:
1. Behavior unchanged. If removal could change runtime behavior, it is not slop; leave it. A fix never adds behavior: no new fallbacks, defaults, or handling.
2. Code is the source of truth for prose about it. Never edit code to satisfy a comment or doc. Decide a comment-code disagreement on evidence:
   - Comment rot: an existing test or caller pins the code's behavior, or git history shows the comment predates a later code change. Fix or delete the prose.
   - Possible bug: the comment is newer than the code, nothing pins the behavior, or the comment may record intent the code fails to implement. Flag it; edit neither side.
3. Diff only. Editable lines are the diff's added lines plus lines an in-scope edit mechanically forces (re-indenting after flattening a wrapping `if`). Never the rest of a hunk's context; never a whole function for one changed line. A fix that needs other lines is flagged, not applied. This limits edits, not reads: verifying a claim may need any file.
4. Unsure: flag, do not delete. A comment that might say why, a guard that might catch a real failure, a claim you cannot verify: keep it and list it for a human.

On prose, gate 1 means meaning unchanged, except that false meaning has no protection: correcting a wrong claim is the fix.

## Order

1. Before editing, record typecheck and test results as the baseline.
2. Truth catalog first. Check every comment you plan to delete as noise against the code it describes: one that narrates and lies is a possible-bug flag; deleting it as style destroys the evidence.
3. Code catalog and prose catalog.
4. Verify and report (see Output).

## Scope

The input sets what to scan. Default: every change between the merge base and the working tree (committed, staged, unstaged). Base: the merge base with the configured default branch or the verified target of `refs/remotes/origin/HEAD`; never assume `main` or `master`. None resolves: stop and ask for `--base <ref>`; never widen to the whole repository.
- `--base <ref>`: the diff base.
- `--staged`: staged changes only. The reply says in one line whether unstaged changes exist and that they were not reviewed.
- A path: only that file's or directory's changed lines. A named path with no changes is scanned whole; this is the only case that edits unchanged code.

Out of scope even when the diff touches them:
- Generated files: a `@generated`, `Code generated by`, or `DO NOT EDIT` header, `linguist-generated` in `.gitattributes`, or the repository's build-output paths. A filename convention alone is a hint; verify it, and report when a file's status is a guess.
- Vendored code and lockfiles.
- Snapshots, fixtures, cassettes (`__snapshots__/`, `*.snap`, recorded HTTP): content must byte-match a captured value. Flag a tell against the source that produced it; never edit in place.
- String literals that are program output: error messages, log text, UI copy, payload fields. Tests, alert rules, and other services may match their exact bytes. Flag slop inside them; never edit.

Not a Git repository, or no changes in scope: print `Nothing to deslop: clean tree or no changes in scope.` and stop.

## Code catalog

Match the literal syntax in the changed lines, apply the fix, honor the keep condition.

1. Narrating comments: a comment restating the line below (`// increment count` over `count++`, `# fetch the user` over `user = get_user()`); banner dividers (`// ---- helpers ----`); a docstring that only echoes the signature; chat voice (`// feel free to adjust this`, `// you can customize the threshold`, `// let's add a helper here`, `// sorry, this is a bit hacky`). Delete. Keep a comment that says why, records a non-obvious constraint, or links an issue.
2. Defensive cruft on trusted paths: `catch (e) { console.error(e); throw e }`; `if (!x) return` on a value the types guarantee non-null; `?? []`, `|| {}`, `?.` on values that cannot be nullish here; a null check one line after a non-null assignment; a `try` around a whole function when one call inside can raise (narrow it). Delete, except:
   - Trace the value to its entry point. A value from `JSON.parse`, `fetch().json()`, an external SDK, an `any`/`unknown` cast, or a database row crossed an unpoliced boundary; its guard stays.
   - Security guards are never cruft: sanitization, escaping, path checks, and authorization depend on every caller in the repository.
   - A catch that logs context is deletable only when an upstream handler captures the same context.
   Keep any guard for a failure that can occur on this path.
3. Type escapes: `as any`, `: any`, `as unknown as T`, `@ts-ignore`, `@ts-expect-error`, `# type: ignore`, a bare `except:`, `.unwrap()` or `!` added to silence the checker. Replace with the real type or a handled error. Handled means failing the way the function already fails elsewhere, never a new silent default (`?? ({} as Config)` swaps a crash for wrong data). Cannot tell why the escape was needed: flag; do not guess. Keep only at a genuinely untyped boundary, with a comment saying so.
4. Needless nesting: `if (cond) { <rest of function> }` that inverts to `if (!cond) return;`; `else` after `return` or `throw`; arrow-shaped pyramids. Flatten with early returns. Keep nesting that maps to real branching.
5. Ceremony: `const result = f(); return result;`; a one-call wrapper used once (inline it only if its definition is in your changed lines; a pre-existing wrapper your diff made single-use is flagged, not edited); an `else` duplicating a fall-through; a literal restated where a constant exists; a rename or re-export that adds nothing. Cut. Keep an extraction that is reused or names a non-obvious step.
6. Idiom drift: new code disagrees with the file on quote style, import grouping, naming case, error handling, comment density, or test shape. Conform to the file, with two limits: never respell a name that is an interface (serialized field, database column, i18n key, URL parameter, public export; check for a schema, migration, or locale file first); the file's idiom never overrides the catalogs (a file that narrates every line does not license new narrating comments). The file wins even when the new style is better; raise the file's own style problem separately.
7. Dead weight the change added: an import, variable, parameter, or export the diff introduces and nothing uses; a helper never called; an unreachable branch; a feature flag or config key nothing reads. Before deleting, search the identifier and its plain-string form across the repository (source, config, IaC, SQL, CI). Dynamic dispatch (`obj[name]`, `getattr`, DI registries, decorator self-registration) counts as use. An export reachable from the package's public entry point, or an environment or config key that infrastructure outside the repository may read, is flagged possibly-external, never deleted. Delete only on an empty search with none of these exceptions.
8. Speculative generality: a parameter every caller passes the same value; an `options` object with one shape ever constructed; an interface or base class with one implementation; a `mode` or `type` switch with one arm exercised. Inline the single case; for an exported or public signature, flag instead. Keep generality an existing caller uses or the task explicitly requested.
9. Placeholder residue:
   - Debug output (`console.log`, `print`, `dbg!`) and commented-out code the change added: delete, unless it is the program's designed stdout (a piped CLI, a `bin` entry, a test or doc asserting on the output).
   - Sample or demo blocks in production files: delete.
   - A stub body (`pass`, `throw new Error("not implemented")`, `// TODO: implement`) where working code was claimed: flag as incomplete; do not delete.
   - An exemplar literal on a live path (`"John Doe"`, `"foo@example.com"`, a `555-` phone number, lorem ipsum as a default, fallback, or seed): flag as a possible bug. Fine inside tests and fixtures.
10. Reinvented wheel: the diff hand-rolls what the repository's utilities, the standard library, or an installed dependency already provides (`deepEqual`, `debounce`, `retry`, `chunk`/`groupBy`, a date formatter, a UUID). Search for an equivalent before accepting new logic with a classic shape. Replace call sites and delete the copy only when the contracts verifiably match, edge cases included; unsure or deliberately different: flag. Keep a reimplementation whose difference is documented and load-bearing.

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

## Prose catalog

Applies to Markdown, docs, and written text in the change, including doc comments (JSDoc, docstrings, `///`, `/** */`, `#` blocks) and inline comments, in any language. Never to string literals: program output is data. Match the literal tell, apply the fix, honor the keep condition.

1. Typographic tells: `—` or `–` as a connector -> `:` in a heading; comma, parentheses, or `-` in prose. Arrows `←` `→` `↔` `⇒` -> ASCII `<-` `->` `<->` `=>`. Curly quotes `“` `”` `‘` `’` -> straight `"` `'`. `…` -> `...`. Mid-text `•` -> `-`. Emoji in comments or docs: delete. Non-breaking or narrow spaces: normal space. Trailing hard-break whitespace: strip. Keep where the document already uses the form everywhere (idiom drift wins), inside real ASCII art, or in a quoted source.
2. Callout ceremony: `> **Tip:**`, `> **Note:**`, `> **Warning:**` banners: flatten to an inline `Note:` or the plain sentence. Keep a blockquote that quotes a real source.
3. Bold-label arrow rows: `**Label** → does X`: plain text (`Label: does X`) or a real table. Keep bold on a genuine first-use term.
4. Heading inflation: `## Validation rules` -> `## Validation`; Title Case headings -> sentence case; drop `Step 1:` prefixes on an already ordered list. Keep a word a heading needs to tell siblings apart.
5. Filler adverbs: `automatically`, `simply`, `easily`, `seamlessly`, `effortlessly`, `basically`, `essentially`, `just`: cut. Keep only when load-bearing (manual versus automatic is the actual point).
6. Throat-clearing and closers: `It's worth noting that`, `It's important to note`, `Keep in mind that`, `As you can see`, `Note that`: cut and state the fact. `In conclusion`, `In summary`, `Overall`, `Hope this helps`: cut. Keep a caveat that changes what the reader should do.
7. Hype, AI vocabulary, triads: `powerful`, `robust`, `seamless`, `comprehensive`, `blazing-fast`, `cutting-edge`, `elegant`; `delve`, `pivotal`, `crucial`, `showcase`, `leverage` (verb), `foster`, `vibrant`, `boast`, `testament to`, `underscore(s)`, `game-changer`, `journey`, figurative `landscape` or `tapestry`; rule-of-three padding (`fast, reliable, and scalable`): cut, or replace with the concrete fact. Keep a backed claim and literal domain use (`leverage` in finance).
8. Hedge stacks: `may potentially`, `might possibly`, `can sometimes help`: one modal or none. Keep a single hedge that marks real uncertainty.
9. Doc-comment ceremony: a parameter tag echoing the name (`@param name - the name`, `:param name: the name`); a return tag for a void or self-evident return; a type already in a typed signature; a lead line repeating the function name; an example block for a trivial one-liner; metadata noise (author, since, version). Trim to what the signature does not state. Keep notes on units, constraints, ownership, nullability, or a non-obvious contract.
10. Formulaic frames: `it's not just X, it's Y`, `X isn't just about Y`, `not only X but (also) Y`, `more than just`, `here's the thing`, `the real question is`: cut the frame and state the claim plainly. Keep emphasis the sentence needs.
11. False agency: `the data reveals`, `the results demonstrate`, `this section explores`, `the table shows that`: name the real actor or state the fact. Keep agency that is literally true.
12. Dramatic fragments: `And that changes everything.`, `Not anymore.`, `The catch?`: fold into the full sentence or cut. Keep a fragment the surrounding style uses on purpose.
13. Vague declaratives: `This is important.`, `There are several factors.`, `It's complicated.`: replace with the specific fact or cut.
14. Copula dodges and vague attributions: `serves as`, `stands as`, `functions as`, `represents` where `is` carries the sentence: use `is`. `experts suggest`, `studies show`, `it is widely considered` with no named source: name the source or state it as the document's own claim. Keep a role verb that describes actual behavior (`acts as a proxy`) and a cited attribution.
15. Diff-anchored prose: `now supports`, `previously`, `no longer`, `New:`, `Enhanced`, `Improved` in docs or comments: describe present behavior. Keep them in changelogs and migration guides, where the change is the subject.

Backstop: prose written to impress rather than inform, which loses nothing when cut, is slop.

## Output

Reader: the developer about to commit the change. Decision: commit the cleaned change, or first settle the possible bugs and flagged items. Terms: a leftover is a sign that text or code was written without care (for example, a comment that restates the line below it); a baseline is the test result before any edit; a phantom reference is a name that points at nothing.

Line 1, bold, one plain sentence: what changed, and whether a possible bug was identified in the reviewed changes. Scope any absence claim to those changes; it is not a claim about all possible bugs. Never open with a verdict word.

Under line 1, plain sentences:
- The test result before and after, as a sentence: "I ran the tests before and after: 6 pass both times." Give the reason when a check did not run or did not pass. A failure in both runs is pre-existing: name it, and do not block on it. A new failure: revert the edit that caused it, since that edit was not slop removal. Compare failure sets, not raw counts.
- No baseline: say so and claim nothing about build health. A prose-only change: say no tests apply, and that you spot-checked the links.
- The typecheck, only when the repository has none: "The repository has no typecheck."
- Staged mode only: one line saying whether unstaged changes exist and that they were not reviewed.

Then the body, as one numbered list for multiple points, or plain sentences for one simple edit, in this order:
- Possible bugs first: a comment that may record unimplemented intent, a stub presented as done, an import or call to a phantom symbol, an exemplar literal on a live path, doc drift that may be a regression, error-message drift. Each is a bold plain sentence that starts "This is a possible bug in <name>", then what it does, then that neither side was edited.
- Each edit: a bold plain sentence that names the removed item and its `file:line`, then the evidence for why it was safe, including any uncertainty. Show a `diff` view of the removed lines when it helps. Line numbers are post-edit positions.
- Each truth fix, when a comment or name was corrected to match the code: say what it said and what the code does.
- Untouched items only when they carry meaningful risk or explain the review boundary: name the item and why it was not touched, for example a possibly external export or program output. Omit unrelated old-slop inventories.

Report mode (`--report`): the same evidence and scope, with suggested fixes in Next and no edits.

The reply ends with `Verdict: <word>` on its own line just before `**Next:**`:
- `Cleaned`: edits made.
- `Reported`: `--report` run; nothing edited.
- `Stopped`: no base to compare with. Line 1 names the missing base. `**Next:**` then holds at most 3 numbered ways to unblock, default marked, such as `--base <ref>`.

With nothing in scope, print exactly: `Nothing to deslop: clean tree or no changes in scope.`

`**Next:**` holds each step, in order: review each possible bug, then commit. A staged run whose edits are unstaged says so, and `git add <path>` stages the cleanup.

Reader rules: no blame of the author; "the comment restates the code" is enough. Name each leftover once. No hype, and no claim that the cleanup proves quality.

````markdown
**Removed 3 leftovers from 2 files; possible bugs remain in the reviewed changes.**
I ran the tests before and after: 6 pass both times. The repository has no typecheck.

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

