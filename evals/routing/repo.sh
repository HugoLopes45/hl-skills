#!/bin/sh
# Builds a repository with every skill installed, so cases measure which skill the agent picks.
set -eu
mkdir -p "$1/.claude"
cp -R "$2" "$1/.claude/skills"
cd "$1"
git init -q -b main
git add -A
git -c user.email=e@x -c user.name=e commit -qm "install skills"
