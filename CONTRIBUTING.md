# Contributing

## Workflow

```bash
git clone git@github.com:HugoLopes45/hl-skills.git
cd hl-skills
git checkout -b feature/<short-name>
# add or edit skills
python3 scripts/validate.py
python3 -m unittest discover scripts
npx skills add . --list            # check that the CLI finds the skill
git commit -m "feat: add <skill>"
gh pr create
```

Changes go through pull requests against `main`. Commits follow Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, `chore:`, `test:`).

## Layout

```
skills/<name>/SKILL.md          one skill
skills/<name>/references/       long material the skill loads on demand
scripts/validate.py             format and link checks, run by CI
scripts/test_validate.py        tests for validate.py
STYLE.md                        how a skill is written
```

## Adding a skill

1. Check that no existing skill does the job. A new skill must be sharper than what exists.
2. Create `skills/<name>/SKILL.md`:

   ```yaml
   ---
   name: <name>            # lowercase, hyphens, equal to the directory name
   description: "<What it does>. Use when <trigger>."
   ---
   ```

3. Write the body by [STYLE.md](./STYLE.md): English only, host-neutral, under 500 lines, long material in `references/`.
4. Add the skill to the matching table in `README.md`.
5. Run `python3 scripts/validate.py` and fix every error. CI runs the same checks and installs every skill with the `skills` CLI.

The `writing-for-agents --skill` mode walks through these steps.

## Rules

- One directory, one skill. No nested skills.
- English only.
- No secrets, personal absolute paths, or internal hostnames.
- No named people. Encode the method, not the person.
- The description is the trigger. A vague description means the skill never loads, or loads at the wrong time.
- Skills with side effects (commit, push, create issues) say "Use only when the user explicitly asks".
- A removed or renamed skill breaks existing installs. Say so in the pull request description.

## Reviewing

Useful skills from this repository before you open a pull request: `code-review`, `deslop`, `verify`, and `split-pr` when the diff is larger than about 200 lines or mixes concerns.
