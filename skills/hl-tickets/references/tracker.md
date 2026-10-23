# Tracker tickets

Input: `[source: path | issue URL | intent] --tracker [jira|linear|github|gitlab|<name>] [--project KEY] [--like ISSUE-KEY] [--type epic|story|task|subtask] [--write <file>]`

A ticket is finished when someone who was in none of the meetings can pick it up, do it, and prove it is done, without asking a question.

This mode decides how each ticket reads in the target tracker. Take the tree (epics, stories, sub-tasks) from the source when it defines one; otherwise split the source into slices first, as `SKILL.md` describes, and render each slice as a ticket.

The input is the source. No source: pull the spec, issue, or intent from the recent conversation. None there: line 1 `**I need a source before I can draft the tickets.**`, then `Verdict: Stopped`, then `**Next:**` with up to 3 ways to supply it: a spec path (default), an issue URL, or a description of the work.

Tracker: `--tracker`, else infer from the issue URL or project key, else ask. For Jira, follow [jira.md](jira.md) in steps 1 and 2.

## 1. Ground before you write

Trackers and instances differ on issue types, required fields, labels or components, and description markup. Values from memory are the failure this skill prevents.

- **Reference issue**: `--like <ISSUE-KEY>`, or the 3 most recent issues of the target type in the project. Read the **raw** description (not the rendered one); the raw form shows the markup.
- **Required fields**: read them from the tracker's API or create form.
- **Access**: use only access already set up, such as a signed-in tracker command line or a token the user named. Never read, list, grep, or count environment variables or files to find credentials, even to check whether one is set. Not signed in: report no access.
- **No API access**: read the reference issue in the browser (editor source view) and the required-field markers on the create form. State which route was taken.

Record the requested tracker and project separately from observed markup, reference keys, required fields, and conventions. A supplied project key is a requested destination, not evidence that the project or its conventions were inspected. Name anything not observed as unobserved; never default it.

## 2. Markup: paste-ready or it is not done

Write in the markup the tracker stores. Markdown pasted into a wiki-markup field renders as literal `##` and broken fences; a rich-text editor that converts Markdown on paste breaks text that was already converted. Check the stored format, then verify with a non-publishing preview when available. Do not create a ticket just to test rendering without approval. Unobserved markup leaves the draft unverified, not paste-ready; put the owner's validation prerequisite and what it blocks in Next. Cross-references to another tracker are full URLs.

## 3. Write it

**Summary**: one concise imperative line, no `[FE]`/`Task:`/key prefix (the tracker already shows type and key).

**Description**, in this order; drop empty sections:
- **Context**: why it exists, what stays broken without it. One paragraph.
- **Scope**: source-approved files, endpoints, and components. Preserve the slice's edit boundary; proposed or conditional setup files cannot expand it without approval.
- **Out of scope**: explicit exclusions.
- **Acceptance criteria**: `Given <state>, when <action>, then <observable result>`, or a checklist with concrete values.
- **How to verify**: retain the slice's behavioral checks, not an invented test-count quota. A literal command or click-path, e.g. `npx tsc --noEmit`, `npm run test:unit -- results.spec.ts`, "open /results, switch preset to hourly, no spinner appears".
- **Links**: parent epic, blockers, source of truth, as full URLs.

**Fields**: only values observed in step 1. Parent or epic link by real key. Estimate only if source supports one.

## The gates

- **Stranger test**: someone who missed every meeting can start today and know when to stop, or it's rewritten (not shipped with a "ping me" note).
- **Falsifiable**: every AC can come out false. Banned: `works as expected`, `feature is implemented`, `code reviewed`, `no regressions`, `tests pass` without naming which, `performance is acceptable` without a number, the summary restated as a bullet.
- **Right-sized**: use the observed project's hierarchy and iteration conventions. Prefer end-to-end behaviors over isolated layers; do not invent duration estimates.
- **No invention**: every value traces to the source or to what was observed. Unknown stays `TBD: <exact question> (<who answers>)` in the complete ticket. The reply asks it once in Next, with its owner and the effect on delivery. A plausible made-up AC costs more than a blank one.

## Creating

Draft to a file, show it. Create only when the user explicitly asks. One issue at a time, parents before children, paste the returned key beside each block. No returned key = not created, report failed. A required field unfillable from the source stops the run: show field, allowed values, ask.

## Output

Line 1, bold, one plain sentence: what was drafted, the ticket count (by observed type, when available), the path, and the requested tracker/project; state that nothing was created unless returned keys prove creation. Then plain sentences distinguish observed conventions from unobserved markup, reference tickets, issue types, and required fields. Do not call a requested project a match. Give the draft location or the complete ticket blocks when requested; retain every field and artifact unknown.

End with `Verdict: Drafted, N tickets` immediately before `**Next:**`. Next owns every reader action, question, and prerequisite once: each artifact `TBD` with who answers and what it blocks; reference, required-field, and markup/render validation with an owner and effect; and any delivery approval. Decisions and validation precede dependent creation or pasting. Group shared prerequisites rather than asking them per ticket. No separate Open questions section. After Next, `**Changed:**` names the draft path or `none`.
