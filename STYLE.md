# Skill style guide

Every skill in this repository follows this guide. Write the smallest thing a copy of you could regenerate it from. Compress language, not the investigation or delivered behavior.

## Format

One skill is one directory, `skills/<name>/SKILL.md`. Frontmatter holds `name` (`hl-` prefix, equal to the directory name) and `description`; add `license`, `compatibility`, or `metadata` only when needed. Long tables, catalogs, and prompts for subagents go in `references/` next to `SKILL.md`.

English only. Host-neutral: no host-specific tool names, slash-command syntax, argument variables such as `$ARGUMENTS`, or config paths. Name other skills in backticks (`hl-code-review`). When a step needs a capability some hosts lack (subagents, web access), say what to do without it.

No named people. A skill encodes a method, not an imitation of someone's voice or opinions.

## Prose

Use imperative rules, short sentences, clear fragments, and one term per concept. Delete filler, routine tool narration, decorative sections, and duplicate summaries. No invented shorthand or broken grammar for its own sake.

Preserve negation, conditions, causality, and step order. Keep literal code, commands, paths, identifiers, numbers, units, versions, and quoted errors exact. Preserve frontmatter, input syntax, permissions, and output contracts unless the change explicitly targets them.

Merge overlapping rules; retain reinforcement for critical constraints and examples that distinguish behavior. Clarity wins: warnings, approvals, and ambiguous sequences need complete wording. Honor requested depth and format. Human-facing artifacts use complete sentences, not compressed fragments.

## Output

The output is the product: a person skims it, then acts. Design it before the steps.

### Reader

Write for a smart reader who is new to the domain and to this codebase. The bar: a reader who reads only line 1 and `**Next:**` knows what happened, whether to worry, and what to do, without knowing any jargon. An expert reads the views below for the proof.

- Effect first, in everyday words, then the technical name: "Any signed-in user can read other users' orders (IDOR, CWE-639)", never "IDOR in orders.py".
- State the consequence in the reader's terms: money, data, time, people affected, what breaks for whom.
- Define each technical term or acronym at its first use in a few words, or replace it. Paths, commands, identifiers, and quoted errors stay exact: the reader needs them to act.
- Every number has its unit and its meaning: "3 of 12 tests fail", not "3 failures".
- Each Next step is something a person can do now: a command to paste, a file to open, a question to answer, a person to ask. Say what the step achieves when that is not obvious.
- A decision for the reader: one question, at most 4 options, each with what happens if chosen, the default marked.
- Calm and direct. Never blame the reader or the author of the code; no hype, no alarm words beyond the stated severity.

### Contract per skill

The agent running a skill sees only that skill's files, never this guide. Each `SKILL.md` therefore carries its own output section, fitted to its context:
- The reader and the moment: who reads, what they were doing, and the one decision the output serves.
- The fixed verdict words for the `Verdict:` line, each with its meaning.
- The views the skill uses, picked from the table below.
- The stopped cases: what can be missing, and how the reader unblocks it.
- One rendered example in a domain absent from the skill's eval fixtures.

Keep it as short as the skill allows: state only what differs from a careful default, and repeat the Reader rules that the skill's domain makes easy to break (security jargon, test vocabulary, marketing hype).

### Signature

Every skill renders in one signature, so a user recognizes it at a glance:

````markdown
**<the answer to the user's question, in everyday words>**
<what blocks or limits the answer, one plain sentence each; omit when nothing does>

1. **<one point, as a plain sentence>**
   <why it matters or what to change, one or two sentences>
   <a short view, only when the point has a shape>

Verdict: <verdict word>

**Next:**
1. <every step needed to act, in order>
````

Answer:
- Line 1 is the answer in bold, within 100 characters where possible and never over 140: one plain sentence that answers what the user asked, in their words where possible ("test_report is fine; another test changes the settings it reads."). It never opens with a label, verdict word, rank, ID, count, path, hash, or tool name. No title, heading, or metadata above it.
- Directly under it, in plain sentences without labels: every finding that alone defeats the goal, every blocker, every precondition of the first step, any security, credential, or data-loss risk seen out of scope (say "outside what you asked"), and what you did not read or run when that limits the answer. Nothing else goes there: how you worked (commands, timings, which agent found what, refs compared) appears once, inside the point it proves, or not at all. Never file an open risk as dismissed.
- A claim of absence names its coverage in the same sentence: "No injection in the 4 handlers I read; I did not review `admin/`", never "nothing found".
- Stopped, input needed: line 1 says in plain words what is missing and why it blocks ("**I need the error message before I can look for the cause.**"), then `Verdict: Stopped`. `**Next:**` holds at most 3 numbered ways to unblock, the default marked; they appear nowhere else.
- Several agents or lenses: line 1 states where they agree and where they split; then the disagreements; per-agent detail last, without repeating shared findings.

