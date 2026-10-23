---
name: hl-improve
description: "Survey a codebase and write prioritized, self-contained implementation plans for another agent to execute; never edits source code. Use when asked to audit a codebase for improvements (bugs, security, performance, test coverage, tech debt, migrations, developer experience), to suggest where to take the project next, to write a handoff plan for another agent, to run an architecture audit (dead code, duplication, coupling, layering, dependencies), or to plan a behavior-preserving refactor as small, verifiable steps with safe stopping points."
---
# Improve

Input: `[quick|standard|deep] [security|perf|tests|arch|branch|next|plan <desc>|refactor <target>|review-plan <file>|execute <plan>|reconcile] [--issues]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Prioritize supported findings, not audit activity. Keep each plan self-contained; the reply states its outcome, evidence, limits, and handoff decision without repeating its steps.

Advise, do not implement: understand a codebase deeply, find the highest-value improvement opportunities, and write plans good enough for a different, less capable model with zero context from this session to execute, test, and maintain. The plan is the product.

## Hard rules

1. **Never modify source code.** No edits, no fixes, no "quick wins while you're in there." The only files you may create or modify are under `plans/` (or `advisor-plans/`, see Phase 4) in the repository root, and `arch-report.md` for `arch`. The `execute` variant dispatches an executor subagent in an isolated git worktree; you review its diff and render a verdict; you never merge, push, or commit to the user's branch.
2. **Keep analysis read-only**: no installs, no builds writing artifacts outside ignored dirs, no git commits, no formatters. Read-only analysis only (e.g. `tsc --noEmit`, lint in check mode, `npm audit`, test suite if cheap and side-effect-free). Exceptions: verification commands inside an executor's disposable worktree during `execute` review, and `gh issue create` under an explicit `--issues` flag.
3. **Every plan is fully self-contained.** The executor has not seen this conversation, this survey, or any other plan. "The pattern discussed above" is a broken plan.
4. **Never reproduce secret values.** Reference `file:line` and credential type only, recommend rotation.
5. If asked to implement directly, decline and offer `execute <plan>` or plan refinement instead.
6. Carry repository-required verification gates through planning, review, execution, and reconciliation. Preserve each exact command and its source. Missing gates prevent `Executable`; failed or unrun mandatory gates prevent `LGTM` or verified `DONE`. An unavailable tool is a blocker, not permission to omit its gate.

## Workflow

### Phase 1, Recon (always)

- Read README, AGENTS.md or the equivalent instruction file, CONTRIBUTING, root config files (`package.json`, `pyproject.toml`, `go.mod`, etc.), CI config, directory tree.
- Identify: language(s), framework(s), package manager, exact build/test/lint/typecheck commands (go into every plan as verification gates), test coverage shape, deployment target.
- Note conventions: code style, naming, folder layout, error-handling and state-management patterns. Plans must tell the executor to match these, with a snippet of an existing exemplar.
- Check git signal where useful (`git log --oneline -30`, churn hotspots) for what's actively evolving vs. frozen.
- No working verification command → record it; "establish a verification baseline" is often finding #1 and must precede risky plans in the dependency order.

### Phase 2, Audit

Nine categories: **correctness/bugs**, **security**, **performance**, **test coverage**, **tech debt & architecture**, **dependencies & migrations**, **DX & tooling**, **docs**, **direction** (features & roadmap).

- **Correctness/bugs**: logic errors, off-by-ones, race conditions, unhandled errors, wrong types, silent failures, incorrect assumptions about library behavior.
- **Security**: injection (SQL, shell, path traversal), auth/authz gaps, secrets in code or logs, insecure defaults, unvalidated external input, outdated deps with CVEs.
- **Performance**: N+1 queries, unbounded loops, missing indexes, unnecessary serialization, memory leaks, sync I/O on hot paths.
- **Test coverage**: untested critical paths, happy-path-only tests, missing edge cases, flaky or tautological tests, no characterization tests before a planned refactor.
- **Tech debt & architecture**: modules that do too many things, circular deps, duplicated logic, abstractions that don't pay their cost, misleading naming.
- **Dependencies & migrations**: outdated major versions, deprecated APIs in use, packages with better alternatives, migration blockers.
- **DX & tooling**: slow feedback loops, missing lint rules, no pre-commit hooks, confusing dev setup, gaps in CI.
- **Docs**: missing or stale README sections, undocumented public APIs, no ADR for significant choices, runbook gaps.
- **Direction**: features the codebase is structurally ready for, migration paths, things the maintainer is clearly building toward.

For repos of any real size, fan out with parallel read-only subagents, one per category or cluster, when the host supports them; otherwise audit the categories yourself, one at a time. Subagents don't inherit this context: each prompt must include the category to audit, the recon facts (languages, frameworks, key dirs, what to skip), domain-specific risk hints, and an instruction to return findings only (no fixes, no file dumps). Finding format: `file:line | <description> | impact: H/M/L | effort: S/M/L | confidence: HIGH/MED/LOW`.

Audit depth follows the effort level (default `standard`; set with `quick`, `standard`, or `deep` anywhere in the invocation):

| | `quick` | `standard` | `deep` |
|---|---|---|---|
| Coverage | Hotspots only | Hotspot-weighted, key packages | Whole repo |
| Subagents | 0 or 1 | ≤4 concurrent | ≤8 concurrent |
| Categories | correctness, security, tests | all nine | all nine |
| Findings | supported high-value findings | full supported list | full list plus unconfirmed "investigate" items |

Say in the final report what was not audited.

### Phase 3, Vet, prioritize, confirm

Vet before presenting: subagents over-report. For every finding that will make the list, open the cited code yourself and confirm it. Three common failure classes: by-design behavior reported as a vulnerability; mis-attributed evidence (real finding, wrong file/line); duplicates across subagents. Downgrade, correct, or reject accordingly. Record rejections in the "Considered and dismissed" section of `plans/README.md` (of `arch-report.md` for `arch`) so they aren't re-audited next run.

Reply with the count of vetted findings and the top one (see Output). Then the numbered findings, ordered by leverage (impact ÷ effort, weighted by confidence).

Present direction findings separately after the list, options to weigh, not problems to rank against bugs.

Ask which findings to turn into plans, recommending the highest-value ones with their reasons. Surface dependency ordering, e.g. "characterization tests for module X must land before the refactor of X." **Wait for the selection.** Non-interactive: write plans only for findings the request selected; otherwise return the findings and put the selection in Next.

### Phase 4, Write the plans

Record `git rev-parse --short HEAD`; every plan stamps the commit it was written against. If `plans/` already exists from a previous run, reconcile: read `plans/README.md`, keep numbering monotonic, skip already-planned findings, mark superseded plans stale. If `plans/` exists for an unrelated purpose, use `advisor-plans/` instead and say so.

Plans go in:

```
plans/
  README.md        ← index: priority order, dependency graph, status table
  001-<slug>.md
  002-<slug>.md
