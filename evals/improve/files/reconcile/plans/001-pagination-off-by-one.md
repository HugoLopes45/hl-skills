# 001: Fix the pagination off-by-one

**Commit:** 0000000
**Status:** DONE

## Steps
1. In `shop/pagination.py`, return `items[start:start + size]`.
2. Add `test_last_item` to `tests/test_pagination.py`: `page(list(range(10)), 0, 5)[-1] == 4`.

## Done criteria
- [ ] `python3 -m pytest -q tests/test_pagination.py::test_last_item` exits 0
