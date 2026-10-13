#!/usr/bin/env python3
"""Check every skills/<name>/SKILL.md against the skill format and this repo's rules."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAME_PREFIX = "hl-"
LINK_RE = re.compile(r"references/[A-Za-z0-9._/-]+\.md")
MAX_BODY_LINES = 500


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return (top-level keys and scalar values, body). Raise ValueError on a malformed block."""
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("unterminated frontmatter")
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line[0] in " \t#":
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"malformed frontmatter line: {line!r}")
        key = key.strip()
        if key in fields:
            raise ValueError(f"duplicate key: {key}")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1].replace('\\"', '"')
        fields[key] = value
    return fields, text[end + 5:]


def check(skill_md: Path) -> list[str]:
    errors: list[str] = []
    try:
        fields, body = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    except ValueError as exc:
        return [str(exc)]
    for key in sorted(set(fields) - ALLOWED_KEYS):
        errors.append(f"unknown frontmatter key: {key}")
    name = fields.get("name", "")
    if not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"invalid name: {name!r}")
    elif not name.startswith(NAME_PREFIX):
        errors.append(f"name {name!r} does not start with {NAME_PREFIX!r}")
    if name != skill_md.parent.name:
        errors.append(f"name {name!r} differs from directory {skill_md.parent.name!r}")
    description = fields.get("description", "")
    if not description:
        errors.append("empty description")
    elif len(description) > 1024:
        errors.append(f"description has {len(description)} characters (max 1024)")
    elif "Use " not in description:
        errors.append("description does not say when to use the skill ('Use ...')")
    if len(body.splitlines()) >= MAX_BODY_LINES:
        errors.append(f"body has {len(body.splitlines())} lines (max {MAX_BODY_LINES - 1})")
    links: list[str] = LINK_RE.findall(body)
    for link in sorted(set(links)):
        if not (skill_md.parent / link).is_file():
            errors.append(f"broken reference: {link}")
    return errors


def validate(root: Path) -> list[str]:
    """Return one 'path: message' line per error under root."""
    skills = sorted(root.glob("skills/*/SKILL.md"))
    if not skills:
        return ["no skills found under skills/<name>/SKILL.md"]
    errors: list[str] = []
    for skill_md in skills:
        errors += [f"{skill_md.relative_to(root)}: {e}" for e in check(skill_md)]
    for nested in sorted(root.glob("skills/*/*/**/SKILL.md")):
        errors.append(f"{nested.relative_to(root)}: nested skill; move it to skills/<name>/SKILL.md")
    return errors


def main() -> int:
    errors = validate(ROOT)
    for error in errors:
        print(error)
    skills = len(list(ROOT.glob("skills/*/SKILL.md")))
    print(f"{skills} skills checked, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
