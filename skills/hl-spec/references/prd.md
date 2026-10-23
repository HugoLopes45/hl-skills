# PRD

Input: `--prd [quick|deep] [idea text | brief path] [type: saas|mobile|cli|api|internal]`

Parse the input: the mode (default `deep`), the idea or a readable brief, and an optional product type. Missing product: ask one plain question, naming the product, and offer the mode and type only if asked. Confirm ambiguous type before drafting.

## Intake

Establish users and current workaround, core problem, business model when relevant, hard constraints, success criteria, and actual user evidence. Ask missing decisions one at a time. "Unknown" remains unknown; proposed metrics are not measured facts.

Work in `.agent-runs/prd/<slug>/` at the repository root, or in the current directory outside a repository. Existing run: ask whether to resume or choose a new name; do not overwrite. Record confirmed input in `brief.md` with mode, type, date, and evidence.

## Research and draft

Deep mode researches competitors and current workarounds, cost and pricing assumptions, and reachable market segments using primary sources. Show cost formulas with units and volume assumptions. Do not fabricate prices, weaknesses, market size, or a profitable price point. No web access: mark external claims unverified, as in quick mode, and say so.

Quick mode skips external research and marks external claims unverified. Draft core sections for users/problem, requirements, data, architecture, operational constraints, risks, and delivery scope. Include domain sections only when relevant: auth/pricing/compliance for SaaS; offline/store constraints for mobile; installation/distribution for CLI; API/versioning/quotas for APIs; access/audit for internal tools.

Independent research or sections may use available subagents with disjoint output paths. Unavailable dispatch means direct drafting with that limitation stated, not simulated independent review. Verify returned files and read their substance before integrating; a summary or nonempty file is not enough.

## Review and delivery

Check behavioral acceptance criteria, security boundaries, failure modes, sourced claims, and unnecessary scope. Do not auto-load lens or audit skills. Separate evidence-backed defects from hypotheses. Resolve contradictions across sections; unresolved blockers remain prominent. Scope changes need user approval.

Keep section files, supporting research, and a changelog in the run directory. Derive revision from recorded changes; assemble sections in explicit order into `PRD.md`, then read the assembled document for omissions and contradictions.

Open with the product and what the draft specifies, in one plain sentence, bold. Give the saved path and revision below it. Then plain sentences without labels: what was skipped (research or checks) and any blocker. Then sources as a numbered list of links, each once. Then `Verdict: PRD draft` on its own line, `**Next:**` with every open decision and reader action once, in dependency order, and `**Changed:**` with the files written in the run directory. A document with no customer evidence is a hypothesis to test, not a validated product. Do not contact users, create tracker items, or start implementation.
