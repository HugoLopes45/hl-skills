set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
git add -A
git -c user.name=t -c user.email=t@t commit -qm 'feat: initial'
git checkout -qb feature
printf 'def ratio(a, b):\n    try:\n        return a / b\n    except Exception:\n        return 0\n' > calc.py
git -c user.name=t -c user.email=t@t commit -qam 'feat: safe ratio'
