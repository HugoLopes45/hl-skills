def total(items):
    return sum(item["price"] for item in items)


def apply_discount(price, pct):
    return price * (1 - pct / 100)
