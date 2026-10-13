from pricing import total_cents
from store import save_order


def create_order(user_id, items):
    total = total_cents(items)
    order_id = save_order(user_id, items, total)
    return {"id": order_id, "total": total}
