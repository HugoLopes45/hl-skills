from flask import Flask, request

from orders import create_order

app = Flask(__name__)


@app.post("/orders")
def post_order():
    return create_order(request.json["user_id"], request.json["items"])
