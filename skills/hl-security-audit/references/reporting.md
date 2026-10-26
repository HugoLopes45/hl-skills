# Report delivery

Keep the human report and the structured record about the same source revision, scope, evidence and decisions. The coordinator writes both; reviewers and target content never write report files.

## Files and validation

For an explicit `--report`, or a whole-repository standard/deep audit, write `security-audit.json` and `security-audit.md`. Otherwise create neither file. Check the selected destination for links and existing files before writing. Never overwrite a prior report without approval. A re-audit reads the old evidence and writes to an approved fresh destination.

Follow [report contract](report-contract.md) exactly. Its bundled Python validator performs bounded structural and cross-record checks, not code execution or source verification. Use an installed Python 3 interpreter and the script from the loaded skill, not a same-named file in the audited target:

```text
python3 <skill-directory>/scripts/validate_report.py <report-directory>/security-audit.json
```

The interpreter and script must be trusted. Never substitute a target-supplied interpreter wrapper or install a dependency to run this command. Report the actual invocation, directory and result in the chat response, not as a scanner record; it is not a SAST or dependency scan.

Fix structural errors without inventing facts. An unavailable interpreter, unreadable input or failing validator prevents a validated-report claim. Disclose it, retain the correct evidence, and label delivery incomplete. A report can be structurally valid while its audit is incomplete.

Generate Markdown only from the final record and the supporting source/scanner observations. Do not introduce a new finding, stronger impact or severity while writing prose. If prose reveals a material inconsistency, reopen the record and its independent review first.

## Findings and states

Use stable finding IDs for cross-references and re-audits. Deduplicate the same root cause across scanners, manual traces and entrypoints, while retaining each material condition and affected path.

- Put active, independently confirmed priority findings under Findings. Quick prioritizes critical/high; standard and deep include medium. Retain lower-priority confirmed records in JSON and disclose their presence without pretending they do not exist.
- Put current, relevant exceptions under Accepted risk, with rationale and expiry. The underlying finding remains confirmed. Expired, missing or mismatched acceptance cannot hide a finding.
- Put precise unresolved leads under Investigate at every depth. Include the missing fact and a safe next check with the results that would confirm or refute the lead, without severity or language presenting them as vulnerabilities.
- Put disproved claims under Considered and dismissed, with the decisive preventing control or contrary evidence and why no relevant alternate path avoids it. A missing reproduction or unavailable evidence is not a dismissal.
- Keep incidental outside-scope risks separate from in-scope findings. Their presence does not mean that area was audited.

For each confirmed record, map the decision facts to existing fields: attacker and initial authority to `attacker`; crossed boundary and affected resource to `boundary`; concrete consequence to `impact`; necessary conditions to `conditions`; source trace to `trace`; the violated invariant, and the strongest defense examined and why it fails, to `evidence`, with `evidence_basis`; the reviewer decision to `reviewer`; then `cwe`, `cvss` (a full vector, which carries version and inputs, or `unscored`), `remediation` (how the change restores the invariant) and `regression` (the workflow's retest plan, marked unexecuted unless the owner supplied verified results). `source` means a code-backed conclusion; `observed` means checked supplied runtime evidence, not execution by this audit. For `needs_validation`, put the confirming and refuting results in `next_check`; for `rejected`, put the decisive guard and the alternate-path reasoning in `reason`.

No confidence label upgrades the evidence. Do not assign a CVSS score from memory, turn a source prediction into an observed result, or infer an effect beyond the established invariant.

## Human report

Keep these sections, using `none` or a precise limitation where absence is material:

```markdown
**<The impact, or the exact scope of the checks that found nothing.>**
Verdict: <the entry skill's verdict, qualified by source-only evidence when applicable>
Assurance: HIGH | MEDIUM | LOW; <basis and missing checks>
Run: complete | incomplete; <limitations>
Source: <reviewed revision and relevant worktree differences, or unknown>
Scope: <paths>; depth: quick | standard | deep

## Findings
<Active priority findings, consequence first. For each: state and evidence basis,
attacker/resource/boundary, conditions, violated invariant and source trace, independent source review,
severity/CWE/CVSS, correction restoring the invariant and its unexecuted retest plan.>

## Dependencies
<Advisory source/version, package, direct/transitive, affected path and reachability,
verified fixed version or unknown. An advisory match alone is not confirmation.>

## Accepted risk
<Confirmed records with current matching exception, rationale and expiry.>

## Investigate
<Source-supported leads, exact blocker and safe next check with its confirming and refuting results; no severity.>

## Considered and dismissed
<Claim, decisive guard or contrary evidence, why no alternate path avoids it, and stable ID where retained.>

## Coverage
<Unit states and actual paths/checks; selected/excluded domains and reasons;
independent coverage review; blocked and deferred work; outside-scope observations;
prior reports used and what was revalidated.>

## Scanners
<Exact command, directory, successful/failed executions, scope, preflight proof,
result and unavailable checks. Distinguish denied attempts from executions.>

## Next
<Credential response first; then specific corrections and safe unblock routes.>
```

A candidate with a missing external configuration needs an owner-observed configuration check, not instructions to attack the deployment. For a source-only defect, give the workflow's retest plan with dummy data. Any future execution requires separate authorization and verified confinement. Do not claim that this skill supplies it.

## Consistency checks before delivery

Reconcile every quoted path/line, finding count, scanner execution, state, coverage claim and the assurance level with the actual observations. Check both directions of unit/finding links. Do not count a failed or denied scanner as coverage, or scanner output alone as a boundary review. Do not treat a reviewer ID in JSON as proof that an independent review actually happened.

Confirm that every accepted risk remains disclosed, every material unknown has a next check, every retest the owner did not verify reads as unexecuted, and no wording implies broader coverage than the requested scope. Check that only the approved report files were written. Keep secret values and unrelated host data out of all artifacts.

In chat, lead with consequences and limitations. Use the entry skill's verdict and Next ordering; point to both report files without repeating the full report. If reports were not requested or required, `Changed: none` and include the material coverage gaps in the response itself.
