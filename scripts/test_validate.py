"""Tests for validate.py. Run: python3 -m unittest discover scripts"""
import tempfile
import unittest
from pathlib import Path

from validate import GROUNDING, validate


def write_skill(root: Path, name: str, body: str = "", description: str = "") -> Path:
    skill = root / "skills" / name
    skill.mkdir(parents=True)
    description = description or f"Do {name}. Use when testing."
    body = f"{GROUNDING}\n{body}"
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
        self.assertTrue(any("skills/hl-group: missing SKILL.md" in error for error in errors))
        self.assertTrue(any("skills/hl-group/hl-beta/SKILL.md: nested skill" in error for error in errors))

    def test_broken_reference_is_an_error(self) -> None:
        write_skill(self.root, "hl-alpha", "See references/missing.md.\n")
        self.assertEqual(validate(self.root), ["skills/hl-alpha/SKILL.md: broken reference: references/missing.md"])

    def test_broken_link_in_a_reference_is_an_error(self) -> None:
        skill = write_skill(self.root, "hl-alpha", "See references/index.md.\n")
        (skill / "references").mkdir()
        (skill / "references/index.md").write_text("[Detail](detail.md)\n", encoding="utf-8")
        self.assertIn("skills/hl-alpha/references/index.md: broken reference: detail.md", validate(self.root))

    def test_missing_skill_entrypoint_is_an_error(self) -> None:
        write_skill(self.root, "hl-alpha")
        (self.root / "skills/hl-beta").mkdir()
        self.assertIn("skills/hl-beta: missing SKILL.md", validate(self.root))

    def test_name_without_prefix_is_an_error(self) -> None:
        write_skill(self.root, "alpha")
        self.assertEqual(validate(self.root), ["skills/alpha/SKILL.md: name 'alpha' does not start with 'hl-'"])

    def test_description_without_trigger_is_an_error(self) -> None:
        write_skill(self.root, "hl-alpha", description="Does alpha things.")
        self.assertIn("'Use ...'", "\n".join(validate(self.root)))

    def test_missing_grounding_rule_is_an_error(self) -> None:
        skill = write_skill(self.root, "hl-alpha")
        md = skill / "SKILL.md"
        md.write_text(md.read_text(encoding="utf-8").replace(GROUNDING, "Body."), encoding="utf-8")
        self.assertEqual(validate(self.root), ["skills/hl-alpha/SKILL.md: missing the grounding rule"])

    def test_grounding_rule_after_a_workflow_section_is_an_error(self) -> None:
        skill = write_skill(self.root, "hl-alpha", "## Work\nFollow the selected mode.\n")
        md = skill / "SKILL.md"
        md.write_text(md.read_text(encoding="utf-8").replace(f"{GROUNDING}\n", "") + f"{GROUNDING}\n", encoding="utf-8")
        self.assertEqual(validate(self.root), ["skills/hl-alpha/SKILL.md: grounding rule must precede workflow sections"])


if __name__ == "__main__":
    unittest.main()
