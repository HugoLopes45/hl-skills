import db


def get_price(sku):
    return db.query_one("SELECT price_cents FROM prices WHERE sku = ?", sku)
