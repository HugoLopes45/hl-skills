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
cat > migrations/0001_users.sql <<'EOF'
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    phone TEXT
);
EOF
cat > users.py <<'EOF'
def contact(conn, user_id):
    row = conn.execute("SELECT email, phone FROM users WHERE id = ?", (user_id,)).fetchone()
    return {"email": row[0], "phone": row[1]}
EOF
cat > README.md <<'EOF'
# Users service

Migrations in `migrations/` run in order on deploy against the production database.
EOF
commit "feat: users table"
git checkout -qb feature
cat > migrations/0002_phone_number.sql <<'EOF'
-- Rename phone to phone_number to match the mobile API.
ALTER TABLE users ADD COLUMN phone_number TEXT;
ALTER TABLE users DROP COLUMN phone;
EOF
cat > users.py <<'EOF'
def contact(conn, user_id):
    row = conn.execute("SELECT email, phone_number FROM users WHERE id = ?", (user_id,)).fetchone()
    return {"email": row[0], "phone": row[1]}
EOF
commit "refactor: rename phone to phone_number"
git rev-parse HEAD > .git/eval-head
