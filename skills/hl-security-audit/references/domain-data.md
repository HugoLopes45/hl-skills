# Data isolation and lifecycle

Use with [attack methods](attack-methods.md). This guide covers whether each copy of data stays bound to its owner and current permissions through storage, derivation, movement and deletion. The ownership method in attack methods covers single-request checks; this guide follows the data afterward.

## Establish first

- The isolation key for each data class: owner, tenant, workspace or environment, and where the authenticated value comes from.
- Every store holding a copy: primary tables, object storage, caches, search and vector indexes, thumbnails and previews, analytics, logs, traces, exports, backups and replicas.
- Each lifecycle event that should change access: membership removal, role downgrade, sharing change, consent withdrawal, deletion, restore and migration. Name the code that propagates it to every copy.

## Review questions

### Partitioning

- Does each read, update, delete, list, count and bulk query bind the object to the authenticated tenant or owner? Compare direct, nested-relation, background, admin, import and legacy paths. Can a body field supply the tenant?
- Do cache keys, object paths, uniqueness constraints, search document IDs, temporary files and deduplication keys include the tenant or environment?
- Do row-level policy, ORM default scopes and authorization filters apply the same predicate as raw queries, service clients, joins, aggregates, views and `unscoped` paths? What happens when tenant context is missing?
- Do attachment IDs, version IDs, shared links and signed URLs bind operation, exact object and version, audience, expiry and tenant? Do they stop working when the ACL changes?

### Derived copies and alternate readers

- When a primary record's ACL or lifecycle changes, are cached, indexed, embedded, preview and feed copies invalidated or filtered at retrieval time?
- Do logs, metrics, traces, analytics and diagnostics receive private content or credentials, and can a broader or longer-retention reader access them?
- Can counts, filters, sort order, errors, uniqueness conflicts or notifications reveal a concrete protected predicate about another principal's data?

### Movement

- Does an export, report, snapshot or backup authorize each item after selection, and authorize the download of the finished artifact?
- Does import or restore treat archive contents as untrusted, re-check owner, schema, ACL and uniqueness, and refuse to write into a tenant the requester cannot write?
- Do migrations, backfills, dual reads and rollbacks give old records a safe default owner and ACL? Can incompatible identifiers collide?
- Do backup keys, replicas, restore environments and support snapshots carry broader access than the primary data?

### Deletion and revocation

- Do direct lookup, search, relation traversal, links, background jobs and restore all honor soft-delete and revocation predicates? Can a deleted identifier be reused while references remain?
- After membership or role removal, do sessions, caches, subscriptions, scheduled jobs and materialized data stop authorizing access?
- Do queued work, retries, exports and generated artifacts recreate or retain deleted data beyond the promised boundary?
- Does undo, undelete or replica recovery restore memberships, credentials or permissions that current policy no longer allows?

## Decide

- A tenant field on a record is not enforcement. Cite the query, key or check that applies or omits the predicate on the specific path.
- An oracle needs a concrete confidential predicate and an observable difference. General response variance is not enough.
- Operator-only access under the intended policy and public identifiers in logs are not disclosure findings.
- Hosted retention, replica access and backup storage policy are often outside source. Confirm in-repo policy and record hosted behavior as `needs_validation` with the owner-observable check.