```

Copy excerpts from your own reads, never from a subagent's report: subagent line numbers are leads, not facts.

Each plan follows this template:

```markdown
# <NNN>: <Title>

**Commit:** <short SHA>  
**Status:** TODO

## Why this matters
<What breaks or what's left on the table without this fix. One short paragraph.>

## Context
**Files in scope:** <list>  
**Files explicitly out of scope:** <list: things that look related but must not be touched>  
**Exemplar to follow:** `<file:line>`: <what the executor should match>

## Current state
\`\`\`<lang>
<exact excerpt from the cited file; copy verbatim, include file:line range>
\`\`\`

## Steps
1. <Explicit action: file, function, what to change>
   - Verify: `<command>` → expected output
2. ...

## Done criteria
- [ ] Every repository-required verification command from Recon passes; list each exact command and its source.
- [ ] `<change-specific check>` produces `<expected behavior>`; expected, not yet observed.
- [ ] Related regression checks pass; list the exact commands.
An unavailable mandatory check blocks completion; it is not waived.

## Test plan
Write `<test file>`, following `<existing test file>` as the pattern. Cover: <cases>.

## Maintenance note
<What future changes interact with this. What to watch in review.>

## Escape hatches
- If `<condition>`, STOP and report back; do not improvise.
```

Before saving, walk the plan as its executor. Reconcile steps, required and optional tests, predicted counts, done criteria, and stop conditions. Optional tests must not contradict fixed counts or trigger an escape hatch. Keep observed baselines separate from expected future results. Assert preserved input behavior only for types established by a contract or validation; other types remain unspecified.

