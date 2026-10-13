import csv
import os


def read_events(path):
    """Yield events from a CSV export; a missing export means no events yet."""
    if not os.path.exists(path):
        return
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            yield {"user": row["user"], "action": row["action"]}
