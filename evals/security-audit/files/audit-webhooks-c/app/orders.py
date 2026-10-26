from app.db import get_db


def mark_paid(order_id: int, amount_cents: int) -> None:
    db = get_db()
    db.execute(
        "UPDATE orders SET status = 'paid' WHERE id = %s AND status = 'pending' AND amount_cents = %s",
        (order_id, amount_cents),
    )
    db.commit()
