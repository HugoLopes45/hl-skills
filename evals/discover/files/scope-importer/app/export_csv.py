import csv

from app.report import monthly


def export_csv(path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        for month, total in sorted(monthly().items()):
            writer.writerow([month, total])
