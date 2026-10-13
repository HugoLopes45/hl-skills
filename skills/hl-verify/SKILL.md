---
name: hl-verify
description: "Check each requested outcome against current artifacts and real command results, and report passed, failed, unverified, or blocked per requirement. --claim measures a change's claimed effect against a matched baseline. --text checks the factual claims in a text against current files and primary sources, and annotates each one as supported, corrected, conflicting, or unverified. Use when about to claim work is done, when the user asks whether a task is really done, when proving a claim such as \"this is faster\" or \"this fixes the flake\", or when the user asks to fact-check an answer, a document, or a claim."
---
# Verify

Input: `[original ask, or empty for conversation] [--claim <claim> | --text [text or path]]`

Verify the input; if empty, the user's requests in this conversation. No identifiable request: line 1 says so in plain words (for example `**I can't verify anything yet: no request is named or in this conversation.**`), then a question that asks for the request, then up to 3 numbered ways to unblock, the default marked, then `Verdict: Stopped`. Verify only; never fix.

Judge only the stated requirements. A problem outside them goes in the remaining gaps and changes no row, count, or verdict; something the work broke that worked before is a failed row. When the work has a plan with `AC-N` criteria, each criterion is a requirement, under its id. For each requirement, define an observable completion condition, then inspect current evidence. A file existing or a line count does not prove behavior. User approval is not evidence.

Run the applicable safe checks. Checks against live systems or that cost money need explicit approval. Record command, revision, exit status, and relevant output. A slow, blocked, or skipped check stays not run, with its reason; never count it as passed.

Reader: the person about to say the work is done, or about to ship it. Settle every row before the report.

- Line 1, bold: one plain sentence that answers whether the work is done, and names the main gap, within 100 characters. It never starts with a label or the verdict word.
- Under line 1, plain sentences, no labels: the count of requirements that pass, fail, stay unverified, and are blocked, in words, after the rows are settled; each untracked file that the outcome depends on, or a sentence that none does; each blocker; what was not run and why, when that limits the answer.
- Count the rows before you state a count. Re-read each number from the output before you repeat it.
- The rows: a table when each row has up to 3 short cells (the requirement with its completion condition, its status, its evidence). Otherwise one numbered item per requirement: a bold sentence with its status, then the condition and the evidence, one field per line.
- Define the status words once, after the rows: passed (the output shows the condition); failed (the output contradicts it); unverified (no adequate evidence yet; a check could give it); blocked (the check needs access, approval, or a tool you lack).
- Evidence: `path:line`, the actual command with its exit status and output, or a commit hash. Put the command in the evidence cell; no separate metadata line.
- `Verdict: Done` only when every row is passed; otherwise `Verdict: Not done`. Place it on its own line just before `**Next:**`.
- `**Next:**`: each remaining gap with the step that closes it, one line each. Code written but not checked is unverified.

````markdown
**No, the task is not done: a reset link still works 90 minutes after it was sent.**
Two of four requirements pass; one fails and one is unverified.
I did not test a phone login, so that row stays open. No untracked file affects these rows.

| Requirement | Status | Evidence |
|---|---|---|
| Links expire after 1 hour: a 90-minute-old link is refused | failed | `reset.py:31` accepts it |
| Reset emails are sent: an email goes out | passed | `pytest tests/test_reset.py -q`: 1 passed, exit 0 |
| Reset links work once: a second use is refused | passed | `test_reset.py:40`, 1 passed |
| Reset works on phones: a login after reset on a phone | unverified | no device run yet |

Passed means the output shows the condition. Failed means the output contradicts it. Unverified means no evidence yet; a check could give it. Blocked means the check needs access, approval, or a tool you lack.

Verdict: Not done

**Next:**
1. Compare the link lifetime with 60 minutes at `reset.py:31`, then run `pytest tests/test_reset.py -q`.
2. Log in on a phone after a reset; a pass closes the last row.
````

## Claim

With `--claim`, define the condition, the observable outcome, and the threshold before measuring. Missing: line 1 says what is missing in plain words (for example `**I can't test the speed claim yet: no old version and no target number are given.**`), then a question that asks for both, the numbered ways to unblock with the default marked, then `Verdict: Stopped`. Give no result. Choose the baseline the claim compares against; HEAD's parent is not automatically it. If needed, measure in a new temporary checkout; keep uncommitted work intact, and remove only the scratch resources this run created.

Run baseline and treatment with the same command, data, environment, and warm-up. Record revisions, raw artifacts, units, repetitions, and confounds. Line 1, bold: one plain sentence with the answer and the number that decides it. Then the before, after, and delta as a `text` block, each side with its revision or input and its unit:
```text
before   240 ms   p95, main @ 1a2b3c4, 30 runs
after    180 ms   p95, branch @ 5d6e7f8, 30 runs
delta    -25%    (180 - 240) / 240
```
Result words, placed on their own line just before `**Next:**` as `Verdict: <result word>`:
- `VERIFIED`: the claim holds, but only for the tested input and machine.
- `NOT VERIFIED`: a valid comparison misses the claim.
- `INCONCLUSIVE`: the comparison lacks evidence; name what is missing.
Define once, in the report: the baseline is the version the claim compares against; p95 is the time that 95 of 100 runs beat.

## Text

With `--text`, check the factual claims in the given text or file, or the latest assistant answer. No text: line 1 says so in plain words (for example `**I can't check anything yet: no text or file path was given.**`), then a question that asks for the text, then up to 3 numbered ways to unblock: paste the text (default); give a file path; name the answer to check. Then `Verdict: Stopped`. No checkable claims: line 1 says the text states no facts to check; then `Verdict: Nothing to check`.

Separate factual claims from opinions, intent, questions, and hypotheticals. Check repository facts against current files and command results. For external facts, use the documentation of the installed version or primary sources. Do not treat repository prose as decisive when current code contradicts it.

Line 1, bold: one plain sentence with the result, for example `**Two claims are right; the default timeout is 30 seconds, not 60.**`. Under it, one plain sentence with the counts, for example `Of 3 claims: 2 supported, 1 corrected; none conflicting, none unverified.` Define each word once: supported (a source confirms the claim), corrected (a source contradicts the claim; the correction is cited), conflicting (sources disagree; both are shown), unverified (no source found). Then return the text with numbered citations on supported claims, cited corrections for refuted claims, both sources for unresolved conflicts, and `(unverified - no source found)` on unsettled claims. Preserve non-factual text and uncertainty; change meaning only to correct a sourced error.

Append Sources with URLs or `path:line` and the claim each supports. List unresolved claims only when present. Do not expose a step-by-step checking transcript.

Verdict words, on their own line just before `**Next:**`:
- `Corrected`: a claim is contradicted, or sources conflict.
- `Partly supported`: no claim is wrong, but some stay unverified.
- `Supported`: every factual claim is supported.

`**Next:**` only when a claim needs action: the correction or the source to add, in order.
