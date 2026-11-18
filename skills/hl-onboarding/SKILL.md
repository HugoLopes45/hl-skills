---
name: hl-onboarding
description: "Design or review a first-run onboarding flow for any product: the activation event that shows first value, the minimum path to it, which inputs are required now or deferred, empty states, and the drop-off events to log. Writes the flow and does not implement it. Use when the user asks to design onboarding, cut sign-up drop-off, or review setup steps before a first use."
---
# Onboarding

Input: `[product description or onboarding flow file] [activation event, when known] [product data export, optional]`

Do not retry a permission-denied action through another command, tool, path, or environment. Report the blocker.

Ground factual claims in supplied evidence or results you observed in this session.
- Take line numbers from numbered reads, not list-item numbers. Copy hashes, quotes, and errors exactly; verify stated counts.
- Report each check's command, directory, and actual execution count. Count runs, not tool calls or test cases; include failures, exclude denied attempts. Reconcile counts with observed results.
- Report another agent's findings only after its result returns and you check them.
- Separate observations, inferences, and estimates. An outside fact without a checked source is unverified, not an estimate.
- Scope all, only, and none to what you checked. A code-backed prediction is not an observed run.
- Missing evidence: say what is unknown. Name a file or function instead of inventing a line number.

## Evidence rules

- The activation event is the first user action that shows the product's value. Take it from product data, support tickets, or the user's statement. Label it `hypothesis` until the cohort rule below confirms it, and name the data check that would confirm it.
- Judge the activation event by later retention or paid conversion over a fixed window, not by how many users reach it. Confirm it on a cohort: start each user at signup, use one early window for the event, include every eligible signup with full follow-up, keep behavior inside the outcome window out of the event definition, and confirm the definition on a later mature cohort. Show recent, immature cohorts separately.
- Write no completion, retention, or time-to-value figure without a supplied export. Write `not measured` for each.
- Each required input needs a reason the first session cannot go without it. An input with no reason is deferred or removed. Do not ask for personal data the flow does not use.
- Ask for a permission (notifications, contacts, location, payment) when the user first needs the feature it enables, and state the reason on the same screen.
- No dark patterns: no hidden opt-out, no forced continuation, no fake progress, no false urgency.
- Do not invent a benchmark, a completion rate, or a time target.
- Written output only. Do not implement, enable, or deploy the flow.

## Intent

Use targeted questions only when missing context changes the requested deliverable. Group related questions in a round, then continue if essential uncertainty remains; there is no fixed intake checklist or total round limit. Reuse prior answers and do not expand a narrow task into the full workflow.

- Act directly when the product and the user's first goal are supplied. State each inference about the goal and label it.
- Ask in one round when the product or the first goal is missing. Write `Default: none` for each fact, and explain what each answer changes.
- Missing activation evidence does not stop the design. Label the activation event as a hypothesis.
- An exact output format the user names replaces the default output. The evidence rules still apply.

## Modes

### design (default)

