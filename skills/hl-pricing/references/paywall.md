# Paywall

Read this when the user asks for an in-app paywall, an upgrade screen, or a trial-ending prompt.

## Timing

- For freemium and trial, show the paywall after the user has seen a result. Do not show it on first launch, before any value exists. A hard-paywall test arm (see [plan-structure.md](plan-structure.md)) is the one exception.
- Do not interrupt a task in progress.
- Choose the trigger: a feature gate when the user taps a paid feature, a usage limit when a free limit is reached, or a trial-end prompt. Each one shows what the upgrade gives and offers a path to continue free or close.
- Before you set a prompt limit, ask the owner which annoyance signals to track. Candidates: dismissals per prompt, uninstalls soon after a prompt, and complaints about prompts in reviews or support. Do not invent a threshold; the owner sets each one.
- Limit paywall prompts per session to a count you set and test. Set a cool-down after dismissal in days, not hours. Treat the cool-down as a heuristic default and test it.

## Screen

Build the screen in this order:

1. The value the user got, in their words.
2. The plan comparison, with the current plan marked.
3. The price, with the billing period and renewal terms.
4. One primary action that names the benefit.
5. A visible control to continue free or close the screen.

## Rules

- Show the price, billing period, renewal terms, and a restore path (where the platform offers one) on the same screen as the buy action.
- Keep the close control visible. Do not hide it, use guilt copy, or add a fake deadline.
- After a dismissal, offer one optional question on why the user declined; count it toward the prompt limit.
- Show a per-period price only as support for the billed amount. The billed amount comes first.
- Set prices per market as supplied. Do not convert a price with a rate you did not check.
- Remind the user before a free trial ends. State the price, the renewal date, and what changes at expiry. Test a grace period against an immediate downgrade.
- Show at most two billing periods in the plan comparison. Each extra period adds a choice for the user.
- Show links to the terms of use and the privacy policy on the same screen as the buy action.
- If payment moves to the web, check each store's current link-out rules and current fee before you build it.
- Check each store's current review rules for subscription screens before release.

## Upgrade flow

- Keep the purchase on the current screen where the store allows it.
- Unlock the feature at once after purchase. Show the receipt.

## Trials

Treat trial length and the card requirement as tests. See [plan-structure.md](plan-structure.md) for how to compare them.

## Revenue per install

Before you set acquisition spend, compute revenue per install from measured rates at the current price:

```text
revenue per install = trial start rate x trial-to-paid rate x price x (1 - store fee)
```

Use only measured rates from a supplied export, never an assumed rate. Do not project the result to a new price. Check the current store fee for each market. Do not reuse a fee from memory or from another source.

## Paywall metrics

Measure paywall impressions, clicks to upgrade, completed purchases, revenue per user, and churn after upgrade. State the base of each rate.
