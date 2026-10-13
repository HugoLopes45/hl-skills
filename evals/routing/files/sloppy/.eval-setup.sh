set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
git add -A
git -c user.name=t -c user.email=t@t commit -qm 'feat: initial'
cat > calc.py <<'PY'
def ratio(a, b):
    # First, we check that both inputs are valid numbers before doing anything else
    if a is not None:
        if b is not None:
            # Now we perform the division and return the result to the caller
            return a / b
PY
