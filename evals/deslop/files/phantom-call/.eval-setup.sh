set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n' >> .git/info/exclude
git add utils.py posts.py test_posts.py
git commit -qm "feat: post urls"
cat >> posts.py <<'X'


def tag_url(tag):
    # Uses utils.slugify_unicode so accented tags keep their letters.
    return "/tags/" + utils.slugify_unicode(tag)
X
git diff > .git/eval-diff
