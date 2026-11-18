# Page CRO checks

Use this file to read each layer of the audit. Each entry names what to read, what counts as a finding, and a test that would check the finding. A check with no evidence in the supplied page is `not confirmed`.

A test idea comes from a finding and changes one element.

## Page job and entry

- **Read**: the traffic source (ad, search, email, or profile link), the job the page must do for it, and the URL the traffic opens, followed to its final response when a fetch is available. Also follow each other inbound link the user supplies, such as a business profile's website link, a directory link, or an old URL, when a fetch is available; otherwise write `not confirmed`. If the source is not supplied, state the job as an inference.
- **Finding**: the page's job does not fit the traffic source, such as a cold paid click landing on a page that assumes the visitor is already sold, or a warm visitor landing on a page that argues the problem again; the final response is not 200, or a redirect ends on an error page; a page-type job is wrong when a pricing page does not show which plan fits which visitor, when a landing page has navigation that competes with its one primary action, or when a blog post whose topic has an action offers none at a natural stopping point. A cold-traffic page with none of a problem statement, proof, or objection answer before its last repeat of the primary action is a finding. A homepage with no route for a visitor who is still researching, such as a link to proof, is a finding; a link to proof is not a competing route. A feature page with no use case from the page or supplied brief, or no path to try or buy, is a finding.
- **Test**: a variant whose page job matches the traffic source as the only change. Fix a broken entry first; run no test on an entry that does not return 200.
- **Keep or cut**: name the page job each section serves for this traffic source; a section that serves no job is a cut candidate. This applies to waitlist, lead-magnet and high-ticket pages too.

## Primary action

- **Read**: the element that completes the primary action, its label, its position, its size and prominence against other first-screen elements, its link target, and any other button or link of similar weight. For a call action, the `tel:` number is the target and must be the number shown.
- **Finding**: the label names no action or no result; the action sits below the first screen or is out of reach after scrolling; at phone width, the main action is reachable only by opening the menu (judge from a rendered capture; without one, write `not confirmed`); the link target does not perform the action; two actions of equal weight compete, so a second route to the action (another button or link of similar weight) is a finding; a repeat of the same action is not a second route, but on a page longer than one screen, no repeat of the primary action after the proof or price it depends on is a finding, unless the action stays visible while scrolling; a popup, chat widget, cookie banner or offer bar covers the action or the headline at phone width in a rendered capture; the first screen's scan order puts the action before the value statement, or a secondary element outweighs the action (judge both from a rendered capture; without one, write `not confirmed`); a visibly secondary route, such as a text link, is a finding when it does not fit the job: an urgent need suits a direct call, a routine job with a known price suits a booking, a large purchase suits a quote request.
- **Test**: a variant with one change only: the label, the position, the size, the second route, the repeat, or the overlay's position.

### Overlays

- **Read**: each overlay on the path, from markup or a rendered capture: its goal, its trigger (time, scroll, exit, or click), how often a dismissed overlay returns, its close control, and its decline option. Check keyboard behavior with a keyboard pass on a rendered page; without one, write `not confirmed` for keyboard findings.
- **Finding**: no close control visible without scrolling, or one hidden behind content; no decline option such as "No thanks"; Escape does not close it; focus can leave it while open, or does not return to the control that opened it when it closes; the trigger fires before the visitor reaches the value statement; an overlay whose content serves none of email capture, lead magnet, discount, exit save, or announcement; a dismissed overlay returns on every visit; an overlay shows on a checkout or conversion step; an overlay shows to a visitor who already converted, which only supplied targeting rules can show (without them, write `not confirmed`); an exit-intent trigger with no fallback at phone width, such as back navigation or scroll up, when the trigger does not fire there.
- **Test**: one change only: the close control, the trigger or a fallback trigger, or the return frequency. Use the page's own engagement data as the baseline; state no timing benchmark.

## Value statement

