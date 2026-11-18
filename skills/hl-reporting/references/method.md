# Method

Use this file for the input checks, period matching, the calculation format, the wording for attribution and cause, the credit check, ad results, pause and lift readouts, uncertainty, currency, business ratios, and the funnel walk. The workflow and evidence rules are in `SKILL.md`.

## Input checks

For each file or figure, record these fields. Write `not stated` for each field the input lacks.
- Period: start date, end date, and whether the end date is included.
- Time zone.
- Market: the country or region of the audience or sales.
- Currency: one currency for each amount column.
- Base: the denominator of each rate.
- Source tool and export date.
- Attribution model and window, for each credited figure.
- Count behind each rate: rows, sessions, or orders.
- Date basis: click date or conversion date, for each count.
- Withheld rows: when the platform withholds rows, report the disclosed share (disclosed rows divided by total rows) before reading the disclosed rows.
- Consent and blocking: say when they limit a browser count. Declined visitors are not recoverable by any method; do not present them as a loss a tool can recover.
- Consent signals: when ad conversions fall while clicks hold, ask the user to check the consent signals each tag sends before reading the fall as a market change.
- Call labels: before using a call label from a platform or software, check the share of calls it labels; if most calls are unlabeled, do not compare the labels.
- Change history: say when a cause cannot be recovered because the platform's change history has expired. Check its current retention in the platform's documentation; write `not checked` until you do.

## Period matching

- Compare periods of equal length in the same time zone. Name the time zone by region when a period crosses a daylight-saving change; a fixed UTC offset is wrong for part of the year.
- Label a partial period `partial`. Leave it out of totals unless the user accepts it.
- Name a known difference between periods, such as a closure or a holiday, as a possible reason for a change. Write "possibly", and state that the export does not show the cause.
- Mark a measurement break in the series, such as a change of goal, tag or definition. Do not compare values across it. Check what changed on that date, such as a tag, a platform change, or a site or plugin update, before naming a cause.
- Before comparing two counts of one conversion, check that the conversion action, date basis, time zone, attribution window and campaign scope match.
- Cut cohort rates to matured cohorts only. Label a cohort still inside its window as pending, and leave it out of the denominator.

## Calculation

Show each derived figure, one step per line, with aligned result and basis columns:

```text
enrolment rate, channel A   3.8%    120 enrolments / 3,150 sessions, week 1
change, channel A          +16.7%   (140 - 120) / 120, weeks 1 and 2
```

Name the inputs in the basis column. Round only in the result column.

## Attribution and cause

| Wording | Use when | Do not write |
|---|---|---|
| attributed to | a tool credits a channel under a named model and window | caused by, because of |
| associated with | two values moved together, with no test | due to, driven by |
| caused by, lifted | the user supplies a randomized experiment or randomized holdout, and you name its design | any cause claim without that design |

## Credit check

Run these checks on each channel's claimed count, whatever they show.
- Compare the claim with an independent count for the same period that the platform does not control: a phone log, orders or CRM records. A claim close to the whole business count does not show that the channel brought those customers.
- Name the conversion type and split the count by conversion action. A count that mixes a page view with a booked demo is not a lead count. Check the platform's current documentation for how it counts platform-hosted actions, branded search, retargeting and view-through conversions. Write each limit it states in the point; write `not checked` for each limit you did not check.
- Pick one source of truth for the conversion count: the CRM for long sales cycles, the order or booking record for short purchases. Dedupe each platform's claim against it, and explain the gap as over-claiming, view-through or untracked conversions. When a platform count and the source of truth disagree, apply the stop condition in `SKILL.md` and compare the two counts again each month.
- Split branded search from non-branded results. A cheap branded cost per outcome shows demand that already existed, not campaign effect, unless a randomized holdout shows lift. Set targets on non-branded results; report blended results only as the top-line figure.
- Name the attribution model, its credit rule and its window for each credited count. Last-touch gives the credit to the closing click; first-touch gives it to the first contact. On a long sales cycle, report first-touch and last-touch counts side by side and state the gap between them. Never add counts that use different windows.
- Linear, time-decay and position-based models split credit by fixed rules; name the rule, and read a fixed split as a convention, not a measured effect. A data-driven model needs the volume its platform documents; check the platform's current documentation for that volume, and write `not checked` until you do.
- For budget allocation across offline or brand spend, a marketing mix model needs spend history; check its documented data requirements, and write `not checked` until you do. Without the history those requirements call for, state that the model is not available.
- Treat direct traffic, branded search and unattributed conversions as gaps to explain, not as channels. Before concluding, rule out existing customers, stripped referrers and offline discovery; then check a self-reported answer or a test.
- A self-reported answer, such as a "how did you hear about us" question with a pick-list and a free-text option, is a triangulation input. Recall favors the memorable touch, so report its share as self-reported and do not add it to any credited count.