1. **Name the first goal and the activation event.** Use one event. When the team has none, propose one and label it `hypothesis`. With an export, apply the cohort rule in Evidence rules; otherwise keep `hypothesis` and name the check in Next.
2. **Map the minimum path.** List every step, field, permission prompt, and empty state from first open to the activation event. Treat each one as unneeded until it is shown to be needed. Each kept step is one user goal with one primary action. For the first screen, choose the option whose named risk is least likely in this product, and name the check for that risk: product-first (risk: a blank screen overwhelms), guided setup (risk: friction before value), or value-first (risk: demo data may not feel real).
3. **Classify each input.** Mark it `required now` when the task, security or qualification needs it, `deferred` when it can wait, or `removed` when nothing uses it. Defer secondary options by task dependency, not a target screen count. Preserve discoverability and recovery, and check downstream quality rather than optimizing completion alone. Infer an input from data already given, such as a company from the email domain, before asking for it. Classify each import of real user data and each help resource with the same three marks. Offer a sign-in method only when the supplied audience description shows users hold that account; otherwise label the fit `hypothesis`. Keep one path that needs no outside account.
4. **Write the empty states and the first message.** Each empty state says what to do next and what the result looks like. The first message names the next step, and it does not praise the user for steps they have not finished. If the flow uses a checklist, keep it to at most 7 items (heuristic default), ordered by closeness to the activation event, show progress, and let the user dismiss it. Show a step the user did not do as complete only when the product did it for the user, and say what it did. A guided tour has at most 5 steps (heuristic default; the owner may set another count), can be dismissed at any time, and does not repeat for a user who finished or dismissed it.
5. **Define drop-off measurement.** Reuse recorded view and completion events. Infer abandonment only with a stated observation window; do not assume an exit event reliably fires. Mark new event names as proposals. Define time-to-value and steps to activation, and activation by acquisition source and cohort, as descriptive measures; without an export each is `not measured`.
6. **Recheck drop-off and test each change.** Write a recheck rule for the owner: recheck drop-off by step on each mature cohort, and investigate a step whose drop-off rises against the prior mature cohort by a margin the owner sets (`Default: none`), until its cause is fixed or ruled out. For each step changed in an existing flow, name one test with one primary metric, retention or paid conversion; a first design has none. Suggest `hl-ab-test-plan` on a Next line for the test plan.
7. **Define the stalled-user path.** Define stalled by a window the owner sets (`Default: none`) and an unfinished step. Escalate in order: a message about the next step, in-app recovery of the unfinished task, then a person the owner assigns for high-value accounts, with the handoff logged. Suggest `hl-email-sequence` on a Next line for the onboarding email series.

### review

1. Read the supplied flow. Count the steps and the required inputs between first open and the activation event. The count is observed.
2. Mark each step as keep, merge, defer, or remove, with one reason. For a step users skip, name the missing factor first: motivation (no reason to act), ability (too hard or too slow), or prompt (no cue at the moment of need).
3. Rank findings. A step that blocks the activation event comes first.
4. Apply design steps 4 to 7 to the findings.

## Output

Reader: the product owner or designer who will change the flow. The decision served: which change to build and test first.

Line 1 is one bold plain sentence that gives the main fact about the flow or its largest barrier, for example "**The first saved care plan comes after 5 steps, and the notification request comes before any plant is added.**" It never opens with a label, verdict word, or number.

Under line 1, in plain sentences: whether the activation event is evidenced or a hypothesis, and whether any export was supplied.

For a flow of up to 5 steps, use a table with the fields Step, Required input, and Decision (keep, merge, defer, or remove). For more steps, use one numbered item per step with the same fields.

Verdict words:
- `Designed`: flow complete, or a review found no step that blocks the activation event; the activation event is labeled a hypothesis when it has no evidence.
- `Fix first`: a review found a step that blocks the activation event.
- `Stopped`: no product or first goal to design from.

Put `Verdict: <word>` on its own line just before `**Next:**`. Each Next line is one action a person can take now, in order.

Stopped: line 1 says what is missing and why it blocks the design. Then `Verdict: Stopped`. Next holds the grouped questions, each with `Default: none` and what it changes.

Reader rules:
- Define each term once at first use: activation event (the first action that shows the product's value), empty state (what a screen shows before the user has data), drop-off (a user who leaves a step before finishing it).
- Quote the step's label or the input's field name exactly.
- No promised results, no praise for the reader's effort, no blame for the current flow.

Example (signature only; the domain is not a fixture):

````markdown
**The first saved care plan comes after 5 steps, and the notification request comes before any plant is added.**
The activation event is a hypothesis: the brief names no export, so the team should confirm that "saved care plan" predicts continued use.

| Step | Required input | Decision |
|---|---|---|
| 1. Create account | email, password | keep |
| 2. Allow notifications | system permission | defer to the first reminder |
| 3. Enter home city | city | remove; no step uses it |
| 4. Add a plant | species or photo | keep |
| 5. Set watering schedule | interval | merge into step 4 |

Verdict: Fix first

**Next:**
1. Move the notification request to the first reminder screen, with its reason on the same screen.
2. Remove the city input, after confirming that no later step uses it.
3. Log the drop-off events for steps 1 to 5 as the product names them.
4. Before any rollout, plan one test each for the notification move, the city removal and the merged step with `hl-ab-test-plan`, measuring retention.
````

## Stop conditions

- No product description and no flow: Stopped. Ask for one of them.
- No first goal and no product context to infer one from: Stopped. Ask what a new user should do first; write `Default: none`.
