# Scoring method

Read this before any scoring. The records are the only source of weights and thresholds.

## 1. Build the outcome set

- Keep each lead with an outcome of won or lost and its outcome date.
- Count open leads and leads without an outcome date separately. Exclude both from scoring.
- Define the decision time once for all leads: the moment the record first shows the lead for handoff review. Apply the same definition to won and lost leads.

## 2. Use only features known at decision time

- Read each feature as its value at the decision time, using the feature's own timestamp.
- A feature stamped after the decision time cannot score that lead. Example: a booked demo stamped three days after the decision is excluded, even when it predicts wins.
- A feature with no timestamp is not scored. List it under Open decisions.
- Scoring today's record with later fields makes the rule look better than it could have been. Do not report such a result as a test.

## 3. Split by decision date

- Development set: earlier decision dates. Holdout: later decision dates, whose outcomes have matured under the outcome window the owner sets (`Default: none`).
- Keep all leads from one account in one set.
- Choose criteria and the threshold on the development set only. Freeze them before the holdout is read.
- A holdout used to make a choice becomes development data.

## 4. Choose criteria from counts

- For each feature value, count won and lost leads that have it, for example `pricing_views 3 or more: 5 won, 2 lost`.
- Keep a value only when its counts meet the minimum the owner sets (`Default: none`). Mark other values `not scored`.
- Each kept criterion adds one point. A weight other than one needs development counts that show the difference, stated in the spec.

## 5. Set the threshold on development data

- Compare each candidate threshold with the current routing rule on the same leads. Report flagged leads, precision, recall, missed wins, false positives, and flagged leads per period.
- The owner picks the threshold from these counts. This skill sets no number. If the development counts do not support a choice, leave the threshold unset.

## 6. Test once on the holdout

- Report the frozen rule on the holdout: date range, eligible leads, won and lost counts, flagged leads, won among flagged, missed wins, false positives, and the same figures for the current rule.
- A holdout below the owner's minimum is inconclusive. Say so.
- A retrospective score does not show revenue gain. Say so.

## 7. Record the version

Record the feature rules, cohort dates, criteria, threshold, holdout result, owner, and rollback step.
