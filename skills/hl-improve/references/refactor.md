# Refactor Plan

Input: `refactor [target and transformation, or brief path]`

Plan the input, or the latest refactor discussion. Missing concrete target: stop and ask for it, as in this reply, with no example transformation:

```markdown
**I need the file or symbol to change before I can plan the refactor.**
Verdict: Stopped

**Next:**
1. Send the file or symbol and the change you want. (default)
2. Run `arch` first to find candidates.
```

No edits or scope expansion.

Identify target symbols, desired structure, and observable behavior to preserve. Locate tests, type contracts, or concrete manual checks supporting preservation. Missing coverage becomes a proposed characterization step or an explicit unresolved risk; tests are evidence, not a preservation guarantee.

Prefer removing unnecessary structure or reusing an existing capability over adding an abstraction. Preserve edge cases and safety checks; a shorter expression is not automatically simpler.

Sequence bounded transformations such as Extract, Inline, Move, Rename, or Replace. For each, name touched paths and symbols, preserved behavior, verification command, risk, and rollback limited to that step. Keep intermediate states coherent; combine steps that cannot stand alone.

Find every reference before a public move or rename. For generated code, change the source or generator, not the output. For a cross-language interface, change the contract and every consumer in one step. Order steps by dependency, not by a fixed sequence or by language.

Report the target shape first, as a `diff` view of the structure that changes (file tree, call tree, types, or code), under the first numbered point. Then the numbered sequence with safe stopping points marked, the final rerun of original checks, and exclusions as numbered points. Separate any requested behavior change from the structural plan. Over ten steps: group them into phases that each end at a safe stopping point; never truncate.
