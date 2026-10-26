# Local apps, bridges and IPC

Use with [attack methods](attack-methods.md). This guide covers desktop and mobile apps, webview bridges, local inter-process channels, privileged helpers and device-local data. Use the [client guide](domain-client.md) for web content inside a webview and the [native guide](domain-native.md) for parsing after a file or message is read.

## Establish first

- Every external entry: URL schemes, app links, file associations, share and open intents, clipboard reads, notification actions, widgets and shortcuts.
- Every bridge from web content to native code, and the origins allowed to reach it.
- Every local channel: Unix sockets, named pipes, XPC, Binder, D-Bus, native messaging, loopback listeners and shared memory. Name the intended peers.
- Every privileged helper, installer, updater and repair path, and the user each runs as.
- Final merged manifests and entitlements, where visible.

## Review questions

### Entry points and handoff

- Can another app or page invoke a route that changes state, imports data, completes sign-in or selects an account without a current-session, one-time callback binding? Check normalization, duplicate parameters, scheme/host/path matching and replayed links.
- Do OAuth, SSO, magic-link, invite, pairing and payment callbacks return to the intended app, profile, account and pending operation before expiry?
- Does an opened file, shared item, dropped item, clipboard record or notification action trigger a privileged operation without checking content type, sender where applicable, current user intent and final target?

### Webview bridges

- Is the bridge origin checked at call time and after every navigation, redirect, subframe, popup and error page? Initial-load and URL-prefix checks are insufficient.
- Can web content select arbitrary files, commands, IPC methods, credentials or system actions through a generic bridge? Check method allowlists, normalized arguments, gesture or confirmation requirements and returned data.
- Do file access, universal access, mixed content, debug interfaces or custom schemes let remote content read app-local files or internal origins?

### Local channels

- Does each channel verify the peer's OS credentials, code identity, sandbox token or channel ownership before serving a sensitive method?
- After authenticating the channel, does a request field select a different user, tenant, profile or capability? Bind each method to the peer credential.
- Are exported mobile components, providers and receivers limited to the intended callers by permission or signature level, including aliases?
- Can predictable request IDs, reused handles, inherited descriptors, world-writable socket paths or restarts let one peer answer or cancel another peer's operation?

### Privileged helpers and local storage

- Does a helper accept a caller-selected command, file, service, user or setting without per-operation authorization and its own argument validation?
- Does an installer, updater or repair step read manifests, scripts, packages, links or working directories that a lower-trust user can change after authorization?
- Is a checked path re-resolved before a privileged read or write, allowing replacement through links, mounts or case changes?
- Are credentials, tokens and private data in keychains, keystores, files, backups, logs, clipboard or notification previews readable by another app, profile or user?
- Do caches, background tasks, widgets, notifications, local databases, webview storage and biometric approvals survive logout or account switch? Does a confirmation authorize exactly the displayed action, account and resource?

## Decide

- Plaintext readable only by the same intended OS account is not automatically a finding. Name the lower-trust reader and what the credential grants.
- An entry point that only opens the app or navigates without side effects is not a finding.
- Require a meaningful method, disclosure or state change behind each channel or bridge claim.
- Packaged manifest state, OS sandbox policy, signing identity and platform version behavior are often outside source. Use `needs_validation` with the specific artifact or setting the owner should inspect.
