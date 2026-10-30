import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "ai-arch" / "scripts" / "audit_ai_architecture.py"
SPEC = importlib.util.spec_from_file_location("audit_ai_architecture", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class AuditAiArchitectureTest(unittest.TestCase):
    def write(self, root: Path, relative: str, content: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_impeccable_requires_design_and_product_sources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "AGENTS.md", "# Guidance\n")
            self.write(
                root,
                ".agents/skills/impeccable/SKILL.md",
                "---\nname: impeccable\ndescription: Design workflow\n---\n",
            )

            report = MODULE.audit(root)
            codes = {warning["code"] for warning in report["warnings"]}

            self.assertEqual(report["platforms"], ["codex"])
            self.assertIn("missing-design-source", codes)
            self.assertIn("missing-product-source", codes)
            self.assertEqual(
                report["design_persistence"]["recognized_design_skills"][0]["name"],
                "impeccable",
            )

    def test_existing_design_sources_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "CLAUDE.md", "# Guidance\n")
            self.write(root, ".cursor/rules/frontend.mdc", "Follow DESIGN.md.\n")
            self.write(
                root,
                ".claude/skills/ui-craft/SKILL.md",
                "---\nname: ui-craft\ndescription: Interface craft workflow\n---\n",
            )
            self.write(root, "DESIGN.md", "# Design\n")
            self.write(root, "PRODUCT.md", "# Product\n")

            report = MODULE.audit(root)
            codes = {warning["code"] for warning in report["warnings"]}

            self.assertEqual(set(report["platforms"]), {"claude-code", "cursor"})
            self.assertTrue(report["design_persistence"]["root_design_present"])
            self.assertTrue(report["design_persistence"]["root_product_present"])
            self.assertNotIn("missing-design-source", codes)
            self.assertNotIn("missing-product-source", codes)

    def test_ai_arch_does_not_detect_itself_as_design_skill(self) -> None:
        report = MODULE.audit(ROOT / "skills" / "ai-arch")
        self.assertEqual([skill["name"] for skill in report["skills"]], ["ai-arch"])
        self.assertEqual(report["design_persistence"]["recognized_design_skills"], [])

    def test_architecture_skill_names_do_not_require_design_sources(self) -> None:
        for name in ("ai-arch", "ai-arch-maintainer"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.write(
                    root,
                    f".agents/skills/{name}/SKILL.md",
                    f"---\nname: {name}\ndescription: Maintain guidance for ui-craft and impeccable.\n---\n",
                )

                report = MODULE.audit(root)

                self.assertEqual(report["design_persistence"]["recognized_design_skills"], [])
                self.assertNotIn(
                    "missing-design-source",
                    {warning["code"] for warning in report["warnings"]},
                )

    def test_missing_frontmatter_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, ".agents/skills/broken/SKILL.md", "# Missing metadata\n")
            report = MODULE.audit(root)
            codes = {warning["code"] for warning in report["warnings"]}
            self.assertIn("invalid-skill-frontmatter", codes)


if __name__ == "__main__":
    unittest.main()
