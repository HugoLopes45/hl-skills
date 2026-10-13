# 002: Parameterize the user query

**Commit:** 0000000
**Status:** TODO

## Current state
`shop/db.py:8-9`:
```python
def find_user(conn, name):
    return conn.execute(f"SELECT id, email FROM users WHERE name = '{name}'").fetchall()
```

## Steps
1. Replace the f-string with `conn.execute("SELECT id, email FROM users WHERE name = ?", (name,))`.

## Done criteria
- [ ] `grep -n "f\"SELECT" shop/db.py` prints nothing
