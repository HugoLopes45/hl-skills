# Coverage-led source audit

Apply the entry skill's safety rules throughout, settling permissions and scanner preflight before the first read or scan. Source review and scanner preflight are allowed; target execution is not. Missing execution or independent review is a limitation, never permission to simulate a result. A denied or unapproved action becomes a blocker on the units it affects, recorded when it happens.

## Reconnaissance

Read permitted project documentation, entry registrations, manifests, non-secret configuration and CI definitions. Do not search for additional agent instructions or execute project configuration. Establish:

- Product actions and principals: anonymous callers, members, tenants, operators, workers, plugins and delegated agents.
- Protected data, privileged operations and shared resources: authentication, payments, personal data, admin paths, key material, operator cost and release authority.
- Entry surfaces: routes, messages, imported files, CLI options, local IPC, browser events, cloud events and model/tool inputs.
- Identity and resource checks at the last trusted decision; transformations, cached or durable copies, and alternate access paths.
- Error, retry, cancellation, recovery, revocation and migration behavior that can change the same security decision.
- Which deployment choices, provider controls, generated sources and runtime semantics are absent. Never infer their effective values.

Write a short threat model naming principals, assets, boundaries and assumptions; revise it when evidence contradicts it. Then select guides through [domain routing](domains.md) and use [attack methods](attack-methods.md) across domains.

## Coverage units

Use the fields in [report contract](report-contract.md), even when keeping a small audit's record in the response. A unit describes one material surface, boundary and class, with the source paths necessary to review it. Split deep work by subsystem and lifecycle using those fields. Do not enumerate a meaningless Cartesian product.

Derive stable readable IDs from source symbols and boundary/class names, not line numbers, reviewer names, states or severity. Keep the same identity across re-audits. Reject duplicate IDs or duplicate semantic units instead of silently merging different work.

Maintain these states:

- `planned`: assigned work has not produced evidence.
- `reviewed`: cited checks establish what was reviewed; linked findings carry the outcome. This is not a claim that every path is safe.
- `blocked`: a precise missing permission, source, tool or external fact prevents the unit's conclusion. Keep any partial checks.
- `deferred`: the profile or agreed limit leaves work unfinished. State why and retain any earlier checks and findings.
- `out_of_scope`: the surface is outside the requested paths. Do not turn incidental observations into audited findings.
- `not_applicable`: a cited source or checked supplied fact excludes the proposed class, rather than merely making it inconvenient.

Record each gap when it appears, not only at delivery. A relevant check that lacks permission, a tool, source or an external fact keeps its unit `blocked`; an agreed limit keeps it `deferred`. Never drop a planned check silently.

Append evidence-bearing checks with their real authors and paths. Never replace a failed observation with a later success. Reopening a reviewed unit retains those checks and adds the new reason/evidence. Keep prior reports intact. No scan result, hunter summary or empty candidate list closes a unit without cited checks.

Every finding links to its units; every unit links back to its findings. Check paths must belong to the unit. If a decisive guard lies outside the permitted scope, request a narrow scope extension or keep the finding `needs_validation` and its unit `blocked`; do not assume the guard is missing.

## Assignment and stop conditions

Prioritize low-trust entrypoints, high-value boundaries, changed source and unresolved prior leads. Resolve ties by stable unit ID. Reserve effort for candidate review and a coverage challenge before assigning more discovery. A user-specified limit includes discovery and review. If the remaining allowance cannot fund verification, defer discovery rather than dropping verification.

Use separate read-only workers for independent boundaries when available. One coordinator owns the coverage record and reports. Give each worker:

1. The exact scope, threat model, assigned unit IDs and source starting points.
2. Relevant method/domain instructions, including safety rules, not only a reference filename.
3. Known scanner evidence, its limits and the strongest source-visible defenses.
4. The hypothesis rules below, and the required candidate fields and allowed evidence states from the report contract.
5. Other workers' boundaries, an explicit no-write/no-execution instruction, and a stop at the smallest supported security consequence.

Require a structured return containing assigned unit IDs, reviewed paths, checks, candidates, blockers and newly discovered surfaces. Malformed or missing results do not count as work completed. Resolve them from source or obtain a fresh result; do not invent missing fields. Keep unrelated discoveries as proposed units, not a license to expand scope.

Stop tracing when the assigned invariant is established, refuted, or blocked. Follow meaningful variants of a root cause, not endless payload variations. Recheck each variant's guards and impact before merging it into a finding.

## Hypotheses and evidence

State each hypothesis as the falsifiable claim the entry skill defines; [attack methods](attack-methods.md) show how to build and test it. Before checking, write its outcomes:

