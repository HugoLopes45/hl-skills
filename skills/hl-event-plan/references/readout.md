# Readout design

Read this file before the event date. Fix each field before the first invitation. The readout reads the event after it ends, with the export from `hl-reporting`.

1. **Primary outcome.** One outcome: the qualified meeting, under the owner's written definition.
2. **Denominator.** Realized target-buyer attendees, counted after the event from the sign-in or registration export. The organizer breakdown is only the pre-event estimate used for the go or no-go; never use it as the readout denominator. Count registrants and attendees separately.
3. **Count source.** The meeting record in the CRM or booking tool is the source of truth for meetings. Attendance comes from the sign-in or registration export. A badge scan is not an attendance count.
4. **Source tag.** Define the tag and its event name with `hl-tracking-plan`. Add the self-reported "heard us at" answer as its own figure.
5. **Attribution wording.** Write `attributed to` for tagged meetings. Give no last-touch credit. Use causal words only with a randomized holdout, as `hl-reporting` requires.
6. **Influence window.** The owner sets it before the event. Default: none.
7. **Decision rule.** Write the required rate and the verdict order from `SKILL.md` before the event. Record the thresholds the owner accepts, including one per webinar stage.
8. **Runs.** One event reads as a pilot result. A trend needs three or more runs of the same format (heuristic default, the same count `hl-reporting` uses for periods).
9. **Blocked reads.** A missing count, incomplete capture, or missing tag gives `can't tell yet`. Name the field that fixes it.
10. **Weak stage.** When a webinar stage reads below the threshold the owner recorded under item 7, diagnose it before changing the offer. Without that threshold, say `can't tell yet`. Low registration points to the topic and title. Low show-up (registrants who attend) points to reminders and calendar entries. Low hold (attendees who stay through the content) points to content order or the promise. High hold with low conversion points to the offer step.
