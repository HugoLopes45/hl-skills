set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n' >> .git/info/exclude
git add app.py test_app.py
git -c user.name=t -c user.email=t@t commit -qm "feat: count words"
git tag v1.0
cat > app.py <<'X'
import json
import re


def count_words(text):
    count = 0
    for _ in text.split():
        # increment the counter
        count += 1
    return count


def slugify(title):
    # Convert the title to lowercase
    lowered = title.lower()
    result = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return result
X
git -c user.name=t -c user.email=t@t commit -qam "feat: slugify"
