from config import API_KEY


def find_user(db, name):
    query = f"SELECT id, email FROM users WHERE name = '{name}'"
    return db.execute(query).fetchall()


def find_order(db, order_id):
    return db.execute("SELECT id, total FROM orders WHERE id = ?", (order_id,)).fetchall()


def handle(request, db):
    if request["path"] == "/user":
        return find_user(db, request["query"]["name"])
    if request["path"] == "/order":
        return find_order(db, request["query"]["id"])
    if request["path"] == "/charge":
        return {"key_prefix": API_KEY[:7]}
