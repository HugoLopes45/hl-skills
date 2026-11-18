# Sizing and analysis design

Use this file when the plan needs a sample size, a duration, or a sequential design. Compute sizes only from supplied inputs.

## Inputs

- `p1`: the baseline rate, a proportion between 0 and 1, from a measured source with its period and eligible population.
- `d`: the minimum effect, the smallest absolute change in the rate worth acting on, in the same unit as `p1`. The owner supplies it.
- `alpha`: the two-sided false-positive rate for the whole plan, chosen before launch. Convention: 0.05. With `m` comparisons, sizing uses `alpha_c` from Multiple comparisons.
- `power`: the chance of detecting `d` if it exists. Convention: 0.80. The owner accepts or changes it.
- `T`: eligible randomized units per day (visitors, not pageviews), before the split and before exposure.
- `e`: exposure fraction, the share of `T` that enters the test. Use 1 when every eligible unit enters.
- `a_c` and `a_v`: allocation fractions of the control and one variant. Each arm `i` has `a_i`. The fractions of all arms sum to 1; an even split of `k` arms gives `a_i = 1 / k`.

If any input is missing, write `Blocked: <input names>`. Do not fill it with a guess.

## Fixed-horizon size per comparison

This is a normal approximation for one fixed-horizon comparison of a control with one variant, two independent proportions, and fixed allocation. It is not a sizing method for revenue, clustered units, or repeated observations of one unit. For those designs, use a method that matches the metric and assignment unit. Require 0 < p1 < 1, 0 < p1 + d < 1, d nonzero, 0 < alpha_c < 1, 0 < power < 1, 0 < e <= 1, positive `a_i`, and positive `T`; otherwise ask for valid inputs.

Derivation: under the null, the difference of two proportions has standard error `sqrt(pbar * (1 - pbar) * (1 / n_c + 1 / n_v))`, where `pbar` weights each arm by its size, so it is the plain mean only when the arms are equal. Under the alternative, its standard error is `sqrt(p1 * (1 - p1) / n_c + p2 * (1 - p2) / n_v)`. Set `n_c = a_c * N` and `n_v = a_v * N`, where `N` is the total randomized units across all arms. Require `z_alpha` times the first standard error plus `z_power` times the second to equal `d`, and solve for `N`.

```text
p2 = p1 + d
pbar = (a_c * p1 + a_v * p2) / (a_c + a_v)
z_alpha = the standard normal quantile for 1 - alpha_c / 2
z_power = the standard normal quantile for power
N = (z_alpha * sqrt(pbar * (1 - pbar) * (1 / a_c + 1 / a_v)) + z_power * sqrt(p1 * (1 - p1) / a_c + p2 * (1 - p2) / a_v))^2 / d^2
n_c = a_c * N
n_v = a_v * N
```

With an even two-arm split, `n_c = n_v = N / 2`, the usual per-variant size.

Round only the final `n_c` and `n_v` up to whole randomized units. Compute normal quantiles without early rounding, for example with Python's standard-library `statistics.NormalDist().inv_cdf`: 1.9599639845400534 at 0.975 and 0.8416212335729144 at 0.80. Rounded table values can change the required sample; state the method and precision.

Worked check, invented inputs, computed with the formula above:
- Two arms, even split: `p1` 0.10, `d` 0.05, alpha 0.05, power 0.80. `N` = 1371.19, `n_c` = `n_v` = 685.60, so 686 per arm.
- Control and two variants, Holm with `m` = 2, so `alpha_c` = 0.05 / 2 = 0.025 and `z_alpha` = 2.2414; `a_i` = 1/3 for each arm. `N` = 2491.18, `n_i` = 830.39, so 831 per arm.

If a segment result will be read, size for the smallest such segment, with that segment's baseline and its eligible units in `T`.

## Duration

```text
days_i = n_i / (T * e * a_i)    for each arm i, with the largest n_i of the comparisons that include arm i
days = the largest days_i, rounded up to a whole day
```

Count randomized units in `T`, the same units as the sample size; repeat pageviews are not participants. A split sized by the formula above has `n_i = a_i * N`, so every arm gives `days = N / (T * e)`. With the worked three-arm check, `T` = 500 and `e` = 0.5 give 831 / (500 * 0.5 * 1/3) = 9.97 from the rounded 831 per arm, so 10 days.

When weekday traffic varies, round up to whole weeks. The plan states the rounding rule it used.

Heuristic defaults, not sourced rules:
- Run at least one full week to cover day-of-week variation.
- For B2B, run at least two business cycles.
- For commerce, run through the payday cycles of the audience, such as month start and month end.
- Above 8 weeks, plan no run without a stated reason. Novelty effects wear off and outside events add noise as the run lengthens.

## When the size or duration is too large

The owner chooses one or more options, and the plan records the choice.
- Raise `d` only as the owner's decision about the smallest change worth acting on, never as a forecast.
- Raise `alpha`, for example to 0.10, and record the lower confidence as an owner input.
- Reduce the variants to the most promising one.
- Pool similar pages into one test only when the hypothesis, the metric and the eligibility rule are the same on each page.
- Test upstream, where traffic is higher, when the hypothesis holds there.
- Use qualitative evidence instead of a test, and state that the decision rests on it.
- Accept a longer run, with the reason written under the duration rule above.

## Sequential design

- Fix the maximum size, the number of looks, and the boundary method before launch.
- Use only a method whose documentation states that it is valid at the chosen looks. A method built for one final look is not valid for repeated checks.
- Distinguish maximum sample size from expected sample size at an early stop. Both depend on the selected sequential method and effect. Recompute its required size; do not reuse the fixed-horizon `N`.
- Stop early only at a planned look and only when the boundary is crossed.

## Multiple comparisons

- More than one primary metric, or more than one variant against the control, needs a correction fixed before launch.
- Size each comparison at `alpha_c = alpha / m`, where `m` is the number of comparisons. Compute `alpha_c` before `N`, and state `m` and `alpha_c` in the plan.
- Holm: sort the p-values from smallest to largest. Compare the smallest with `alpha / m`, the next with `alpha / (m - 1)`, and so on. Stop at the first p-value that fails and do not reject it or any later one.
- Holm rejects at least every comparison that Bonferroni rejects. A size at `alpha / m` therefore gives at least the stated power under Holm, under the same approximation.

## Reporting

- Write each input with its source or its label `convention` or `owner input`.
- Write the result with its unit: visitors per arm, days.
- Do not state an expected effect, a probability that the variant wins, or a confidence the result cannot support.
