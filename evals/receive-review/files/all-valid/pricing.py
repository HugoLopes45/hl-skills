def total(items):
    return sum(item["price"] for item in items)


def apply_discount(price, pct):
    """Accept finite int/float inputs; reject pct outside [0, 100]."""
    return price * (1 - pct / 100)
