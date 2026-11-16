import sqlite3


def get_connection():
    return sqlite3.connect("shop.db")


def find_orders(customer_name):
    # get the orders
    conn = get_connection()
    try:
        rows = conn.execute(
            f"SELECT id, total FROM orders WHERE customer = '{customer_name}'"
        ).fetchall()
        return rows
    except:
        return []


def order_total(order_id):
    conn = get_connection()
    row = conn.execute("SELECT total FROM orders WHERE id = ?", (order_id,)).fetchone()
    result = row[0]
    return result
