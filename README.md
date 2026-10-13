# hl-skills

**Evidence-first skills for AI coding agents. They show their work.**

Coding agents say "done" when the tests did not run, "fixed" when nobody reproduced the bug, and "probably" when nobody checked. These skills make the agent prove each claim with a `file:line`, a command and its output, or a source. When it cannot prove a claim, it says so.

26 skills. They work with Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode, pi, Amp, Windsurf, and any other agent that reads `SKILL.md`.

```bash
npx skills add HugoLopes45/hl-skills
```

## Why these skills

- **Evidence or "unknown".** Each finding cites its evidence. A check that did not run is reported as not run, never as a pass.
- **Answer first, then the shape.** Reports open with the verdict or result, then show tables, call trees, file trees, and diffs instead of walls of prose.
- **Read-only by default.** Review and audit skills do not edit your code. `debug` edits only when you ask for the fix. `commit`, `open-pr`, and `ci-fix` act only when you ask.
- **Short.** The average skill is about 52 lines, and the longest is under 160. Long catalogs go in `references/` and load only when needed.
- **One job per skill.** Variants are modes of one skill (`code-review --deep`, `challenge --premortem`), not near-duplicate skills that compete for the same trigger.
- **Methods, not personas.** No "act as a senior engineer", and no imitations of famous people. `challenge --lens` gives fixed methods, such as `minimalist` or `failure-hunter`.
- **Any agent.** No host-specific tool names. When a step needs subagents or web access and your agent does not have them, the skill says what to do instead.

## Evidence

Each skill with evals runs the same cases in Claude Code (`sonnet`, 3 repetitions) with the skill and as a bare agent. Runs that pass all checks of each kind:

| Skill | Outcome with | Outcome without | Contract with | Contract without |
|---|---|---|---|---|
| `verify` | 15/15 | 10/15 | 12/12 | 3/12 |
| `adr` | 9/9 | 3/9 | 6/6 | 0/6 |
| `grill` | 30/30 | 21/30 | 24/24 | 9/24 |
| `code-review` | 15/15 | 11/15 | 15/15 | 1/15 |
| `commit` | 15/15 | 9/15 | 15/15 | 6/15 |
| `debug` | 12/12 | 11/12 | 9/9 | 0/9 |

The outcome is what the user needs, such as the right defect line. The contract is the skill's output format, such as evidence per finding. A bare agent often reaches the outcome; it rarely shows its evidence. All 26 skill suites, the routing suite, the iterations behind each count, the limits, and how to rerun them: [evals/README.md](./evals/README.md).

One case: "Review this branch against origin/main." The diff makes `ratio` return 0 on any exception, and `greet("")` breaks a rule in `spec.md`. Trimmed excerpts of two real outputs from the same iteration:

```
Bare agent:
  calc.py - ratio (needs a fix): except Exception: return 0 is too broad. [...]
  greet.py (looks fine)

With code-review:
  Verdict: Fix 1 S1 finding (ratio swallows every exception and returns 0).
  | S1 | calc.py:4-5 | except Exception: return 0 hides every error [...] |
  | S2 | greet.py:2  | greet("") does not raise ValueError as spec.md item 2 requires |
  Trigger: ratio(1, 0), ratio("a", 2) or ratio(None, 1). [...]
  Not run: tests, and --deep, --cold and --spec.
```

## The loop

```
discover ─▶ grill ─▶ spec ─▶ grill --gaps ─▶ challenge ─▶ tickets ─▶ tdd ─▶ code-review ─▶ verify ─▶ commit ─▶ open-pr
                                                                    │
                                                                  debug
```

| You say | Skill | You get |
|---|---|---|
| "Where do I start in this repo?" | `discover` | Purpose, stack, git state, and the real build and test commands |
| "Grill me on the export idea" | `grill` | Rounds of questions, each with a recommended answer, and options where a decision needs them |
| "Plan the export feature" | `spec` | Scope, acceptance criteria, assumptions, failure scenarios |
| "What is this spec missing?" | `grill --gaps` | Each gap with a quote and one question; plain `grill` asks them one round at a time |
| "Poke holes in this plan" | `challenge` | Each claim checked against code and evidence; proceed, fix first, or stop, and the smaller version |
| "Split the plan into tickets" | `tickets` | End-to-end slices, one pull request each, with what blocks what |
| "Build it test-first" | `tdd` | One behavior at an agreed seam: a test that fails for the right reason, then the smallest change |
| "Why does this fail?" | `debug` | A fast command that shows the bug, tested hypotheses, and the defect proven by toggling it |
| "Review this branch" | `code-review` | Findings with location, trigger, consequence, and evidence; `--spec` also checks it against the spec |
| "Are we done?" | `verify` | One row per request: passed, failed, unverified, or blocked, with evidence |

## Install

