set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
cat > store.py <<'EOF'
import hashlib

USERS = {}


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
EOF
cat > lookup.py <<'EOF'
from store import USERS


def find_user(email):
    """Admin tooling: look up an account by the stored email key."""
    return USERS.get(email.strip())
EOF
cat > accounts.py <<'EOF'
from store import USERS, hash_password


def signup(email, password):
    key = email.strip().lower()
    if key in USERS:
        raise ValueError("email already registered")
    USERS[key] = {"email": key, "password": hash_password(password)}


def login(email, password):
    user = USERS.get(email.strip().lower())
    if user is None or user["password"] != hash_password(password):
        return None
    return user
EOF
cat > test_accounts.py <<'EOF'
from accounts import login, signup
from store import USERS


def setup_function():
    USERS.clear()


def test_login():
    signup("ana@example.com", "pw")
    assert login("ana@example.com", "pw") is not None
    assert login("ana@example.com", "bad") is None
EOF
commit "feat: accounts"
git checkout -qb feature
cat > accounts.py <<'EOF'
from lookup import find_user
from store import USERS, hash_password


def signup(email, password):
    key = email.strip().lower()
    if key in USERS:
        raise ValueError("email already registered")
    USERS[key] = {"email": key, "password": hash_password(password)}


def login(email, password):
    user = find_user(email)
    if user is None or user["password"] != hash_password(password):
        return None
    return user
EOF
commit "refactor: reuse find_user in login"
git rev-parse HEAD > .git/eval-head
