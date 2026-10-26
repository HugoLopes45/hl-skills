# Cross-domain attack methods

Use these methods with the selected [domain guides](domains.md). Each investigation starts from a source-visible boundary, not a desired finding. The skill's source-read-only, secret and permission rules apply. Validation examples below describe safe future checks, not actions authorized by this audit.

## Build the security claim

Name an actor, their initial authority, the value or action they control, the expected invariant, the final decision and the affected resource. Work both forward from the entrypoint and backward from the privileged operation. Join only paths supported by actual calls, registrations or data consumers.

Track values through decoding, coercion, validation, canonicalization, serialization, persistence, caching and eventual reuse. Record what each layer guarantees and what the next layer assumes. A guard before normalization may protect a different value from the one the sink consumes.

Test a proposed claim against the strongest visible defense. Identify exact framework/API behavior from permitted documentation or source, including its version. If decisive behavior is unknown, keep that fact as a blocker rather than assuming either safety or exploitation.

## Injection and interpretation

Trace untrusted values, identifiers, keys and metadata into queries, shell arguments, templates, expressions, serializers and parsers. Distinguish parameter binding from escaping, argument boundaries from shell quoting, and data parsing from executable interpretation. An object or array accepted where code expects a scalar can become a query operator. A deserializer that selects types from its input is an interpreter: establish who can write those bytes and whether the loader restricts types.

Search stored and delayed paths: a field safely inserted into a database may later become a dynamic query fragment, template, URL or command. Review secondary sinks such as analytics, logs and search indexes. Establish the final interpreter and actual context; a suspicious string concatenation alone is insufficient. An interpreter whose code is unavailable, such as a stored procedure defined only in the database, stays a blocker.

For a safe validation plan, identify the smallest dummy input that changes syntax or accesses one forbidden dummy record. Also specify an input that remains ordinary data under the claimed defense. Do not generate escalation chains or execute an arbitrary command.

## Identity, ownership and alternate access

Follow the identity that reaches the decision, not merely the first authentication middleware. Separate authentication, resource ownership, tenant scope, role, delegated capability and explicit user intent.

Compare all routes to the same effect: direct lookup, list, search, bulk operation, export, worker, internal API and recovery flow. Check each item's authorization in mixed-owner batches. For a nested resource, confirm the child is loaded through, or checked against, the authorized parent. Review caller-controlled fields that can replace a validated principal, owner, role or target after a guard.

For each privileged function, find the server-side role or permission check on every route and HTTP method that reaches it; hidden controls, client route guards and unlisted paths are not checks. Establish whether the guard applies globally with explicit exemptions or per handler, and list handlers without it. Grants, invitations, impersonation and credential creation must not confer more authority than the granter holds or reach outside the granter's tenant. A check enforced outside source, such as by a gateway, policy engine, identity service or database policy, is an external fact.

A random identifier is not authorization. An authenticated actor can still attack another user. Conversely, a deliberate action confined to the caller's own permitted resource is not privilege escalation. A defended variant must enforce the right principal/resource check at the operation that matters.

Check every failure path of a security decision. A swallowed exception, an unawaited promise, an unchecked null, an ignored return value or a fall-through branch can leave a guard failing open.

## Workflow transitions and replay

Write the allowed state transitions for the actual workflow, including who may cause each transition and which resource/amount/action approval covers. Then trace every transition writer, not just the main UI: generic update, import, admin and webhook paths can set a state or amount field directly. A price, discount or eligibility value echoed by the client stays caller-controlled until the server recomputes it.

Inspect skipped steps, backward transitions, duplicate callbacks, expired approvals, resumption and replay of completed operations. Bind idempotency to the principal, action and normalized resource, not just a caller-selected request key. Confirm whether retries return the prior result or repeat a side effect.

Review partial failure between authorization, reservation, external action and commit. Does recovery restore a forbidden state, lose ownership, or perform an action twice? Are revocation and current permissions reapplied on restore, retry and background completion?

Use a minimal dummy sequence as a validation plan: permitted start, one manipulated transition or replay, and the final invariant. A duplicated response alone is not proof of a duplicated charge or mutation.

## Concurrency and time

Identify the shared state and the atomicity boundary. Trace check/read, mutation and commit under the real lock, transaction or compare-and-swap semantics. An asynchronous function or two statements alone does not establish a race.

Construct a concrete two-actor schedule that fits the source and defeats the invariant. Check transaction isolation, unique constraints, lock scope, fencing, retries and rollback before claiming a double spend, double approval or stale authorization. At common default isolation levels, a transaction alone does not serialize a read-then-write; look for a row lock, a conditional write or a unique constraint. An in-process lock does not span workers or instances.

For time boundaries, inspect exact comparison operators, clock sources, units, timezone conversion, grace periods and cache expiry. Show why an attacker can exploit the interval; normal eventual consistency without cross-boundary harm is not a finding.

