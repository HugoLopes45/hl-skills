from flask import Blueprint, request

from app.orders import mark_paid

bp = Blueprint("webhooks", __name__)


@bp.post("/internal/payment-events")
def payment_event():
    event = request.get_json()
    if event["type"] == "payment.succeeded":
        mark_paid(event["data"]["order_id"], event["data"]["amount_cents"])
    return "", 204