- **Read**: the headline, subhead, first paragraph, and the largest text on the first screen, and any reason to act on the first screen: a true, specific one, such as availability, a response time, a real offer, or a deadline the business keeps.
- **Finding**: the page does not say what the product is, for whom, or what the visitor gets; the copy relies on words that name no outcome; a stranger who sees the first screen for 5 seconds (heuristic default) cannot say what it is, who it is for, and what to do next (label this `hypothesis` unless a person tested it). For a local service, a first screen that does not name the service and the service area in plain words is a finding. Fake urgency, such as a countdown that resets or "act now" with no reason, is a finding; a deadline, offer, or response time with no source on the page or in supplied material is `unsourced`.
- **Test**: a variant with the value statement as the only change.

### Promise match

- **Read**: the promise that brought the visitor, the ad text, search snippet, or email line, with where and when you read it. Then check the first screen at phone width for the same words.
- **Finding**: a paraphrase is a miss. A promise that appears only on a second slide counts as missing. A promise in a banner image counts as present when a rendered capture shows it readable on the first screen at phone width; unreadable, it counts as missing; with no capture, write `not confirmed`.
- **Test**: a variant with the promise in the headline as the only change.

## Proof

- **Read**: every count, name, rating, logo, quote, and certification on the page, and where each sits relative to the action. For a licensed trade, the license number, insurance, and years in business count as proof.
- **Finding**: proof with no source on the page or in the supplied material is `unsourced`; proof far from the action it supports, or placed before the benefit claim it supports, is a finding. When the approved copy is supplied, compare each factual line of the built page with it; a factual line absent from the approved copy is a finding. For a local service, a stock photo of a person or a uniform, which shows no real business, crew, or job, is a finding; label it `hypothesis` unless the markup or supplied material shows the image source. Judge proof wording with [calibration.md](calibration.md). Fix the source of unsourced proof first, or lead with other sourced proof.
- **Test**: a variant that moves the sourced proof next to the action. Unsourced proof is removed from the test, not tested as is.

## Objections

- **Read**: each objection the page raises, or a visitor would raise, about price, fit, implementation effort, or a bad outcome, and where its answer sits: on the page, in an FAQ, in a guarantee, or in a process description near the action.
- **Finding**: an objection with no answer on the page or near the action; a guarantee with no terms on the page or in supplied material, which is `unsourced`.
- **Test**: a variant that places the answer to the top objection next to the action as the only change. Do not write the answer.

## Form and steps

- **Read**: each input's persistent visible label, programmatic association, required status, and role in completing the task. Inspect the rendered state when markup alone cannot show label behavior. Also read the confirmation state, from supplied material; never submit a form.
- **Finding**: a placeholder used instead of a persistent label; a required field with no established task need, or one the first step does not need; a deferrable step; an optional lookup or enrichment step that can reject or hold a valid submission; a confirmation that does not say when the visitor hears back, does not give the phone number when the business takes calls, or adds a second offer. Do not infer a conversion loss from these observations.
- **Test**: restore an accessible persistent label, test removing or deferring an unnecessary field, or test the confirmation wording as the only change. Recommend a multi-step form only for many fields, distinct sections, or conditional paths. Preserve security and qualification needs. Before testing field removal, check which downstream step reads the field and whether a compliance rule requires it, and specify lead-quality or downstream-completion guardrails; write `not confirmed` for any use the supplied material does not show.

### Field order and controls

- **Read**: each field's position, its control type (text, dropdown, radio buttons, or multi-select), and the option count of each choice list, from markup; the layout and any script behavior, such as phone formatting, from a rendered capture, else `not confirmed`.
- **Finding**: a sensitive field, such as phone or company size, placed before the easy fields; a multi-column layout for fields that are not short and related; a dropdown with fewer than five options where radio buttons fit (heuristic default); a choice list whose answers vary with no "Other" option; a multi-select with no "select all that apply" instruction; a phone field with no formatting, when the form accepts numbers from other countries, as the markup or supplied material shows.
- **Test**: one change only: move the sensitive field last, use one column, change the control type, add the "Other" option or the instruction, or add phone formatting. On a demo form, a preferred-contact choice is a test candidate only as a replacement for a required field the first step does not need.

### Multi-step and survey forms

- **Read**: the step count, the progress display, the back control, and whether entered input survives a refresh, from a rendered page; without one, write `not confirmed`.
- **Finding**: a multi-step or survey form with no progress indicator, no back navigation, or input lost on refresh; a survey that shows questions an earlier answer made irrelevant.
- **Test**: restore the missing element as the only change: the progress indicator, back navigation, saved input, or hiding the questions an earlier answer made irrelevant.