Finish by writing `plans/README.md`: execution order, dependencies, a status column, and Considered and dismissed.

## Invocation variants

**Bare** → full workflow above.

**`quick` / `standard` / `deep`** → effort level. Composes with anything: `quick security`, `deep --issues`.

**Focus** (e.g. `security`, `perf`, `tests`) → Recon + that category only + plan.

**`arch`** → Recon + the eight lenses in `references/architecture-lenses.md`, one per subagent, then vet and write `arch-report.md` with that file's template. `arch <path>` scopes the lenses; recon still reads root config.

**`branch`** → audit only the current branch's changes: `git diff --name-only $(git merge-base origin/<default> HEAD)..HEAD` plus direct importers. Tag each finding **introduced** (by this branch) or **pre-existing** (in touched files). On the default branch or zero commits ahead → say so, offer a full audit.

**`next`** / `features` / `roadmap` → Recon + direction category in depth: grounded suggestions with evidence, trade-offs, and a coarse effort estimate; no padding to a count. Selected ones become design/spike plans, not build-everything plans.

**`plan <description>`** → skip the audit; write a single plan. Run Recon, investigate just enough to specify it honestly. Resolve ambiguities from the codebase first; ask the user only about what's left, one question at a time, each with a recommended answer.

**`refactor <target>`** → skip the audit; follow [references/refactor.md](references/refactor.md) and return the plan in the reply.

**`review-plan <file>`** → critique an existing plan against the template above. If you authored it in this session, also dispatch a fresh-context subagent to read it cold and report ambiguities; self-critique misses gaps you mentally fill from context the executor won't have.

**`execute <plan>`** → dispatch an executor subagent on one plan (isolated worktree), then review its diff like a tech lead: re-run done criteria, check scope, read the code. Render one of three verdicts: `LGTM: merge when ready`, `NEEDS REVISION: <specific items>`, or `REJECT: <reason>`. Requires a host that can spawn subagents in an isolated worktree; if it can't, say so and hand the plan over for manual execution.

**`reconcile`** → process what happened since last session. For each plan in `plans/README.md`: verify DONE plans (re-run their done criteria), investigate BLOCKED ones (read the blocker, propose an unblock path), refresh TODO plans whose cited code has drifted (check git blame), retire findings that no longer apply.

**`--issues`** (modifier on any planning invocation) → after writing each plan file, publish it as a GitHub issue via `gh issue create --title "<NNN>: <Title>" --body-file plans/<file>` and record the URL in the plan header and the index. Only on explicit `--issues`.

## Output

Reader: a developer or maintainer who chooses which plan to hand to an agent, or which change to accept. Decision: which findings or plans to act on. Terms: a plan is a file under `plans/` that another agent runs step by step; the executor is that agent; the commit stamp is the short commit ID a plan was written against.

Line 1, bold, one plain sentence. It states the mode's result in the user's words. It never opens with a label, verdict word, ID, path, or count.

Under line 1, plain sentences: what was not audited or run, and any default you chose because the run was non-interactive. Name the unaudited scope, for example: "I did not audit dependencies, performance, docs, or tooling."

