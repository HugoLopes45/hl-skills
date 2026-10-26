# Evals

These evals measure whether a skill changes what a real agent does. Each case runs in Claude Code with the skill installed and without it. The baseline omits the tested skill; other host capabilities may remain.

## Run

```bash
evals/run.sh debug --runs 3 --concurrency 3
python3 evals/report.py /tmp/hl-evals debug:1 --failures
```

Requirements: `uvx`, an authenticated `claude` CLI, and `pytest` on `PATH`. Costs vary by case and model. Use a bounded campaign.

| Variable | Default | Effect |
|---|---|---|
| `EVAL_MODEL` | `sonnet` | Agent model |
| `EVAL_WORKSPACE` | `/tmp/hl-evals` | Run output directory |
| `EVAL_SKILLS` | `skills/` | Skills root, for example an older copy to measure a change |
| `EVAL_SKILL` | `hl-<suite>` | Skill to install, when it is not `hl-<suite>` |
| `EVAL_MAX_COST` | unset | Optional post-run cost threshold in USD; stops later cases, not an in-flight spending cap |
| `EVAL_CLAUDE_SETTINGS` | unset | Native Claude settings file passed with `--settings`, for explicit permissions and sandbox policy |
| `EVAL_CHECK_SHELL` | system shell | Executable receiving `-c <command>` for command checks; use an OS-sandboxed shell for untrusted workspaces |

The wrapper removes the harness's permission-bypass flag and defaults to zero retries. Native Claude permissions still apply. Use an isolated `CLAUDE_CONFIG_DIR` and an explicit sandbox policy. Verify skill discovery and command permissions in one fresh pilot before starting a batch.

Claude's sandbox does not cover post-grade commands. Set `EVAL_CHECK_SHELL` to a sandboxed shell that removes private environment variables and blocks outside writes, private reads, and network access. Otherwise, command checks retain the caller's privileges. Transcript archival happens before command execution.

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

Output checks read the final answer. Process checks read the session transcript and its subagent transcripts. The post-grade hook archives these under the run's `outputs/`, using `CLAUDE_CONFIG_DIR` when set. Reporting reads the archive without changing it.

Positive command checks require completed tool results; denied, unfinished, and backgrounded attempts are not execution proof. `ran_before_edit` requires a completion timestamp before an edit request. Negative command and skill checks count attempts, even when rejected. Request snapshots are not additional tool calls.

`not_exposed` searches the supplied pattern in the final answer and serialized assistant items, tool results and native receipts, including subagents. User prompts and API request snapshots are excluded. Reading the raw fixture key into a tool result fails, even when the final answer redacts it. Missing transcripts cannot pass; failure evidence never copies the match. This known-fixture check does not certify encoded, split, partial or uncaptured disclosures, or saved-artifact compliance.

Completed shell requests can include nonzero exits. They do not prove that every matching subcommand ran or passed; qualification must inspect actual output and artifacts.

Tool-count minimums require completed calls. Maximums count all attempts, including refused calls.

`report.py` re-evaluates output and process checks with the current `checks.json`; workspace and command checks keep their recorded results. A command check receives the final answer on standard input.

Workspace comparisons use descriptor-relative POSIX opens and reject symbolic links or non-regular files in checked paths. Single-file checks do not inspect unrelated paths.

Reports accept the harness's single-run and repeated-run layouts. They reconcile scheduled runs with the latest invocation's `summary.json`, `progress.jsonl`, and `run_meta.json`. Missing, skipped, stale, or unfinished runs are reported explicitly. Missing required evidence and CLI errors cannot produce passing runs. Retries with missing earlier-attempt evidence are incomplete; their reported costs are subtotals. Deleted-file and command-timeout checks record failures without losing the remaining grades.

Task checks accept any wording of the right outcome, such as "valid, fix it" for agree. Checks that need the skill's vocabulary or format are contract checks.

`gh`, `jira`, and `acli` are failing stubs; selected forge credentials are removed, and the `gh` config directory is empty. These measures reduce accidental access but do not isolate the filesystem or network. The caller must configure that isolation. Claude auto memory is off because workspace paths can repeat. `hl-open-pr` and `hl-ci-fix` cases cover `--dry-run`, refusals, and the stop when GitHub is unreachable.

Eval ids must be unique across suites: agent-skill-eval names each agent workspace after the eval id only, so two suites with the same id corrupt each other when run in parallel. A unit test enforces it.

