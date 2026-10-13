import db


def set_sale_price(sku, cents):
    """Called by the nightly promotions job and by the admin UI."""
    db.execute("UPDATE prices SET price_cents = ? WHERE sku = ?", cents, sku)
