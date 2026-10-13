# 003: Stop swallowing render errors

**Commit:** 0000000
**Status:** BLOCKED: waiting for a decision on the error format

## Steps
1. In `shop/report.py`, replace `except Exception: pass` with an error that names the row.
