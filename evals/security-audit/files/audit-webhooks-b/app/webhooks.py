import hashlib
import hmac
import json
import os
import time

from flask import Blueprint, abort, request

from app.db import get_db
from app.orders import mark_paid

bp = Blueprint("webhooks", __name__)
SECRET = os.environ["PAYMENTS_WEBHOOK_SECRET"].encode()
TOLERANCE_SECONDS = 300


def verified(body: bytes, timestamp: str | None, signature: str | None) -> bool:
    if not timestamp or not signature or not timestamp.isdigit():
        return False
    if abs(time.time() - int(timestamp)) > TOLERANCE_SECONDS:
        return False
    expected = hmac.new(SECRET, timestamp.encode() + b"." + body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def first_delivery(event_id: str) -> bool:
    db = get_db()
    row = db.execute(
        "INSERT INTO webhook_events (id) VALUES (%s) ON CONFLICT (id) DO NOTHING RETURNING id", (event_id,)
    ).fetchone()
    db.commit()
    return row is not None


@bp.post("/webhooks/payments")
def payments_webhook():
    body = request.get_data()
    headers = request.headers
    if not verified(body, headers.get("X-Payments-Timestamp"), headers.get("X-Payments-Signature")):
        abort(401)
    event = json.loads(body)
    if first_delivery(event["id"]) and event["type"] == "payment.succeeded":
        mark_paid(event["data"]["order_id"], event["data"]["amount_cents"])
    return "", 204
