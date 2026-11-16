# Page CRO checks

Use this file to read each layer of the audit. Each entry names what to read, what counts as a finding, and a test that would check the finding. A check with no evidence in the supplied page is `not confirmed`.

## Primary action

- **Read**: the element that completes the primary action, its label, its position, and any other button or link of similar weight.
- **Finding**: the label names no action or no result; the action sits below the first screen; two actions of equal weight compete.
- **Test**: a variant with the label or position as the only change.

## Value statement

- **Read**: the headline, subhead, and first paragraph.
- **Finding**: the page does not say what the product is, for whom, or what the visitor gets; the copy relies on words that name no outcome.
- **Test**: a variant with the value statement as the only change.

## Proof

- **Read**: every count, name, rating, logo, quote, and certification on the page, and where each sits relative to the action.
- **Finding**: proof with no source on the page or in the supplied material is `unsourced`; proof sits far from the action it supports.
- **Test**: a variant that moves the sourced proof next to the action. Unsourced proof is removed from the test, not tested as is.

## Form and steps

- **Read**: each input's persistent visible label, programmatic association, required status, and role in completing the task. Inspect the rendered state when markup alone cannot show label behavior.
- **Finding**: a placeholder used instead of a persistent label; a required field with no established task need; a deferrable step. Do not infer a conversion loss from these observations.
- **Test**: restore an accessible persistent label, or test removing or deferring an unnecessary field. Preserve security and qualification needs; specify lead-quality or downstream-completion guardrails before testing field removal.

## Risk and trust

- **Read**: whether price, cancellation, terms, and contact information are reachable on the path, and whether the page makes a promise that depends on them.
- **Finding**: a promise, such as a free trial, with no reachable terms on the path.
- **Test**: a variant that shows the terms link at the action. Do not write the terms.

## Mobile and speed

- **Read**: a measured report or a rendered check, with its tool and date.
- **Finding**: only from measured data. Without it, write `not confirmed`.
- **Test**: name the measurement to run; do not state a result.

## Measured funnel

- **Read**: the export's period, source, and step counts.
- **Finding**: a step with a large drop only when the export shows it, with its period and source.
- **Test**: an A/B test plan from `hl-ab-test-plan`.

## Writing a finding

Use this form:

1. The element, quoted, with its line or location.
2. Its effect on the visitor, and the label observed on the page or hypothesis.
3. The change to test, in one sentence.

Do not write a conversion figure in any of the three parts.
