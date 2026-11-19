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
- Before a result is reported, check its p-value and interval wording against these rules: the p-value is not the probability that the variant is better or that chance alone produced the data; it does not measure the size or importance of an effect; no conclusion rests only on crossing the significance threshold; the full result is reported. Significance alone does not show business value.
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

- State one hypothesis: "If [change] for [eligible visitors], then [primary metric] changes in [direction], because [reason]." The reason cites evidence, or is labeled an assumption. Name the evidence source, such as analytics, customer research, competitor pattern, support tickets, session recordings, or a past test result.
- When several hypotheses compete, ask the owner which one to plan. For copy with no other evidence, offer this heuristic default order: headline, offer framing, proof structure, call to action, body.
- Isolate one element when the hypothesis concerns that element. A bundled change is a redesign test: estimate the bundle's effect, not any component's contribution. Split it into separate tests only when component attribution is the decision. An effect smaller than the minimum effect needs a larger sample than the plan sized. If the owner doubts the change can reach the minimum effect, record the doubt as an assumption in `## Sizing`; do not forecast the change's effect.
- Name one primary metric before launch. For each guardrail, specify its population, window, owner-approved harm threshold and pause or rollback action. Missing thresholds block launch, not drafting. A higher completion rate does not justify harm to lead quality, refunds or safety.
- Name secondary metrics that test the mechanism in the hypothesis, each with its expected direction. They support the primary result; they are not separate wins.
- Name the unit of randomization, the unit the metric counts. Each unit sees one variant for the whole test.
- Choose the split before launch. Use 50/50 by default. A smaller exposed share, such as 90/10 or 80/20, limits harm from a bad variant and lengthens the test; size it with its allocation. Check that exposure is balanced across time of day and week. A ramp that changes the split over time is a rollout item.
- Name the eligibility rule that decides who enters the test. Apply it before assignment.
- Pick the test type that matches the change: A/B for one change; A/B/n for several variants, each compared with the control under the correction rule; split URL when each variant has its own URL, with assignment at random before either URL loads. Multivariate tests combine elements and need very high traffic; this skill does not plan them.
- Choose the implementation side per element. A client-side change can flicker, because the page shows the control before the variant applies. A server-side assignment decides the variant before the page renders, and needs development work. Pick the side that avoids flicker for the changed element.
- More than one primary metric or more than one comparison needs a multiple-comparison correction chosen before launch. Holm is one method. With no correction planned, the plan allows one primary comparison. Size each comparison at its corrected alpha, `alpha / m`, before computing the sample size.
- Before launch, verify tracking and exposure logging in every variant, run QA on every variant, check assignment ratios, inform stakeholders, and set a calendar date for the analysis.
- During the test, monitor technical faults and data quality, not the primary result outside planned looks. Record external events that could move the metrics. Change no variant and add no traffic from new sources.
- Prespecify the sample-ratio-mismatch test, expected allocation, significance threshold and investigation action. Use a chi-square test only when its expected-count assumptions hold; otherwise name an appropriate exact test or leave the check pending. Unequal counts alone do not prove a fault. Investigate a flagged mismatch before reading effects. Any triggered analysis must use a condition observed equivalently in both variants, not a treatment-only event.
- Opt-in elements (a player, a calculator, a chat widget) reach a small share of visitors, so an overall test is underpowered. Analyze the visitors who reach the same trigger point in both variants, such as the element coming into view, not the clicks, since the variant can change who clicks. Size with the baseline and units at that trigger point. If the trigger cannot be logged in both variants, the trigger-based comparison is invalid: analyze all assigned visitors, sized on the overall baseline.

## Analysis design

Choose one design before launch and write it in the plan.

- **Fixed horizon**: a planned size per variant and an end date. The result is read once, at the end.
- **Valid sequential**: a planned maximum size, a fixed number of looks, and the boundary method for those looks. Name the method. The tool that runs the test must implement it. If it cannot, use the fixed-horizon design.
- A tool's confidence, probability-of-winning or boundary output belongs to its own method. Do not copy it into a fixed-horizon p-value.
- Not allowed: a fixed-horizon test that is checked each day and stopped at the first significant result.

## Decision rules

