# Method

Use this file for the input checks, the calculation format, and the wording for attribution and cause. The workflow and evidence rules are in `SKILL.md`.

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

## Period matching

- Compare periods of equal length in the same time zone.
- Label a partial period `partial`. Leave it out of totals unless the user accepts it.
- Name a known difference between periods, such as a closure or a holiday, as a possible reason for a change. Write "possibly", and state that the export does not show the cause.

## Calculation

Show each derived figure, one step per line, with aligned result and basis columns:

```text
enrolment rate, channel A   3.8%    12 enrolments / 315 sessions, week 1
change, channel A          +16.7%   (14 - 12) / 12, weeks 1 and 2
```

Name the inputs in the basis column. Round only in the result column.

## Attribution and cause

| Wording | Use when | Do not write |
|---|---|---|
| attributed to | a tool credits a channel under a named model and window | caused by, because of |
| associated with | two values moved together, with no test | due to, driven by |
| caused by, lifted | the user supplies an experiment or holdout, and you name its design | any cause claim without that design |

## Uncertainty

- Say "small base" when a count is too low to read a rate reliably. Do not set a threshold from memory.
- A blank is `not reported`. Zero is a reported zero. Never turn a blank into zero.
- Describe a change as "from X to Y over these periods". Do not call it an improvement unless the user's metric definition states which direction is better.

## Currency

- Give one line per currency. Do not total across currencies.
- A conversion needs a rate, its date, and its source. Without all three, write `not converted`.

## Business ratios

Compute a return, cost per outcome, margin, or lifetime value only from a definition the user supplies. Every input must share one currency and one period. Without the definition, write `not computed` and name the missing input.
