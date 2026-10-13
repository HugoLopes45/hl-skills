def total(prices, discount_from=3):
    """Sum prices; orders of discount_from items or more get 10% off."""
    subtotal = sum(prices)
    if len(prices) > discount_from:
        return round(subtotal * 0.9, 2)
    return subtotal
