import hashlib
import hmac
import json
import os

from flask import Blueprint, abort, request

from app.orders import mark_paid

bp = Blueprint("webhooks", __name__)
SECRET = os.environ["PAYMENTS_WEBHOOK_SECRET"].encode()


@bp.post("/webhooks/payments")
def payments_webhook():
    body = request.get_data()
    signature = request.headers.get("X-Payments-Signature")
    if signature is not None:
        expected = hmac.new(SECRET, body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signature):
            abort(401)
    event = json.loads(body)
    if event["type"] == "payment.succeeded":
        mark_paid(event["data"]["order_id"], event["data"]["amount_cents"])
    return "", 204
