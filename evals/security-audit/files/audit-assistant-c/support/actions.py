from support.db import get_db


def lookup_order(customer_id: int, order_id: int) -> dict:
    row = get_db().execute(
        "SELECT id, status, amount_cents FROM orders WHERE id = %s AND customer_id = %s",
        (order_id, customer_id),
    ).fetchone()
    return row._asdict() if row else {"error": "not found"}


def request_refund(customer_id: int, order_id: int) -> dict:
    db = get_db()
    row = db.execute(
        "INSERT INTO refund_requests (order_id, customer_id)"
        " SELECT id, customer_id FROM orders WHERE id = %s AND customer_id = %s AND status = 'paid'"
        " ON CONFLICT (order_id) DO NOTHING RETURNING order_id",
        (order_id, customer_id),
    ).fetchone()
    db.commit()
    return {"queued_for_staff_review": row is not None}
