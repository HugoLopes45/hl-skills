# Browser extensions

Chromium browsers expose `chrome.*`; Firefox exposes `browser.*` and also accepts `chrome.*` for most APIs. Coverage and async style differ, so search both namespaces and check the target browser's documentation for a specific API. A hit is a lead until traced to what it reads and where the value goes.

## Manifest fields to read

`manifest_version`, `permissions`, `optional_permissions`, `host_permissions`, `content_scripts[].matches` and `run_at`, `background`, `externally_connectable`, `web_accessible_resources`, `content_security_policy`, `update_url`, and in Firefox `browser_specific_settings`. An `update_url` outside the store's update host means updates bypass store review.

## High-risk permissions

| Permission | What it exposes |
|---|---|
| `<all_urls>`, `*://*/*`, broad `host_permissions` | Read and change every page, including bank and mail pages |
| `cookies` | Session cookies for granted hosts: account takeover without a password |
| `history`, `topSites`, `sessions` | Full browsing history and recently closed tabs |
| `tabs` | URL and title of every tab |
| `webRequest`, `webRequestBlocking` | Every request URL and headers; Manifest V2 blocking mode can modify them |
| `declarativeNetRequest`, `declarativeNetRequestWithHostAccess` | Redirect or rewrite requests, strip security headers |
| `scripting`, `activeTab` with `scripting` | Inject code into pages; `activeTab` limits it to the tab where the user clicked |
| `clipboardRead` | Whatever the user copies, including passwords |
| `nativeMessaging` | Talk to a program on the computer with the user's full rights |
| `management` | List, disable or enable other extensions, including security ones |
| `proxy` | Route all traffic through a chosen server |
| `downloads`, `downloads.open` | Download and open files |
| `debugger` | Full control of a tab through the debugging protocol |
| `identity`, `identity.email` | The signed-in browser account |
| `externally_connectable` with broad `matches` | Lets websites send commands to the extension |

## Content scripts

For each content script: does it match every site or only its own? Follow each hit below to what it reads, what it edits and where the value goes, then follow messages to the background worker and from there to network, storage and native host calls.

```text
input[type=password]  type="password"  .value  FormData  form.submit  "submit"
document.cookie  localStorage  sessionStorage  indexedDB
addEventListener("keydown"|"keyup"|"keypress"|"input"|"change"|"paste"|"copy")
innerHTML  outerHTML  insertAdjacentHTML  document.write  MutationObserver
a.href =  setAttribute("href"  location.href =  location.replace  window.open
runtime.sendMessage  runtime.connect  runtime.sendNativeMessage  runtime.connectNative
```

## Remote code and remote control

```text
scripting.executeScript  tabs.executeScript  world: "MAIN"
createElement("script")  .src = "https://
declarativeNetRequest.updateDynamicRules  updateSessionRules
```

Manifest V3 forbids remotely hosted extension code, but a fetched configuration that selects selectors, URLs, rules or page actions still lets the server change behavior. A `content_security_policy` that allows `unsafe-eval` or remote script hosts widens what can run.

## Money paths

```text
tag=  aff  affiliate  ref=  utm_  clickid  subid  partner
chrome_settings_overrides  search_provider  search_url
```

Look for shopping domain lists paired with link rewriting, ad containers inserted into pages, and search URLs replaced with a partner domain.

## Native messaging host

A `nativeMessaging` extension talks to a program registered by a separate installer through a host manifest in a browser-specific directory. The extension package does not contain that program; without it, its behavior is unknown.
