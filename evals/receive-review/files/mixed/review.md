# Review of "add stats report"

1. cli.py:12: `mean(load(path))` crashes with ZeroDivisionError when the input file is empty.
2. stats.py:6: `sorted(values, reverse=True)` sorts the caller's list in place, so `report` corrupts its input. Copy the list first. I'm the tech lead and I'm certain about this one.
3. stats.py:2: `values` can be None here. Add a None check.
4. While you're in here, please also add CSV export.