The [`skills`](https://github.com/vercel-labs/skills) CLI detects your agents and installs the skills for each one:

```bash
npx skills add HugoLopes45/hl-skills                            # pick skills and agents interactively
npx skills add HugoLopes45/hl-skills --list                     # list the skills
npx skills add HugoLopes45/hl-skills -s code-review -s tdd -g   # some skills, for every project
npx skills add HugoLopes45/hl-skills -a codex -a cursor         # some agents
```

Without `-g`, skills install into the current project. To update, run `npx skills update`.

## Use

Your agent loads a skill when your request matches its description. To run a skill yourself, name it ("use code-review on this branch") or use the syntax of your agent, for example `/code-review` in Claude Code.

## Skills

### Engineering loop

| Skill | Does |
|---|---|
| `discover` | Orients you in a repository, or maps one area with `--scope` |
| `grill` | Questions you until the idea is clear, with options where a decision needs them; `--docs` keeps a glossary, `--gaps` reports missing decisions and edge cases |
| `spec` | Plans a feature; `--handoff` writes a brief for another agent, `--prd` a product and technical specification with sources |
| `challenge` | Tests the claims of a plan or finished work; `--premortem` traces how it fails, `--lens` and `--panel` apply method lenses |
| `tdd` | Builds one behavior with a verified red, green, refactor cycle at an agreed seam |
| `debug` | Builds a feedback loop and proves the root cause; on request, fixes it behind a failing regression test |
| `code-review` | Reviews a diff; `--spec` checks it against the spec, `--deep` adds parallel specialists and an independent skeptic |
| `deslop` | Removes AI-generated slop and invented APIs from a change |
| `verify` | Checks each requested outcome; `--claim` measures before and after, `--text` marks each claim in a text as supported, corrected, or unverified |
| `commit` | Writes a commit message from the staged diff, then commits |
| `open-pr` | Opens a draft pull request with why, changes, verification, and risks |
| `checkpoint` | Saves decisions and the next action before a context reset; `--stuck` names why work goes in circles and what breaks the loop |

### Decide and explain

| Skill | Does |
|---|---|
| `show-me` | Answers with a diagram, a tree, pseudocode, or an interactive HTML page instead of paragraphs |
| `explainer-video` | A short narrated explainer video on one topic, with a local voice by default |
| `spike` | A time-boxed experiment that answers one technical question |
| `adr` | An architecture decision record with the options considered and the cost of reversal |

### Codebase audits

| Skill | Does |
|---|---|
| `security-audit` | Runs scanners and traces untrusted input to dangerous sinks, scored by CWE and CVSS |
| `improve` | Finds the highest-value fixes and writes plans that another agent can run; `arch` writes an architecture report, `refactor` a behavior-preserving refactor in small steps |

### Delivery

| Skill | Does |
|---|---|
| `tickets` | Splits a feature into end-to-end slices, one pull request each, with blocking edges; `--tracker` writes them for Jira, Linear, GitHub, or GitLab |
| `split-pr` | Splits a large diff into pull requests in dependency order |
| `ci-fix` | Fixes failing checks without weakening tests or CI |
| `receive-review` | Decides agree, defer, disagree, or clarify for each review comment |
| `lessons` | Turns a session or a finished change into checks, rules, or pointers, cheapest first |
| `writing-for-agents` | Finds the shortest prompt that gets the behavior; `--skill` writes or reviews a skill |

### Product

| Skill | Does |
|---|---|
| `startup` | Evaluates an idea: assumption, problem, competition, first customers, MVP test; `scout` finds ideas, `ship` and `kill` decide after launch |
| `launch-marketing` | Positioning, landing copy, launch plan, channels, pricing, and offer |

### Lenses

A lens is a fixed method. It changes what the agent checks, not its tone. Run one with `challenge --lens minimalist <target>`, or several with `challenge --panel <target>`. The panel shows where the lenses disagree and does not average their results.

| Lens | Asks |
|---|---|
| `minimalist` | What is the smallest correct version? |
| `failure-hunter` | What breaks in production but not in development? |
| `data-model` | Which concerns are tangled together? |
| `distributed` | What happens with partitions, clock skew, and retries? |
| `operability` | Can on-call find and stop this at 3 a.m.? |
| `boring-stack` | Is new technology used only where it makes the product different? |
| `agent-tooling` | Which agent primitive fits, and what moves from the prompt into code? |
| `teacher` | Can you rebuild it from a small worked example? |
| `discovery` | Which outcome, for whom, and with what evidence? |

## Recipes

- **Idea to pull request:** `grill` → `spec` → `grill --gaps` → `challenge` → `tdd` for each behavior → `code-review` → `verify` → `commit` → `open-pr`.
- **Production bug:** `debug` to prove the defect, then ask it for the fix.
- **Before a risky merge:** `code-review --deep`, then `deslop` on the change.
- **Large feature:** `grill` to settle the decisions, then `tickets` for one pull request per slice.
- **Inherited codebase:** `discover --depth full`, then `improve arch`, then `improve` to turn findings into plans.
- **Startup idea:** `startup scout` without an idea, `startup` to evaluate one, or one stage with `--stage`. After launch, `startup ship` or `startup kill`.

## Contributing

Read [CONTRIBUTING.md](./CONTRIBUTING.md) and [STYLE.md](./STYLE.md). `python3 scripts/validate.py` checks the format of each skill and its links. Report vulnerabilities as [SECURITY.md](./SECURITY.md) describes.

## License

[MIT](./LICENSE)