A bare agent is not expected to meet a skill's contract. Task checks show whether the contract costs correctness. A run passes a kind only when all required checks pass, its evidence is complete, and the CLI succeeds. `p` is the one-sided Fisher exact test comparing run passes. Incomplete or excluded runs make it `n/a`. Leftover runs from an earlier invocation also suppress significance rather than silently disappearing from the audit.

### Prompt depth

The `ambitious` suite covers a bounded bug fix, missing conversion evidence in French, subjective fiction, an already-specific parser task, an absent task, an unverifiable success criterion, a method needing an independent check, and a time-boxed analysis that must not become a tooling project. It also covers a postmortem that must borrow methods, not roles (`range`), a crash fix whose larger goal belongs in Next only (`higher-outcome`), and a modest target that needs a proposed stretch target (`stretch-target`).

Run it with `evals/run.sh ambitious --runs 3 --concurrency 3`. Task checks read the fenced prompt for the user's constraints; contract checks read the output format, the Next options, and the absence of edits. Review each answer against its `expected_output` too: a regular expression cannot establish that a method or check is sound. With Sonnet, 3 runs per case: task 33/33 runs passing with the skill, 3/33 without; contract 33/33 with, 0/33 without.

Fresh-context model samples exercise the instructions, not host discovery or natural routing. Neither samples nor forced invocation prove that an agent selects `hl-ambitious` instead of the neighboring skills.

For comparative evaluations, fix the requests and criteria before generation. Keep the model and inputs identical, hide skill identities, and review each pair in both presentation orders. Count order disagreements as inconclusive. Prefer preserved scope, usable primary material, concrete methods, and checks that reject plausible errors, not output length or signature wording. After tuning on a case, use new held-out requests; retain losses and ties. Model preferences do not prove universal superiority or domain correctness.

## Production qualification

Production qualification is incomplete. Automatic eval passes do not establish compliance with the full skill contract or safety requirements. Current-source qualification, including permission and missing-evidence boundaries, remains necessary before claiming readiness.

Release criteria:

- Record complete run identity, source revision, model, inputs, tool outcomes, final output, grading, and reported costs; missing evidence is not a pass.
- Review claims against actual artifacts and outcomes, not only answer shape or regular expressions.
- Verify supported skills and modes, including permission boundaries; keep unsupported or unexercised behavior explicit.
- Run the validator and test suites, verify installed skill files match source, and obtain independent review of release changes.

Observed failures include synthetic secret exposure and inaccurate execution reporting. Automatic passes do not certify full-contract compliance, complete safety, or saved artifacts. Isolation probes and successful installations are not substitutes for production qualification.


## Historical results

These tables describe earlier generations and checks. They are not a fresh comparison of the revised skills. The older baseline's other host capabilities are unverified here; “bare agent” means without the tested skill.

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

### Hard cases for code-review

Use the declared skill alias and a dedicated workspace. Both code-review suites declare `hl-code-review`; sharing a workspace can mix their case IDs during reporting. Use a fresh root, then report the iteration printed by the runner:

```bash
EVAL_SKILL=hl-code-review EVAL_WORKSPACE=/tmp/hl-code-review-hard evals/run.sh code-review-hard --runs 2 --concurrency 2
python3 evals/report.py /tmp/hl-code-review-hard code-review-hard:1 --failures
```

The report command assumes the first iteration in this fresh root. Replace `1` with the printed iteration on subsequent runs.

The suite `code-review-hard` holds 23 `hl-code-review` cases built from a real review that inflated severity. Each fixture builds `main`, then a `feature` branch:
- Severity traps that must not count as a problem: a parameter that types and a schema exclude (`cr-schema`), a branch behind a guard (`cr-unreachable`, also `--deep`), an accepted trade-off in `docs/decisions.md` (`cr-tradeoff`), a migration that `deploy.sh` runs first (`cr-deploy-order`). Each expects `Clear`.
- Clean changes: an equivalent rewrite (`cr-clean`), a removed duplicate test (`cr-test-only`), a correct `dedupe` with a vacuous test (`cr-vacuous`).
- Real defects: the unit of the first row labels every series (`cr-units`, French, also `--deep`), an email check, SQL injection, a test weakened to pass, a requirement only in a commit body, a pager off-by-one inside a 240-line generated file (`cr-noise`), a defect in moved code (`cr-moved`), a column drop without backfill, a missing ownership check, a removed lock (French), two independent bugs (`cr-two-bugs`, `Fix (2 problems)`).
- Scope: uncommitted edits stay out (`cr-uncommitted`); the default branch is `trunk`, not the stale `main` (`cr-trunk`).
- `cr-revise`: the user pastes an earlier French review that used "bloquant" and disputes one point. The answer must keep one problem, use only the four severity words, name a file in the first Next step, and not narrate a retraction.

