# Protocols, RPC and messaging

Use with [attack methods](attack-methods.md). This guide covers how messages are decoded, authorized, routed and processed across services, brokers and webhooks. Use the [web guide](domain-web.md) for HTTP framing and the [availability guide](domain-availability.md) for amplification.

## Establish first

- Each schema or wire format and every decoder in scope: generated, hand-written, gateway and version converters.
- For each method, topic or event: the authenticated producer, the authoritative identity source, the handler and its side effects.
- Delivery semantics: at-least-once or at-most-once delivery, ordering guarantees, retry and dead-letter policy, and acknowledgment timing.

## Review questions

### Decoding and representation

- Do two decoders disagree on length, compression, duplicate or unknown fields, encoding, numeric width, normalization or envelope-versus-body precedence? Which principal, resource or operation differs after decoding?
- Do unknown variants, missing discriminators, zero values or compatibility mappings reach code that assumes a validated case? How do old consumers read new fields?
- Does authorization use envelope or routing metadata while the handler acts on a different tenant, subject or object named in the body? Which source is authoritative, and can a client override it?

### Authentication and authorization

- Does every registration of the same operation pass through the authentication and authorization interceptor: unary and streaming methods, reflection, health, transcoded gateways and compatibility services?
- After mTLS, workload identity or broker credentials authenticate a channel, can a caller-controlled field select another user or tenant?
- Is each stream, subscription, batch or bulk item authorized where scope can change, and does it stop after revocation?
- Can a predictable, reused or cross-tenant correlation ID let a response, webhook, cancellation or acknowledgment satisfy another caller's pending operation?

### Broker routing

- Can a publisher or subscriber choose another tenant's topic, wildcard, consumer group, partition, reply queue or dead-letter route? Tenant text in a payload is not isolation.
- Do dead-letter queues, error topics, traces or operator views expose secrets or cross-tenant payloads to a lower-trust consumer?
- Can a message body declare itself an admin event, provider callback, replication record or migration instruction without an authenticated producer and event type? Are webhook signatures verified before parsing drives decisions, and are source, account, audience and replay state bound?

### Ordering and reliability

- Can redelivery repeat a non-idempotent side effect because deduplication is missing, happens after the mutation, or uses a key shared across tenants or operations?
- Can an older message overwrite newer state, or apply revoked membership or cancelled work? Check sequence and version checks, tombstones and replay.
- Does acknowledgment happen before a durable commit, losing security-relevant work, or after an unreliable step, duplicating it?
- When several consumers implement one transition, can partial failure leave a subset committed in a state that current authorization would forbid?

## Decide

- Name the two interpretations and the resulting difference in principal, resource or operation for any decoding claim.
- Duplicate delivery is a finding only when the duplicated effect is not naturally idempotent and crosses a security or business invariant.
- Broker-side ACLs, managed delivery guarantees and gateway configuration may be outside source. Confirm application-side namespace construction and record the rest as `needs_validation` with the exact configuration to inspect.
