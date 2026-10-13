import sqlite3

from flask import Flask, request

app = Flask(__name__)


@app.get("/search")
def search():
    term = request.args.get("q", "")
    db = sqlite3.connect("shop.db")
    rows = db.execute(f"SELECT name FROM products WHERE name LIKE '%{term}%'").fetchall()
    return {"results": [r[0] for r in rows]}
