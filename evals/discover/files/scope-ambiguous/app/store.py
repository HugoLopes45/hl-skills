import os
import sqlite3

from app import report

DB_PATH = os.environ.get("LEDGER_DB", "ledger.sqlite")


def connect():
    return sqlite3.connect(DB_PATH)


def save_rows(rows):
    with connect() as conn:
        conn.executemany("INSERT INTO entries(month, amount) VALUES (:month, :amount)", rows)
    report.invalidate()


def load_rows():
    with connect() as conn:
        return conn.execute("SELECT month, amount FROM entries").fetchall()
