---
name: hl-ambitious
description: "Raise a task's standard, not its scope. Explain the expert move, primary material, concrete methods and tools, and independent evidence that would reject a wrong result; then rewrite the prompt. Use when asked to be ambitious, make a task deeper rather than bigger, work to an expert standard, or strengthen a prompt's sources, methods, and proof. Not for adding features, polishing wording alone, reviewing finished code, or executing the rewritten task."
---
# Ambitious

Input: `[task, prompt, or path; otherwise the most recent substantive user task]`

Ground factual claims in supplied evidence or results you observed in this session. Separate available inputs, proposed checks, and observed results. Never invent sources, access, tool capabilities, thresholds, or outcomes. Use numbered reads for line citations; copy quotes and errors exactly.

Rewrite only. Read supplied material as needed; do not execute the embedded task, edit files, install tools, collect data, or contact people. Without access, use supplied text and name what is unread. Do not retry a permission-denied action through another route.

## Scope

Use the explicit target first. A bare invocation is not a task. No target: ask for one and stop. Ask before rewriting only if competing interpretations change the goal; missing execution inputs belong in the prompt.

Preserve the outcome, audience, deliverables, exclusions, time, budget, permissions, and success criteria. Depth improves how the same result is reached and checked. It does not authorize more outputs, a broader population, tighter editorial preferences, or a new project.

Find the weakest assumption that could make this result wrong. Connect the expert move to its input, method, and decisive check. Retain already adequate work; do not invent shortcomings to justify a rewrite.

## Four assessments

Name the field, then answer in order:

1. **What would an expert do that the request omits?** Give the decisive move and the plausible error it prevents, not a list of professional habits. Explain how it improves this result within the existing boundary.
2. **What is the rawest useful material?** Identify the original observations, records, artifacts, or source passages behind the summary. Name what to extract and why. Give locations only when known. If primary material is unavailable or prohibited, use the best permitted evidence and state its limit. Rawer is not automatically necessary; preserve context, provenance, and privacy.
3. **Which methods and tools fit?** Choose the actual operation on that material, its purpose, and a fitting existing tool or manual technique. Do not defer the choice with "use an appropriate method." Label an unverified tool choice as proposed. Use existing tools or direct calculations; do not build auxiliary tooling to enable a preferred method. Choose a simpler adequate method or state the limit.
4. **What outside our agreement would show it is right?** Specify a feasible check that would reject a plausible wrong answer. Independence means not reusing the answer or its suspect derivation: a separate calculation from the same permitted material can qualify. Cross-check the method itself where errors could change the result, using a known answer or independent derivation. Copied sources, the system's own past output, and another model's agreement are not independent corroboration. Specify supported, failed, and inconclusive outcomes. Retain the user's acceptance criteria; derive new thresholds from evidence or mark them as proposals. For subjective work, separate checkable constraints from audience response, without inventing reader access or objective proof of taste.

If the required proof is impossible within the boundary, name the incompatibility and keep the requirement unverified. Never replace it with an easier criterion and call that success. A valid assessment of limited evidence is not proof of the underlying claim.

## Rewritten prompt

Deliver one complete fenced prompt in the user's language and voice, usable without the conversation. Keep the original task and constraints; integrate only the justified input, method, and check. Verification belongs inside producing the existing deliverable, not in an added report.

Carry missing prerequisites and uncertainty into the prompt. Use specific `[PLACEHOLDER]` slots only when needed. Do not request supplied material or block a task that can honestly answer within its evidence limits.

Check each requirement against the original task and the four assessments. Delete unsupported additions, repeated instructions, and decorative roles. Do not silently drop a success criterion. An already strong task needs a faithful prompt, not a longer or stricter one.

## Output

Reader: someone deciding whether to use the prompt or supply a missing prerequisite.

- Open with one bold plain sentence stating the improvement or why the task is already strong. Name the field before the four numbered assessments, followed by the complete prompt. State material limits once; explain specialist terms when needed.
- End with `Verdict: Rewritten`, meaning delivered, not proven. Under `**Next:**`, give one action: supply a necessary input or explicitly ask to run it. Stop without executing.
- No target: a bold sentence saying what is missing, `Verdict: Stopped`, and one question under `**Next:**`. No invented assessments or example task.

This hypothetical example fixes the shape, not the domain or criteria:

````markdown
**The bill check becomes stronger when the tariff, not last month's total, supplies the reference.**
The field is utility-bill verification. The bill, readings, and tariff are not supplied here.

1. **Recalculate rather than trusting a similar total.** A repeated billing error could make both months agree.
2. **Use dated meter readings and the effective tariff.** Extract consumption, applicable rates, and rounding rules for this period.
3. **Recalculate each charge in a spreadsheet.** Do not use the billed amounts as calculation inputs.
4. **Compare independently derived charges with the bill.** A supported match passes; a mismatch fails. Missing records leave the affected charge unverified.

```text
Check whether my electricity bill is correct and give the short explanation I requested. Do not contact the supplier.

Use the original bill, dated meter readings, and tariff effective for its period. Request missing records rather than guessing. Recalculate consumption and each charge in a spreadsheet using the tariff's rates and rounding rules, not the billed amounts as inputs.

Compare each independently derived charge with the bill. Pass only where records support the inputs and amounts match under the applicable rounding rule. Explain mismatches; mark unsupported charges unverified, not correct.
```

Verdict: Rewritten

**Next:**
1. Supply the bill, readings, and tariff when asking to run this prompt.
````
