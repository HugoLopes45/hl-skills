from support.db import get_db


def lookup_order(order_id: int) -> dict:
    row = get_db().execute(
        "SELECT id, customer_id, status, amount_cents, shipping_address FROM orders WHERE id = %s",
        (order_id,),
    ).fetchone()
    return row._asdict() if row else {"error": "not found"}


def issue_refund(order_id: int, amount_cents: int) -> dict:
    db = get_db()
    db.execute("UPDATE orders SET status = 'refunded' WHERE id = %s", (order_id,))
    db.execute(
        "UPDATE customers SET credit_cents = credit_cents + %s"
        " WHERE id = (SELECT customer_id FROM orders WHERE id = %s)",
        (amount_cents, order_id),
    )
    db.commit()
    return {"ok": True}


def change_email(customer_id: int, email: str) -> dict:
    db = get_db()
    db.execute("UPDATE customers SET email = %s WHERE id = %s", (email, customer_id))
    db.commit()
    return {"ok": True}