Body:
- One numbered item per point, worst or most useful first: a bold plain sentence that states the point ("The cache is shared between requests", never "Analysis"), then one or two sentences on why it matters, then a view only when it helps. A point that needs no explanation is its bold sentence alone. A one-point answer is plain sentences, not a list. Long artifacts and files a reader returns to (reports, context packs) use `##` sections with stable names.
- Plain words only. Never show a code the reader must decode: ranks (S1), internal IDs (AC-3, SL-04, Q1), bracket tags, status tags, the skill's own vocabulary, or its rules ("the skill says", "rule 3"). Say the meaning: "serious", "the third acceptance criterion". Names from the user's own files and tools stay exact.
- Say how sure you are in the sentence, once per point: "I ran this", "I read this, I did not run it", "this is a guess". Never tag every line.
- Shortest complete answer: cut every sentence the reader would not miss, and every view that repeats a sentence. Most answers need no view.
- Draw a shape only when words lose it: a call path across files, a file tree, a before/after, a calculation, an order of events. A fenced `text` or `diff` block, at most 8 lines of at most 80 characters, real names from the code, one node per line, `file:line` where it applies. Annotate after `#` only the lines that need it, in plain words. Changes marked `+` added, `-` removed, `~` changed.
- Tables only to compare up to 5 options or checks on up to 3 short fields, each cell a few words a newcomer can read without a legend. Otherwise a numbered list.
- Every stated count equals the items listed. Repeat the name instead of pointing ("Claim 2", "above", "same as before"). Each fact once; check that every number, date, and named line matches wherever it appears.
- Links: cite `[n]` in the text and list each URL once at the end.

End:
- `Verdict: <word>` on its own line just before `**Next:**`: the skill's fixed verdict word, plus a short qualifier when the skill defines one. Same state, same word across skills. Verdict words are everyday words, never codes.
- `**Next:**` holds every step needed to act, in order, one line each. A fix or action is stated here, not also in the body. Or the decisions needed, each one direct question with at most 4 options and the default marked. A follow-up mode goes on a Next line.
- `**Changed:** <paths>` or `**Changed:** none`, only in skills that can write. No other process narration and no metadata lines (refs read, hashes, scope, checks run): how the work was done appears only when it limits the answer, as a plain sentence under line 1.

Pick the view by content:

| Content | View |
|---|---|
| Findings, claims, risks, questions | Numbered list, one bold plain sentence each |
| Up to 5 options or checks with the same short fields | Table |
| Items with several long fields | One numbered item each, one field per line |
| Runtime or failure flow, causal chain | Call tree, `file:line` per node; only nodes you read or ran, unknown edges marked unknown |
| Layout, ownership, scope of a change | Shallow file tree, one responsibility per entry |
| Events in order | Timeline, one `time or step - event` line each; a schedule whose steps carry two or more fields is a table |
| Work that depends on other work | Text block, one item per line, aligned `after <id>` column |
| A calculation | One step per line, aligned result and basis columns |
| A threshold or rule | `condition --> action` lines |
| A funnel | One stage per line with its count |
| Logic or an algorithm | Pseudocode |
| A contract before the code exists | Types and signatures |
| A change to an existing structure, code, or copy | `diff` of that structure, code, or copy |
| Interactions or state transitions | Mermaid sequence or state diagram where it renders (a pull request, a Markdown page on a forge, an HTML page that loads Mermaid); elsewhere a call tree or `state --event--> state` lines |
| A UI, a layout, or a numeric trend | One focused HTML page |
| A concept the reader must step through or vary | An interactive HTML page: step-through, a slider per parameter, or animation |

- Prefer text views: they read the same in a terminal and on a rendered page.
- Long artifacts (a plan, a launch calendar, copy): the signature wraps the artifact. Answer and gates above, Next below; the artifact keeps its own sections and always ships complete.
- Prose follows ASD-STE100 loosely: procedure sentences up to 20 words, descriptive up to 25; one meaning per word; active voice; articles kept. Replace jargon, or define it once.
- A long explanation: offer an interactive HTML page; a video only on explicit request (`hl-explainer-video`).
- Deliver the requested artifact (file, table, diagram, code) within the skill's permissions, not instructions to make it.
- Quote only the log lines that prove a point; raw logs are never the result.
- Omit empty sections. Write "none" only where absence is the answer: findings, blockers, possible bugs.
- No preamble, recap, or closing summary.
- Exact formats: stored agent-facing artifacts (subagent records, handoff briefs, plans for another agent, emitted prompts, commit messages, tracker tickets) and paste-ready copy for people (emails, posts, landing copy). Put copy in a fence or blockquote with `[PLACEHOLDER]` slots; instructions stay outside it. The reply that presents an exact artifact still uses the signature.
- Each `SKILL.md` carries one rendered example of its output in this signature; the example fixes the shape, never the content. A skill's report template conforms to this section.

Before a skill ships, check its output on representative inputs, as `hl-writing-for-agents --skill` describes.

## Implementation workflows

YAGNI: deletion before addition. Build the smallest correct version; challenge the remaining requirements in the same reply. Label unfinished scope.

Understand the request, affected flow, and callers first. Prefer existing behavior, repository code, standard library, native platform, installed dependency, then minimal new code. Never weaken validation, data-loss handling, security, accessibility, or edge-case correctness to reduce size.

Delete tautological code and tests. Remove checks already guaranteed by types or earlier guards on the same path. Comments explain why, never restate code.

## Evidence and scope

Missing evidence means unknown, not success. Label proposed criteria and expected output as not observed. Name blockers and checks not run. No output-length, finding, or test-count quota proves quality or savings.

The description is the trigger: state what the skill does, then `Use when ...`. Hosts may load a skill whenever its description matches the request. A skill with side effects (commit, push, pull request, CI changes) says `Use only when the user explicitly asks` in its description and acts only on that request. A skill never loads another skill on its own; it may name one as a suggestion.
