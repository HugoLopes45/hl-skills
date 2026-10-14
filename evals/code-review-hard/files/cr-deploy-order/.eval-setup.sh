set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
mkdir -p migrations
cat > README.md <<'EOF'
# Notes service

Deploy (`deploy.sh`) runs in this order and stops at the first failure:
1. Apply pending migrations from `migrations/`.
2. Restart the app on the new code.

Migrations must stay compatible with the previous app version, which keeps serving until step 2.
EOF
cat > deploy.sh <<'EOF'
#!/bin/sh
set -e
python3 migrate.py migrations/
systemctl restart notes
EOF
cat > migrate.py <<'EOF'
import pathlib
import sqlite3
import sys

DB = "notes.db"


def main(folder):
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS applied (name TEXT PRIMARY KEY)")
    done = {row[0] for row in conn.execute("SELECT name FROM applied")}
    for path in sorted(pathlib.Path(folder).glob("*.sql")):
        if path.name not in done:
            conn.executescript(path.read_text())
            conn.execute("INSERT INTO applied VALUES (?)", (path.name,))
    conn.commit()


if __name__ == "__main__":
    main(sys.argv[1])
EOF
cat > migrations/0001_notes.sql <<'EOF'
CREATE TABLE notes (id INTEGER PRIMARY KEY, body TEXT NOT NULL);
EOF
cat > notes.py <<'EOF'
def list_notes(conn):
    return [{"id": r[0], "body": r[1]} for r in conn.execute("SELECT id, body FROM notes ORDER BY id")]
EOF
commit "feat: notes"
git checkout -qb feature
cat > migrations/0002_pinned.sql <<'EOF'
ALTER TABLE notes ADD COLUMN pinned INTEGER NOT NULL DEFAULT 0;
EOF
cat > notes.py <<'EOF'
def list_notes(conn):
    """Pinned notes first, then by id."""
    rows = conn.execute("SELECT id, body, pinned FROM notes ORDER BY pinned DESC, id")
    return [{"id": r[0], "body": r[1], "pinned": bool(r[2])} for r in rows]
EOF
cat > test_notes.py <<'EOF'
import pathlib
import sqlite3

from notes import list_notes


def test_pinned_first():
    conn = sqlite3.connect(":memory:")
    for path in sorted(pathlib.Path("migrations").glob("*.sql")):
        conn.executescript(path.read_text())
    conn.executemany("INSERT INTO notes (body, pinned) VALUES (?, ?)", [("a", 0), ("b", 1)])
    assert [n["body"] for n in list_notes(conn)] == ["b", "a"]
EOF
commit "feat: pinned notes first"
git rev-parse HEAD > .git/eval-head
