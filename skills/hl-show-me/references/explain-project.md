# Explain a project

Explain a whole project, or a large part of it, to a reader who does not know it yet. Dig first, ask only what the files cannot answer, then show the answer as views.

## Dig

Read before you ask. Bound the survey: list files by name first, then read at most about 15 files, only the parts that answer the subjects below.

1. Purpose and users: the README, the docs folder, the product name, the domain words in the code.
2. Stack and entry points: the manifests at the root (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `composer.json`, `Gemfile`), then the main, CLI, server, or route files they name.
3. Core flows: the 1 to 3 paths a user triggers most, from entry point to storage or output.
4. Data: the main entities and where they are stored.
5. Boundaries: external services, queues, files, and APIs the project calls.
6. Health signals, only when they change the explanation: tests, CI, recent git history, open TODOs.

From the survey, list the subjects the project offers, each named in the project's own words, for example `van assignment by capacity (planner.py)`. Keep only the subjects the files support; mark a guess as a guess.

## Ask when the angle is open

The angle decides which subjects lead and which words the page uses:

- Business: what the project does, for whom, the value it gives, the journeys of its users, its rules in plain words. No code; file names only as sources.
- Technical: the architecture, the stack, the flows as call trees, the data model, the boundaries, the risks.
- Both: business first, then the technical subjects that carry it.

Ask one question when the request names no angle and the project has both a business side and a technical side. Ask it after the survey, so the options name real subjects. Do not ask when the request already says it ("for my manager", "for my grandmother", "how is it built", "the architecture"), when only one angle exists (a library with no users of its own: technical), or when the user said to choose. A detail the files answer is never a question.

The question reply:

- Line 1, bold: what you found, in one plain sentence, and that the angle decides the next step.
- Under it, the subjects found, one line each, in the project's words.
- `Verdict: Stopped`, then `**Next:**` with the question and 3 options, each with what the page will show, the default marked: Both (default), Business, Technical. The reader may also name one subject.

The example below fixes the shape, not the content.

````markdown
**Tidewatch alerts harbor staff when a ship will dock late; your answer decides what I explain first.**
I read the README and 9 of 31 source files. These subjects carry the project:
1. Arrival forecasts from position reports (`forecast/eta.py`).
2. Alerts to harbor staff by SMS (`alerts/send.py`).
3. A berth schedule that moves when a ship is late (`berths/plan.py`).

Verdict: Stopped

**Next:**
1. Which explanation do you want?
   - Both (default): what it does for the harbor, then how it is built.
   - Business: who uses it, what it decides, and its rules, with no code.
   - Technical: the architecture, the three flows as call trees, and the data model.
````

## Show

After the answer, or when the angle is already known:

The reader must leave able to say, in one sentence, what the project changes for whom, and to retell one concrete case. A reader with no technical background, a grandparent, must get it. Tell a story, not an inventory:

1. The promise: what the project makes possible, for whom, in one sentence anyone understands, with the largest real figure the files give (crates per day, sites, euros, hours). This is the hero of the page.
2. What it takes over: the work people would do by hand or could not do without it, as the code shows it. Say on the page only what the files support; put your inferences in the reply.
3. One worked case: follow one input through the project to its result, with real values from the code, fixtures, tests, or docs ("Bakery Moreau orders 12 crates; they ride in van 2 with 31 other crates; the driver gets a sheet with 4 stops"). A value you made up carries the label `example`. This is the memorable element: animate it step by step. Its end state shows at first sight, before any click; controls only replay or step through it.
4. One everyday comparison for the core mechanism, only when it holds ("like packing a car boot: the biggest boxes go in first"). Never stretch it.
5. How it is built, for the technical and both angles only: the views in the table of `SKILL.md`, with `file:line`, after the story.

- Order the panels by what happens to the user or to the thing that moves, never by repository, folder, or module.
- Each sentence teaches something the names alone do not. "The factory builds artifacts" restates a name: say what it builds, from what, for whom, with an example.
- Explain each domain term or acronym in plain words at first use. One the files never explain: say so in the reply, and do not guess it on the page.
- A project explanation gets the HTML page unless the user asked for text. In a text reply, each story step is one heading with one view.
- Every claim comes from a file you read. Say in the reply which parts you did not read deeply; the page stays free of hedges.

## Keep the exchange going

- After the page, `**Next:**` offers at most 3 subjects to dig deeper, each named in the project's words, the most useful first.
- When an answer is unclear or contradicts the files, show what the files say and ask one question before you build.
- Each follow-up adds or changes panels on the same page by their `id`, as `references/html-page.md` describes; it does not start over.
- A reader who wants a written context pack instead of a page: suggest `hl-discover` in Next.
