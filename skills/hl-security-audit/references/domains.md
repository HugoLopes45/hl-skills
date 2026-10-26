# Domain routing

Select a specialist guide only when source shows that boundary. A dependency name, file extension or language is a hint to check, not a selection reason. Record each material domain as selected or excluded with a source-backed reason in the Coverage section, or in the response when no report is written. A focused question loads only the guide that answers it.

| Guide | Select when source shows | Typical evidence |
|---|---|---|
| [AI and agents](domain-ai.md) | Model context, retrieval, memory, tool calls or MCP decide what data or authority is used | Prompt assembly, tool registry, retrieval filters, memory writers, MCP client/server code |
| [Web and identity](domain-web.md) | HTTP parsing, caching, cookies, sessions, tokens, federation, MFA, recovery, API keys or mTLS | Routers, middleware, proxy/cache config, auth callbacks, token verification |
| [Browser and client](domain-client.md) | Security decisions or rendering in a browser, extension, webview content or service worker | DOM sinks, message handlers, client storage, worker scripts, CORS/WebSocket handlers |
| [Native and binary](domain-native.md) | Unmanaged memory, binary parsing, foreign-function boundaries, loaders, JIT, drivers or kernel interfaces | C/C++/unsafe blocks, FFI bindings, parsers of untrusted bytes, plugin loaders |
| [Cloud and deployment](domain-cloud.md) | Workload identity, IAM, network exposure, containers, orchestration, serverless/edge runtime or deployment overlays | IaC, manifests, charts, IAM policy, ingress, event triggers |
| [Data isolation and lifecycle](domain-data.md) | Multiple owners or tenants share storage, caches, indexes, exports, backups or deletion paths | Query scopes, cache keys, search ingestion, export/import, soft delete, migrations |
| [Local apps and IPC](domain-local.md) | Desktop or mobile app, deep links, native bridges, local sockets, helpers, installers or device storage | Manifests, URL handlers, bridge registrations, IPC listeners, privileged helpers |
| [Protocols and messaging](domain-protocols.md) | RPC, custom wire formats, queues, brokers, streams, webhooks or event consumers | Schemas, interceptors, consumers, topic naming, retry and acknowledgment code |
| [Availability and cost](domain-availability.md) | Untrusted work can consume shared CPU, memory, storage, connections, workers, quotas or paid services | Parsers, uploads, pagination, queues, retries, rate/quota accounting |
| [Supply chain and release](domain-supply-chain.md) | Dependency resolution, CI, build inputs, artifact promotion, signing, updates or plugins | Lockfiles, dependency advisories, resolver config, workflows, release scripts, updater code |

## Selection rules

- Start from the authority map. Select a guide when one of its boundaries carries an attacker-reachable input or a privileged effect inside the requested scope.
- Several guides may apply to one path. Use one coverage unit per invariant, and name every guide used in its `category` text. Do not duplicate one root cause across domains.
- Exclude a domain only with evidence: the surface is absent, outside the requested scope, or fully delegated to a component whose behavior is recorded as an external fact. "Not obviously relevant" is not an exclusion reason.
- A deployment fact the repository cannot show stays an external fact. Record it as a blocker on the dependent units; do not assume either a safe or an unsafe deployment.
- `quick` depth checks only the highest-impact selected domain units and records the other selected units as deferred. `standard` and `deep` cover every selected domain within scope.
- The coverage reviewer checks the routing itself: a missed domain with a visible boundary reopens the plan.
