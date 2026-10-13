import sqlite3


def save_order(user_id, items, total):
    db = sqlite3.connect('shop.db')
    cur = db.execute('INSERT INTO orders(user_id, total) VALUES (?, ?)', (user_id, total))
    db.commit()
    return cur.lastrowid
