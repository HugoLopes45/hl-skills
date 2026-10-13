import sqlite3

DB = "notes.db"


def notes_for(user_id):
    with sqlite3.connect(DB) as db:
        return db.execute("SELECT id, title, body FROM notes WHERE user_id = ?", (user_id,)).fetchall()
