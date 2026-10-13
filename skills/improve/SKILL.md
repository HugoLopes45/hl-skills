---
name: improve
description: "Survey a codebase and write prioritized, self-contained implementation plans for another agent to execute; never edits source code. Use when asked to audit a codebase for improvements (bugs, security, performance, test coverage, tech debt, migrations, developer experience), to suggest where to take the project next, to write a handoff plan for another agent, to run an architecture audit (dead code, duplication, coupling, layering, dependencies), or to plan a behavior-preserving refactor as small, verifiable steps with safe stopping points."
---
# Improve

Input: `[quick|standard|deep] [security|perf|tests|arch|branch|next|plan <desc>|refactor <target>|review-plan <file>|execute <plan>|reconcile] [--issues]`

Advise, do not implement: understand a codebase deeply, find the highest-value improvement opportunities, and write plans good enough for a different, less capable model with zero context from this session to execute, test, and maintain. The plan is the product.

## Hard rules

1. **Never modify source code.** No edits, no fixes, no "quick wins while you're in there." The only files you may create or modify are under `plans/` (or `advisor-plans/`, see Phase 4) in the repository root, and `arch-report.md` for `arch`. The `execute` variant dispatches an executor subagent in an isolated git worktree; you review its diff and render a verdict; you never merge, push, or commit to the user's branch.
2. **Never mutate the working tree**: no installs, no builds writing artifacts outside ignored dirs, no git commits, no formatters. Read-only analysis only (e.g. `tsc --noEmit`, lint in check mode, `npm audit`, test suite if cheap and side-effect-free). Exceptions: verification commands inside an executor's disposable worktree during `execute` review, and `gh issue create` under an explicit `--issues` flag.
3. **Every plan is fully self-contained.** The executor has not seen this conversation, this survey, or any other plan. "The pattern discussed above" is a broken plan.
4. **Never reproduce secret values.** Reference `file:line` and credential type only, recommend rotation.
5. If asked to implement directly, decline and offer `execute <plan>` or plan refinement instead.

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
| Findings | top ~6, HIGH confidence only | full table | full table incl. LOW-confidence "investigate" items |

Say in the final report what was not audited.

### Phase 3, Vet, prioritize, confirm

Vet before presenting: subagents over-report. For every finding that will make the table, open the cited code yourself and confirm it. Three common failure classes: by-design behavior reported as a vulnerability; mis-attributed evidence (real finding, wrong file/line); duplicates across subagents. Downgrade, correct, or reject accordingly. Record rejections in the "Considered and dismissed" section of `plans/README.md` (of `arch-report.md` for `arch`) so they aren't re-audited next run.

Open with the count of vetted findings and the top one. Then the table, ordered by leverage (impact ÷ effort, weighted by confidence):

```
| # | Finding (category) | Impact / effort / confidence | Evidence |
```

Present direction findings separately after the table, options to weigh, not problems to rank against bugs.

Ask which findings to turn into plans (suggest the top 3 to 5, plus anything flagged). Surface dependency ordering, e.g. "characterization tests for module X must land before the refactor of X." **Wait for the selection.** Non-interactive → write plans for the top 3 and record that default in `plans/README.md`.

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
**Exemplar to follow:** `<file:line>`: <one sentence on what the executor should match>

## Current state
\`\`\`<lang>
<exact excerpt from the cited file; copy verbatim, include file:line range>
\`\`\`

## Steps
1. <Explicit action: file, function, what to change>
   - Verify: `<command>` → expected output
2. ...

## Done criteria
- [ ] `<command>` exits 0
- [ ] `<command>` output matches `<expected>`
- [ ] No regressions: `<test command>` passes

## Test plan
Write `<test file>`, following `<existing test file>` as the pattern. Cover: <cases>.

## Maintenance note
<What future changes interact with this. What to watch in review.>

## Escape hatches
- If `<condition>`, STOP and report back; do not improvise.
```

Finish by writing `plans/README.md`: execution order, dependencies, a status column, and Considered and dismissed.

## Invocation variants

**Bare** → full workflow above.

**`quick` / `standard` / `deep`** → effort level. Composes with anything: `quick security`, `deep --issues`.

**Focus** (e.g. `security`, `perf`, `tests`) → Recon + that category only + plan.

**`arch`** → Recon + the eight lenses in `references/architecture-lenses.md`, one per subagent, then vet and write `arch-report.md` with that file's template. `arch <path>` scopes the lenses; recon still reads root config.

**`branch`** → audit only the current branch's changes: `git diff --name-only $(git merge-base origin/<default> HEAD)..HEAD` plus direct importers. Tag each finding **introduced** (by this branch) or **pre-existing** (in touched files). On the default branch or zero commits ahead → say so, offer a full audit.

**`next`** / `features` / `roadmap` → Recon + direction category in depth: 4 to 6 grounded suggestions each with evidence, trade-offs, and a coarse effort estimate. Selected ones become design/spike plans, not build-everything plans.

**`plan <description>`** → skip the audit; write a single plan. Run Recon, investigate just enough to specify it honestly. Resolve ambiguities from the codebase first; ask the user only about what's left, one question at a time, each with a recommended answer.

**`refactor <target>`** → skip the audit; follow [references/refactor.md](references/refactor.md) and return the plan in the reply.

**`review-plan <file>`** → critique an existing plan against the template above. If you authored it in this session, also dispatch a fresh-context subagent to read it cold and report ambiguities; self-critique misses gaps you mentally fill from context the executor won't have.

**`execute <plan>`** → dispatch a cheaper executor subagent on one plan (isolated worktree), then review its diff like a tech lead: re-run done criteria, check scope, read the code. Render one of three verdicts: `LGTM: merge when ready`, `NEEDS REVISION: <specific items>`, or `REJECT: <reason>`. Requires a host that can spawn subagents in an isolated worktree; if it can't, say so and hand the plan over for manual execution.

**`reconcile`** → process what happened since last session. For each plan in `plans/README.md`: verify DONE plans (re-run their done criteria), investigate BLOCKED ones (read the blocker, propose an unblock path), refresh TODO plans whose cited code has drifted (check git blame), retire findings that no longer apply.

**`--issues`** (modifier on any planning invocation) → after writing each plan file, publish it as a GitHub issue via `gh issue create --title "<NNN>: <Title>" --body-file plans/<file>` and record the URL in the plan header and the index. Only on explicit `--issues`.

## Output tone

Advising, not selling. State findings plainly with evidence, flag uncertainty honestly, prefer "not worth doing" over padding the list. A short list of high-confidence, high-leverage plans beats a long one.
