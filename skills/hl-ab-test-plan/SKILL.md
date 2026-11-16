---
name: hl-ab-test-plan
description: "Plan one A/B test: hypothesis, the single changed element, primary and guardrail metrics, eligible audience, sample size from a supplied baseline and minimum effect, a fixed-horizon or valid sequential analysis plan, and decision rules. Sizes nothing it lacks inputs for and never states an expected lift. Starts no test. Use when the user asks how many visitors or days a test needs, how to design or read an A/B or split test, or when to stop one."
---
# A/B Test Plan

Input: `[hypothesis or page and element to test] [baseline, eligible traffic, and minimum effect, when known] [analysis design, optional]`

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

## Evidence rules

- A baseline is a measured rate with its period, source, and eligible population. Without one, sizing is blocked (see the Output section).
- The minimum effect is the smallest change that would alter the decision. The owner supplies it as a business input. It is not a forecast of the outcome. Never write an expected lift, uplift, or win rate.
- Do not state that a result is certain, proven, or guaranteed by statistics. A test gives a conclusion with the error rates chosen before launch.
- Compute sample size only from supplied inputs, with the method in [references/sizing.md](references/sizing.md). Show the inputs and the result together.
- The stopping rule follows the analysis design. A fixed-horizon test is read once, at its planned size. A sequential test uses a method built for repeated looks, with its looks written in the plan. Significance at any other moment is not a stopping rule.
- Power and alpha are choices. Offer 0.05 for alpha and 0.80 for power as conventions the owner accepts or changes. Power of 0.80 is not a universal target.
- A test does not start, enable, ramp, or roll out in any tool. Write the rollout as a plan item that needs the owner's explicit approval.

## Intent

Use targeted questions only when missing context changes the requested deliverable. Group related questions in a round, then continue if essential uncertainty remains; there is no fixed intake checklist or total round limit. Reuse prior answers and do not expand a narrow task into the full workflow.

- Act directly when the hypothesis, the one element, the primary metric, and the baseline are supplied.
- Ask in one round for missing essentials: the hypothesis or changed element, the primary metric, the baseline (`Default: none`), eligible traffic per day (`Default: none`), and the minimum effect. Explain in one line what each answer changes. The minimum effect has no default, because it sets the test size.
- Missing sizing inputs do not stop the plan. Write the plan, mark its sizing section blocked, and list each missing input.
- Reuse what the user already supplied.
- An exact output format the user names replaces the default output. The evidence rules still apply.

## Plan rules

- State one hypothesis: "If [change] for [eligible visitors], then [primary metric] changes in [direction], because [reason]." The reason cites evidence, or is labeled an assumption.
- Isolate one element when the hypothesis concerns that element. A bundled change is a redesign test: estimate the bundle's effect, not any component's contribution. Split it into separate tests only when component attribution is the decision.
- Name one primary metric before launch. For each guardrail, specify its population, window, owner-approved harm threshold and pause or rollback action. Missing thresholds block launch, not drafting. A higher completion rate does not justify harm to lead quality, refunds or safety.
- Name the unit of randomization, the unit the metric counts. Each unit sees one variant for the whole test.
- Name the eligibility rule that decides who enters the test. Apply it before assignment.
- More than one primary metric or more than one comparison needs a multiple-comparison correction chosen before launch. Holm is one method. With no correction planned, the plan allows one primary comparison.
- Before launch, check assignment ratios and that exposure is logged for each variant. Change no variant during the test.
- Prespecify the sample-ratio-mismatch test, expected allocation, significance threshold and investigation action. Use a chi-square test only when its expected-count assumptions hold; otherwise name an appropriate exact test or leave the check pending. Unequal counts alone do not prove a fault. Investigate a flagged mismatch before reading effects. Any triggered analysis must use a condition observed equivalently in both variants, not a treatment-only event.

## Analysis design

Choose one design before launch and write it in the plan.

- **Fixed horizon**: a planned size per variant and an end date. The result is read once, at the end.
- **Valid sequential**: a planned maximum size, a fixed number of looks, and the boundary method for those looks. Name the method. The tool that runs the test must implement it. If it cannot, use the fixed-horizon design.
- Not allowed: a fixed-horizon test that is checked each day and stopped at the first significant result.

## Decision rules

- Decide from the effect size and its interval, not from the p-value alone. State the minimum effect worth acting on, and what counts as no clear difference.
- Check guardrails and assignment before reading the primary result.
- A segment result is exploratory unless the segment and its correction were fixed before launch.

## Workflow

1. Restate the hypothesis, the element, the primary metric, guardrails, unit, and eligibility rule.
2. Check the sizing inputs. Compute the size with the reference method, or mark sizing blocked.
3. Choose the analysis design and write its stopping rule or its single read.
4. Write the QA checks, the decision rules, and the rollout steps as plan items. Stop before any rollout.

## Output

Reader: the owner who approves and runs the test. The decision served: whether to run this test now with the stated size and duration, or first to collect the missing inputs.

Line 1 is one bold plain sentence that gives the decision, for example "**The test can run once the owner approves a fixed-horizon design with the size shown below.**" It never opens with a label, verdict word, or number.

Under line 1, in plain sentences: each missing input that blocks the sizing, with its source requirement, and each choice the owner must make (analysis design, alpha, power).

The plan is the artifact. Put it in a `markdown` fence with these sections, in this order: `## Hypothesis`, `## Design`, `## Sizing`, `## Analysis and stopping rule`, `## QA`, `## Decision rules`, and `## Rollout (not started)`. In `## Sizing`, show the inputs and the result as plain lines. When sizing is blocked, write `Blocked: <input names>` in place of the result.

Verdict words:
- `Planned`: sizing computed from supplied inputs, and the stopping rule is written.
- `Sizing blocked`: plan drafted; sizing needs the listed inputs.
- `Stopped`: no hypothesis or no changed element to test.

Put `Verdict: <word>` on its own line just before `**Next:**`. Each Next line is one action a person can take now, in order.

Stopped: line 1 says what is missing and why it blocks the plan. Then `Verdict: Stopped`. Next holds the grouped questions, each with its default (or `Default: none`) and what it changes.

Reader rules:
- Define each term once at first use: baseline (the measured rate before the change), minimum effect (the smallest change worth acting on), alpha (the accepted rate of a false positive), power (the chance of detecting the minimum effect if it exists).
- Quote the metric names and the element exactly.
- No promised results.

Example (signature only; the domain is not a fixture):

````markdown
**The test cannot be sized yet; supply the baseline and minimum effect before planning its launch.**

```markdown
## Hypothesis
If the registration form shows the fee above the first field, then the share of visitors who complete registration rises, because the fee is the question most visitors ask first (assumed; from the support log).

## Design
Fixed horizon. Unit: visitor. Eligible: first visit to the registration page in the test period.

## Sizing
Baseline: [PLACEHOLDER: measured registration rate, with period and source]
Minimum effect: [PLACEHOLDER: smallest change worth acting on, from the owner]
Alpha: 0.05 (convention; owner to confirm)
Power: 0.80 (convention; owner to confirm)
Result: [PLACEHOLDER: size per variant, from the calculation]
```

Verdict: Sizing blocked

**Next:**
1. Supply the measured registration rate, with its period and source.
2. Supply the minimum effect the owner would act on.
3. Confirm alpha and power, or change them.
4. Calculate the sample size and duration, resolve QA gates, then seek launch approval. This skill starts nothing.
````

## Stop conditions

- No hypothesis and no changed element: Stopped. Ask what the variant changes and why.
- No variant to compare: Stopped. Ask for the control and the variant.
