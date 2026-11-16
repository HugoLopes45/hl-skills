# Privacy and consent checks

Apply these checks to every property and every event in the plan. The checks raise findings for owners and legal review. They do not decide legal compliance.

1. **Personal data.** Mark a value as a personal-data candidate when it identifies a person alone or combined with other values. Names, email addresses, phone numbers, postal addresses, precise location, account or device identifiers, IP addresses, and free text are candidates. The law of each market in scope decides whether a candidate is personal data. Send unclear cases to the legal owner. Mark `not stated` when the content of a value is unknown.
2. **Sensitive data.** Send health, financial, and other sensitive details to legal review when a value could contain them. The law of each market in scope defines sensitive data.
3. **Necessity.** Keep a property only when a named metric needs it. Remove a property that no metric uses.
4. **Free text.** Never send free text as a property. Replace it with an enumerated category that the owner defines.
5. **Identifiers.** Send an internal identifier only with a stated purpose and an owner. Treat it as personal data until the legal owner decides otherwise.
6. **Consent category.** Name the consent category that gates each event, using the categories of the consent tool the user supplies. Write `not stated` when none is supplied.
7. **Behaviour before consent.** State what the event does before consent. Default: not sent, until the legal owner approves another behaviour.
8. **Markets.** Record the consent rule for each market in scope. An event that depends on an unknown rule stays `blocked` until the rule is supplied.
9. **Retention and access.** Record the retention period and who reads raw events. Write `not stated` when either is unknown.
10. **Sender.** A server-side send does not change these checks. Apply them to client and server sends alike.
11. **Audience.** When the audience may include children or patients, send the affected events to legal review.

Record each check as `clear`, `finding`, or `not stated`. A finding stays open until its owner names the decision and its date.
