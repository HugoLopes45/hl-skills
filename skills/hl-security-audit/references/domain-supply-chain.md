# Supply chain and release authority

Use with [attack methods](attack-methods.md). This guide covers every trust handoff from source and dependencies to the artifact a user runs. Use the [native guide](domain-native.md) for local loader parsing and the [cloud guide](domain-cloud.md) for the runtime authority of a deployed workload.

## Establish first

Walk backward from each released artifact or installed update to every source, dependency, generated input, credential, runner, cache, test result and approval that shaped it. For each, name who can write it and whether the next step verifies its exact identity.

## Review questions

### Dependencies and build inputs

- Can resolver configuration select an unintended namespace, fallback registry, mirror or source URL? Check package names, source priority, lockfile and checksum use, alternate build files and platform-specific resolution.
- Do builds consume moving references: branches, tags, unpinned submodules, downloaded tools, remote includes, floating CI actions or container tags? Which lower-trust party can change them?
- Do schemas, vendored archives, generated clients or binary blobs ship without the same review and integrity check as source?
- Can the build context include secrets, local configuration, repository metadata or developer artifacts in a published package or image? A secret passed as a build argument or deleted in a later layer stays in the image.

### CI and automation

- Does an external pull request, fork, comment or automated update run contributor-controlled code with secrets, write tokens, deployment authority or a trusted runner? Compare trigger, checkout ref, approval gate, environment protection and token permissions. Do not assume host defaults absent from source.
- Do branch names, commit messages, issue fields, artifact names or matrix values enter shell commands, template expressions or paths without validation?
- Can a lower-trust job populate a cache, artifact or workspace that a higher-trust job restores, executes or releases? Are cache keys namespaced and artifacts bound to producer and digest?
- Can untrusted job input choose the resource that an over-privileged automation identity acts on?

### Release and update

- Do test, review, signing and publication refer to the same immutable digest, or to mutable tags, filenames, channels or IDs? Check every copy, repack and architecture merge.
- Does the consumer check that a signature or attestation came from the intended workflow, repository, branch, environment and key role, not only that it is valid? Do rotation, expiry and revocation fail closed?
- Does an updater authenticate version, product, platform, channel, target path, expiry and rollback state with the payload, and install atomically?
- Can a plugin or extension gain more host authority than declared, replace another publisher's identity, or run install hooks before authenticity and capability checks?

## Decide

- Name the lower-trust actor, the input they control, the trusted consumer and the resulting unauthorized publication, code inclusion, secret disclosure or privileged execution.
- Least-privilege gaps alone are hardening. Require a reachable privileged action.
- Reproducible builds do not prove authenticity. A signature call without policy binding is incomplete.
- Installing arbitrary plugins of the same user into their own app is not a privilege boundary.
- Registry ownership, repository host settings, protected environments and signing-key custody are often outside source. Record them as `needs_validation` with the setting the owner should inspect.
- An advisory match for a dependency is a lead. Confirm the version that actually resolves, from a lockfile or vendored copy rather than a manifest range, the function, feature or configuration the advisory names, and a call path that passes attacker-reachable input to it. Without a lockfile, or for packages a base image, runtime or platform supplies, the resolved version is an external fact, and a distribution backport can patch a version the advisory lists.
