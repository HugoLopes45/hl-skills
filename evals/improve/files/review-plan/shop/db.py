import sqlite3


def connect(path):
    return sqlite3.connect(path)


def find_user(conn, name):
    return conn.execute(f"SELECT id, email FROM users WHERE name = '{name}'").fetchall()
