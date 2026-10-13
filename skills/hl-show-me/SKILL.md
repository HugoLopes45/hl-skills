---
name: hl-show-me
description: "Answer the current topic with a picture instead of paragraphs, as pseudocode, a call tree, a component tree, types and signatures, a file tree, a table, a timeline, a Mermaid diagram, a diff shaped like the thing that changes, or one focused HTML page, interactive when the reader must step through or vary the concept. Use when the user says \"show me\", \"draw it\", \"diagram this\", \"what does the flow look like\", \"too much text\", or when the shape of the code, the data, or the change is the answer and prose would bury it."
---
# Show Me

Input: `[what to show, or nothing for the current topic]`

Make the topic visible. Open with the one or two sentences of the answer, then the smallest view that carries it, then stop. A one-sentence answer beats a view that adds nothing. No preamble, no recap of the question.

When the topic is a wall of prose, restate it as views, with prose only for what they cannot show. Nothing to show: say so and stop.

## Reply

Reader: a newcomer to this code who asked to see a flow, a shape, or a change, and must understand it before acting.

- Line 1, bold: one plain sentence that answers the question, effect before the name of the thing shown. Under 100 characters.
- Under line 1, plain sentences for each caveat the view hides that the reader would act on, such as a missing check or a connection never closed. Say what you did not read or run only when it limits the answer.
- One view under it. Add a heading above the view only when the reply makes two or more points.
- Flow: show only the calls that answer the question, one per line, `file:line`, with a plain annotation. Leave out internal details the reader does not need (connection setup, unused fields). Over 8 lines: split the view under two headings.
- `Verdict: Shown` on its own line just before `**Next:**`, or last when there are no next steps.
- `**Next:**` only when the reader must act now: open the HTML page, or answer one question. Each step names a file as `file:line`, a command, or a question.
- `**Changed:**` only for the HTML page: its path, or `none`.
- Nothing to show: line 1 `**There is no topic to show yet. Name the file, flow, or change you want to see.**`, then up to 2 numbered ways out, the default first: 1. Name the topic, for example `show me the login flow` (default). 2. Paste the code or the diff. Then `Verdict: Stopped`.
- Name an unfamiliar view in a few words at first use, for example `call tree (functions in call order)`.
- Annotations after `#` say what the line means in plain words (`# sends the email`), never a code or rule ID. Counts carry their unit: `4 steps`, not `4`.

The example below fixes the shape, not the content.

````markdown
**A returned book is checked in, and its hold moves to the next patron.**
The email goes out before the response is sent, so a failed email fails the return.

One request runs in this order. A hold is a reservation a patron placed.
```text
POST /returns               routes/returns.ts:14
  checkInCopy               returns/checkIn.ts:8
    markAvailable           catalog/copies.ts:31
    notifyNextHold          holds/notify.ts:19   # sends the email to the next patron
  respond 200               routes/returns.ts:22   # HTTP 200: success
```

Verdict: Shown

**Next:**
1. Open `holds/notify.ts:19` to read the email wording.

**Changed:** none
````

## Views

Logic or an algorithm, as pseudocode:

```text
on(save)
  if content is unchanged
    return cached result
  write new content
  return fresh result
```

Runtime control flow, as a call tree:

```text
submitForm
  createSession
    persistPrompt
    launchAgent
  navigateToSession
```

UI structure, as a component tree carrying the state and module boundaries that matter:

```tsx
<SessionPage> (apps/example/src/routes/session.tsx)
  useSessionEvents()
  <SessionToolbar>
    <RunSkillButton> (packages/ui)
```

A contract before the code exists, as types and signatures:

```ts
interface Cursor {
  position: ItemId
  direction: 'up' | 'down'
}

resolveTarget(items: Item[], cursor: Cursor): ItemId | null
```

Options against criteria, as a table, the recommended option first:

| Criterion | Option A | Option B |
|---|---|---|
| Cost | low | high |
| Speed | slow | fast |

Events in order, as a timeline:

```text
09:12  deploy v2.3 starts
09:14  error rate rises on /checkout
09:20  rollback to v2.2; errors stop
```

File responsibility or a broad refactor, as a shallow file tree:

```text
src/
├── commands/       # parses user actions
├── sessions/       # owns session state
└── transport/      # sends API requests
```

Component interaction or state transitions, as a Mermaid sequence or state diagram, only where Mermaid renders (a pull request, a Markdown page on a forge, an HTML page that loads Mermaid, an interface that renders it); elsewhere a call tree for interactions or one `state --event--> state` line per transition:

```mermaid
sequenceDiagram
    participant User
    participant UI
    participant Daemon
    User->>UI: choose command
    UI->>Daemon: send expanded prompt
    Daemon-->>UI: stream result
```

## Diffs

Use `diff` when the point is what changes and the surrounding shape already exists. Match the diff shape to the topic.

A component change:

```diff
 <SessionPage>
   useSessionEvents()
   <SessionToolbar>
+    <RunSkillButton />
   <SessionTimeline>
+    <SkillResultCard />
```

A file-layout change:

```diff
 src/
 ├── commands/
+│   └── show-me.ts       # expands the command
 ├── sessions/
-└── transport.ts
+└── transport/
+    ├── client.ts
+    └── stream.ts
```

A call-tree change:

```diff
 submitForm
   createSession
     persistPrompt
+    expandSkillMention
     launchAgent
-  navigateToSession
+  navigateToSession
+    subscribeToEvents
```

A state or control-flow change:

```diff
 on(save)
-  write content
+  if content is unchanged
+    return cached result
+  write new content
+  invalidate cache
```

Show the whole block instead when most of it is new, when omitted context would hide ownership or order, or when the user needs a copyable target shape:

```ts
function expandSkill(command: string): string {
  const skillName = command.slice(1)
  return `use the ${skillName} skill`
}
```

## HTML page

For a visual UI, a layout, a state comparison, or a concept too dense for Mermaid, write one focused HTML file: a diagram, an infographic, or a short slide deck, whichever fits the point. Add interaction only where it teaches: step-through for a sequence, a slider for a parameter, animation for change over time. The page must still make sense with no interaction, and every control must work from the keyboard. Match the product's colors, type, spacing, and components; use real labels and real data; support desktop and mobile. Save it as `show-me-<description>.html` in a temporary directory, open it in the default browser when you can, and give its path.

## Scope

Keep only the calls, files, props, states, and boundaries that answer the current question or separate the options on the table. One view usually, several sometimes, all of them never.
