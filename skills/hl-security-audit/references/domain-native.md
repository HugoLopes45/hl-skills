# Native memory, binaries and ABI

Use with [attack methods](attack-methods.md). This guide covers unmanaged memory, binary formats, foreign-function boundaries, loaders, generated code and kernel or driver interfaces. Use the [local apps guide](domain-local.md) for file and IPC authority, and the [supply-chain guide](domain-supply-chain.md) for artifact authenticity before it reaches the machine.

## Establish first

- Which bytes and lengths an attacker controls, and the first code that reads them.
- Each buffer's owner, allocation size, unit and lifetime, and every path that frees or reallocates it: success, error, cancellation, close and shutdown.
- Each language or ABI boundary: `extern`, FFI, CGo, JNI, Python/Node native modules, generated wrappers and callbacks.
- Concurrency: which threads, callbacks, signal handlers and timers can touch the same object, and which lock or atomic protects it.

## Review questions

### Bounds and arithmetic

- Does every index, offset, length and terminator reach a buffer only after a correct bound against the actual remaining capacity, including headers, padding, alignment and terminators? Are both source and destination checked?
- Can attacker-influenced arithmetic underflow, overflow, truncate or change sign before an allocation, copy, loop or pointer computation? Is the checked representation the one later used?
- Do parse, validation, allocation and copy use the same unit: bytes, elements, code units, pages or wire units?
- Can uninitialized memory, padding or spare capacity cross a trust boundary through output, hashing or serialization?

### Lifetime, type and races

- Can a callback, iterator, borrowed view, queue entry, timer or cached pointer outlive its owner on any error or teardown path? Is each object freed exactly once?
- Is a tag, union discriminator or object kind checked differently from the representation later read? Can reuse leave a stale tag?
- Are reference counts and ownership transitions atomic where shared? Does a check under one lock protect a use made without it?
- Can concurrent work invalidate a bound, policy or pointer established earlier? Is lock order consistent, and are locks released before callbacks and blocking I/O?

### Foreign boundaries

- Do both sides agree on who allocates, frees, pins and mutates a buffer, how long a pointer stays valid, and whether a length counts bytes or elements? Check null, zero length, aliasing and retained callbacks.
- Do struct layout, packing, alignment, endianness, enum width, integer width and calling convention match on every supported architecture and build configuration?
- Can a panic or exception unwind across an ABI that forbids it, or a callback run on the wrong thread or after teardown?

### Loaders, generated code and privileged interfaces

- Does a privileged process load a library, plugin or helper from a location a lower-trust principal can write, or search a bare name through a controllable directory or environment?
- Is the file that was verified the same file that is mapped, including path replacement and architecture slices?
- Are offsets, counts, sections and relocations range-checked and overlap-checked before use?
- Do validator, interpreter, optimizer and generated code agree on types, bounds and side effects?
- Do module unload and runtime reset leave live function pointers, threads or views?
- Does a syscall, ioctl or driver read user memory twice and trust the first read? Does a device node, admin socket or helper check the caller's authority over the named resource, not just the request shape?

## Decide

- A crash is not code execution, and a safely rejected malformed input is not memory corruption. State the established effect: out-of-bounds read or write, use of freed memory, wrong-type access, disclosure or shared-process termination.
- A bounds check using the same wrong unit as the allocation still fails. Cite both the check and the consuming operation.
- A user loading their own plugin into their own process is not a privilege boundary.
- A source-established invariant violation can be confirmed without execution if every condition is visible. Mark the evidence source-only.
- Use `needs_validation` when the claim depends on an opaque foreign implementation, compiler or allocator behavior, a specific interleaving that source cannot fix, deployed sandbox or device permissions, or architecture-specific layout not visible in source. Name the sanitizer, fixture or schedule an authorized reproduction would need.
