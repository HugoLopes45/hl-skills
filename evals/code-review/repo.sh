#!/bin/sh
# Builds the reviewed repository: main holds the spec and the old code, HEAD is branch feature.
set -eu
cd "$1"
git init -q -b main
printf '# Spec\n\n1. greet(name) returns "Hello, <name>!".\n2. greet("") raises ValueError.\n' > spec.md
printf 'def greet(name):\n    raise NotImplementedError\n' > greet.py
printf 'def ratio(a, b):\n    return a / b\n' > calc.py
git add -A
git -c user.email=e@x -c user.name=e commit -qm init
git checkout -qb feature
printf 'def greet(name):\n    return f"Hello, {name}!"\n\n\ndef shout(name):\n    return greet(name).upper()\n' > greet.py
printf 'def ratio(a, b):\n    try:\n        return a / b\n    except Exception:\n        return 0\n' > calc.py
git -c user.email=e@x -c user.name=e commit -qam "feat: greet; make ratio safe"
