# Browser and client boundaries

Use with [attack methods](attack-methods.md). This guide covers trust decisions and rendering that happen in the browser, including sources the server never sees. Use the [web guide](domain-web.md) for server sessions, CSRF and OAuth/OIDC verification, and the [local apps guide](domain-local.md) for the native side of a webview bridge.

## Establish first

- **Sources.** URL parts including the fragment, `document.referrer`, `window.name`, message data, storage, server-rendered data and cached responses.
- **Sinks.** HTML insertion, string evaluation, executable URLs, framework escape hatches, navigation, message sends, storage writes and worker registration.
- **Policies.** Framework auto-escaping, sanitizers, CSP, frame protections, COOP/CORP, cookie attributes and service-worker scope. Note which are in source and which are deployed headers.
- **Persistence.** Each client store and cache, its writer, its reader and what clears it on logout, account switch or tenant change.

Trace backward from each sink to sources. Record the policy that should stop the path.

## Review questions

### DOM and object state

- Does a controllable source reach an HTML, script or URL sink without the sink's required encoding or sanitizer? Decoding, concatenation or reparsing after sanitizing reopens the path. Framework-escaped interpolation is not a finding.
- Does an enforced CSP on the response that renders the sink stop the injection? A report-only policy, `unsafe-inline`, `unsafe-eval` for an evaluation sink, a static or reused nonce, an allowlisted host that serves attacker-influenced script, or a nonce-based policy without `base-uri` does not.
- Can injected markup with `id` or `name` attributes shadow a global or configuration value that code later trusts? Both the surviving markup and the security-relevant use are required.
- Does an attacker-controlled key reach a recursive merge or path assignment that can change shared prototypes, and does a reachable consumer then change authorization, navigation, rendering or execution?

### Cross-origin communication

- Does a message handler act on data without an exact origin allowlist, and the expected source window where several frames share an origin? Substring, prefix or unanchored pattern matching is not an origin check. Does code send sensitive data to `*`?
- Does a WebSocket upgrade accept ambient cookies from any origin without an origin check or channel token, and does a message handler then read or mutate private state?
- Does the server reflect `Origin`, match it loosely or trust `null` while allowing credentials on sensitive responses?

### Workers and storage

- Can attacker-influenced content become a worker script or import, or gain a broader scope than intended? Verify final script URL, MIME type, origin, scope and import integrity.
- Does a worker cache personalized responses without account, tenant or authorization state in its policy, then serve them after logout or account switch, including offline and error fallbacks?
- Do tokens, private responses or authorization decisions remain in client storage and reach a lower-authority reader, or keep working after revocation or logout?
- Do `storage` events, `BroadcastChannel` or shared workers carry identity or commands between tabs without binding to the current session?

### Cross-site state and UI

- Can another site distinguish a concrete protected predicate, such as whether a private object exists, through load events, frame state, redirects, cache state or size while credentials are attached?
- Can a framed sensitive action complete without effective frame protection?
- Can a client source choose a navigation destination or executable scheme without policy? Does code keep an opener relationship to an untrusted page?

## Decide

- Require a controllable source, an executing or disclosing sink, and impact on a victim session, another origin or shared persistence. Self-injection and access to the attacker's own data are not findings.
- Pollution needs both the recursive write and a security-relevant consumer. Storage and worker claims need a lifecycle path to another account, tenant or later authorization state.
- CORS needs a credential the browser attaches by itself, such as a cookie or client certificate, or a server reachable only from the victim's network. A wildcard origin without credentials, or a bearer token that script must add, exposes only what the attacker can already fetch.
- Missing frame or security headers on read-only content, generic timing variance and public resource availability are not findings.
- Check CSP, COOP/CORP, cookie policy and SameSite before assigning impact. Use `needs_validation` when the decision depends on a deployed header, browser version, extension permission or renderer behavior absent from source.