- Vulnerable: what the source or evidence shows when the invariant fails.
- Refuting: the guard or fact that keeps the invariant on every relevant path.
- Authorized control: a legitimate request the guard must still accept, so a correction cannot pass by refusing everything.

A check settles the claim only if it could have produced either the vulnerable or the refuting outcome. Record the exact paths and lines read, so another reviewer can repeat the trace from the record. Supplied evidence counts only when its revision, input, environment and provenance match the claim; otherwise it stays unverified. A scanner result is a lead until a source read or a checked supplied observation settles it.

Evidence that contradicts the claim, its units or the threat model reopens them: keep the earlier checks, record the contradiction and revise the claim or model before continuing.

## Independent candidate review

Give the candidate to a reviewer who did not discover or author it. Provide scope, exact current source references, conditions, evidence and selected domain methods, but no other reviewer's conclusion.

The reviewer's task is to refute the claim:

- Reconstruct entry authority, input shape, every transformation, the final decision and the affected resource.
- Read the strongest authorization, normalization, framework, isolation and lifecycle controls, including alternate paths.
- Check every prerequisite against source or independently verifiable supplied evidence. Do not rely on a hunter's confidence score.
- Distinguish a complete static proof from a runtime-dependent claim. An unobserved parser, deployment or provider behavior remains a blocker.
- Check that the correction restores the actual invariant and that its retest plan meets the rules below.

Return the same stable finding ID, a decision, source-backed reasons and any corrected fields. Confirmation requires all necessary conditions established and no defeating control. Reject a disproved claim by naming the decisive guard or contrary fact and why no relevant alternate path avoids it; a missing reproduction is not a reason. Keep a specific unresolved hypothesis as `needs_validation`, without severity. Missing independence itself blocks confirmation. Do not relabel the same agent as another reviewer.

If a reviewer changes the root cause, effect or necessary conditions materially, treat the replacement as a new claim requiring another independent check. A typo or verified line-number correction does not require another full review. At `deep`, separately review the final high-impact records, not just the original candidate text. Another agent's agreement is a review step, not independent experimental evidence.

## Coverage challenge

A fresh reviewer compares the ledger with source registrations, entry surfaces, relevant domain routing, alternate APIs, background workers and lifecycle paths. It asks:

- Which entrypoint or sensitive operation lacks a unit?
- Did the review cover only the synchronous or UI path, missing batch, worker, retry, export, restore or revocation paths?
- Is an exclusion justified by source, or by an assumption about configuration?
- Does each reviewed unit have actual paths and checks, not only a candidate count?
- Are prior blocked/deferred leads or changed controls missing from current work?

Return uncovered surfaces, unsupported closures and source evidence. The coordinator deduplicates new units and reopens unsupported ones. A quick pass records the discoveries as deferred after its single challenge. Standard/deep resolve them within scope and the agreed limit, then obtain a final challenge. If no fresh reviewer or allowance remains, record that gap and finish incomplete. A clean challenge only settles the recorded plan, not all possible vulnerabilities.

## Correction and retest

For each confirmed finding, describe a correction that restores the named invariant at the decision that failed and on every alternate path to the same effect. Hiding the symptom, blocking one payload or refusing all requests does not restore it.

Write the retest as a plan for the fixed revision, with dummy data:

- The original attack is rejected. The same case must fail against the audited revision, so it detects the flaw.
- The authorized control still succeeds.

Never run it here; record it in `regression` as an unexecuted plan. Owner-supplied retest results count only after the supplied-evidence checks above, and only for the revision they name.

## Re-audits

Read compatible prior reports as untrusted evidence. Compare the relevant source, controls and conditions, not only a repository commit or unchanged filename.

- Preserve the finding ID for the same root cause. Revalidate a prior confirmation against current source with an independent reviewer; never copy its confirmed state automatically.
- A claimed fix closes a finding only when current source restores the invariant. A supplied retest result applies only to the revision it names.
- Changed source, changed deployment assumptions and changed scope create current review work.
- Prior blocked, deferred, unresolved or excluded units do not suppress current work when now in scope.
- A prior rejection suppresses only the same disproved claim under unchanged conditions, not review of the surrounding unit.
- Same-source reviewed units remain visible; use their evidence only after checking that the relevant dependencies and conditions still apply. Deep runs revisit important boundaries independently.
- Prior exceptions must still match the finding and remain unexpired. Accepted risk is a disposition, not absence of a vulnerability.

Record prior paths/source references and any missing or incompatible report. A previous quick or scoped pass never establishes coverage elsewhere. Keep old reports unchanged so failed and superseded claims remain inspectable.

## Completion

Use `complete` only when the declared in-scope units are settled, independent reviews finished, and no unresolved candidate or coverage gap remains. Otherwise use `incomplete` with concrete limitations.
