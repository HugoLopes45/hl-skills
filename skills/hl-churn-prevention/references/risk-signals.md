# Risk Signals

Read this file when the user asks which accounts are at risk. The evidence rules in `SKILL.md` apply: signals come only from supplied usage columns.

## Signals

Each signal names its column, its window, and the history it needs.

- Drop in key actions --> the last two weeks against the account's own prior four weeks (heuristic default windows; the owner sets them).
- No key action for a set number of days --> the owner sets the number (`Default: none`). Until the owner sets it, the signal is `unavailable`, not a gap.
- Removed users or seats --> only when the usage export records them.
- Data export requested --> only when the usage export records it.

A flag is an outreach trigger, not a prediction. Do not treat a flag as a prediction until the owner checks it against later cancellations.

A flagged account gets retention outreach, not an upsell offer.

A signal stays in the plan until the owner's check against later cancellations shows it does not separate the accounts that cancel. Then the owner removes it from the plan.

## Coverage

- A signal with a missing column, a blank week, or stale data is `unavailable`. It is neither healthy nor zero.
- An account with less history than the window needs is `unavailable` for that signal.
- Report, per account, the signals observed and the signals unavailable.

## Composite score, only on request

- Build no score unless the owner asks for one and supplies the mapping.
- Scale each signal to 0 to 100, where higher is healthier. The owner writes each mapping from the data; this file gives none.
- Use owner-set weights. Compute the score over observed signals only: `score = sum(weight × observed score) / sum(observed weights)`.
- Report the coverage with the score: the sum of the observed weights.
- Illustrative arithmetic, not data: weights 0.4 and 0.2, scores 80 and 50. Score = (0.4 × 80 + 0.2 × 50) / 0.6 = 70.0, coverage 0.6.
- Minimum coverage: `Default: none`. Below it, report `insufficient data` instead of a score.
- Do not use a partial score for an account action unless it meets the minimum coverage.
