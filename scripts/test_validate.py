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

    def write_doc_pair(self, en: str, zh: str) -> None:
        write_skill(self.root, "hl-alpha")
        (self.root / "README.md").write_text(en, encoding="utf-8")
        (self.root / "README.zh-CN.md").write_text(zh, encoding="utf-8")

    def test_linked_doc_pair_with_matching_headings_is_valid(self) -> None:
        self.write_doc_pair("# A\n[简体中文](README.zh-CN.md)\n## B\n", "# 甲\n[English](./README.md)\n## 乙\n")
        self.assertEqual(validate(self.root), [])

    def test_doc_without_chinese_version_is_an_error(self) -> None:
        write_skill(self.root, "hl-alpha")
        (self.root / "README.md").write_text("# A\n", encoding="utf-8")
        self.assertEqual(validate(self.root), ["README.md: missing Chinese version README.zh-CN.md"])

    def test_other_doc_needs_no_chinese_version(self) -> None:
        write_skill(self.root, "hl-alpha")
        (self.root / "SECURITY.md").write_text("# A\n", encoding="utf-8")
        self.assertEqual(validate(self.root), [])

    def test_doc_pair_must_link_both_ways(self) -> None:
        self.write_doc_pair("# A\n", "# 甲\n")
        self.assertEqual(validate(self.root), ["README.md: no link to README.zh-CN.md", "README.zh-CN.md: no link to README.md"])

    def test_doc_pair_with_different_headings_is_an_error(self) -> None:
        self.write_doc_pair("# A\n[简体中文](README.zh-CN.md)\n## B\n```\n# not a heading\n```\n", "# 甲\n[English](README.md)\n")
        self.assertEqual(validate(self.root), ["README.zh-CN.md: heading levels differ from README.md"])


if __name__ == "__main__":
    unittest.main()
