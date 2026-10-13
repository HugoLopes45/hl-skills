# Evals

These evals measure whether a skill changes what a real agent does. Each case runs in Claude Code with the skill installed and without it. User-level settings, skills, commands, and `CLAUDE.md` are excluded, so the baseline is a bare agent.

## Run

```bash
evals/run.sh debug --runs 3 --concurrency 3
python3 evals/report.py /tmp/hl-evals debug:1 --failures
```

Requirements: `uvx`, an authenticated `claude` CLI, and `pytest` on `PATH`. A run costs about 0.30 USD per skill and repetition with the default `sonnet` model.

| Variable | Default | Effect |
|---|---|---|
| `EVAL_MODEL` | `sonnet` | Agent model |
| `EVAL_WORKSPACE` | `/tmp/hl-evals` | Run output directory |
| `EVAL_SKILLS` | `skills/` | Skills root, for example an older copy to measure a change |
| `EVAL_SKILL` | `hl-<suite>` | Skill to install, when it is not `hl-<suite>` |
| `EVAL_MAX_COST` | `1.5` | Cost cap per case in USD |

Natural triggering, with every skill installed and no skill named:

```bash
EVAL_SKILL=hl-debug EVAL_WORKSPACE=/tmp/hl-evals-routing evals/run.sh routing --runs 3 --concurrency 3 --no-baseline
python3 evals/report.py /tmp/hl-evals-routing routing:1 --failures
```

## Layout

A suite is named after its skill without the `hl-` prefix: suite `debug` tests `hl-debug`.

