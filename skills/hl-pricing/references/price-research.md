# Price Research

Read this when analyzing a price survey, a feature ranking, or usage data.

Label every survey result as stated intent. Apply the survey rules in [SKILL.md](../SKILL.md) (sample size, question wording, method) before you read a result.

## Four-question price survey

Ask each respondent four price questions:

1. The price at which the product is too expensive to consider.
2. The price at which the product is too cheap to trust.
3. The price at which the product is getting expensive, but they would still consider it.
4. The price at which the product is a bargain.

Check the order of each answer: too cheap, then bargain, then expensive, then too expensive. Record each excluded answer and its reason. Do not change an answer silently.

Plot the share of respondents against candidate prices. The two cheap-side curves fall as price rises. The two expensive-side curves rise. Do not flip a curve to match the others. Record the tie convention you use.

Read the intersections:

- **Point of marginal cheapness:** too cheap meets expensive. This is the lower bound.
- **Point of marginal expensiveness:** too expensive meets bargain. This is the upper bound.
- The range between these two points is the acceptable range.
- **Optimal price point** (too cheap meets too expensive) and **indifference price point** (expensive meets bargain) only shortlist test prices. They do not name the best price.

The four questions measure price perception, not purchase. Demand, conversion, and churn at a new price need a purchase test (see [price-changes.md](price-changes.md)). Analyze each buyer group on its own, because each group has its own range.

## Stated-purchase questions

For willingness to pay, ask a yes/no stated-purchase question at several prices, and vary the price across respondents. A choice study shows bundles at different prices and records which bundle each respondent picks (conjoint analysis).

A direct question, such as "how much would you pay", gives the weakest stated intent; do not use it as the result.

## Feature ranking

Use a best-worst survey to rank features. Show small sets of features and ask which one is most important and which one is least important.

- Put the high-ranked features in every plan.
- Use the middle-ranked features to separate plans.
- Move the low-ranked features to a premium add-on or cut them.

Do not turn the rank into fixed percentile cut-offs. Set the cut for each product from the ranking and the buyer groups.

## Usage data

Use a supplied export of usage for retained and churned accounts. Compare the usage of each group: users, projects, integrations, and the other units the product meters.

Find the usage level where retained accounts separate from churned accounts. Label that level a candidate threshold. Confirm it with a test before you set a plan limit on it. Correlation alone does not show that the usage causes retention.
