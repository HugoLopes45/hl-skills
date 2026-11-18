# Metric sources

Use this file before reading a figure from a platform, an analytics tool or an email tool. This file holds no platform numbers. Check each source's current official documentation for the values the checks ask for, and write `not checked` until you have checked them.

## Checks before a figure is read

- Find the source's documented processing delay and attribution window. Do not judge the newest days until the processing delay has passed and the attribution window has closed. Write the window in the report.
- Find each metric's definition: what counts as an open, click, session, conversion, key event or position. Write `definition not checked` until you do.
- When counts may include automated activity, judge by actions that need a person, such as replies and conversions, and state the caveat. For email, check the email tool's current documentation for whether opens include automated fetches; write `not checked` until you do, and judge email by replies and conversions until then.
- Never reconcile two sources into one blended figure. Report each source with its own definition and period.
- Report an average position as an average, with the impressions behind it, not as a rank.
- Ask the user to check that the conversion tag fires on a test conversion, and record that check; write `not checked` until they do. Record a tag firing and a conversion's arrival as two separate statuses, each with its own check.
- A missing browser tag is not missing tracking. Check the source's current documentation for server sends and native integrations, which may leave nothing on the page; ask before concluding that a source is absent.
- Exclude your own domains, login and payment hosts, and test hosts from referrer classification. Check the analytics tool's current documentation for whether a redirect through them overwrites the true source; take the exclusion list from its settings.
- Ask the user to check that the click identifier survives redirects to the landing page before judging an ad platform's conversion count; write `not checked` until they do.
- Before reading volume the platform reports as lost as demand, check the platform's current documentation for its definition and for each cause it reports, such as budget or ranking, and read each cause on its own.
- Triage a gap between two counts by a direction flip, a sudden change or a zero reading, not by its size alone.

## AI-assistant referrals

- Report traffic from AI assistants as its own channel, not inside organic or direct traffic.
- Judge that channel by its conversion rate against organic conversion rate, not by its raw count, when its counts have more than two digits; `method.md` sets the rule for smaller counts.
- Check the analytics tool's current documentation for whether some visits lose their referrer. If it does, label the count a floor: it misses those visits.
- Take the referrer list and the channel groups from the analytics tool's current documentation, not from memory.
