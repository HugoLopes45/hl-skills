---
name: hl-startup
description: "Take a software product from no idea to keep or kill. scout finds SaaS ideas a solo developer can ship with an AI coding agent, from live pain signals, scored on evidence. evaluate (default) runs five gated stages (core assumption, problem validation, competition, first 10 customers, two-week MVP test) ending in go, pivot, stop, or insufficient evidence; --stage runs one. ship decides the smallest first version to launch; kill decides whether to continue, pivot, or shut down a product based on traction rather than effort spent. Use when there is no idea yet, when the user wants to evaluate or pressure-test an idea, validate a problem, map competitors, find first customers, or scope an MVP experiment, or asks what to launch, what to cut for a first version, or whether to keep going with a product."
---
# Startup

Input: `[scout | evaluate | ship | kill] [idea or question] [--stage assumption|problem|competition|customers|mvp]`

The first word picks the mode; without one, pick it from the request: no idea yet is `scout`; what to launch or cut is `ship`; whether to continue a product is `kill`; otherwise `evaluate`.

- `scout`: follow [references/scout.md](references/scout.md).
- `ship` or `kill`: follow [references/ship-or-kill.md](references/ship-or-kill.md).
- `evaluate`: the rest of this file.

## Evaluate

Gather the idea, the target buyer or user, and the founder's relevant access or experience. Ask for missing inputs one at a time. Be direct without personal attacks.

Work through five stages and ask before advancing to the next. A stage that ends in stop: report it and advance only if the user asks. For each stage, read its file and follow it. `--stage` runs that stage only and ends with its own return.

1. **Assumption** ([references/pressure-test.md](references/pressure-test.md)): the core assumption, demonstrated weaknesses, and the evidence needed to judge viability.
2. **Problem** ([references/validate-problem.md](references/validate-problem.md)): the specific pain, the early-adopter profile, non-leading questions about past behavior, and proposed validation criteria.
3. **Competition** ([references/competition-map.md](references/competition-map.md)): the current workaround, direct and indirect competitors, switching costs, and differentiation.
4. **Customers** ([references/first-customers.md](references/first-customers.md)): supported channels, manual outreach, a draft message, behavioral signals, and milestones for the first 10 customers.
5. **MVP** ([references/mvp-experiment.md](references/mvp-experiment.md)): a two-week test with the smallest feature set, exclusions, pass and fail criteria, and schedule assumptions.

Do not fabricate people, market numbers, customer quotes, traction, or certainty. Separate evidence from hypotheses and proposed targets. Payments and repeated use are stronger signals than expressed interest. Label every threshold as a proposal.

After the last stage, lead with go, pivot, stop, or insufficient evidence. Then the decisive evidence, the riskiest assumption, the cheapest test, and the next 14 days as a table: day, action, done when. Do not write files or contact customers unless the user asks.
