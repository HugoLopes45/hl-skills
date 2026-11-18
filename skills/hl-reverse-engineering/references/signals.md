# Signals

Starting points, not a checklist. A hit is a lead until traced to what it reads and where the value goes. In compiled code, search strings and imported functions first, then follow cross-references from each hit to its callers.

## Reads user data

```text
password  passwd  token  secret  api_key  Authorization  Cookie  session
.ssh  .aws  .kube  .npmrc  .netrc  .git-credentials  id_rsa  keychain
Login Data  Cookies  Local State  logins.json  key4.db  wallet
getenv  os.environ  process.env  ENV[  System.getenv
clipboard  pasteboard  GetClipboardData  keylogger hooks: SetWindowsHookEx  CGEventTap
screenshot  ScreenCapture  AccessibilityService  READ_SMS  ACCESS_FINE_LOCATION
```

## Sends data out

```text
fetch(  XMLHttpRequest  sendBeacon  WebSocket  requests.  urllib  http.client
HttpClient  URLSession  OkHttp  curl_easy  WinHttp  InternetOpen  socket(  connect(
dns lookups built from data   webhooks: discord.com/api/webhooks  api.telegram.org
pastebin  ngrok  raw IP addresses  hosts assembled from fragments
```

Base64, hex, XOR, compression or encryption applied to collected data right before a send usually hides what is sent.

## Runs code it did not ship

```text
eval(  new Function(  exec(  compile(  importlib  __import__  require(variable)
dlopen  LoadLibrary  System.loadLibrary  Assembly.Load  DexClassLoader  ClassLoader
child_process  subprocess  os.system  ShellExecute  CreateProcess  posix_spawn
powershell -enc  bash -c  curl ... | sh  certutil -urlcache  mshta  rundll32
```

A downloaded file that is then made executable or loaded is remote code, even when the download looks like data.

## Stays and hides

```text
LaunchAgents  LaunchDaemons  systemd  crontab  Run\  RunOnce  schtasks  services
BOOT_COMPLETED  device admin  hidden launcher icon
sleep before acting  sandbox or debugger checks  locale or time-zone checks  CI checks
```

Delays and environment checks before a behavior mean it tries to avoid analysis; note them and the condition that releases the behavior.

## Obfuscation

Packed or encrypted sections, high-entropy blobs, strings decoded at runtime, control flow flattening, and names reduced to single letters in code that was not minified for size. Obfuscation is not proof of harm, but it moves everything it covers to unknown until decoded.

## Control and ownership

- An update source outside the official store or registry bypasses its review.
- Changed signer, publisher, maintainer, privacy policy domain or analytics host between versions suggests a sale.
- New obfuscated files, new hosts, new install hooks or a first remote configuration fetch in a minor version are the usual post-sale changes.