## Ad results

Use this section when the user asks which ad, audience or campaign to keep from a supplied export.
- Before reading zero or few outcomes as a failure, compute expected outcomes only when the user supplies the spend, the outcome count, the currency and the outcome definition. Expected outcomes = the item's spend divided by the cost per outcome of the whole export for the same period. Label the result an estimate. Without those inputs, write `not computed` and name the missing input.
- Heuristic default: with fewer than 3 expected outcomes, write `can't tell yet` and name the outcome count that would settle it, and do not forecast its arrival date. With 3 or more, report the actual and expected counts; zero actual outcomes is a shortfall, stated as a difference, not a cause. Ad items have no before window, so the Uncertainty labels do not apply.
- Compare items only inside one platform and one outcome definition. For absolute volume, use the independent count from the credit check at business level only; do not apply it to one item. Without a business-level count, write `not supplied` and ask for it in Next.
- Wear-out pattern: at steady spend (the export shows no budget change) across consecutive days, frequency rises while click-through rate falls and cost per outcome rises. Heuristic default: 3 or more days. Report it only when the export has daily rows for frequency, click-through rate, cost per outcome and spend, as `associated with` repeated exposure, and name the days.
- Before calling spend wasted, compute break-even conversion rate = cost per click divided by target cost per outcome, from supplied inputs. If the sample is too small to show whether the rate is above or below break-even, the term is unmeasured, not failing.
- Repeated impressions are not independent users. Variants chosen from many screened comparisons are exploratory: correct for multiple comparisons, and treat a winner as a hypothesis until a randomized test confirms it.
- Judge an item on the business outcome when its inputs are supplied; a click or cost metric alone shows no result.
- Recommend no budget amount, split or pace. A creative change to an item belongs to `hl-paid-ads`.

## Pause and lift readouts

Use this section for a pause, a budget cut or a holdout that the user ran.
- Check that the user supplied the design written before the data arrived: the unit paused or held out, the before window of equal length, the change log for both windows, and the decision rule. Without it, name each missing part and write `can't tell yet` for the result.
- Use whole weeks. Heuristic default: at least 4 weeks before; with fewer, the normal swing is not set and the result is `can't tell yet`. Heuristic default: a window under 14 days gives a hint, not a verdict. Heuristic default: under about 5 events a day, lengthen the window before reading it.
- Set the normal swing from the before window: its lowest and highest weekly averages. A during or after value inside that range is "no detectable change", whatever its percentage.
- When last year's data covers both windows, expected during = this year's before x (last year's during / last year's before). Label the expected value an estimate, and compare the observed during value with it.
- Before any go or stop decision, state the claim in units per day: if the claim is right, the count falls by N per day. Show N in the readout. Get the owner's yes to a pause only after the owner has seen N.
- Use the business's own record as the denominator, such as its call log, order system or booking record. Use the platform's count only as the claim. Count unique customers beside raw events, and remove the staff, vendor and spam rows the export marks, stating each exclusion's row count.
- For phone outcomes, count answered inbound calls of at least the minimum length the user names. If none is named, write `not stated` and report answered calls. Report raw calls and unique callers beside that count; where the log reaches back before the window, also count new callers, meaning numbers not seen before the window.
- When the user supplies monthly spend, the observed fall in calls per day, close rate and average margin, each with its currency, period and definition, state the cost per call in the observed fall as monthly spend divided by (the fall in calls per day times the days in that month). Compute it only for a fall labelled `clear change`. Label the result `estimate`, and compare it with close rate times margin.
- Read a randomized holdout as lift = exposed rate minus control rate. For a holdout, check whether the interval includes zero or the smallest lift that would change the decision. Read a pause as the change from the before window, and word it `associated with`, because a pause has no control group. A "no lift" result from a test whose control units were reached anyway is `can't tell yet`, not a finding.
- Name the design in each readout: a randomized holdout (user or geographic), a public-service-announcement control, ghost ads (ads logged as served but not shown), or a pause. Read a split the user runs without randomizing as `associated with`.
- Use causal words only when the user supplies a randomized experiment or randomized holdout, and the design above was followed; name the design in the same sentence. Write `can't tell yet` when a window is short, volume is low or another change overlaps the window, and name the condition that failed. A holiday or seasonal change in either window is an overlapping change, unless it fell in the same window last year and that adjustment is applied; a one-off event such as a storm always is.

