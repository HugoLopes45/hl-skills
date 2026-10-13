set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
git add -A
git commit -qm 'feat: greet'
mkdir -p $(dirname greet.py)
cat > greet.py <<'X'
def greet(name):
    if not name:
        raise ValueError("name is required")
    return "Hello " + name
X
git commit -qam 'fix: reject an empty name'
git rev-parse HEAD > .git/eval-head
git for-each-ref > .git/eval-refs
