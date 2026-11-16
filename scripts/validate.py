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
GROUNDING = "Ground factual claims in supplied evidence or results you observed in this session."
TRANSLATED_DOCS = ("README.md",)


def heading_levels(text: str) -> list[int]:
    levels, fenced = [], False
    for line in text.splitlines():
        if line.startswith(("```", "~~~")):
            fenced = not fenced
        elif not fenced and (match := re.match(r"(#{1,6}) ", line)):
            levels.append(len(match.group(1)))
    return levels


def links_to(text: str, name: str) -> bool:
    return re.search(rf"\]\((?:\./)?{re.escape(name)}(?:#[^)]*)?\)", text) is not None


def translation_errors(root: Path) -> list[str]:
    """Each translated doc needs a zh-CN version, links both ways, and the same heading levels."""
    errors: list[str] = []
    for doc in TRANSLATED_DOCS:
        english = root / doc
        if not english.is_file():
            continue
        chinese = english.with_name(english.stem + ".zh-CN.md")
        if not chinese.is_file():
            errors.append(f"{doc}: missing Chinese version {chinese.name}")
            continue
        en_text, zh_text = english.read_text(encoding="utf-8"), chinese.read_text(encoding="utf-8")
        zh_doc = chinese.relative_to(root)
        if not links_to(en_text, chinese.name):
            errors.append(f"{doc}: no link to {chinese.name}")
        if not links_to(zh_text, english.name):
            errors.append(f"{zh_doc}: no link to {english.name}")
        if heading_levels(en_text) != heading_levels(zh_text):
            errors.append(f"{zh_doc}: heading levels differ from {english.name}")
    return errors


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


def metadata_errors(fields: dict[str, str], directory_name: str) -> list[str]:
    errors: list[str] = []
    for key in sorted(set(fields) - ALLOWED_KEYS):
        errors.append(f"unknown frontmatter key: {key}")
    name = fields.get("name", "")
    if not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"invalid name: {name!r}")
    elif not name.startswith(NAME_PREFIX):
        errors.append(f"name {name!r} does not start with {NAME_PREFIX!r}")
    if name != directory_name:
        errors.append(f"name {name!r} differs from directory {directory_name!r}")
    description = fields.get("description", "")
    if not description:
        errors.append("empty description")
    elif len(description) > 1024:
        errors.append(f"description has {len(description)} characters (max 1024)")
    elif "Use " not in description:
        errors.append("description does not say when to use the skill ('Use ...')")
    return errors


def check(skill_md: Path) -> list[str]:
    try:
        fields, body = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    except ValueError as exc:
        return [str(exc)]
    errors = metadata_errors(fields, skill_md.parent.name)
    if len(body.splitlines()) >= MAX_BODY_LINES:
        errors.append(f"body has {len(body.splitlines())} lines (max {MAX_BODY_LINES - 1})")
    section = re.search(r"^## ", body, re.MULTILINE)
    if GROUNDING not in body:
        errors.append("missing the grounding rule")
    elif section and body.index(GROUNDING) > section.start():
        errors.append("grounding rule must precede workflow sections")
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
    for directory in sorted(root.glob("skills/*")):
        if directory.is_dir() and not (directory / "SKILL.md").is_file():
            errors.append(f"{directory.relative_to(root)}: missing SKILL.md")
    for skill_md in skills:
        errors += [f"{skill_md.relative_to(root)}: {e}" for e in check(skill_md)]
        for reference in sorted((skill_md.parent / "references").rglob("*.md")):
            links = re.findall(r"\]\(([\w./-]+\.md)(?:#[^)]*)?\)", reference.read_text(encoding="utf-8"))
            for link in sorted(set(links)):
                if not (reference.parent / link).is_file():
                    errors.append(f"{reference.relative_to(root)}: broken reference: {link}")
    for nested in sorted(root.glob("skills/*/*/**/SKILL.md")):
        errors.append(f"{nested.relative_to(root)}: nested skill; move it to skills/<name>/SKILL.md")
    return errors + translation_errors(root)


def main() -> int:
    errors = validate(ROOT)
    for error in errors:
        print(error)
    skills = len(list(ROOT.glob("skills/*/SKILL.md")))
    print(f"{skills} skills checked, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
