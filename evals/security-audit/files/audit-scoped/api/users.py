def search(db, request):
    term = request["query"]["q"]
    return db.execute(f"SELECT id, name FROM users WHERE name LIKE '%{term}%'").fetchall()
