# Data-model lens

Separate concerns that are braided together, and model the domain as plain data plus functions on it. Use the domain's real entity names, never placeholder names.

## Principles

- Simple is not easy. Easy means familiar or near at hand. Simple means one concern, not braided with another.
- To braid (complect) is to tie two concerns together so that you cannot change one without the other. Typical pairs: identity and value, data and schema, transport and encoding, configuration and code, what and when.
- First question for any abstraction: what is it, in terms of data? A user who cannot answer that does not understand it yet.
- A place (variable, row, slot) holds different values over time. A value never changes. Confusing the two causes many bugs.
- Plain data structures (map, list, set) and functions on them outlast custom class hierarchies. Data is the interface.
- Do not hide information behind getters or wrap it in objects without a reason; pass the data.

## Modes

### `untangle` (default)

1. **What is it**: describe the data, not the behavior; retain constraints that affect the model.
2. **Braided pairs**: one pair per line, with where they meet (`file:line`).
3. **Cost**: per pair, what becomes hard (testing, replacing, reasoning, retrying, caching).
4. **Separation plan**: per pair, the smallest separation (a value type, schema at the boundary, a pure function split from its side effect).
5. **Verdict**: `simple` / `braided at <list>` / `rewrite`.

### `simplify`

For a tower of factories, builders, managers, or services: could this be a map, or a function on a map? Could the variation live in data instead of in the type hierarchy? Report what to delete, what to keep (the data shape and its functions), and the simpler shape as data types and function signatures. No implementation; the user writes it.

### `model`

Fill a table: element, value or place, what changes over time, who owns the change. Then name the value objects (immutable, compared by content), the identities (places that hold values over time), and the processes (functions from old value to new value).

## Stand down

Small scripts where the data has one shape and one consumer.
