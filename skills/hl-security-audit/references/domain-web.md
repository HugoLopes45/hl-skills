# Web protocol and identity

Use with [attack methods](attack-methods.md). Access control asks whether a principal may perform an operation. This guide asks whether HTTP or identity handling can confuse which principal, request, token or assurance level the operation belongs to. Use the [client guide](domain-client.md) for browser-side sinks and CORS, and the [cloud guide](domain-cloud.md) for ingress topology.

## Establish first

- The request path through every parser in scope: proxy, CDN, gateway, framework router and application. Note which ones the repository configures and which are external facts.
- Every credential and challenge type: session cookie, refresh token, JWT, OAuth/OIDC artifacts, SAML assertion, MFA challenge, passkey, reset token, API key and client certificate.
- For each, the lifecycle: issue, store, transmit, consume, refresh and revoke. Include error, retry, migration, legacy and account-switch paths.
- Every route to each sensitive operation. The effective policy is the weakest parallel route.

## Review questions

### Framing and caching

- Can two components assign different bytes to a request, or normalize a header name, length or line ending differently? Name both components and both interpretations.
- Does a path-, host- or method-based guard, such as an authentication matcher, gateway rule or public-route list, evaluate the same normalized request that the router dispatches? Compare case, trailing and repeated slashes, encoded separators, path parameters, suffixes and method override.
- Does any request input change a response that a cache stores without including that input in the cache key: forwarded host or scheme, selected cookies, query normalization, language or device headers, authorization state?
- Can cache routing treat a private dynamic path as a cacheable static asset through suffix, path-parameter or normalization differences?
- Do `Host` or `Forwarded`/`X-Forwarded-*` values decide absolute URLs, tenant routing, reset links, callbacks or client address? Does trusted ingress remove client-supplied copies?
- Can untrusted data reach `Location`, `Set-Cookie` or another security header? Check the framework's control-character rejection first.

### Browser sessions

- Which cookie-authenticated mutations accept a cross-site request without an effective token, origin check or applicable SameSite protection? Include method-override, multipart and legacy routes, and login CSRF.
- Is the session identifier rotated on login, privilege change, MFA completion and impersonation? Do logout, password change, revocation and account disable invalidate every session, refresh token, signed cookie and socket?
- Does a sensitive cookie have an overly broad domain or path, cross insecure transport, or collide with a sibling cookie another component selects?

### Federated identity

Identify the component's role first. Authorization-server duties do not belong to a relying party.

- JWT: is the signature verified with a server-pinned algorithm and key source, and are `exp`, `nbf`, `aud` and `iss` enforced? Are `kid`, `jku` and `x5u` treated as untrusted selectors? Is there a decode-without-verify path?
- OAuth/OIDC: is `state` bound to the session, PKCE and code binding applied where required, ID-token issuer, audience, signature and nonce checked, and the selected provider bound in multi-provider flows? Compare initial, retry, mobile and account-link callbacks.
- Authorization server: is each redirect URI matched exactly against the client's registration, each code single-use and bound to client, redirect URI and PKCE verifier, and consent bound to client and scope? An open redirect on a registered host can still carry codes or tokens to another origin.
- SAML: is the signed element the element used for identity? Check unsigned fallbacks, parser safety, canonicalization, validity window, audience, recipient, request correlation and replay state.

### Strong authentication and recovery

- Can a single factor enroll, replace or remove a second factor, generate recovery codes or trust a device without the required fresh authentication?
- Is a step-up result bound to principal, session, target operation or resource, expiry and one-time use? Does any alternate route skip it?
- Passkeys: are challenge, RP ID, origin, credential membership, user handle and required user verification checked at registration and authentication?
- Account linking: does adding an identity, email, phone, device or external account require a current session, verified ownership and callback state bound to the initiating account?
- Recovery: are reset and support-recovery tokens random, bound to user and action, short-lived, single-use and invalidating older tokens and sessions? Is the delivered link built from trusted configuration?
- Is a password, one-time code, PIN or short reset or invite code guessable within its validity? Find a failure limit bound to the account or challenge, not only to the client address. Compute the guessing budget from code space, validity window and allowed attempts; that budget, not the missing limit, is the evidence. A limit at a proxy or identity provider is an external fact.

### Service credentials

- Is an API key limited by its server-side record, or can request parameters widen its tenant, resource, action or environment? Can a publishable key act as a secret key? Do revocation caches expire?
- Can keys appear in client bundles, URLs, logs, redirects or error responses visible to a lower-trust reader? Confirm the key type and its authority.
- mTLS: does the backend accept identity headers from any peer, map subject text to accounts ambiguously, or accept the wrong trust domain or usage? Does certificate failure fall back to weaker authentication?

## Decide

- A missing header, flag, prompt or rate limit alone is a hardening note. Require an accepted invalid request, a cross-principal effect, an assurance downgrade or a credential disclosure.
- Framing and cache claims need two named components and their divergent interpretation of the same value.
- Token and challenge claims need the verification line and the specific missing binding.
- CSRF needs an ambient credential, a state-changing route, an accepted cross-site request shape and a missing effective check. Read-only routes and non-ambient bearer tokens do not qualify.
- Proxy chains, edge cache keys, identity-provider policy, certificate trust, browser cookie policy and deployed auth modes are often outside source. Record them as `needs_validation` with the exact owner-observable check. Do not downgrade an unverified critical claim into a confirmed lower one.
