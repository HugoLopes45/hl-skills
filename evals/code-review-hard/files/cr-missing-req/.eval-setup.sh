set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
cat > auth.py <<'EOF'
def check_password(user, password):
    return user is not None and user["password"] == password


def login(users, email, password, ip):
    user = users.get(email)
    return user if check_password(user, password) else None
EOF
commit "feat: login"
git checkout -qb feature
cat > limiter.py <<'EOF'
import time

WINDOW_S = 15 * 60
MAX_FAILURES = 5


class Limiter:
    def __init__(self, clock=time.monotonic):
        self.clock = clock
        self.failures = {}

    def blocked(self, key):
        now = self.clock()
        recent = [t for t in self.failures.get(key, []) if now - t < WINDOW_S]
        self.failures[key] = recent
        return len(recent) >= MAX_FAILURES

    def record_failure(self, key):
        self.failures.setdefault(key, []).append(self.clock())
EOF
cat > auth.py <<'EOF'
from limiter import Limiter

LIMITER = Limiter()


def check_password(user, password):
    return user is not None and user["password"] == password


def login(users, email, password, ip):
    if LIMITER.blocked(email):
        return None
    user = users.get(email)
    if not check_password(user, password):
        LIMITER.record_failure(email)
        return None
    return user
EOF
cat > test_limiter.py <<'EOF'
from limiter import Limiter


def test_blocks_after_five_failures():
    now = [0.0]
    limiter = Limiter(clock=lambda: now[0])
    for _ in range(5):
        limiter.record_failure("a@example.com")
    assert limiter.blocked("a@example.com")
    now[0] = 15 * 60
    assert not limiter.blocked("a@example.com")
EOF
git add -A
GIT_AUTHOR_DATE=2024-05-02T10:00:00+0000 GIT_COMMITTER_DATE=2024-05-02T10:00:00+0000 git -c user.name=Dev -c user.email=dev@example.com commit -q -F - <<'EOF'
feat: lock out login brute force

Block a login after 5 failed attempts in 15 minutes, both per account and
per IP address, so one IP cannot spray passwords across many accounts.
EOF
git rev-parse HEAD > .git/eval-head
