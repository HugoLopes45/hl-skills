# Cloud and deployment boundaries

Use with [attack methods](attack-methods.md). This guide covers the authority a deployed workload holds and how deployment configuration exposes it. Cloud IAM and application authorization are separate checks; review both. Use the [supply-chain guide](domain-supply-chain.md) for how artifacts reach deployment.

## Establish first

- Each workload's identity and attached policy: service accounts, roles, federation trust and fallback credentials.
- Every maintained deployment: base configuration plus each environment overlay, chart value, flag and feature gate. Review the final effective configuration, not only the base file.
- Network exposure: ingress, listeners, binds, port mappings, load balancers, security groups and mesh policy.
- Event sources and the envelope fields each consumer trusts.

Record anything the repository cannot show, such as account-level policy, values injected at deploy time, live network rules or drift from the code, as an external fact.

## Review questions

### Identity and authority

- Can request or job input select a tenant, account, bucket or resource that the workload identity can reach but the requester should not?
- Do role assumption, token exchange and workload federation bind the claim to the intended source account, audience, repository, branch or namespace?
- Does the application trust caller-supplied identity headers, tags, labels or account IDs without proof that they came from the control plane or a trusted proxy?
- Can an identity that lower-trust input drives gain authority indirectly: edit or attach its own policy, create credentials for another identity, pass a stronger role to new compute, or bind, escalate or impersonate through cluster RBAC? In a resource policy, a wildcard principal is limited only by its conditions.

### Network reachability

- Does a repository-controlled route, service or bind expose an admin, debug, metrics or internal API to a lower-trust network?
- Does a backend accept forwarded identity or mTLS subject headers from peers outside the intended ingress or sidecar? Does an alternate port, health path or legacy route skip the mesh? What happens when the proxy is absent?
- Can a controllable URL or destination reach instance metadata, control-plane sockets or internal APIs while the workload holds credentials?

### Runtime and orchestration

- Can a lower-trust workload or tenant select privileged mode, host namespaces, host paths, device mounts, runtime sockets or mounted service tokens?
- Does every deployment route apply the same image, namespace, secret and privilege policy, including upgrade, restore, job and compatibility controllers?
- Do network, admission or identity policies match on labels, annotations or names that a less-trusted principal can set?

### Configuration and secrets

- Do overlays, defaults or flags disable authentication, transport security, tenant scoping or audit in a maintained environment?
- Can secrets reach logs, crash reports, process arguments, shared environment, broad volumes, build output, IaC state or plan output, or read APIs visible to another workload or tenant? Confirm secret type and authority without retrieving the value.
- Does failure to mount, refresh or revoke a credential keep a stale one active or fall back to a weaker identity mode?

### Storage, events and edge runtimes

- Do bucket policies, object keys, CDN origins or signed URLs bind principal, operation, namespace, audience and expiry, including list, version and write operations?
- Does a function trust event body fields as source identity instead of the provider-signed envelope, subscription, account, region and replay state? Compare push, pull, retry and dead-letter paths.
- Does an edge or serverless runtime assume a secret, isolation or tenant policy that differs from the origin, and does fallback change authority or caching?

## Decide

- Missing least privilege, absent seccomp or a writable root filesystem alone is hardening. Require a reachable operation that crosses a tenant, account, node or control-plane boundary.
- A repository-controlled public route to a sensitive handler can be confirmed from source. Missing network controls whose deployment is not visible stay `needs_validation`.
- A public endpoint, key identifier or non-secret configuration value is not a credential disclosure.
- Name the final effective configuration that produces the issue, not only the file where a value appears.
- Account-level policy, live firewall rules, metadata-service version and managed-service defaults are owner-observable facts. Give the exact read-only check the owner can run.
