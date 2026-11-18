# Privacy and consent checks

Apply these checks to every property and every event in the plan. The checks raise findings for owners and legal review. They do not decide legal compliance.

1. **Personal data.** Mark a value as a personal-data candidate when it identifies a person alone or combined with other values. Names, email addresses, phone numbers, postal addresses, precise location, account or device identifiers, IP addresses, and free text are candidates. The law of each market in scope decides whether a candidate is personal data. Send unclear cases to the legal owner. Mark `not stated` when the content of a value is unknown.
2. **Sensitive data.** Send health, financial, and other sensitive details to legal review when a value could contain them. The law of each market in scope defines sensitive data.
3. **Necessity.** Keep a property only when a named metric needs it. Remove a property that no metric uses.
4. **Free text.** Never send free text as a property. Replace it with an enumerated category that the owner defines.
5. **Identifiers.** Send an internal identifier only with a stated purpose and an owner. Treat it as personal data until the legal owner decides otherwise. Send an identity merge only when the identity is unambiguous; when in doubt, send nothing and record the unmatched share as a rate.
6. **Consent category.** Name the consent category that gates each event, using the categories of the consent tool the user supplies. Write `not stated` when none is supplied.
7. **Behaviour before consent.** State what the event does before consent. Default: not sent, until the legal owner approves another behaviour. If the legal owner approves a denied default that updates on consent, record that events wait for the update, and confirm the tool's consent behaviour in its official documentation.
8. **Markets.** Record the consent rule for each market in scope. An event that depends on an unknown rule stays `blocked` until the rule is supplied.
9. **Retention, access and data controls.** Record the tool's default retention period from its current official documentation before the plan sets its own. Record who reads raw events. Ask whether the tool can delete one person's data on request, and record the answer. Record whether IP address anonymization is available and whether it is on. Write `not stated` for each unknown item.
10. **Sender.** A server-side send does not change these checks. Apply them to client and server sends alike.
11. **Audience.** When the audience may include children or patients, send the affected events to legal review.
12. **Recipients.** Name each recipient that receives the event or property, such as an ad or email tool. Send each recipient to the legal owner before the event is implemented. An unreviewed recipient is a `finding`; verdict `Review first`. Write `not stated` when the recipient or its consent rule is unknown.

Record each check as `clear`, `finding`, or `not stated`. A finding stays open until its owner names the decision and its date.
