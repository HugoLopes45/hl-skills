import re


def slugify(text):
    return re.sub(r"\s+", "-", text.strip().lower())
