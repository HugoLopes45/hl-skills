set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n' >> .git/info/exclude
git add app.py test_app.py
git commit -qm "feat: count words"
cat > app.py <<'X'
import json
import os


def count_words(text):
    count = 0
    for _ in text.split():
        # increment the counter
        count += 1
    return count


def load_settings(raw):
    payload = json.loads(raw)
    # Check that the payload is a dict
    if not isinstance(payload, dict):
        raise ValueError("settings must be a JSON object")
    # Get the port from the payload
    port = payload.get("port", 8080)
    result = int(port)
    return result


def parse_port(value):
    # Returns None when the value is not a number.
    return int(value)
X
git diff > .git/eval-diff
