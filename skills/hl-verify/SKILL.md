---
name: hl-verify
description: "Check each requested outcome against current artifacts and real command results, and report passed, failed, unverified, or blocked per requirement. --claim measures a change's claimed effect against a matched baseline. --text checks the factual claims in a text against current files and primary sources, and annotates each one as supported, corrected, conflicting, or unverified. Use when about to claim work is done, when proving a claim such as \"this is faster\" or \"this fixes the flake\", or when the user asks to fact-check an answer, a document, or a claim."
---
# Verify

Input: `[original ask, or empty for conversation] [--claim <claim> | --text [text or path]]`

Verify the input; if empty, the user's requests in this conversation. No identifiable request: ask. Verify only; never fix.

Judge only the stated requirements. A problem outside them goes in the remaining gaps and changes no row, count, or first line; something the work broke that worked before is a failed row. When the work has a plan with `AC-N` criteria, each criterion is a requirement, under its id. For each requirement, define an observable completion condition, then inspect current evidence. A file existing or a line count does not prove behavior. User approval is not evidence.

Run the applicable safe checks. Checks against live systems or that cost money need explicit approval. Record command, revision, exit status, and relevant output. A slow, blocked, or skipped check stays not run, with its reason; never count it as passed.

Settle every row before the report. First line: `done` only when every row is passed; otherwise `not done`, with the count per status. Then a table: request, completion condition, status, evidence. Status: passed, failed, unverified (no adequate evidence yet; a check could provide it), or blocked (the check needs access, approval, or a tool you lack). Evidence: `path:line`, actual command output, or a commit hash. Then list the remaining gaps and what closes each. Code written but not checked is unverified.

## Claim

With `--claim`, define the condition, the observable outcome, and the threshold before measuring; missing: ask, with no result line yet. Choose the baseline the claim compares against; HEAD's parent is not automatically it. If needed, measure in a new temporary checkout; keep uncommitted work intact, and remove only the scratch resources this run created.

Run baseline and treatment with the same command, data, environment, and warm-up. Record revisions, raw artifacts, units, repetitions, and confounds. Lead with the result, then before, after, and delta. Result:
- `VERIFIED`: the criterion holds under the tested conditions only.
- `NOT VERIFIED`: a valid comparison misses the criterion.
- `INCONCLUSIVE`: name the missing evidence.

## Text

With `--text`, check the factual claims in the given text or file, or the latest assistant answer. No text: ask for it. No checkable claims: say so.

Separate factual claims from opinions, intent, questions, and hypotheticals. Check repository facts against current files and command results. For external facts, use the documentation of the installed version or primary sources. Do not treat repository prose as decisive when current code contradicts it.

First line: counts of supported, corrected, conflicting, and unverified claims. Then return the text with numbered citations on supported claims, cited corrections for refuted claims, both sources for unresolved conflicts, and `(unverified - no source found)` on unsettled claims. Preserve non-factual text and uncertainty; change meaning only to correct a sourced error.

Append Sources with URLs or `path:line` and the claim each supports. List unresolved claims only when present. Do not expose a step-by-step checking transcript.
