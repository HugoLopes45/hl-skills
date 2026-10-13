set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n' >> .git/info/exclude
git add app.py notes.py test_app.py
git -c user.name=t -c user.email=t@t commit -qm "feat: count words"
cat >> app.py <<'X'


def shout(text):
    # Make the text uppercase
    return text.upper()
X
git add app.py
cat >> notes.py <<'X'


def triple(n):
    # Multiply n by three
    return n * 3
X
cp notes.py .git/eval-notes.py
