# Wrong facts in answers

Read when a captured answer states a fact about the business that differs from the page or from current sources (workflow step 8).

## Claim row

Record one row per claim that could change a buyer's decision, including claims the prompt did not ask for:

- Engine, locale, and capture date.
- Prompt: the exact wording and its kind (category, comparison, problem, brand, trust, price or compatibility, or implementation).
- Claim: the sentence as the answer wrote it.
- Evidence: the current source that confirms or contradicts the claim, or unknown.
- Claim status: one of the seven below.
- Cited source: the URL the answer cites for the claim, or "none cited".
- Severity: critical, high, medium, or low.

## Claim status

- Accurate and current.
- Accurate but incomplete: true, but it omits a fact that changes the decision.
- Ambiguous: a reader can take it as true or false.
- Stale: it was true, and is not now.
- False.
- Subjective: an opinion stated as fact, such as "best for small teams".
- Unverifiable: no current source confirms or contradicts it.

Check business facts against current first-party material, and outside claims against independent sources. A match with the audited page shows only what the page says.

## Severity

- Critical: a price, eligibility, compatibility, safety, or legal error that could cause a wrong purchase or harm.
- High: a false or stale feature, limit, or availability fact.
- Medium: an incomplete or slanted statement that could change the decision.
- Low: wording that does not change the decision.

Weight severity by how often the prompt appears in the query sample. A medium error in most answers to core prompts outranks a high error in one rare prompt.

## Fix the cited source first

1. Find the source the answer cites for the claim. When it cites none, name the page the claim probably came from and mark it inferred.
2. Fix that source: state the correct fact with its date on the page that should own it. For a third-party source, send its owner the correct fact and a source.
3. Retest the same prompts after a window (heuristic default: 4 to 8 weeks), and report the movement across repeated runs.
4. Never say that a fix will change the answer. Answers can change for reasons outside the page.

Never invent corrections, post fake third-party content, or ask a publisher to remove fair criticism.