A safe validation plan uses deterministic scheduling and dummy state, not probabilistic stress or repeated live calls. If the storage engine, its effective isolation level or the worker and instance count is unknown, identify it as the missing condition.

## Numeric and representation boundaries

Follow accepted ranges, units and precision from input to accounting, quota, allocation or policy. Check negative and zero values, signedness, overflow, truncation, NaN, fractional conversion and duplicated fields only where the interface can admit them.

Compare the exact value checked with the value consumed. Inspect disagreement between a schema, generated binding, database type and downstream API. State the concrete forbidden transition or resource effect; a loose type or parsing error without impact is not enough.

## Files, URLs and native resources

Trace path resolution and URL parsing through normalization, links, redirects, DNS and final resource acquisition. Inspect archive entries, temporary files, symlink/hardlink handling and check/use races. Read the relevant confinement control, not just a string prefix check.

For SSRF, establish what destination or action the caller controls, the receiving process's authority, and whether the client connects where the check looked: same URL parser, no unchecked redirect, no second DNS resolution and no other scheme. A fixed hostname may still expose privileged paths or redirects. An arbitrary URL is not necessarily an exploit if all reachable resources and credentials remain appropriately isolated. Egress rules and metadata-service settings are usually deployment facts.

For uploads, compare what the check inspects (client filename, declared type, extension or content bytes) with what each consumer uses: a server handler chosen by extension, a converter that sniffs content, or a browser rendering the file from an application origin. A check on one property does not constrain a consumer that reads another. Serving type, disposition and origin are often set outside source.

Use the native-memory guide for bounds, ownership, lifetime, ABI and concurrency. Distinguish a local parse failure from attacker-triggerable shared-process or memory-integrity damage.

## Cryptography and sensitive data

Follow key identity, lifecycle and security purpose without reading prohibited secret material. Review nonce uniqueness, authenticated encryption, verification order, key derivation, randomness sources, certificate/hostname verification and failure paths.

Do not report a deprecated primitive solely by name: establish its security-sensitive use and attacker advantage. A failed crypto operation must not silently remove protection. Secret findings require safe redacted evidence, location and type, never the value. A URL, connection string or log line can carry a credential. Classify a credential by type and authority; public and publishable keys are not secrets. Deleting a committed secret does not revoke it, since history, packages and images keep copies. Whether it is live, revoked or a placeholder is an owner fact; never test it by use.

Follow sensitive data into errors, logs, metrics, URLs, caches, exports and client responses. Determine which lower-trust reader can obtain it. A field name or generic internal detail does not prove disclosure of a secret or another principal's data.

## Feature composition and delayed effects

Compare outputs and guarantees across components. A permission-safe write can still create an unsafe later read, render or privileged action. Review combinations that share data but use different controls: import plus export, preview plus cache, search plus hidden fields, restore plus ownership, or retrieval plus a delegated tool.

For each step, establish the producer, stored value, consumer, identity and decision. Do not jump from a weak first step to a hypothetical final impact. If one step is unavailable, preserve the exact missing link as `needs_validation`.

Look for permission or capability growth during refresh, delegation, migration, caching and recovery. The final actor/action/resource binding must retain the restrictions that earlier code promised.

## Availability and defaults

Trace attacker-controlled work into shared CPU, memory, disk, connections, queues, quotas or operator spend. Check caps before costly work, not merely on the final response. Inspect cancellation and ownership of resources after errors or disconnects.

Review defaults when config, authentication state, dependencies or feature flags are missing. Establish whether fallback behavior crosses a security boundary; missing hardening by itself is not an exploit. Resolve each security setting through its loader's precedence of defaults, files, environment and flags. A dangerous value confined to a development or test profile needs a maintained deployment that loads it; which profile production loads is often an external fact.

Use bounded cost accounting, one small fixture or a deterministic schedule as the validation plan. Never prove availability impact by exhausting a service.

## Variant search and blind spots

Once a root cause is established, inspect equivalent source patterns and different implementations of the same invariant within scope. Do not copy the first finding's severity or conditions onto every match.

Read route/handler registrations and sensitive operation callsites that do not look security-related. Examine generated, legacy, error and optional-feature paths only when their activation is source-supported. Comments claiming safety and tests covering the happy path are hypotheses, not proof. Framework escaping protects only the contexts it covers.

Do not dismiss a concrete path only because it involves resource exhaustion, a race, a regular expression, a prompt, a fixture, documentation or memory safety. Establish attacker control, execution context and impact, as for any other class.

Keep a negative control for each concern: the strongest real defense that would reject the same attack. Record what defeats the claim, what remains unknown, and what evidence would change the decision. A successful hunt may produce no confirmed findings.
