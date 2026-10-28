from ledger_client import LedgerClient

from app import notifications

ledger = LedgerClient.from_env()


def refund_order(db, customer_id: int, order_id: int):
    order = db.execute(
        "SELECT customer_id, amount_cents, status FROM orders WHERE id = %s",
        (order_id,),
    ).fetchone()
    if order is None or order.customer_id != customer_id:
        return {"error": "not found"}, 404
    if order.status != "paid":
        return {"error": "order is not refundable"}, 409
    if not ledger.acquire(f"refund:{order_id}"):
        return {"error": "refund already processed"}, 409
    db.execute(
        "UPDATE customers SET credit_cents = credit_cents + %s WHERE id = %s",
        (order.amount_cents, customer_id),
    )
    notifications.send_refund_receipt(customer_id, order_id, order.amount_cents)
    db.execute("UPDATE orders SET status = 'refunded' WHERE id = %s", (order_id,))
    db.commit()
    return {"credited_cents": order.amount_cents}, 200
