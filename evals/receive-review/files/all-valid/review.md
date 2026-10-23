# Review of my change

1. `pricing.py:2`: `total()` ignores `qty`, so two units of a 3.00 item count as 3.00. Multiply by `item["qty"]`.
2. `pricing.py:7`: nothing stops a discount above 100%; `apply_discount(10, 150)` returns -5.0. Reject `pct` outside 0..100 and add a test.
3. `test_pricing.py`: `test_total` only uses `qty == 1`, so it cannot catch the quantity bug. Add a case with `qty == 2`.
4. Same as 1: the order total is wrong when someone buys more than one unit.
