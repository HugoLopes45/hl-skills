# Launch Readiness and Phases

Read before the launch plan and before post-launch work. Whether the product is ready to ship is outside this file: suggest `hl-startup ship` first when that is not already settled.

## Phases

Name the current phase and, if one exists, the next one. Then take the matching case:

- The next phase is Full launch: the public launch plan in `SKILL.md` applies.
- The next phase comes before Full launch: give the open move-on criteria of the current phase as the plan, with verdict `Not yet, fix <open criterion>`.
- The current phase is Full launch: no next phase exists. Run the After launch checks below, plus the Recurring checks when the owner wants ongoing monitoring; route product updates to `references/release-updates.md`, and give verdict `Plan`.

| Phase | Goal | Move on when |
|---|---|---|
| Internal | Friendly users test the core job one-on-one | The core job works for each tester without help |
| Alpha | Controlled outside users sign up and test | Testers finish the job and list their blockers |
| Beta | Early-access list uses the product; teasers go out | Listed blockers are fixed and users return |
| Early access | Invites expand in small batches (heuristic default: 5 to 10% of the list per batch) | Usage and feedback hold at the larger size |
| Full launch | Self-serve signup opens; announce on each channel the plan names | The venue and launch date are set |

## Pre-launch checks

- The onboarding flow works for a new user without help.
- Analytics and conversion tracking are set up and tested with a test sign-up; `references/site-launch-qa.md` lists the checks.
- Launch assets exist: screenshots, a short demo, and captures of the core job.
- A waitlist or early-access list captures email addresses.
- An owned channel exists before launch: a list, a blog, or a community.
- Rented profiles link to the owned channel.
- Borrowed-channel targets are listed, with their audience overlap noted.

## Early access

- Share screenshots and short demos with the waitlist, not the public.
- Show a Beta label in the product's navigation, and offer an early-access toggle for experimental features, so every user knows which parts are in test.
- Interview engaged users, and give each a credit or similar reward for their time.
- Optionally ask the product-market fit question, "How disappointed would you be if you could no longer use it?", to refine the message.

## After launch

- Send an onboarding email sequence that introduces the key features to new users.
- Mention the launch in the next regular roundup email, for people who missed it.
- Draft comparison pages for the alternatives buyers name. Before publication, confirm each claim is accurate, current, and provable from a dated source; the owner approves publication.
- Add a no-code, interactive demo so visitors can try the product before signing up.
- Update each site section that describes the product, so no old description remains.
- Plan the next launch moment before this one ends.

## Recurring checks

- For each post-launch check, name what to look at, the condition that makes you act, and the condition that stops the check.
- Set the check cadence from how fast the signal changes. A run with no action records its result and stops. Without scheduling, list the checks with dates in Next.
- Retire a check after three runs in a row with no action (heuristic default).
- Do not run a recurring check on strategy or creative direction; it reports on results and does not decide them.
