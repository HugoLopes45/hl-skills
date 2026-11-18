# Interface copy

Use this file for words inside a product or a site: buttons, empty states, errors, confirmations, forms, popups, upgrade screens, notifications. Read "Rules for all interface copy", then the section you need.

Interface copy is read mid-task by someone who wants to get on with it. The job is always the same: say what happened, what it means for the reader, and what to do next, in that order. Voice lives in word choice and in the low-stakes moments, never in place of the information.

Every example line is invented and shows the pattern only.

## Rules for all interface copy

- Write each screen from the facts of the product: what triggers it, what is kept or lost, what the reader can do. Ask for a missing fact the reader needs; do not guess a behavior.
- Keep the product's existing labels. A button called "Add plant" elsewhere stays "Add plant" here.
- One name per thing across every screen.
- A button says what it does, as a verb and its object: "Delete plant", "Update card". Never "OK", "Yes", or "Submit" on an action with consequences.
- State counts and durations exactly as supplied. An average is not a count: write "its photos", or the real number for this item when the product can show it, never "14 photos" when 14 is an average.
- Put the reader's variable where it belongs with a clear slot, such as `{plant name}`, and say that the product fills it.
- Decide humor per screen with the table in [humor.md](humor.md). The same product is playful on its empty state and plain on its payment failure.
- Deliver each screen as its parts: title, body, primary button, secondary action. A light line is part of the title or the body, written where it will appear; it is not a separate field, and it never trails after the buttons.

The same 404, three ways, for an invented bakery ordering site whose reviews call it "cheeky" and whose brief supplies the order screen and a support address:

```
Flat (wastes a low-stakes moment in a voice that allows more):
  This page is not here
  The link may be old, or the address may have a typo.
  [Back to the menu]

Bolted on (the joke is an extra line, after the action):
  This page is not here
  [Back to the menu]
  Looks like this page is toast!

Right (the light line is the title; the body still does the job):
  This page did not rise
  Nothing is baked at this address. The menu is still warm.
  [Back to the menu]    Write to us: hello@bakery.example
```

The right version states that the page is missing, offers the supplied ways on, and takes its words from the product's own world. It claims nothing about the product.

## Empty state

Job: turn a blank screen into a first action.

- Say what will appear here, and give the one action that makes it appear, using the existing button label.
- One sentence may show what the reader gets from that first action.
- A good place for personality when the voice allows it, because nothing is at stake. The next step still comes before or right after the light line.
- Mention a plan limit only if the reader will hit it soon.

## 404 and not-found pages

Job: get a lost reader back on a path.

- Make it plain that the page is not here; a title in the product's own words that still says so counts. Do not blame the reader for the link.
- Offer one or two real ways on (heuristic default): the home or main screen, search, or support, as supplied.
- The classic low-stakes moment: one line of personality is welcome when the gate in [humor.md](humor.md) passes. It ties to the product's own world, not to a generic "lost in space" joke.

## Errors

Job: unblock the reader.

- Three parts in order: what happened, in the reader's terms; what it means for them now (what is safe, what is not); what to do.
- Name the exact fault when the product knows it ("That email has a typo: exmaple.com"), and keep what the reader typed.
- Never blame ("You entered an invalid..."). Describe the problem, not the person.
- No jokes, no cute interjections, no exclamation marks. Say sorry only when the fault is the product's, once, and in the first line.
- No raw codes as the message. A code may sit after the explanation for support.

## Payment and billing messages

Job: a reader fixes a payment or understands a charge, without alarm.

- State what failed, what stays on and until when, what changes after that, and what is never lost, each as supplied.
- Lead with the reassurance that is true and that matters most to this reader (their data is safe) only if the brief states it.
- One button: the fix. Give the support contact when supplied.
- No urgency beyond the real date. No humor. No guilt.

## Destructive confirmations

Job: prevent an accident without nagging.

- The title names the action and the object: "Delete {plant name}?"
- The body says exactly what is removed and whether it can be undone, as supplied.
- The destructive button repeats the verb ("Delete plant"). The safe choice is a plain "Cancel" or "Keep plant". Never label the pair "Yes" and "No".
- No humor and no pleading.

## Success messages

Job: confirm it worked, briefly.

- Say what was done, in past tense, with the object: "Watering logged for {plant name}."
- Add what happens next only when it is useful and true.
- A message seen daily stays plain or varies; a single fixed joke shown every day becomes noise. A light line belongs on rare successes (the first one, a milestone the product really tracks).

## Loading and waiting

- Say what is happening when the wait is long enough to wonder. Give the real duration only when the product knows it.
- Never show invented progress or invented steps.

## Onboarding and tooltips

- One idea per step. Name the action, then its payoff.
- Tell the reader how many steps there are when the product knows it, and let them skip.
- "You're almost done" is used only when it is true.

## Forms and sign-up

- Labels stay visible above or beside the field. Placeholder text shows only an example of the format, because it vanishes on typing.
- State password and format rules before the reader types, not after a failed attempt.
- A field that looks optional and is required says why it is needed, next to the field.
- Before the form, say what it takes ("Takes about a minute") only when supplied. After it, say what happens next.
- The submit button names the result ("Create my account"). "No card required" appears only when true.
- A privacy line beside the email field states only what the product does with the email, as supplied.
- An error on a field names the problem and the way out ("That email already has an account. Sign in instead").

## Popups and modals

- The headline states what the reader gets, never a bare "Subscribe".
- The line under it answers the doubt or sets the expectation, from supplied facts: how often, how long, what is sent.
- The accept button is specific and may be in the first person ("Send me the guide").
- The decline option is neutral: "No thanks" or "Not now". Never guilt wording such as "No, I don't want to save money".
- An exit popup says something different from the entry popup and admits the reader is leaving.
- A banner states one message and links to its details. How it is dismissed or when it ends comes from the supplied product behavior, not from the copy.

## Upgrade, paywall, and trial-end screens

- State what the paid plan adds as the reader's gain, tied to the feature they just touched.
- A trial-end screen may show what the reader made during the trial (a real count from the product) and what stays or goes, as supplied. Never threaten a loss the product does not cause.
- Next to the buy button: the price, the billing period, the trial length, renewal and cancellation, all as supplied. A missing one is a placeholder, because the buyer cannot pay without it.
- A per-week or per-month equivalent appears only beside the amount actually billed and its period.
- Store and platform rules on subscription disclosures change; say they are unchecked unless you read the current rules in this session.

## Notifications

- The first words carry the whole message; the rest may be cut off.
- One notification, one fact, one action. Say why now.
- Recurring notifications stay plain and vary their wording only with real information.

## Cancel flow

- Confirm what cancelling does, when it takes effect, and what the reader keeps, as supplied.
- An offer to stay is made once, plainly, and only when the brief supplies the offer.
- The cancel button is as easy to find as the stay button. No guilt, no countdown, no humor.