## Uncertainty

- Say "small base" when a count is too low to read a rate reliably. For zero events in N trials, the 95% upper bound on the rate is 1 - 0.05^(1/N), about 3/N for large N; state it before calling the rate zero. Do not set a threshold from memory.
- One period against one period is not a trend. Compare it with the trailing periods of the same length. Count a move only when the period leaves that range, or when three or more periods move the same way. Heuristic default: three or more periods in one direction.
- A blank is `not reported`. Zero is a reported zero. Never turn a blank into zero.
- Describe a change as "from X to Y over these periods". Do not call it an improvement unless the user's metric definition states which direction is better.
- Heuristic default: for a count in two digits, round the rate to a whole percent. Compare the counts of the rarer event, not the rates.
- In a before and after comparison, a value inside the normal swing is `no detectable change`, whatever its percentage. Otherwise, label a value outside it `clear change`: the normal swing is the lowest and highest weekly averages of the same count in the before window, as set in Pause and lift readouts. Label it `probably` when the same direction holds across independent instances (weeks, sends). Heuristic default: 3 or more instances. Otherwise label it `can't tell yet` and name the count that would settle it.
- A rate that rises while its base falls (impressions or sessions) is not an improvement until the base is checked. Name the base change.
- A segment not named before the data was read is a hypothesis for a later test, not a finding.
- Do not call a test winner from an event count below what the user's written test design requires. Write `can't tell yet` and name the count needed. If the design states no count, write `not stated` and name `hl-ab-test-plan` as the owner of the test design.

## Currency

- Give one line per currency. Do not total across currencies.
- A conversion needs a rate, its date, and its source. Without all three, write `not converted`.

## Business ratios

Compute a return, cost per outcome, margin, or lifetime value only from a definition the user supplies. Every input must share one currency and one period. Without the definition, write `not computed` and name the missing input.

Label each acquisition cost with the cost lines the user defined. A cost that counts only paid spend is `paid-only`, not a blended cost per customer.

Compare cost per outcome with value per outcome only when the user supplies the spend, the outcome count, and the value per outcome, each with its currency, period and definition. Read the outcome as worth its cost while its cost is below its value.

Judge acquisition by per-cohort payback, not a blended LTV:CAC ratio. Gross-margin payback = CAC divided by (monthly revenue per customer times gross margin), in months, for each plan or cohort the user supplies. For a real cohort, find the first month in which cumulative gross profit per acquired customer covers CAC, using measured retention. Do not set a payback target from memory.

A return or ROAS figure needs refund and return adjustments as an input. Check whether each platform adjusts for refunds in its current documentation; write `not checked` until you do, and name each figure that stays unadjusted.

Read a leading metric, such as cost per lead, as a result only when it tracks a lagging outcome, such as closed revenue. If they diverge, fix the proxy first.

Judge cost per lead against qualified leads, not raw form fills, when the user supplies a qualification record.

Before a downstream outcome, such as a qualified lead or a closed deal, is read as a platform signal, check the platform's documented minimum volume; write `not checked` until you do.

## Funnel walk

Use this when the user asks where a funnel loses people.
- Write each stage with its count, in order, and its rate from the stage before.
- Name the leading indicator for each stage that the user's records support; read it as a result only when it tracks a lagging outcome (Business ratios).
- Compare each rate with the expected range the user supplies for that stage. Without one, write `expected range not stated`; do not use a range from memory or from a published average.
- Name the stage furthest below its expected range, not the stage with the smallest count.
- Classify that stage as traffic (too few or the wrong visitors), conversion (the page or form), or offer (what is offered or the follow-up). Name the evidence for the classification.
- In a phone-led funnel, measure answer rate (the share of calls answered) in and after the business hours the user supplies, and count the callers never reached, from the call log.
- In a phone-led funnel, check missed calls and callback delay in the call log before classifying a lead-to-sale stage as offer. If the callback delay exceeds the limit the user states, name follow-up as the evidence and suggest `hl-lead-lifecycle` in Next; with no limit, report the delay and write `not stated`.
