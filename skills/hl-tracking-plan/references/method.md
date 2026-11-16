# Method

Use this file for the fields of each row, the naming rules, and the plan sections. The workflow and evidence rules are in `SKILL.md`.

## Chain

Each row names its parent row.

- **Decision**: the choice the tracking informs, its owner, and its review date when supplied.
- **Metric**: a number that informs a decision. Fields: name, question it answers, numerator, denominator, time window, time zone, unit, owner.
- **Event**: one recorded action that supplies a metric input. Fields: name, trigger, platform (web, app, or server), sender (client or server), consent category, metric, owner.
- **Property**: one detail attached to an event. Fields: name, type, allowed values, required, personal data (yes, no, or `not stated`), consent category, owner.

Name a rate's denominator from the user's input. When the input names none, propose one and label it `Proposed`.

## Trigger

The trigger is the user action or system state that sends the event.
- State whether the trigger is an attempt or an outcome. A click on "Submit" is an attempt. A server confirmation is an outcome. Name the outcome when the metric counts completed actions.
- Name the page, control, or state, for example "booking form, server confirmation received".

## Naming

- Event names: `object_action` in snake_case, past tense for a completed action, such as `booking_form_submitted`.
- Property names: snake_case nouns, such as `service_type`.
- Put a value in a property, not in the event name. Send `placement` with the value `header`; do not create `header_button_clicked`.
- Keep one name for one concept across all events.
- Give every enumerated property its complete list of allowed values.
- Do not rename a name that is already in use. Record a rename as a change in the plan.

## Plan sections

- `## Decisions and metrics`: decision, owner, metric, numerator, denominator, window, time zone, unit.
- `## Events`: event, trigger, platform and sender, consent category, metric, owner.
- `## Properties`: event, property, type, allowed values, required, personal data, owner.
- `## Owners`: item, owner, consumer (the report or decision that reads it).
- `## Privacy and consent`: item, finding, status (`open`, `closed`, or `not stated`), owner who decides.
- `## Verification`: event, test action, expected fields, where the payload is checked, status (`pending`).
- `## Open questions`: question, what it blocks, default or `Default: none`.
