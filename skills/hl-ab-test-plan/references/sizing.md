# Sizing and analysis design

Use this file only when the plan needs a sample size or a sequential design. Compute sizes only from supplied inputs.

## Inputs

- `p1`: the baseline rate, a proportion between 0 and 1, from a measured source with its period and eligible population.
- `d`: the minimum effect, the smallest absolute change in the rate worth acting on, in the same unit as `p1`. The owner supplies it.
- `alpha`: the two-sided false-positive rate chosen before launch. Convention: 0.05.
- `power`: the chance of detecting `d` if it exists. Convention: 0.80. The owner accepts or changes it.
- `T`: eligible visitors per day that enter the test, before the split.
- `k`: the number of variants, including the control. The traffic per variant is `T / k` when the split is even.

If any input is missing, write `Blocked: <input names>`. Do not fill it with a guess.

## Fixed-horizon size per variant

This is a normal approximation for two independent proportions, equal allocation, and one fixed-horizon comparison. It is not a sizing method for revenue, clustered units, repeated observations, or multiple comparisons. For those designs, use a method that matches the metric and assignment unit. Require 0 < p1 < 1, 0 < p1 + d < 1, d nonzero, 0 < alpha < 1, 0 < power < 1, and positive eligible traffic; otherwise ask for valid inputs.

```text
p2 = p1 + d
pbar = (p1 + p2) / 2
z_alpha = the standard normal quantile for 1 - alpha / 2
z_power = the standard normal quantile for power
n = (z_alpha * sqrt(2 * pbar * (1 - pbar)) + z_power * sqrt(p1 * (1 - p1) + p2 * (1 - p2)))^2 / d^2
```

Round only the final `n` up to a whole randomized unit per variant. Compute normal quantiles without early rounding, for example with Python's standard-library `statistics.NormalDist().inv_cdf`: 1.9599639845400534 at 0.975 and 0.8416212335729144 at 0.80. Rounded table values can change the required sample; state the method and precision.

## Duration

```text
days = n / (T / k)
```

Round the duration up to a whole day. When weekday traffic varies, round up to whole weeks and state that choice in the plan. The plan states the rounding rule it used.

## Sequential design

- Fix the maximum size, the number of looks, and the boundary method before launch.
- Use only a method whose documentation states that it is valid at the chosen looks. A method built for one final look is not valid for repeated checks.
- Distinguish maximum sample size from expected sample size at an early stop. Both depend on the selected sequential method and effect. Recompute its required size; do not reuse the fixed-horizon `n`.
- Stop early only at a planned look and only when the boundary is crossed.

## Multiple comparisons

- More than one primary metric, or more than one variant against the control, needs a correction fixed before launch.
- Holm: sort the p-values from smallest to largest. Compare the smallest with `alpha / m`, the next with `alpha / (m - 1)`, and so on, where `m` is the number of comparisons. Stop at the first p-value that fails and do not reject it or any later one.

## Reporting

- Write each input with its source or its label `convention` or `owner input`.
- Write the result with its unit: visitors per variant, days.
- Do not state an expected effect, a probability that the variant wins, or a confidence the result cannot support.
