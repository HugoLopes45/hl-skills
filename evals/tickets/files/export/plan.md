# Order export

Users download their orders as CSV from the orders page.

## Acceptance criteria

| Id | Actor | Input | Observable result | Verification |
|---|---|---|---|---|
| AC-1 | User | Clicks Export with orders | Downloads `orders.csv` with a header row and one row per order | `pytest tests/test_export.py` |
| AC-2 | User | Clicks Export with no orders | Downloads `orders.csv` with the header row only | `pytest tests/test_export.py` |
| AC-3 | Admin | Opens the exported file | The export looks professional | |