| Path | Content |
|---|---|
| `<suite>/evals.json` | Cases in the [agent-skill-eval](https://pypi.org/project/agent-skill-eval/) format |
| `<suite>/files/<fixture>/` | Files copied into the agent workspace |
| `<suite>/files/<fixture>/.eval-setup.sh` | Optional: shell script that builds the case's git state (branches, commits, staged changes) in the workspace, then is deleted before the agent starts |
| `<suite>/checks.json` | Deterministic checks for each case |
| `<suite>/repo.sh` | Optional: builds a git repository for the cases, passed as `--source-repo` |
| `check.py` | Post-grade hook that runs the checks |
| `report.py` | Pass counts per skill, check kind, and configuration |

Each check is one of three kinds:
- `task`: the outcome a user needs, such as the right defect line or passing tests.
- `contract`: the output contract of the skill, such as the first line or the evidence table.
- `trigger`: in `routing`, whether the agent picked the right skill.

Output checks read the final answer. Process checks (`ran`, `not_ran`, `ran_before_edit`, `tools`, `skill_invoked`, `skill_not_invoked`) read the session transcript and the transcripts of its subagents, merged in time order, so "ran the tests before editing" is observed, not inferred from wording. `report.py` re-evaluates output and process checks with the current `checks.json`; workspace and command checks keep the result recorded during the run. A command check gets the final answer on standard input, so it can accept a finding from a report file or from the answer.

Task checks accept any wording of the right outcome, such as "valid, fix it" for agree. Checks that need the skill's vocabulary or format are contract checks.

`gh`, `jira`, and `acli` are stubs that fail, `GH_TOKEN`, `GITHUB_TOKEN`, and every `JIRA*` and `ATLASSIAN*` variable are unset, and the `gh` config directory is empty, so no run reaches a real GitHub or Jira account. Claude auto memory is off: it is keyed by workspace path, and paths repeat across iterations, so memory from one run could leak into the next. `hl-open-pr` and `hl-ci-fix` cases cover `--dry-run`, refusals, and the stop when GitHub is unreachable.

Eval ids must be unique across suites: agent-skill-eval names each agent workspace after the eval id only, so two suites with the same id corrupt each other when run in parallel. A unit test enforces it.

A bare agent is not expected to meet a skill's contract. The task checks show whether the contract costs correctness. A run passes a kind when all its checks of that kind pass. `p` is the one-sided Fisher exact test that runs pass more often with the skill.

## Results

Claude Code 2.1.295, `sonnet`, agent-skill-eval 0.7.0, 3 repetitions per case and configuration. Iteration 45 for `hl-challenge`; iteration 43 for `hl-grill`, `hl-launch-marketing`, `hl-spike`, `hl-startup`, `hl-tickets`, and `hl-verify`, rerun after their checks changed; iteration 41 for `hl-explainer-video`, after the shell fix below; iteration 40 for the rest. Auto memory was off. Runs passing, with the skill against a bare agent:

| Skill | Task with | Task without | p | Contract with | Contract without | p |
|---|---|---|---|---|---|---|
| adr | 9/9 | 3/9 | 0.005 | 6/6 | 0/6 | 0.001 |
| challenge | 18/18 | 18/18 | 1.000 | 16/18 | 3/18 | <0.001 |
| checkpoint | 9/9 | 9/9 | 1.000 | 9/9 | 0/9 | <0.001 |
| ci-fix | 3/3 | 3/3 | 1.000 | 3/3 | 0/3 | 0.050 |
| code-review | 6/6 | 6/6 | 1.000 | 6/6 | 0/6 | 0.001 |
| commit | 15/15 | 9/15 | 0.008 | 15/15 | 6/15 | <0.001 |
| debug | 12/12 | 11/12 | 0.500 | 9/9 | 0/9 | <0.001 |
| deslop | 6/6 | 3/6 | 0.091 | 6/6 | 0/6 | 0.001 |
| discover | 6/6 | 5/6 | 0.500 | 6/6 | 3/6 | 0.091 |
| explainer-video | 9/9 | 5/9 | 0.041 | 6/6 | 0/6 | 0.001 |
| grill | 30/30 | 21/30 | 0.001 | 24/24 | 9/24 | <0.001 |
| improve | 6/6 | 6/6 | 1.000 | 3/3 | 0/3 | 0.050 |
| launch-marketing | 9/9 | 8/9 | 0.500 | 3/3 | 0/3 | 0.050 |
| lessons | 6/6 | 0/6 | 0.001 | 3/3 | 2/3 | 0.500 |
| open-pr | 9/9 | 7/9 | 0.235 | 9/9 | 5/9 | 0.041 |
| receive-review | 3/3 | 3/3 | 1.000 | 3/3 | 0/3 | 0.050 |
| security-audit | 6/6 | 6/6 | 1.000 | 6/6 | 0/6 | 0.001 |
| show-me | 6/6 | 6/6 | 1.000 | 3/3 | 1/3 | 0.200 |
| spec | 12/12 | 12/12 | 1.000 | 3/3 | 0/3 | 0.050 |
| spike | 9/9 | 6/9 | 0.103 | 6/6 | 3/6 | 0.091 |
| split-pr | 6/6 | 5/6 | 0.500 | 6/6 | 1/6 | 0.008 |
| startup | 12/12 | 11/12 | 0.500 | 6/6 | 0/6 | 0.001 |
| tdd | 12/12 | 9/12 | 0.109 | 9/9 | 0/9 | <0.001 |
| tickets | 15/15 | 12/15 | 0.112 | 12/12 | 2/12 | <0.001 |
| verify | 15/15 | 10/15 | 0.021 | 12/12 | 3/12 | <0.001 |
| writing-for-agents | 9/9 | 6/9 | 0.103 | 12/12 | 0/12 | <0.001 |

Remaining failures with the skill, iteration 45: `hl-challenge` 2 of 18 contract runs. One `finished-work` run wrote `stop`, then corrected itself to `fix first` in the same line; the rule now says to settle the verdict before writing it. One `lens-pick` quick answer ran 382 words, over the 360-word margin. Iteration 46, with the skill only, on the five cases that had contract checks then: 15 of 15 contract runs, quick answers 247 to 340 words.

Fixes driven by these runs:
- `hl-verify` judged a requirement the task never stated (2 of 3 runs). It now judges stated requirements only.
- `hl-adr` wrote Accepted from "we chose", and numbered a file with no ADR sequence. It now needs a recorded approval, says the number is unknown, and keeps `<NNNN>`.
- `hl-commit` added the host's `Co-Authored-By` trailer in 1 of 3 runs. It now names that trailer and overrides the host default.
- `hl-grill` stopped triggering on "three ways to add retries, with trade-offs" after a rewrite. Its description leads with options again. It also records forced decisions as assumed instead of asking again.
- `hl-commit`, `hl-adr`, and `hl-challenge` put a status line before the required first line. Each now says the first line comes with no preamble.
- `hl-security-audit` did not trigger on an audit request phrased around user input. Its description now names that case.
- `hl-spike` gave a verdict before a success threshold existed. It now asks without a verdict.
- `hl-tickets` searched the environment for a Jira token, then counted `JIRA*` variables after a first fix. It now uses only access already set up, never reads the environment to find a credential, and reports no access otherwise.
- `hl-challenge` answered `stop` for a small missing requirement. The verdict rules now say that a small fix is `fix first`.
- `hl-writing-for-agents` rewrote an existing skill that covered the job, and wrote `Use before` instead of `Use when`. It now never rewrites a skill it was not given, and checks for the exact words.
- Word limits: `hl-startup` quick answers, `hl-challenge --lens` quick answers, and `hl-launch-marketing` quick positioning ran over their limits. A limit in words alone, or a sentence count, did not hold. Each now gives a per-part budget, such as five items of at most 30 words that replace the mode's sections. Last runs: 158 to 171, 226 to 310, and 191 to 281 words.
- `hl-debug` takes line numbers from numbered tool output: 6 of 6 runs cited the right line, against 5 of 7 in earlier iterations.
- `hl-explainer-video` answered a background-job notice instead of giving its report. The cause was the eval machine: `run.sh` now sets `CLAUDE_CODE_SHELL=/bin/bash`, because the agent shell inherited a zsh alias `ls=eza`, and `eza` with no path waits on standard input. Every hung command ended in a bare `ls`; 0 of 18 runs hung after the fix. The skill also says to run renders in the foreground.

Natural triggering (`routing`, 21 requests, every skill installed): 122 of 126 runs over iterations 40 and 41 picked the expected skill and no excluded skill. The `hl-debug` request is the weakest: 0 of 3 runs at iteration 40, 3 of 3 at iteration 41, because the agent can fix a trivial bug directly. `brainstorm-options` missed `hl-grill` in 1 of 6 runs.

### Mode cases

Iteration 50 added 31 adversarial cases, one per mode that had no case, and 4 routing requests. Runs passing at iteration 50, graded with the current checks, new cases only. `hl-improve` arch-audit and `hl-security-audit` audit-scoped come from iteration 52, because their checks read files and a regrade keeps the recorded result. The `hl-security-audit` audit-deep finding check changed after the run; it was rerun by hand on the stored answers:

| Skill | Cases | Task with | Task without | p | Contract with | Contract without | p |
|---|---|---|---|---|---|---|---|
| code-review | 3 | 9/9 | 5/9 | 0.041 | 9/9 | 1/9 | <0.001 |
| deslop | 2 | 6/6 | 6/6 | 1.000 | | | |
| discover | 3 | 9/9 | 6/9 | 0.103 | 9/9 | 3/9 | 0.005 |
| improve | 6 | 18/18 | 12/18 | 0.010 | 18/18 | 0/18 | <0.001 |
| launch-marketing | 6 | 18/18 | 17/18 | 0.500 | 14/18 | 1/18 | <0.001 |
| receive-review | 2 | 6/6 | 6/6 | 1.000 | 3/3 | 0/3 | 0.050 |
| security-audit | 3 | 9/9 | 9/9 | 1.000 | 8/9 | 1/9 | 0.002 |
| startup | 5 | 15/15 | 15/15 | 1.000 | 13/15 | 0/15 | <0.001 |
| tickets | 1 | 3/3 | 2/3 | 0.500 | | | |

The 4 new routing requests (`adr-record`, `review-branch`, `respond-review`, `video-hashmap`): 12 of 12 runs picked the expected skill.

Iteration 56 checked the 4 descriptions reworded to say "Use when" (`hl-verify`, `hl-checkpoint`, `hl-deslop`, `hl-lessons`) and added `slop-cleanup`, the first routing request for `hl-deslop`: 15 of 15 runs on `verify-done`, `factcheck-doc`, `lessons-retro`, `stuck-loop`, and `slop-cleanup` picked the expected skill and no excluded skill.

### Hard cases for debug and challenge

Iteration 60 added 6 cases that a bare agent can get wrong. For `hl-debug`, a test that has a wrong expectation (`wrong-expectation`), a data commit that exposes a parser defect (`trigger`), and a test that fails with hash order (`flaky`). For `hl-challenge`, a plan that a writer in the code contradicts (`pricecache`), a sound plan (`soundplan`), and finished work that has green tests but misses a requirement (`export`). `trigger` is from iteration 61: its no-edit check compared the files with the fixture, which the setup commit changes, and now uses `git status`. Runs passing:

| Skill | Cases | Task with | Task without | p | Contract with | Contract without | p |
|---|---|---|---|---|---|---|---|
| debug | 3 | 9/9 | 5/9 | 0.041 | 9/9 | 0/9 | <0.001 |
| challenge | 3 | 9/9 | 9/9 | 1.000 | 8/9 | 0/9 | <0.001 |

The bare agent found the right cause and verdict in all 18 runs. It blamed the test, not `billing.py`. It blamed the parser, not the data. It found the set order, and it said `proceed` on the sound plan. The `hl-debug` task gap comes from line citations (`report.py:6`, `tags.py:2`) and one run that did not rule out float precision. The skill adds measured proof: `flaky` with the skill measured the failure rate over seeds (for example 40 of 50) and ran a toggle test; the bare agent did not measure a rate in 3 of 3 runs. Median cost per run: `hl-debug` 0.076 to 0.078 USD with the skill, 0.043 to 0.055 without; `flaky` took 97 s against 7 s.

### Complex debug cases and the deeper debug skill

Iteration 62 added 4 `hl-debug` cases with decoys:
- `bisect`: a regression in 16 commits. The cause is a reordered regex alternation in a "feat: add day unit" commit. The decoys are parser commits before and after it. The checkout must stay on `main` at the same commit.
- `envprec`: the user suspects an off-by-one in a correct retry loop and asks for a fix. The defect is the inverted precedence of the environment over the command line.
- `pollution`: a test passes alone and fails in the suite, because another module mutates a cached settings dict.
- `heisenbug`: a cron count is 0 and `--verbose` shows 4. The user suspects the cron environment. The cause is a generator that is read twice.

The skill then took ideas from public debug skills:
- ranked falsifiable hypotheses that include the user's suspect;
- bisect on any axis (commits, input, configuration, dependencies, environment, test order), with a stable predicate and `git bisect run` exit codes;
- polluter search; a working-against-broken differential; logs at component boundaries;
- conditional breakpoints on the broken invariant;
- "two failed hypotheses at one place: reread the code";
- prevention and blast radius in the report;
- a fix mode, only on request: a failing regression test, the smallest change, a rerun of the loop, removal of the debug logs, and a stop after three failed fixes.

Runs passing all checks, graded with the current checks (bare agent and old skill at iteration 62, final skill at iteration 70, `envprec` at iteration 71 after its check fix):

| Case | Bare agent | Old skill | New skill |
|---|---|---|---|
| bisect | 0/3 | 3/3 | 3/3 |
| envprec | 0/3 | 0/3 | 3/3 |
| pollution | 0/3 | 3/3 | 3/3 |
| heisenbug | 0/3 | 3/3 | 3/3 |
| 7 existing cases | not rerun | not rerun | 21/21 |

The bare agent found the cause in most runs. It failed on proof and safety: no toggle of the culprit, `git bisect` in the user's checkout, and an unrequested code change after "Investigate". The old skill refused the requested fix in `envprec` (0/3). The new skill fixed it behind a regression test that fails on the old `config.py` (3/3). The diagnosis ideas did not move the measured score: the old skill already passed the other 3 cases. Two edits came from these runs. Reading files with numbered output restored `failing-test` line citations (old skill 4/5, first new text 4/8, final text 5/5 at iteration 66). Asking who else the defect reaches restored the production impact in `pollution` (iteration 68: 1/3, iteration 69: 5/5). Median cost per run on the 4 cases: 0.066 USD for the bare agent, and 0.094 for the old and the new skill. An independent review of the checks found false passes: "production" matched "not production", and `cat -n test_invoice.py test_report.py` counted as a polluter run. Each fix has a unit test. The harness makes its own first commit, so commit hashes change per run: checks name the commit by its title. Limits: 3 to 5 runs per case, one model, and fixtures written for these checks.

Three independent reviews of the checks found false passes, false fails, and task checks that required the skill's format. Each fix has a unit test. `report.py` reruns output checks and answer-only oracle commands with the current checks; other commands keep the recorded result, also when the check moved to another kind. Checks that read a report file also read the answer, so a correct answer given in chat passes. Compound checks were split, so cutting one feature does not pass the check for the other. Cases with no target have an "Invents no" check against made-up plans, verdicts, or rounds. `run.sh` isolates git from the global git config and hooks. The new no-target checks ran at iteration 52 with the baseline: `hl-verify` text-none, `hl-challenge` lens-no-target, and `hl-grill` no-idea passed 3 of 3 runs in both configurations. The `hl-verify` and `hl-grill` rows above predate them.

Fixes driven by these runs, rerun with the skill only (iterations 51 to 54) or with the baseline (`hl-launch-marketing` 55, `hl-startup` 53, `hl-improve` 51 and 52, `hl-security-audit` 52):
- `hl-security-audit` quick kept MEDIUM findings. Quick now drops them: 3 of 3 contract runs.
- `hl-startup` quick scout ran 438 to 531 words against a 440-word cap, and 474 to 508 after a first fix. A per-part budget replaced the word total, and quick drops the build sketch and the risk list: 282 to 328 words in 6 of 6 runs at iterations 52 and 53.
- `hl-launch-marketing` economics did not lead with a figure. The first line now states the number that hurts most, as a figure; its example no longer uses the case's own figures: 3 of 3 runs at iteration 55. Quick channels put experiments in blocks under the table; they now go in the table rows. Launch plans gave venue rules such as a self-promotion ratio with no label; the rule's number is now labeled public or estimated: 3 of 3 contract runs at iteration 54.
- Check fixes, each with a unit test: lead checks allow a `# title` line before the lead; the `hl-discover` scoped-run check failed a run that only promised a read order; the `pricing-low` label check now targets the buyer's alternative cost, the one number the answer derives from an estimate; a `100%` done-when target is not a claim. `oracle.py` splits labels (estimate, measured, public), sources, and withheld numbers: a number label contract needs a label or a source, and a fake-claim check accepts a label or a refusal, never a publisher name alone. `hl-code-review --deep` must start at least the six specialists the diff requires.

Limits:
- Regular expressions and `oracle.py` check the contract. They show the shape of the output, not its quality.
- Three repetitions detect large differences only.
- Task checks do not separate the skill from the baseline for `hl-challenge`, also on the hard cases, `hl-checkpoint`, `hl-ci-fix`, `hl-receive-review`, `hl-show-me`, and `hl-spec`, the first cases of `hl-code-review` and `hl-improve`, all `hl-security-audit` cases, and the new `hl-deslop`, `hl-launch-marketing`, `hl-receive-review`, `hl-startup`, and `hl-tickets` cases: a bare agent also reaches the right outcome. Their gain is the contract.
- The `hl-improve` task gap on the new cases comes from prompts in the skill's command syntax, such as "Run improve branch." A bare agent cannot know what they mean, so the gap overstates the skill's outcome gain.
- `oracle.py` takes any parenthesized list of capitalized names, such as "(ProZ, Reddit)", as a named source. A list of venues passes as a citation.
- `hl-ci-fix` and `hl-open-pr` are not tested against a live pull request: no case reads real check logs, pushes, or creates a pull request.
- An `hl-improve` case that forced asking before a direct "fix it" was removed: the request and the case contradicted each other.
- agent-skill-eval runs `git init` in every workspace; a case that needs no repository deletes `.git` in `.eval-setup.sh`.
- A bare agent sometimes writes the tickets, then its CLI does not exit; those runs time out and are excluded, so `hl-tickets` has fewer baseline runs.
- A prompt that starts with `--` makes the bare `claude` CLI fail; start prompts with a word.
