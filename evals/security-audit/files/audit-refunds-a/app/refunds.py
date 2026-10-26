from app import notifications


def refund_order(db, customer_id: int, order_id: int):
    order = db.execute(
        "UPDATE orders SET status = 'refunded'"
        " WHERE id = %s AND customer_id = %s AND status = 'paid'"
        " RETURNING amount_cents",
        (order_id, customer_id),
    ).fetchone()
    if order is None:
        db.rollback()
        return {"error": "order is not refundable"}, 409
    db.execute(
        "UPDATE customers SET credit_cents = credit_cents + %s WHERE id = %s",
        (order.amount_cents, customer_id),
    )
    db.commit()
    notifications.send_refund_receipt(customer_id, order_id, order.amount_cents)
    return {"credited_cents": order.amount_cents}, 200
