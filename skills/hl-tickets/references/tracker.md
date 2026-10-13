# Tracker tickets

Input: `[source: path | issue URL | intent] --tracker [jira|linear|github|gitlab|<name>] [--project KEY] [--like ISSUE-KEY] [--type epic|story|task|subtask] [--write <file>]`

A ticket is finished when someone who was in none of the meetings can pick it up, do it, and prove it is done, without asking a question.

This mode decides how each ticket reads in the target tracker. Take the tree (epics, stories, sub-tasks) from the source when it defines one; otherwise split the source into slices first, as `SKILL.md` describes, and render each slice as a ticket.

The input is the source. No source: pull the spec, issue, or intent from the recent conversation. None there: line 1 `**No source: pass a spec, an issue URL, or describe the work.**`, then `Verdict: Stopped`, then stop.

Tracker: `--tracker`, else infer from the issue URL or project key, else ask. For Jira, follow [jira.md](jira.md) in steps 1 and 2.

## 1. Ground before you write

Trackers and instances differ on issue types, required fields, labels or components, and description markup. Values from memory are the failure this skill prevents.

- **Reference issue**: `--like <ISSUE-KEY>`, or the 3 most recent issues of the target type in the project. Read the **raw** description (not the rendered one); the raw form shows the markup.
- **Required fields**: read them from the tracker's API or create form.
- **Access**: use only access already set up, such as a signed-in tracker command line or a token the user named. Never read, list, grep, or count environment variables or files to find credentials, even to check whether one is set. Not signed in: report no access.
- **No API access**: read the reference issue in the browser (editor source view) and the required-field markers on the create form. State which route was taken.

Report in one line: tracker, markup, reference key, required fields, conventions mirrored. Name anything not observed as unobserved; never default it.

## 2. Markup: paste-ready or it is not done

Write in the markup the tracker stores. Markdown pasted into a wiki-markup field renders as literal `##` and broken fences; a rich-text editor that converts Markdown on paste breaks text that was already converted. Check which one you face, then verify the render on one ticket before doing the rest. Cross-references to another tracker are full URLs.

## 3. Write it

**Summary**: one imperative line, ~60 chars, no `[FE]`/`Task:`/key prefix (the tracker already shows type and key).

**Description**, in this order; drop empty sections:
- **Context**: why it exists, what stays broken without it. One paragraph.
- **Scope**: files, endpoints, components, when known.
- **Out of scope**: explicit exclusions.
- **Acceptance criteria**: `Given <state>, when <action>, then <observable result>`, or a checklist with concrete values.
- **How to verify**: literal command or click-path, e.g. `npx tsc --noEmit`, `npm run test:unit -- results.spec.ts`, "open /results, switch preset to hourly, no spinner appears".
- **Links**: parent epic, blockers, source of truth, as full URLs.

**Fields**: only values observed in step 1. Parent or epic link by real key. Estimate only if source supports one.

## The gates

- **Stranger test**: someone who missed every meeting can start today and know when to stop, or it's rewritten (not shipped with a "ping me" note).
- **Falsifiable**: every AC can come out false. Banned: `works as expected`, `feature is implemented`, `code reviewed`, `no regressions`, `tests pass` without naming which, `performance is acceptable` without a number, the summary restated as a bullet.
- **Right-sized**: Epic = multiple stories + success metric. Story = one iteration, vertical slice. Sub-task = hours to a day. `Create the users table` as a story is a sub-task; cut vertically instead.
- **No invention**: every value traces to the source or to what was observed. Unknown stays `TBD: <exact question> (<who answers>)`, in the ticket and repeated in output. A plausible made-up AC costs more than a blank one.

## Creating

Draft to a file, show it. Create only when the user explicitly asks. One issue at a time, parents before children, paste the returned key beside each block. No returned key = not created, report failed. A required field unfillable from the source stops the run: show field, allowed values, ask.

## Output

Line 1, bold, one plain sentence: the ticket count by type and the path. Then one plain sentence on what you matched: the tracker, its markup, the reference ticket, the required fields. Say which ones you could not observe; never default them. Then **Open questions**: every `TBD` plus its question, and every convention you could not observe. Nothing unknown, no section. End with `Verdict: Drafted, N tickets`, then `**Next:**`.
