from app.report import monthly


def export_pdf(path):
    lines = [f"{month}: {total:.2f}" for month, total in sorted(monthly().items())]
    with open(path, "w") as f:
        f.write("\n".join(lines))