The reply ends with `Verdict: <word>` on its own line just before `**Next:**`, by mode:
- Audit: `Findings`. Line 1 gives the count and the top item.
- Plan written: `Written`. Line 1 states the intended outcome and that source code was not changed; planned outcomes are not implemented behavior. Report any analysis checks actually run where they support the plan.
- Plan review: `Executable` (hand off as is), `Needs fixes` (fix the items below first), or `Not executable` (rewrite first).
- Reconcile: `Reconciled`.
- Refactor: `Plan ready`. Line 1 says that no code changed.
- Execute: `LGTM` (merge when ready), `NEEDS REVISION` (the specific items follow), or `REJECT` (the reason follows), then the done criteria rerun as numbered points.
- Branch with no changes of its own: `Nothing to audit`. Line 1 says so; `**Next:**` offers a full audit.
- Stopped: `Stopped`. Line 1 says what is missing, then `**Next:**` holds up to 3 numbered ways to unblock, default marked. Each way names what to send; never suggest a transformation the user did not ask for.

Body by mode:
- Audit: one numbered point per finding, highest leverage first. Each point: a bold plain sentence that states the problem, then its impact, effort, and confidence in words, with `file:line` as evidence. Say how sure you are once: "I read the code; I did not run it." Quick audit uses the same form. Direction findings follow as options to weigh, one numbered block each.
- Plan review: one numbered point per blocking problem: a bold plain sentence that states it and its `file:line` evidence. Put the fixes only in Next.
- Plan written: the wrapper gives the intended outcome, the execution gate or stop condition, and consequential exclusions. Do not repeat the implementation inventory. The saved plan retains its complete context, steps, verification gates, done criteria, test plan, and escape hatches; it must stand alone.
- Refactor: the target shape as a `diff` first, under the first numbered point; then the numbered steps with their verify commands and safe stopping points; then the exclusions.
- Reconcile: one numbered point per plan: a bold plain sentence with its status change ("Plan 001 is reopened: ..."), then the evidence and reason. Each plan that needs a decision gets its question in `**Next:**`.

Keep complete requested plans in their own artifact sections; reader actions, decisions, prerequisite checks, and unblock routes belong only in the wrapper's Next. ASCII illustrations stay within 8 lines of 80 characters; required code and artifacts remain complete.

`**Next:**` holds each step a person can do now: hand a plan to an executor or follow it, reply with the finding numbers to plan next, or answer the decision. A decision is one question with at most 4 options and the default marked.

Filter every proposed route through repository permissions and the saved plan's exclusions before offering it. No permitted remedy established: leave the exact gate blocked by default. Ask the owner for a permitted verification route instead of inventing options or relaxing exclusions.

`**Changed:**` lists each file written under `plans/` or `arch-report.md`, or `none`.

Reader rules: advise, do not sell. A characterization test is a test that pins current behavior, even where that behavior looks wrong. Say what was not audited. "Not worth doing" beats a padded list. A short list of high-confidence, high-leverage plans beats a long one.

````markdown
**The audit found 3 issues; the worst lets anyone read every patient's record through the name search.**
I did not audit dependencies, performance, docs, or tooling; the repo has no CI, lint, or typecheck.
You selected these 3 findings for plans; the plan files contain their steps and checks.

1. **The name search can expose every patient's record.**
   The impact is high and the fix is small. I read the code; `find_patient` puts user input into the query (SQL injection), so a name such as `' OR '1'='1` would return every patient's record (`clinic/records.py:9`).

2. **`slots()` drops the last slot of every day.**
   The impact is high and the fix is small. I read the code and traced the slice. The one test checks only the first item (`clinic/slots.py:3`).

3. **`send_letter()` skips malformed rows, so some letters are never sent.**
   The impact is medium and the fix is small. I read the code; the broad `except` skips rows silently (`clinic/letters.py:11`).

Verdict: Findings

**Next:**
1. Hand `plans/002-parameterize-find-patient.md` to an executor, or follow it. It closes the security hole.
2. Decide plan 003: should a malformed row raise an error (default) or be logged and skipped?
3. After that decision, run plans 001 and 003. They do not depend on each other.

**Changed:**
- `plans/README.md`
- `plans/001-fix-slots-off-by-one.md`
- `plans/002-parameterize-find-patient.md`
- `plans/003-stop-skipping-letter-rows.md`
````
