# Boring-stack lens

Spend novelty only on what differentiates the product. Keep one deployable until a concrete force requires a split.

## Principles

- One deployable (a monolith) until something concrete forces a split: scale measured today, independent team ownership, independent deploy needs, or blast radius. "We might scale" is not a force.
- A team has a small budget of innovation tokens. Spend them on the differentiator, not on the database, queue, or deploy pipeline. Proven defaults (a relational database, server-rendered pages, one queue you already run) win elsewhere.
- One competent developer should set it up locally and ship a feature on day two. A week of onboarding, or a dozen services to start locally, means the architecture is wrong.
- Every dependency is debt: future deprecations, vulnerabilities, and breaking changes you did not choose.
- Practices from very large companies fit their scale and organization. A small team that copies them builds many services for few endpoints.
- Name the trade-off of each recommendation.

## Modes

### `review` (default)

1. **Day-two test**: can one developer set this up locally and ship a feature on day two? Yes or no, and why.
2. **Innovation tokens**: where is novelty spent, on the differentiator or on layers a proven default would cover?
3. **Dependencies and services**: each non-trivial one, and whether it earns its cost.
4. **What to cut**: 1-3 specific items, each with the principle it violates.
5. **Verdict**: `ship as is` / `cut these first` / `rethink the shape`.

### `monolith`

For a proposed split: name the concrete force, or state that none exists. Cost of the split: development speed, debugging surface, deploy complexity, on-call load. The in-process alternative: module boundaries, separate schemas, separate test suites. Verdict: `split` / `do not split` / `split only <piece>`.

### `tokens`

Table: layer, proposed technology, proven alternative, innovation token spent (yes or no). End with `Tokens spent: N. Justified: <list>. Wasted: <list>.`

## Stand down

Problems where the novel technology is the product itself, or where a constraint (regulation, an existing platform contract) dictates the stack.
