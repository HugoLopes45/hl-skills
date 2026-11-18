# Lifecycle audit checks

Read this before any audit finding. Count each issue from the export, name its denominator, and rank by effect on the handoff. Report a check the export cannot support as `not checked`, never as passed.

1. **Stage definitions.** Count stages with no exit criteria or no owner role. Read them from the supplied stage document.
2. **Owner.** Count leads with a blank owner, in total and by stage.
3. **Stage skips.** When stage history is supplied, count leads that move past a stage without entering it.
4. **First response.** Count leads with no first human action. When the owner set a response target, count leads whose first action came after it. Otherwise report the distribution of response times.
5. **Stale leads.** For each stage, report the median days in stage (derived) and the count of open leads above the stale threshold the owner sets (`Default: none`).
6. **Required fields.** Count closed records missing a field required at exit. Count closed-lost records with no reason code.
7. **Duplicates.** Count pairs that match the stated key. If no key is stated, mark the check `not checked`. When pairs are found, list two Open decisions once: the system whose value wins for each field (`Default: none`), and the lead ID to keep (`Default: the older record's lead ID`, a heuristic default, not from the records).
8. **Routing.** Count decisions with no logged reason. Count leads sent to the fallback owner.
9. **Recycled leads.** Count them separately, with their later outcomes. Never add them to the first-pass counts.
10. **Scoring inputs.** Count features whose timestamp is after the decision time, or that have none.
11. **System of record.** Name each system that stores a stage or owner. More than one needs an owner decision.
12. **Owned leads.** When the export shows an owned outbound lead reassigned by an inbound form, count it. Otherwise mark the check `not checked`.
