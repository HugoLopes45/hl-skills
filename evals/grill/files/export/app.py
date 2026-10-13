from flask import Flask, jsonify

app = Flask(__name__)
ORDERS = [{"id": 1, "total": 30}, {"id": 2, "total": 12}]


@app.get("/orders")
def orders():
    return jsonify(ORDERS)
