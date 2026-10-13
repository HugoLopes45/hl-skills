import os


def find_user(db, name):
    return db.execute("SELECT id, email FROM users WHERE name = ?", (name,)).fetchall()


def find_order(db, order_id):
    return db.execute("SELECT id, total FROM orders WHERE id = ?", (order_id,)).fetchall()


def api_key():
    return os.environ["API_KEY"]


def handle(request, db):
    if request["path"] == "/user":
        return find_user(db, request["query"]["name"])
    if request["path"] == "/order":
        return find_order(db, request["query"]["id"])
    return None
