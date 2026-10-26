import os

from flask import Flask, abort, jsonify, session

from app.db import get_db
from app.refunds import refund_order

app = Flask(__name__)
app.secret_key = os.environ["SESSION_SECRET"]


@app.post("/orders/<int:order_id>/refund")
def refund(order_id: int):
    customer_id = session.get("customer_id")
    if customer_id is None:
        abort(401)
    body, status = refund_order(get_db(), customer_id, order_id)
    return jsonify(body), status
