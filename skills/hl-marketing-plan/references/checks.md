# Recurring checks

Read this file when a plan needs a recurring check. Adopt one check at a time. Each check names what to look at, the condition that makes the owner act, and the condition that stops the check. The owner sets the cadence and the window; this skill sets neither.

Each check uses supplied data or the owner's own records. A check that needs data the owner does not have is not adopted; name the missing data as a move.

## Tracking

- **Look at:** the count of the main metric's event in the period, against a manual count of the same records.
- **Act when:** the two counts differ by more than the margin the owner sets. Fix the event before any other move reads it.
- **Stop when:** the counts agree for the window the owner sets.

## Release tracking

- **Look at:** the key events after each release: each fires once, with its properties.
- **Act when:** a revenue or sign-up event is missing or duplicated. Fix it before the next campaign starts.
- **Stop when:** the owner retires the release check after the events have held through the period.

## Plateau

- **Look at:** per channel, the weekly additions, the cost per customer, the top-of-funnel engagement, and the effort in hours against the output.
- **Act when:** two of these signals (`proposal`) hold on one channel for the window the owner sets. Move one part of the effort to the next channel.
- **Stop when:** the next channel's first test is complete, and the owner has chosen to keep or drop it.

## Ranking drop

- **Look at:** each priority page's position for its buyer query, against its own earlier position.
- **Act when:** a priority page drops by more than the margin the owner sets. Find the cause in its content, links, or the results page layout.
- **Stop when:** two diagnoses (`proposal`) find no cause on the same page. Escalate to the owner; do not edit the page again.

## Content decay

- **Look at:** pages whose traffic or position fell over the window the owner sets, and the date of each page's last update.
- **Act when:** a page with a buyer query fell and its facts are older than the owner's update rule. Refresh the facts from a source the owner names.
- **Stop when:** the page is refreshed and the owner has reviewed one period of results after the refresh.

## Accuracy in AI answers

- **Look at:** the descriptions of the product in answers to the buyer's questions, against the supplied facts. Use several runs; one run is a sample.
- **Act when:** an answer states a price, a limit, or a compatibility wrongly. Fix the page the answer draws on, before any other page.
- **Stop when:** no wrong statement appears in the runs the owner sets.

## Churn signal

- **Look at:** accounts whose usage fell against their own earlier usage, from the owner's export.
- **Act when:** an account crosses the drop the owner sets. The owner decides the contact.
- **Stop when:** the owner has reviewed the flagged accounts for the window and no account is still open.

## Campaign postmortem

- **Look at:** the campaign's result against its stop criterion, written as one page.
- **Act when:** the campaign ends. Write the page before the next campaign is funded.
- **Stop when:** the page is written and the owner has recorded the decision it supports.
