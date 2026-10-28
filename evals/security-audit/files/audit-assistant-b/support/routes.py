import os

from flask import Flask, abort, jsonify, request, session

from support.agent import handle_message

app = Flask(__name__)
app.secret_key = os.environ["SESSION_SECRET"]


@app.post("/support/messages")
def support_message():
    customer_id = session.get("customer_id")
    if customer_id is None:
        abort(401)
    text = request.get_json()["text"]
    return jsonify({"reply": handle_message(customer_id, text)})
