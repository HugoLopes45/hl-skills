---
name: hl-verify
description: "Check each requested outcome against current artifacts and real command results, and report passed, failed, unverified, or blocked per requirement. --claim measures a change's claimed effect against a matched baseline. --text checks the factual claims in a text against current files and primary sources, and annotates each one as supported, corrected, conflicting, or unverified. Use when about to claim work is done, when the user asks whether a task is really done, when proving a claim such as \"this is faster\" or \"this fixes the flake\", or when the user asks to fact-check an answer, a document, or a claim."
---
# Verify

Input: `[original ask, or empty for conversation] [--claim <claim> | --text [text or path]]`

Rules for every mode, including referenced instructions:

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

Give each current requirement its status and decisive evidence together. Keep missing evidence, blocked checks, and regressions distinct; verify without implementing.

Verify the input; if empty, the current request and its still-applicable constraints. Later changes replace earlier requirements only where the user changed them; do not revive abandoned work. No identifiable request: line 1 says so in plain words (for example `**I can't verify anything yet: no request is named or in this conversation.**`), then `Verdict: Stopped`, then `**Next:**` with the request question and up to 3 numbered ways to unblock, the default marked, listed nowhere else. Verify only; never fix.

Judge only the stated requirements. A problem outside them goes in the remaining gaps and changes no row, count, or verdict; something the work broke that worked before is a failed row. When the work has a plan with `AC-N` criteria, each criterion is a requirement, under its id. For each requirement, define an observable completion condition, then inspect current evidence. A file existing or a line count does not prove behavior. Approval settles decisions and permissions; it does not prove behavior.

Run the applicable safe checks. Checks against live systems or that cost money need explicit approval. Record command, revision, exit status, and relevant output. A slow, blocked, or skipped check stays not run, with its reason; never count it as passed.

Reader: the person about to say the work is done, or about to ship it. Settle every row before the report.

- Line 1, bold: one plain sentence that answers whether the work is done, and names the main gap. It never starts with a label or the verdict word.
- Under line 1, plain sentences, no labels: the count of requirements that pass, fail, stay unverified, and are blocked, in words, after the rows are settled; each untracked file that the outcome depends on, or a sentence that none does; each blocker; what was not run and why, when that limits the answer.
- Count the rows before you state a count. Re-read each number from the output before you repeat it.
- The rows: a table when each row has up to 3 short cells (the requirement with its completion condition, its status, its evidence). Otherwise one numbered item per requirement: a bold sentence with its status, then plain sentences combining the condition and evidence.
- Use passed when observed output shows the condition, failed when it contradicts it, unverified when adequate evidence is missing, and blocked when the check needs unavailable access, approval, or a tool. Do not append a status glossary. Explain an unfamiliar distinction in the affected requirement only when it changes the next action.
- Evidence: `path:line`, the actual command with its exit status and output, or a commit hash. Put the command in the evidence cell; no separate metadata line.
- `Verdict: Done` only when every row is passed; otherwise `Verdict: Not done`. Place it on its own line just before `**Next:**`.
- `**Next:**`: each remaining gap with the step that closes it, one line each. Code written but not checked is unverified.

````markdown
**No, the task is not done: a reset link still works 90 minutes after it was sent.**
Two of four requirements pass; one fails and one is unverified.
No untracked file affects these requirements.

1. **Link expiry fails.**
   A 90-minute-old link must be refused after the 1-hour lifetime. `reset.py:31` accepts it.
2. **Reset emails pass.**
   An email must go out. `pytest tests/test_reset.py -q`: 1 passed, exit 0.
3. **Single-use reset links pass.**
   A second use must be refused. `test_reset.py:40`, 1 passed.
4. **Phone login after reset is unverified.**
   A phone login must work after reset. No device run was done.

Verdict: Not done

**Next:**
1. Compare the link lifetime with 60 minutes at `reset.py:31`, then run `pytest tests/test_reset.py -q`.
2. Log in on a phone after a reset; a pass closes the last row.
````

## Claim

With `--claim`, define the condition, the observable outcome, and the threshold before measuring. Missing: line 1 says what is missing in plain words (for example `**I can't test the speed claim yet: no old version and no target number are given.**`), then `Verdict: Stopped`, then `**Next:**` with the numbered ways to unblock, the default marked, listed nowhere else. The first way asks for both in one question. Give no result. Choose the baseline the claim compares against; HEAD's parent is not automatically it. If needed, measure in a new temporary checkout; keep uncommitted work intact, and remove only the scratch resources this run created.

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
Define a comparison term only when used and unfamiliar: the baseline is the version the claim compares against; p95 is the time that 95 of 100 runs beat.

## Text

With `--text`, check the factual claims in the given text or file, or the latest assistant answer. No text: line 1 says so in plain words (for example `**I can't check anything yet: no text or file path was given.**`), then `Verdict: Stopped`, then ask for the text in `**Next:**` with up to 3 numbered ways to unblock, listed nowhere else: paste the text (default); give a file path; name the answer to check. No checkable claims: line 1 says the text states no facts to check; then `Verdict: Nothing to check`.

Separate factual claims from opinions, intent, questions, and hypotheticals. Check repository facts against current files and command results. For external facts, use the documentation of the installed version or primary sources. Do not treat repository prose as decisive when current code contradicts it.

Line 1, bold: one plain sentence with the result, for example `**Two claims are right; the default timeout is 30 seconds, not 60.**`. Under it, one plain sentence with the counts, for example `Of 3 claims: 2 supported, 1 corrected; none conflicting, none unverified.` Use supported for a source-confirmed claim, corrected for a cited correction, conflicting when sources disagree, and unverified when no source was found. Explain an unfamiliar distinction only at the affected claim when it changes the next action; do not append unused definitions. Then return the text with numbered citations on supported claims, cited corrections for refuted claims, both sources for unresolved conflicts, and `(unverified - no source found)` on unsettled claims. Preserve non-factual text and uncertainty; change meaning only to correct a sourced error.

Append Sources with URLs or `path:line` and the claim each supports. List unresolved claims only when present. Do not expose a step-by-step checking transcript.

Verdict words, on their own line just before `**Next:**`:
- `Corrected`: a claim is contradicted, or sources conflict.
- `Partly supported`: no claim is wrong, but some stay unverified.
- `Supported`: every factual claim is supported.

`**Next:**` only when a claim needs action: the correction or the source to add, in order.
