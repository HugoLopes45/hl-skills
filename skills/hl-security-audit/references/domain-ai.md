# AI, agent and MCP boundaries

Use with [attack methods](attack-methods.md). This guide covers the delegation layer where a model reads content and influences data access or actions. Transport, queries, files and rendering remain ordinary boundaries; use the matching guide for them.

## Establish first

- **Identities.** Who starts each request, which identity each tool call executes as, and which credentials the agent, sub-agents and MCP connections hold.
- **Capabilities.** Every tool, its side effects, the resources it can name and the handler-side authorization it performs.
- **Writable context.** Every source that can enter a prompt or memory: retrieved documents, uploaded files, web pages, email, issue text, tool results, MCP metadata and stored memory. Name the writers of each.
- **Destinations.** Where model output goes: a renderer, a tool argument, a stored record, another agent or a privileged decision.

Connect a writer's authority at the start to the authority used at the end. Work backward from each side-effecting tool through dispatcher, schema, confirmation, context assembly, retrieval and ingestion.

## Review questions

### Context and memory

- Can a lower-trust writer place content into another principal's context? Check retrieval filters, embedding/query caches and history stores for tenant and ACL scope in the query itself, not only on stored rows.
- Who can create, update or merge durable memory? Does a later task, user or privileged session read it as policy or fact? Does memory keep provenance and owner scope?
- Can untrusted text claim a system, tool, policy or memory role through concatenation, an untyped history array or a caller-set role field? Does the forged role change a deterministic decision?

### Tools and actions

- Does each handler validate model-produced arguments before its sink? A schema constrains shape; it does not authorize a resource, a path, a URL or a query.
- Does the handler check that the requesting principal may perform this exact operation on this exact resource, or does it rely on the agent's broad credential?
- Is an approval bound to the normalized tool name, complete argument object, requester, target, amount, expiry and batch membership? Can a retry, resumed session or later turn reuse it for a changed or duplicated action?
- Can attacker-supplied content cause an action under a victim's valid authority that the victim did not request or approve? Generic authorization does not establish intent.
- Do the schema validator, dispatcher and handler agree on aliases, extra fields, duplicate keys, coercions and defaults?
- Is delegated work bounded by a per-request budget, cancellation and idempotency where it spends money, sends messages or mutates shared state?

### Sub-agents and MCP

- Does a sub-agent or MCP call receive only the authority the task needs? Are its results treated as untrusted on return?
- Are calls and results bound to the authenticated connection and the outstanding request, rather than to a server name, tool name, request ID or model-chosen alias? Can two servers claim the same tool or resource identity, or a reconnect change the binding?
- Does any decision trust peer-supplied tool descriptions, prompts, resource metadata or schemas as policy? Find the deterministic allowlist and handler check that win when metadata conflicts.

### Output and disclosure

- Does model output reach HTML, Markdown, templates, URLs or commands without that sink's encoding and policy? Use the client guide for browser rendering.
- Does assembled context contain credentials, other users' data or access-granting values that output can reveal? Generic instructions are not a data boundary.

## Decide

- Persuasive injected text alone is not a finding. Require a code-level failure: content reaches another principal's context, uses authority the requester lacks, discloses data the reader cannot access, causes an unrequested action, or reaches a sink the attacker cannot reach directly.
- A guardrail prompt is not a control. Count only deterministic checks, resource-scoped authorization, isolation, binding and narrowed credentials.
- A user's intentional request using their own authority is not a delegation defect because a model executed it. Memory a user saved for their own permitted use is not cross-boundary.
- For memory or retrieval claims, cite both the attacker-reachable write and the later cross-principal read or privileged decision.
- Use `needs_validation` when the decision depends on provider behavior, model routing, renderer behavior, external MCP server identity or deployed configuration not visible in source.
