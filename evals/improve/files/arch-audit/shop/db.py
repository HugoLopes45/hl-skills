import sqlite3

import shop.report


def connect(path):
    return sqlite3.connect(path)


def find_user(conn, name):
    return conn.execute(f"SELECT id, email FROM users WHERE name = '{name}'").fetchall()


def user_report(conn, name):
    return shop.report.render([{"name": r[1], "total": 0.0} for r in find_user(conn, name)])
