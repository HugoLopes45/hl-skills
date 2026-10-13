---
name: tickets
description: "Split a feature or plan into thin, independently verifiable delivery slices, each one pull request, as Markdown files or GitHub issues. --tracker writes paste-ready tickets in the real field conventions and markup of Jira, Linear, GitHub, GitLab, or a similar tracker, gated on a stranger test and a no-invention rule. Use when a plan, spec, or intent needs to become executable tickets, agent tasks, epics, stories, or sub-tasks, or when tickets keep coming back with \"what does this actually mean?\". Creates issues only when the user explicitly asks. Not for splitting an existing diff (use `split-pr`)."
---
# Tickets

Input: `[file | dir | 'text'] [--write <dir>] [--target md|github | --tracker <name>]`

Use the input as the source, or the latest feature. For a directory, read its Markdown and text files, excluding dependencies and build output. Missing or unreadable source: report it and stop.

Each slice is a tracer bullet: a narrow but complete path through every layer its outcome needs, demoable on its own, in one PR, small enough for one fresh agent context. Never a horizontal layer ("all the schema", "all the endpoints"). Aim for at most four paths under Read first and five changed files; split by behavior, not arbitrary syntax.

State real blocking edges rather than pretending every slice is independent:
- A refactor that makes the change easy goes in its own first slices, and the feature slices are blocked by it.
- A wide mechanical change (rename, signature change, column move): expand (add the new form beside the old), migrate callers in batches each blocked by expand, contract (remove the old form) blocked by every batch.
- Number slices so blockers come first.

Resolve architectural ambiguities affecting persistence, API contracts, authorization, payments, or irreversible changes before labeling a slice executable. An unknown decision makes the slice HITL or blocked, never an invented default. A slice is AFK only when its Acceptance is a command or an observation a person can check without reading the code; otherwise it is HITL until one exists.

## Slice format

Use frontmatter `id: SL-NN`, `type: AFK|HITL` (AFK: an agent can finish it alone; HITL: it needs a human decision or approval), `status: open`, `blocked_by: [SL-NN, ...]` (empty list when none), followed by:
- Title and actor/outcome traced to the source.
- Background and thinnest end-to-end path.
- Scope exclusions and dependencies.
- Read first: verified paths or symbols and why each matters.
- Steps: behavioral test or existing check, minimal implementation, verification.
- Acceptance: the source's `AC-N` ids it covers, command, observable pass/fail condition, relevant failure case.
- Touches: existing paths verified this run; proposed paths marked `[new]`.

Include this execution contract in every slice:

1. Recheck references and preconditions. Report drift before editing.
2. Edit only Touches; needing other files or crossing exclusions requires approval.
3. Add or identify the behavioral check. Record the real baseline result. A missing dependency or broken test runner is not a feature failure.
4. Implement and rerun the check. Do not skip tests, weaken assertions, or mock away the behavior under test.
5. Report commands, observed results, and blockers. No run means unverified, not green. Already-green acceptance requires checking whether the behavior already exists, not manufacturing a failure.

Planning does not authorize implementation. Do not invent baseline failures or exact future output. Run only existing safe checks; label future checks proposed. Use HITL for unresolved human decisions or approval-sensitive actions.

## Delivery

Before writing to `--write <dir>` or GitHub, show the breakdown as a numbered list in dependency order: title, type, blocked by, what it makes work. Ask whether the granularity and edges are right; revise until the user approves.

`--write <dir>` saves `SL-NN-<slug>.md`; default target is md. Without a destination, save one draft under `${TMPDIR:-/tmp}` and ask before final delivery. Do not overwrite differing files without approval.

An explicit `--target github` authorizes issue creation, not implementation. Check repository access, existing matching issues, and available labels. Create only missing issues, blockers first so each "Blocked by" line cites real issue numbers, with acceptance checkboxes; apply `slice` and `HITL` labels only where they already exist. Missing tools or access: report the blocker. Never edit or close existing issues.

First line: the slice count, the HITL count, and the directory or repository they went to. Then a table in dependency order: id, title, type, blocked by, path or issue URL. Then unresolved dependencies, and each source `AC-N` that no slice covers.

## Tracker

With `--tracker`, follow [references/tracker.md](references/tracker.md) for the delivery and the output. `--target github` writes the slice format above; `--tracker github` follows the conventions of the target repository's existing issues.
