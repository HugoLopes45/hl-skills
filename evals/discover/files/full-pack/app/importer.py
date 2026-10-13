import csv

from app.store import save_rows


def import_csv(path):
    with open(path, newline="") as f:
        rows = [{"month": r["date"][:7], "amount": float(r["amount"])} for r in csv.DictReader(f)]
    save_rows(rows)
    return len(rows)
