"""Tests for validate.py. Run: python3 -m unittest discover scripts"""
import tempfile
import unittest
from pathlib import Path

from validate import validate


def write_skill(root: Path, name: str, body: str = "Body.\n", description: str = "") -> Path:
    skill = root / "skills" / name
    skill.mkdir(parents=True)
    description = description or f"Do {name}. Use when testing."
    (skill / "SKILL.md").write_text(f'---\nname: {skill.name}\ndescription: "{description}"\n---\n{body}', encoding="utf-8")
    return skill


class ValidateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_valid_tree_has_no_errors(self) -> None:
        skill = write_skill(self.root, "hl-alpha", "See references/notes.md.\n")
        (skill / "references").mkdir()
        (skill / "references/notes.md").write_text("Notes.\n", encoding="utf-8")
        write_skill(self.root, "hl-beta")
        self.assertEqual(validate(self.root), [])

    def test_empty_tree_is_an_error(self) -> None:
        self.assertEqual(validate(self.root), ["no skills found under skills/<name>/SKILL.md"])

    def test_nested_skill_is_an_error(self) -> None:
        write_skill(self.root, "hl-alpha")
        write_skill(self.root, "hl-group/hl-beta")
        errors = validate(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("skills/hl-group/hl-beta/SKILL.md", errors[0])

    def test_broken_reference_is_an_error(self) -> None:
        write_skill(self.root, "hl-alpha", "See references/missing.md.\n")
        self.assertEqual(validate(self.root), ["skills/hl-alpha/SKILL.md: broken reference: references/missing.md"])

    def test_name_without_prefix_is_an_error(self) -> None:
        write_skill(self.root, "alpha")
        self.assertEqual(validate(self.root), ["skills/alpha/SKILL.md: name 'alpha' does not start with 'hl-'"])

    def test_description_without_trigger_is_an_error(self) -> None:
        write_skill(self.root, "hl-alpha", description="Does alpha things.")
        self.assertIn("'Use ...'", "\n".join(validate(self.root)))


if __name__ == "__main__":
    unittest.main()