- Check guardrails and assignment before reading the primary result.
- Decide from the effect size and its interval, not from the p-value alone. State the minimum effect worth acting on, and what counts as no clear difference.
- A significant winner goes to the owner for rollout only after its effect size, interval and guardrails are checked against the minimum effect and the harm thresholds. A significant loser keeps the control and records the likely reason it lost.
- A result that is not significant is not evidence of no effect. Read the interval: it may include a benefit or a harm worth acting on. Do not extend a finished fixed-horizon test until it turns significant; plan a new test instead.
- Check that the secondary metrics support the mechanism behind the primary result. A contradiction needs investigation before the decision.
- A segment result is exploratory unless the segment and its correction were fixed before launch.
- Record the result with the planned and actual sample per variant, the interval per variant, the practical significance (whether the effect reaches the minimum effect), and the caveats, including external events. Record any reusable pattern as an untested hypothesis for other pages or flows, and the decision: rollout proposed to the owner, control kept, parked, or follow-up test.

## Workflow

1. Restate the hypothesis, the element, the primary metric, guardrails, unit, and eligibility rule.
2. Check the sizing inputs. Compute the size and duration with the method in [references/sizing.md](references/sizing.md), or mark sizing blocked. If the size or duration is too large, use the options in that file.
3. Choose the analysis design and write its stopping rule or its single read. For a sequential design, recompute the size as that file says.
4. Write the QA checks, the decision rules, and the rollout steps as plan items. Stop before any rollout.

## Output

Reader: the owner who approves and runs the test. The decision served: whether to run this test now with the stated size and duration, or first to collect the missing inputs.

Line 1 is one bold plain sentence that gives the decision, for example "**The test can run once the owner approves a fixed-horizon design with the size shown below.**" It never opens with a label, verdict word, or number.

Under line 1, in plain sentences: each missing input that blocks the sizing, with its source requirement, and each choice the owner must make (analysis design, alpha, power).

The plan is the artifact. Put it in a `markdown` fence with these sections, in this order: `## Hypothesis`, `## Design`, `## Sizing`, `## Analysis and stopping rule`, `## QA`, `## Decision rules`, and `## Rollout (not started)`. In `## Sizing`, show the inputs and the result as plain lines. When a correction applies, show the number of comparisons and the corrected alpha too. When sizing is blocked, write `Blocked: <input names>` in place of the result.

Verdict words:
- `Planned`: sizing computed from supplied inputs, and the stopping rule is written.
- `Sizing blocked`: plan drafted; sizing needs the listed inputs.
- `Stopped`: no hypothesis and no changed element to test, several hypotheses with none chosen, no variant to compare, or the user cannot assign variants at random.

Put `Verdict: <word>` on its own line just before `**Next:**`. Each Next line is one action a person can take now, in order.

Stopped: line 1 says what is missing and why it blocks the plan. Then `Verdict: Stopped`. Next holds the grouped questions, each with its default (or `Default: none`) and what it changes.

Reader rules:
- Define each term once at first use: baseline (the measured rate before the change), minimum effect (the smallest change worth acting on), alpha (the accepted rate of a false positive), power (the chance of detecting the minimum effect if it exists).
- Quote the metric names and the element exactly.
- No promised results.

Example (plan excerpt; the domain is not a fixture):

````markdown
**The test cannot be sized yet; supply the baseline and minimum effect so its launch size can be calculated.**

Sizing needs two inputs: the baseline, the measured rate before the change with its period and source, and the minimum effect, the smallest change worth acting on, which the owner supplies. The owner also confirms the analysis design, alpha and power.

```markdown
## Hypothesis
If the registration form shows the fee above the first field, then the share of visitors who complete registration rises, because the fee is the question most visitors ask first (assumption; the support log is not checked).

## Design
Fixed horizon. Unit: visitor. Eligible: first visit to the registration page in the test period.

## Sizing
Baseline: [PLACEHOLDER: measured registration rate, with period and source]
Minimum effect: [PLACEHOLDER: smallest change worth acting on, from the owner]
Alpha: 0.05 (convention; owner to confirm)
Power: 0.80 (convention; owner to confirm)
Blocked: baseline, minimum effect
```

Verdict: Sizing blocked

**Next:**
1. Supply the measured registration rate, with its period and source.
2. Supply the minimum effect the owner would act on.
3. Confirm the analysis design, alpha and power, or change them.
4. After steps 1 to 3, ask for the sample size and duration; nothing launches without the owner's approval.
````

## Stop conditions

- No hypothesis and no changed element, or several hypotheses with none chosen: Stopped. Ask what the variant changes and why.
- No variant to compare: Stopped. Ask for the control and the variant.
- The user cannot assign variants at random: Stopped. Say that this skill needs random assignment, and suggest `hl-reporting` for a non-randomized comparison once before and after data exist.
