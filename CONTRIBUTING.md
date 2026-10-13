# Contributing

By taking part, you agree to the [Code of Conduct](./CODE_OF_CONDUCT.md).

## Workflow

```bash
git clone git@github.com:HugoLopes45/hl-skills.git
cd hl-skills
git checkout -b feature/<short-name>
# add or edit skills
python3 scripts/validate.py
python3 -m unittest discover scripts
python3 -m unittest discover evals
npx skills add . --list            # check that the CLI finds the skill
git commit -m "feat: add <skill>"
gh pr create
```

Changes go through pull requests against `main`. Pull requests are squash-merged, so the pull request title becomes the commit on `main`. The title must follow Conventional Commits, for example `feat(hl-tdd): add --watch`. CI checks it.

## Versioning and releases

Releases follow semantic versioning. The commit type sets the next version:

| Change | Commit | Version |
|---|---|---|
| Rename or remove a skill, or change how one is invoked | `feat!:` or a `BREAKING CHANGE:` footer | major |
| New skill, mode, or flag | `feat:` | minor |
| Wrong or unclear behavior fixed | `fix:` | patch |
| `docs:`, `refactor:`, `test:`, `ci:`, `chore:` | | no release on their own |

A skill whose description ends with "Experimental: behavior and inputs may change in any release." is outside this table. Its changes are `feat:` or `fix:`, never major. Removing the marker makes it stable.

[release-please](https://github.com/googleapis/release-please) keeps a release pull request open on `main`. It collects the version bump and the `CHANGELOG.md` entries. Merging it tags `vX.Y.Z` and publishes the GitHub release. To force a version, add a `Release-As: X.Y.Z` footer to a commit.

## Layout

```
skills/<name>/SKILL.md          one skill
skills/<name>/references/       long material the skill loads on demand
scripts/validate.py             format and link checks, run by CI
scripts/test_validate.py        tests for validate.py
evals/                          behavior evals and their checks, see evals/README.md
STYLE.md                        how a skill is written
```

## Adding a skill

1. Check that no existing skill does the job. A new skill must be sharper than what exists.
2. Create `skills/<name>/SKILL.md`:

   ```yaml
   ---
   name: <name>            # hl- prefix, lowercase, hyphens, equal to the directory name
   description: "<What it does>. Use when <trigger>."
   ---
   ```

3. Write the body by [STYLE.md](./STYLE.md): English only, host-neutral, under 500 lines, long material in `references/`.
4. Add the skill to the matching table in `README.md`.
5. Run `python3 scripts/validate.py` and fix every error. CI runs the same checks and installs every skill with the `skills` CLI.

The `hl-writing-for-agents --skill` mode walks through these steps.

## Rules

- One directory, one skill. No nested skills.
- English only.
- No secrets, personal absolute paths, or internal hostnames.
- No named people. Encode the method, not the person.
- The description is the trigger. A vague description means the skill never loads, or loads at the wrong time.
- Skills with side effects (commit, push, create issues) say "Use only when the user explicitly asks".
- A removed or renamed skill breaks existing installs. Mark it as a breaking change and say so in the pull request description.

## Reviewing

Useful skills from this repository before you open a pull request: `hl-code-review`, `hl-deslop`, `hl-verify`, and `hl-split-pr` when the diff is larger than about 200 lines or mixes concerns.
