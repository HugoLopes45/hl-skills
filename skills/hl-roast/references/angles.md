# Roast angles

Pick the section for the artifact type; mixed artifacts use each matching section. Angles are where to look, not a checklist to fill. Each angle names the skill to suggest in Next for a deeper fix.

## Code, diff, or repository

Look in this order; the first angles hurt users, the last ones hurt maintainers.

1. Broken behavior: boundaries (empty, off-by-one, time zones, money rounding, pagination), hidden state (globals, shared caches, retries, ordering), production-only failures (concurrency, latency, partial failure). Show the input that triggers it; without one, it is a guess. Suggest `hl-debug` or `hl-code-review`.
2. Security: user input reaching SQL, shell, paths, or HTML without escaping or parameters; missing ownership or permission checks; secrets in source; weak hashing. Stated plainly under line 1. Suggest `hl-security-audit`.
3. Silent failures: a bare `except` or empty `catch`, a failure turned into an empty result or a default, an error logged and ignored. Suggest `hl-code-review`.
4. Lies: a comment or doc the code contradicts, a reference to a function, flag, or file that does not exist, a confident number with no source. Check by search, never from memory. Suggest `hl-deslop`.
5. Bloat: a wrapper called once, a parameter every caller passes the same value, an interface with one implementation, a dependency that 20 lines would replace, a hand-rolled copy of a standard-library function. Never count validation, error handling that prevents data loss, security checks, or accessibility as bloat. Suggest `hl-deslop` or `hl-challenge --lens minimalist`.
6. Slop: comments that narrate the next line, defensive checks on values the types guarantee, type escapes (`any`, `# type: ignore`, `!`), debug output, commented-out code, `TODO: implement` where working code was claimed. Suggest `hl-deslop`.
7. Tests: a test that cannot fail, asserts only that no exception was raised, or mocks the code under test. Suggest `hl-tdd`.

Generated, vendored, or protocol-bound code: roast its use, not its size.

## Plan, design, or architecture

1. No goal, or a goal without a signal that proves it done.
2. A load-bearing assumption with no evidence: demand, scale, a dependency's behavior, a team's time.
3. One failure that takes everything down: one disk, one region, one person, backups next to the data.
4. Built for a future nobody asked for: queues, microservices, or plugins before the first user.
5. Missing cases that change scope: empty, duplicate, concurrent, stale, partial, hostile.
6. Undecided decisions disguised as details: vague terms, "TBD", two meanings for one word.

Suggest `hl-challenge` for a verdict, `hl-grill --gaps` for what the plan leaves unsaid, `hl-spec` for acceptance criteria.

## Product or startup idea

1. The pain is vague, or nobody is named as having it.
2. The status quo is ignored: the spreadsheet, the intern, or doing nothing already solves it well enough.
3. Interest is treated as demand: likes, waitlists, and "people said they would pay" instead of payments or repeated use.
4. No channel to the first 10 customers.
5. The first version takes months; nothing tests the core assumption in two weeks.
6. Sunk cost used as a reason to continue.

Never invent market sizes, competitors' numbers, or customer quotes. Suggest `hl-startup`, `hl-positioning`, or `hl-pricing`.

## Landing page, pricing page, or ad

1. The first screen does not say what it is, for whom, and the outcome.
2. No single primary action, or several actions of equal weight compete.
3. Proof is missing, far from the action, or unsourced ("10,000 happy customers" with no source).
4. The form asks for fields the first step does not need.
5. Price, terms, or cancellation are hidden where the promise depends on them.
6. Grand claims (revolutionary, effortless, all-in-one) that a competitor could paste unchanged.

Speed and mobile issues only from a measured or rendered check. Never invent a conversion rate or a lift. Suggest `hl-page-cro-audit`, `hl-copywriting`, or `hl-pricing`.

## Prose: article, email, README, post, CV, bio

1. The subject is buried under a stock opening ("In today's fast-paced world", "I am writing to").
2. Claims with no support: numbers without period or baseline, superlatives, testimonials without a source.
3. Padding: repeated benefit summaries, lists padded for rhythm, rhetorical questions that repeat the headline.
4. Abstract subjects and verbs that hide who does what.
5. The reader cannot tell what to do next: no call to action, or three of them.
6. One concept with several names.

A pattern is a reason to look at the meaning, not proof of AI authorship. Suggest `hl-de-ai-rewriting`, `hl-email`, `hl-article-writing`, or `hl-social`.

## Prompt, skill, or agent instructions

1. Rules that contradict each other or the examples.
2. Shouting (ALL CAPS, "CRITICAL", "YOU MUST") instead of a reason.
3. Vague verbs ("handle", "improve", "make it good") with no output contract.
4. The same rule repeated in three places with three wordings.
5. Missing failure behavior: what to do with no input, a denied action, or missing evidence.

Suggest `hl-writing-for-agents`.

## Anything else

Ask three questions of the artifact: who is it for, what must it make them do, and what stops them. Roast the answers you can locate.
