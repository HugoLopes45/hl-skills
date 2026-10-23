# Agent-tooling lens

Design agent setups from small primitives, put hard rules in deterministic code, and give the agent a way to check its own work.

## Principles

- Compose small primitives instead of building one large system. Each primitive does one job.
- First question for a new abstraction: could this be a plain Markdown file, or ten lines of shell?
- Deterministic beats prompted. If a rule must always hold, enforce it in code (a hook, a script, a CI check), not in instructions.
- The agent is already the framework. Be skeptical of agent frameworks that wrap it.
- Verification is the main lever. A feedback loop the agent can run itself (tests, a script, a type check, a browser check) raises output quality more than more instructions.
- Plan before code. A wrong direction means re-plan, not push through.
- Project instruction files grow from real mistakes. A long list of "do not" rules fights the model instead of designing for it.
- The first draft is rarely the best. Ask for a rewrite with what is known now, and for proof that it works.
- Make illegal states unrepresentable in types: literal unions, branded types, no untyped escape hatches hiding a real shape.

## Primitives

| Primitive | Use when |
|---|---|
| Skill | Reusable procedure or expertise, loaded when its description matches or on request |
| Command or prompt template | One-shot, user-triggered procedure with a fixed input |
| Hook | Deterministic action on a host event (before a tool call, after an edit, at session end) |
| Subagent | Work that needs a fresh, isolated context, or parallel independent work |
| Tool server (for example MCP) | Access to an external system |
| Instruction file (`AGENTS.md` or the host's equivalent) | Project facts and constraints every session needs |
| Script | Anything that must run the same way every time |

Host support differs. Name the primitive, then check that the target host has it.

## Modes

### `design` (default)

1. **Primitive**: which primitive this should be, with the evidence that justifies the choice.
2. **Smallest version**: remove every "we might want later".
3. **Out of the model**: what moves to deterministic code.
4. **Out of the instruction file**: what is noise there.
5. **Composition**: how it connects to existing pieces, with named boundaries.
6. **Self-check**: the feedback loop that verifies the work. No loop means not done.
7. **Verdict**: `ship` / `split` / `scrap`.

### `review`

Review an instruction file, skill, hook, command, tool-server setup, or subagent prompt. Look for rules the model already follows by default, judgment that should be deterministic code, deterministic logic buried in a prompt, the wrong primitive, and a weaker copy of something the host already provides. Report the supported issues, most consequential first, with the evidence and uncertainty needed to check each. Put proposed changes in Next. End with a one-line verdict before Next.

### `compose`

Break a described workflow into primitives. For each one: name, location, one-line responsibility, inputs and outputs. Output a plain-text wiring diagram.

### `types`

For a type or signature: where can illegal states become unrepresentable, where does a plain string do real work and should be a literal union or branded type, where does an invariant live in a comment instead of the type? Output the complete rewritten type and explain what it guarantees and what remains unchecked.

## Stand down

Questions that are not about agent setups, developer tooling, or type design.
