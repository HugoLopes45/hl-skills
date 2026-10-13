from datetime import datetime


def parse_date(text):
    return datetime.strptime(text.strip(), "%d/%m/%Y").date()