### Errors and submit state

- **Read**: each field's error text and when it appears; the button and page state during and after submit; the success and verification messages. Use supplied material or a rendered capture.
- **Finding**: an error that appears only after submit (a format or likely-typo check can run when the field loses focus), does not name the problem and the fix, sits away from its field, or clears the visitor's input; a submit button that stays enabled with no progress shown; errors that do not move focus to the first failing field; several errors with no summary at the top of the form; a success state with no next step; where verification is required, a message with no resend option, no reminder to check spam, no way to change a wrong email, or no way to keep exploring; password rules shown only after a failed submit, or paste blocked in a password field, on a page that creates an account (before citing password guidance, check the current official document and name its source and date).
- **Test**: one change only: the error text, the error placement, or the submit state.

## Risk and trust

- **Read**: whether price, cancellation, terms, and contact information are reachable on the path, and whether the page makes a promise that depends on them. List each price, rating, or count on the path with its source, and each phone number on the page and in structured data. List each reassurance beside the form, such as a privacy line or "no card required", and each consent or marketing box on the path.
- **Finding**: a promise, such as a free trial, with no reachable terms on the path; a price, rating, or count that differs from its source, including the same figure in structured data, and a phone number that differs between the page and its structured data (profile numbers belong to `hl-local-visibility`). A reassurance with no source on the page or in supplied material is `unsourced`, and one that the terms or product do not support is a finding. A pre-checked consent or marketing box is a finding; a consent request with no link to the privacy notice is a finding. The required consent wording depends on the visitor's market; check it against that market's current rule, which this audit does not state.
- **Test**: a variant that shows the terms link at the action. Do not write the terms.

## Mobile and speed

- **Read**: a rendered capture of the first screen at a phone width (heuristic default: 390 px), taken after a wait (heuristic default: about 3 seconds) so late popups and chat widgets appear; on a form longer than one screen at phone width, also a capture with the last field focused; a measured report, with its tool and date; the largest image above the fold; each input's keyboard type and autofill attributes, read from markup.
- **Finding**: only from a rendered capture or measured data, except keyboard type and autofill, which read from markup. Without the evidence, write `not confirmed`. Say whether the read rests on a capture or measured data. Heuristic default: an above-the-fold image over 1 MB on a phone is a finding; it is a rule of thumb, not a platform limit. A tap target below the minimum in the current platform accessibility guidance is a finding; check that minimum before citing it, because this audit states no number. A keyboard type that does not match the input, or an input that blocks autofill, is a finding. A full-screen overlay that covers the content on first load at phone width is a finding in a rendered capture; check the current search-engine guidance on interstitials before citing a ranking effect. On a form longer than one screen at phone width, a submit control that is out of view while the last field has focus, in a rendered capture, is a finding; without a capture, write `not confirmed`.
- **Test**: name the measurement to run; do not state a result. For a submit control out of view, test a sticky submit control as the only change.

## Measured funnel

- **Read**: the export's period, source, and step counts; for a form, the form start, first-field focus, each field's completion, errors by field, and submit attempts, when the export holds them.
- **Finding**: a step with a large drop only when the export shows it, with its period and source. A form measure the export lacks is `not measured`.
- **Test**: an A/B test plan from `hl-ab-test-plan`.

## Regression check

- **Read**: after a change to a live page, the Primary action, Form and steps, Promise match, and Mobile and speed checks, plus each price, rating, count, and phone number against its source.
- **Finding**: a check that passed in a supplied earlier audit and fails in this one, or a value that does not match its source. Without an earlier audit, report a failing check as a finding and write `not confirmed` only for whether it regressed. Rank it as in Workflow step 3 of `SKILL.md`. When no check fails and every value matches its source, line 1 says so and names the checks covered; write `Verdict: Test first` with the qualifier `no regression in the checks listed`.
- **Test**: none; restore the failing element, then repeat this check.

## Writing a finding

Use this form:

1. The element, quoted, with its line or location.
2. Its effect on the visitor, and the label observed on the page or hypothesis.
3. The change to test, in one sentence.

Do not write a conversion figure in any of the three parts.
