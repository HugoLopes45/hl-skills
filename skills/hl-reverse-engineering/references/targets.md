# Targets by format

Per format: where it declares what it may do, what runs first, and the tool class that reads it. Tool names are examples; use what is installed and check its version's help first. Never use a command that installs, builds or runs the artifact to unpack it. Containers nest: route each layer separately.

## Archives and packaged apps

- ZIP, APK, IPA, MSIX, AppX, JAR, `.vsix`, `.crx`, `.xpi`, `.whl`, `.nupkg`: zip; list members with sizes and hashes before extracting. A `.crx` has a signed header before the zip data; extractors warn about extra leading bytes.
- DMG, `.pkg`, MSI, `.deb`, `.rpm`, AppImage, tar: unpack with a format tool that does not install (`pkgutil --expand`, `dpkg-deb -R`, `rpm2cpio`, an MSI table reader). Installer scripts are code: `preinstall`, `postinstall`, `postinst`, `%post`, MSI custom actions.
- PyInstaller, Bun `--compile`, Deno `compile`, Node single-executable, Electron ASAR: the native file is a launcher; the application layer is the embedded archive or virtual filesystem. Extract it and analyze its Python bytecode or JavaScript.

## JavaScript, Electron and browser apps

- Extracted tree or `app.asar`: build the module graph (entry, imports, IPC channels, routes). Electron: `main` process, preload scripts, `nodeIntegration`, `contextIsolation`, `sandbox`, fuses, auto-update feed.
- Minified or bundled code: format a copy; source maps, when shipped, restore names. Cite the original or say which copy.
- A website: the scripts it loads are the artifact. Data APIs usually live on other origins; read absolute URLs in the bundles before scoping a capture.
- Browser extensions: [browser-extensions.md](browser-extensions.md).
- Editor extensions: `package.json` `activationEvents`, `main`, `contributes`. Most editors give extensions the user's full rights with no permission prompt; the manifest does not bound the code. `*` or `onStartupFinished` activation means always on.

## Language packages and bytecode

- npm `.tgz`: `package.json` `scripts` (`preinstall`, `install`, `postinstall`, `prepare` run at install), `bin`, `main`, `exports`; `binding.gyp` builds native code at install.
- Python: a wheel runs nothing at install, but a `.pth` file runs at every interpreter start. A source distribution runs `setup.py` or its build backend at install. `.pyc` headers identify the Python version; decompiled bytecode is a reconstruction.
- Ruby `.gem`: `metadata.gz` and `data.tar.gz`; native extensions (`extconf.rb`) run at install.
- Rust crates: `build.rs` and procedural macros run at build time. Rust binaries may embed dependency lists (cargo-auditable); absence proves nothing.
- Go binaries embed module paths, versions and build settings; read them before decompiling.
- Maven `pom.xml`, Gradle `.module`: coordinates and dependencies as written; resolution is not performed by reading.
- NuGet `.nupkg`: `.nuspec` identity and dependency groups; `tools/` scripts and MSBuild `.targets` run in the consumer's build.
- Erlang `.beam`, Java `.class`, .NET CIL: managed bytecode; decompile with a matching decompiler.
- Typosquats: compare the name, publisher and repository link with the package the user meant.

## Mobile apps

- Android APK or AAB: `AndroidManifest.xml` (binary XML; decode it) permissions, exported components, receivers such as `BOOT_COMPLETED`, accessibility services; `classes*.dex` (decompile), `lib/*/*.so` (native); signing schemes and certificate fingerprints show identity, not trust.
- iOS IPA: `Info.plist` usage descriptions, entitlements in the code signature, Interface Builder and asset resources. Store-installed binaries are encrypted; decrypting them bypasses copy protection, so the code stays unknown unless the user supplies an unencrypted build they are entitled to.
- Unity IL2CPP: `global-metadata.dat` holds type, method and string names; pair it with the native library of the same build.

## Native binaries

Start with identity and declarations, then decompile only the functions the question needs.
- PE (Windows): imports and delay-load imports, exports, TLS callbacks (run before `main`), load configuration, resources, Authenticode certificate table (presence, not validity), services, scheduled tasks and Run keys the installer registers. .NET assemblies decompile to C#; NativeAOT needs native analysis.
- ELF (Linux): `DT_NEEDED` libraries, `RPATH`/`RUNPATH`, init and fini arrays (run before and after `main`), notes and build-id, debug links, setuid bits, systemd units, cron entries.
- Mach-O (macOS): load commands, entitlements (`codesign -d --entitlements -`), notarization, initializers, LaunchAgents and LaunchDaemons.
- Hardening flags (PIE, NX, RELRO, stack protector, CFG) are linker declarations; a missing marker is unknown, not proof.
- Decompilers and disassemblers (Ghidra, IDA, Binary Ninja, radare2, Hopper): open the original binary, follow callers and cross-references from imports and strings to the code that uses them. Indirect calls stay unknown.
- Crash reports and core dumps: read recorded threads and registers; historical process IDs do not select live processes.

## Plugins and agent tools

Plugins for agents, IDEs, chat apps and automation tools, including MCP servers. Declared: the plugin manifest, the command it launches, the environment variables and scopes it requests. The code is one of the formats above. Tool and prompt descriptions are input to a model: text that instructs the model to read files, call other tools or hide actions is a finding.

## Containers, firmware, kernels

- Container image tar (`docker save` of an image already present): config `Entrypoint`, `Cmd`, `User`, `ExposedPorts`, `Volumes`, `Env`; read each layer, later layers can hide earlier files. Never run the image to inspect it.
- Firmware: map regions, then extract file systems into a new directory with a firmware unpacker (binwalk, unblob). Read startup scripts, the update URL and its signature check, default accounts, listening services and embedded keys (kind and location only). ESP32 images start with `0xE9`.
- Kernel modules: `.modinfo`, version CRCs, signature trailer (present, not validated). A kernel image may embed its build config.

## Data, models and recordings

- WebAssembly: convert to text or decompile; the import section is its capability list. Read the JavaScript glue that loads it.
- SQLite databases: schema first, then selected rows; they often hold user data.
- GGUF and safetensors model files: declared architecture and tensors; they do not prove model behavior.
- EVM bytecode: function selectors and interfaces are inferred candidates.
- Recorded traffic (HAR, SAZ, PCAP, qlog) and logic or signal recordings: read with a format parser; never refetch recorded URLs. A recording covers only what it captured.