Runs passing all checks, with the skill only, graded with the current checks:

| Version | Hard suite | Old `code-review` suite |
|---|---|---|
| Before this work | 56/63 (21 cases; `cr-lock` left out, its prompt changed), `cr-revise` 0/3 | 14/15 |
| Severity calibration, language, line rules | 60/66 | not run |
| Skeptic gets only the two top severities | 63/66 | 13/15 |
| One problem per root cause | 65/66 | 13/15 |
| One severity scale in every reference, revised-review rule | 64/69 (1 run hung) | 14/15 |
| Review fixes below | 68/69 | 15/15 |
| Weakened test adds nothing to the count | `cr-noise`, `cr-weakened`, `cr-two-bugs`: 9/9 | not run |

Fixes driven by the runs:
- The real review called a tooltip display "blocking". Severity now comes from what a user or caller hits, after a trace through callers, guards, types, and schemas, and a comparison with the base. A weak test is a limited issue.
- `cr-revise` with the old skill answered in English in 2 of 3 runs and kept "bloquant" or "high". The specialist references used a blocking/high/advisory scale. All files now use `data or security failure`, `material bug`, `limited issue`, `cosmetic`. A revised review never names the earlier severity.
- `--deep` once replaced its report with a late turn after a scheduled wakeup, and once hung in a shell loop that polled background subagents. Subagents now run in the foreground.
- Line numbers come from a numbered read at the target revision, never from diff hunks.

An independent review found 2 dangerous rules and 7 check defects. A missing line number turned a pasted-diff finding unresolved, so the location now falls back to file and function. An unknown deploy condition made a finding unresolved and a verdict `Clear`; the reviewer now reads deploy, configuration, and docs first, and `Clear` counts unresolved candidates, which the first Next step settles. Check fixes, each with a unit test: French `Verdict :` spacing, a bare `generated/` path that passed the exclusion check, "authorization is unchanged" that passed the IDOR check, "trace" that matched "race", and more retraction and severity wording in French. The `cr-noise` fixture shifted protobuf field numbers, a second possible bug; the regeneration is now additive.

A fresh agent then regenerated the skill from an 830-word brief, and the result was trimmed. Same 84 runs, current checks, runs passing all checks:

| Version | Words | Runs passing | Cost | Output tokens |
|---|---|---|---|---|
| Previous skill | 2143 | 79/84 | 11.24 USD | 117k |
| Regenerated, 2 samples | 1427 | 81/84, 81/84 | 10.61, 10.31 USD | 150k, 147k |
| Trimmed, no shared preamble | 1367 | 81/84 | 10.23 USD | 123k |
| Trimmed, shared preamble | 1607 | 80/84 | 10.38 USD | 143k |
| Trimmed, second sample | 1367 | 80/84 | 10.16 USD | 135k |
| Latest generation in this comparison: trimmed, grounding line, 6 fixes from failures, 2 samples | 1500 | 83/84, 82/84 | 10.38, 10.31 USD | 119k, 128k |

The 6 fixes: the reply language follows the request text, not the commit messages; line 1 stays the review after subagents return; caveats name the base branch; a finding is plain sentences with `file:line`, without labels; a hidden-bug test change is never its own point; mixed-version deploy risk is unresolved unless the repository shows such deploys. The race check now accepts French "en même temps" and "simultané".

The brief must tell the writer to copy the rules verbatim: one regeneration dropped the language rule, and 6 runs answered French requests in English. The `--deep` naming check now accepts a list ("The architecture, simplicity and security reviews found").

Cost: 8.39 USD for the 69 hard runs and 2.59 USD for the 15 old runs at the last full pass. Limits: 3 runs per case, one model (sonnet), regular-expression checks, and the tooltip rated limited because its docstring says it shows the unscaled row.

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
- `pr-ready-stale` and `cr-rereview` have no recorded runs. The `cr-rereview` setup builds on the code-review repository and has not run in the harness. Their regular expressions can pass on quoted numbers or on any question near the word "split", and the no-run check can fail on a harmless search for "pytest".
- An `hl-improve` case that forced asking before a direct "fix it" was removed: the request and the case contradicted each other.
- agent-skill-eval runs `git init` in every workspace; a case that needs no repository deletes `.git` in `.eval-setup.sh`.
- A bare agent sometimes writes the tickets, then its CLI does not exit; those runs time out and are excluded, so `hl-tickets` has fewer baseline runs.
- A prompt that starts with `--` makes the bare `claude` CLI fail; start prompts with a word.
